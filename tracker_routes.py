"""Daily tracker routes for HeartGuard lifestyle tracking."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from bson import ObjectId
from flask import Blueprint, jsonify, request

from auth_routes import require_auth

tracker_bp = Blueprint("tracker", __name__)


def get_db():
    from api import get_mongo_db
    return get_mongo_db()

IST = timezone(timedelta(hours=5, minutes=30))

def today_str() -> str:
    return datetime.now(IST).strftime("%Y-%m-%d")


@tracker_bp.route("/api/tracker", methods=["GET"])
def get_logs():
    """Get daily logs for a month. Query: ?month=2026-02"""
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()

    days = request.args.get("days")
    if days:
        try:
            days_int = int(days)
            cutoff = (datetime.now(IST) - timedelta(days=days_int)).strftime("%Y-%m-%d")
            logs = list(
                db.daily_logs.find(
                    {"user_id": ObjectId(user_id), "date": {"$gte": cutoff}},
                    {"_id": 0, "user_id": 0},
                ).sort("date", 1)
            )
            return jsonify({"days": days_int, "logs": logs})
        except ValueError:
            pass

    month = request.args.get("month", today_str()[:7])
    logs = list(
        db.daily_logs.find(
            {"user_id": ObjectId(user_id), "date": {"$regex": f"^{month}"}},
            {"_id": 0, "user_id": 0},
        )
    )

    return jsonify({"month": month, "logs": logs})


@tracker_bp.route("/api/tracker/today", methods=["POST"])
def update_today():
    """Update today's tracking data.
    Body: {
        "completed": ["walk", "water", ...],
        "values": {"walk": 8500, "water": 3, "sleep": 7.5, ...},
        "notes": "Felt great today, went for a morning jog"
    }
    """
    user_id, err = require_auth()
    if err:
        return err

    data = request.get_json(force=True)
    completed = data.get("completed", [])
    values = data.get("values", {})
    notes = data.get("notes")
    mood = data.get("mood")       # e.g. "great", "good", "okay", "bad"
    energy = data.get("energy")   # 1-5

    db = get_db()

    # Get user's goals for computing progress
    goals_doc = db.goals.find_one({"user_id": ObjectId(user_id)})
    goals = goals_doc["goals"] if goals_doc else []
    total_goals = len(goals)

    date = today_str()
    completion_pct = round((len(completed) / total_goals) * 100) if total_goals > 0 else 0

    # Compute per-goal progress
    goal_progress = {}
    for g in goals:
        gid = g["id"]
        target = g.get("target", 0)
        actual = values.get(gid)
        if actual is not None:
            if target == 0:
                # Binary goals (no_smoking, no_junk) — completed = 100%
                pct = 100 if gid in completed else 0
            else:
                pct = min(round((actual / target) * 100), 100)
            goal_progress[gid] = {"actual": actual, "target": target, "pct": pct}
        elif gid in completed:
            goal_progress[gid] = {"actual": target, "target": target, "pct": 100}

    update_set = {
        "completed": completed,
        "values": values,
        "goal_progress": goal_progress,
        "total_goals": total_goals,
        "completion_pct": completion_pct,
        "updated_at": datetime.now(IST),
    }
    if notes is not None:
        update_set["notes"] = notes
    if mood is not None:
        update_set["mood"] = mood
    if energy is not None:
        update_set["energy"] = energy

    db.daily_logs.update_one(
        {"user_id": ObjectId(user_id), "date": date},
        {
            "$set": update_set,
            "$setOnInsert": {
                "user_id": ObjectId(user_id),
                "date": date,
                "created_at": datetime.now(IST),
            },
        },
        upsert=True,
    )

    return jsonify({
        "date": date,
        "completed": completed,
        "values": values,
        "goal_progress": goal_progress,
        "total_goals": total_goals,
        "completion_pct": completion_pct,
        "mood": mood,
        "energy": energy,
    })


@tracker_bp.route("/api/tracker/streak", methods=["GET"])
def get_streak():
    """Calculate current streak, longest streak, and streak freeze tokens."""
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()

    logs = list(
        db.daily_logs.find(
            {"user_id": ObjectId(user_id)},
            {"_id": 0, "date": 1, "completion_pct": 1},
        ).sort("date", -1)
    )

    # Fetch or initialize streak freeze data
    streak_doc = db.streak_data.find_one({"user_id": ObjectId(user_id)}) or {}
    freezes_available: int = int(streak_doc.get("freezes_available", 0))
    freezes_used: list = list(streak_doc.get("freezes_used", []))
    freezes_earned_at: list = list(streak_doc.get("freezes_earned_at", []))

    if not logs:
        return jsonify({
            "current_streak": 0, "longest_streak": 0,
            "total_days_tracked": 0, "freezes": freezes_available,
            "freezes_used": freezes_used
        })

    good_days = {log["date"] for log in logs if log.get("completion_pct", 0) >= 80}
    frozen_days = set(freezes_used)

    # Calculate current streak (good days + frozen days count as streak)
    current_streak = 0
    check_date = datetime.now(IST).date()
    today_str_val = check_date.strftime("%Y-%m-%d")

    # If today isn't tracked yet, start from yesterday
    if today_str_val not in good_days and today_str_val not in frozen_days:
        check_date -= timedelta(days=1)

    while True:
        ds = check_date.strftime("%Y-%m-%d")
        if ds in good_days or ds in frozen_days:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    # Calculate longest streak (including frozen days)
    all_streak_days = good_days | frozen_days
    if not all_streak_days:
        longest_streak = 0
    else:
        sorted_dates = sorted(all_streak_days)
        longest_streak = 1
        run = 1
        for i in range(1, len(sorted_dates)):
            d1 = datetime.strptime(sorted_dates[i - 1], "%Y-%m-%d").date()
            d2 = datetime.strptime(sorted_dates[i], "%Y-%m-%d").date()
            if (d2 - d1).days == 1:
                run += 1
                longest_streak = max(longest_streak, run)
            else:
                run = 1

    # Auto-award freeze tokens: 1 per 7-day streak milestone
    new_freezes = 0
    milestones_to_award = []
    for milestone in [7, 14, 21, 28, 35, 42, 49, 56, 63, 70]:
        if current_streak >= milestone and milestone not in freezes_earned_at:
            new_freezes += 1
            milestones_to_award.append(milestone)

    if new_freezes > 0:
        freezes_available += new_freezes
        freezes_earned_at.extend(milestones_to_award)
        db.streak_data.update_one(
            {"user_id": ObjectId(user_id)},
            {"$set": {
                "freezes_available": freezes_available,
                "freezes_earned_at": freezes_earned_at,
            }},
            upsert=True,
        )

    # Badges
    badges = []
    if len(logs) >= 1:
        badges.append({"id": "first_step", "name": "First Step", "icon": "🌱", "desc": "Tracked your first day"})
    if len(logs) >= 10:
        badges.append({"id": "consistent_10", "name": "Consistent 10", "icon": "📅", "desc": "Tracked 10 total days"})
    if longest_streak >= 3:
        badges.append({"id": "warrior_3", "name": "3-Day Warrior", "icon": "💪", "desc": "Achieved a 3-day streak"})
    if longest_streak >= 7:
        badges.append({"id": "warrior_7", "name": "1-Week Warrior", "icon": "⭐", "desc": "Achieved a 7-day streak"})
    if longest_streak >= 14:
        badges.append({"id": "champion_14", "name": "Fortitude", "icon": "🔥", "desc": "Achieved a 14-day streak"})
    if longest_streak >= 30:
        badges.append({"id": "legend_30", "name": "Legend", "icon": "🏆", "desc": "Achieved a 30-day streak"})
    if freezes_available > 0 or len(freezes_used) > 0:
        badges.append({"id": "freeze_holder", "name": "Ice Shield", "icon": "🧊", "desc": "Earned a Streak Freeze"})

    return jsonify({
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_days_tracked": len(logs),
        "badges": badges,
        "freezes": freezes_available,
        "freezes_used": freezes_used,
    })


@tracker_bp.route("/api/tracker/streak/freeze", methods=["POST"])
def use_streak_freeze():
    """Use a streak freeze to protect yesterday's missed day."""
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    streak_doc = db.streak_data.find_one({"user_id": ObjectId(user_id)})
    if not streak_doc or streak_doc.get("freezes_available", 0) <= 0:
        return jsonify({"error": "No streak freezes available"}), 400

    # The freeze covers yesterday
    yesterday = (datetime.now(IST) - timedelta(days=1)).strftime("%Y-%m-%d")

    # Check if yesterday is already a good day
    log = db.daily_logs.find_one({"user_id": ObjectId(user_id), "date": yesterday})
    if log and log.get("completion_pct", 0) >= 80:
        return jsonify({"error": "Yesterday was already a good day — no freeze needed"}), 400

    # Check if freeze already used for this date
    used = streak_doc.get("freezes_used", [])
    if yesterday in used:
        return jsonify({"error": "Freeze already used for this date"}), 400

    used.append(yesterday)
    db.streak_data.update_one(
        {"user_id": ObjectId(user_id)},
        {"$set": {
            "freezes_available": streak_doc["freezes_available"] - 1,
            "freezes_used": used,
        }},
    )

    return jsonify({
        "success": True,
        "date_frozen": yesterday,
        "freezes_remaining": streak_doc["freezes_available"] - 1,
    })

