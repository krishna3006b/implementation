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


def today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@tracker_bp.route("/api/tracker", methods=["GET"])
def get_logs():
    """Get daily logs for a month. Query: ?month=2026-02"""
    user_id, err = require_auth()
    if err:
        return err

    month = request.args.get("month", today_str()[:7])  # e.g. "2026-02"

    db = get_db()
    logs = list(
        db.daily_logs.find(
            {"user_id": ObjectId(user_id), "date": {"$regex": f"^{month}"}},
            {"_id": 0, "user_id": 0},
        )
    )

    return jsonify({"month": month, "logs": logs})


@tracker_bp.route("/api/tracker/today", methods=["POST"])
def update_today():
    """Toggle goal completion for today. Body: { "completed": ["walk", "water", ...] }"""
    user_id, err = require_auth()
    if err:
        return err

    data = request.get_json(force=True)
    completed = data.get("completed", [])

    db = get_db()

    # Get total goals count
    goals_doc = db.goals.find_one({"user_id": ObjectId(user_id)})
    total_goals = len(goals_doc["goals"]) if goals_doc else 10

    date = today_str()
    completion_pct = round((len(completed) / total_goals) * 100) if total_goals > 0 else 0

    db.daily_logs.update_one(
        {"user_id": ObjectId(user_id), "date": date},
        {
            "$set": {
                "completed": completed,
                "total_goals": total_goals,
                "completion_pct": completion_pct,
                "updated_at": datetime.now(timezone.utc),
            },
            "$setOnInsert": {
                "user_id": ObjectId(user_id),
                "date": date,
                "created_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )

    return jsonify({
        "date": date,
        "completed": completed,
        "total_goals": total_goals,
        "completion_pct": completion_pct,
    })


@tracker_bp.route("/api/tracker/streak", methods=["GET"])
def get_streak():
    """Calculate current streak and longest streak."""
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()

    # Get all logs sorted by date descending
    logs = list(
        db.daily_logs.find(
            {"user_id": ObjectId(user_id)},
            {"_id": 0, "date": 1, "completion_pct": 1},
        ).sort("date", -1)
    )

    if not logs:
        return jsonify({"current_streak": 0, "longest_streak": 0, "total_days_tracked": 0})

    # Build a set of dates with >= 80% completion
    good_days = {log["date"] for log in logs if log.get("completion_pct", 0) >= 80}

    # Calculate current streak (consecutive days ending today or yesterday)
    current_streak = 0
    check_date = datetime.now(timezone.utc).date()

    # Allow streak to count from yesterday if today hasn't been logged yet
    if check_date.strftime("%Y-%m-%d") not in good_days:
        check_date -= timedelta(days=1)

    while check_date.strftime("%Y-%m-%d") in good_days:
        current_streak += 1
        check_date -= timedelta(days=1)

    # Calculate longest streak
    if not good_days:
        longest_streak = 0
    else:
        sorted_dates = sorted(good_days)
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

    return jsonify({
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_days_tracked": len(logs),
    })
