"""Goal management routes for HeartGuard lifestyle tracking."""

from __future__ import annotations

from datetime import datetime, timezone

from bson import ObjectId
from flask import Blueprint, jsonify, request

from auth_routes import require_auth

goals_bp = Blueprint("goals", __name__)

DEFAULT_GOALS = [
    {"id": "walk",       "label": "Walk 10K Steps",       "icon": "🚶", "target": 10000, "unit": "steps"},
    {"id": "water",      "label": "Drink 4L Water",       "icon": "💧", "target": 4,     "unit": "liters"},
    {"id": "sleep",      "label": "Sleep 8 Hours",        "icon": "😴", "target": 8,     "unit": "hours"},
    {"id": "meditation", "label": "Meditate 15 Min",      "icon": "🧘", "target": 15,    "unit": "minutes"},
    {"id": "no_smoking", "label": "No Smoking",           "icon": "🚭", "target": 0,     "unit": "cigarettes"},
    {"id": "fruits",     "label": "Eat 5 Fruits/Veggies", "icon": "🥗", "target": 5,     "unit": "servings"},
    {"id": "exercise",   "label": "Exercise 30 Min",      "icon": "🏋️", "target": 30,    "unit": "minutes"},
    {"id": "salt",       "label": "Limit Salt < 5g",      "icon": "🧂", "target": 5,     "unit": "grams"},
    {"id": "bp",         "label": "Monitor BP",           "icon": "❤️",  "target": 1,     "unit": "reading"},
    {"id": "no_junk",    "label": "No Junk Food",         "icon": "🍔", "target": 0,     "unit": "meals"},
]


def get_db():
    from api import get_mongo_db
    return get_mongo_db()


@goals_bp.route("/api/goals", methods=["GET"])
def get_goals():
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    doc = db.goals.find_one({"user_id": ObjectId(user_id)})

    if not doc:
        # Auto-init goals on first access
        doc = {
            "user_id": ObjectId(user_id),
            "goals": DEFAULT_GOALS,
            "created_at": datetime.now(timezone.utc),
        }
        db.goals.insert_one(doc)

    return jsonify({"goals": doc["goals"]})


@goals_bp.route("/api/goals/init", methods=["POST"])
def init_goals():
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    existing = db.goals.find_one({"user_id": ObjectId(user_id)})
    if existing:
        return jsonify({"goals": existing["goals"], "message": "Goals already initialized"})

    doc = {
        "user_id": ObjectId(user_id),
        "goals": DEFAULT_GOALS,
        "created_at": datetime.now(timezone.utc),
    }
    db.goals.insert_one(doc)
    return jsonify({"goals": DEFAULT_GOALS, "message": "Goals initialized"}), 201


@goals_bp.route("/api/goals/<goal_id>", methods=["PATCH"])
def update_goal(goal_id):
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    data = request.get_json(force=True)

    update_fields = {}
    if "label" in data:
        update_fields["goals.$.label"] = data["label"]
    if "target" in data:
        update_fields["goals.$.target"] = data["target"]

    if not update_fields:
        return jsonify({"error": "Nothing to update"}), 400

    result = db.goals.update_one(
        {"user_id": ObjectId(user_id), "goals.id": goal_id},
        {"$set": update_fields},
    )

    if result.matched_count == 0:
        return jsonify({"error": "Goal not found"}), 404

    return jsonify({"message": "Goal updated"})
