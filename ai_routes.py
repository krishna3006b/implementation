"""AI-powered health coaching routes using Groq (LLaMA 3.3 70B)."""

from __future__ import annotations

import os
from datetime import datetime, timezone

from bson import ObjectId
from flask import Blueprint, jsonify, request
from groq import Groq

from auth_routes import require_auth

ai_bp = Blueprint("ai", __name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL = "llama-3.3-70b-versatile"


def get_db():
    from api import get_mongo_db
    return get_mongo_db()


def _get_client():
    if not GROQ_API_KEY:
        return None
    return Groq(api_key=GROQ_API_KEY)


def _build_user_context(user_id: str) -> str:
    """Build a context string from the user's data for the AI."""
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    goals_doc = db.goals.find_one({"user_id": ObjectId(user_id)})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_log = db.daily_logs.find_one({"user_id": ObjectId(user_id), "date": today})

    # Recent 7 days of logs
    recent_logs = list(
        db.daily_logs.find(
            {"user_id": ObjectId(user_id)},
            {"_id": 0, "user_id": 0},
        ).sort("date", -1).limit(7)
    )

    # Streak
    from tracker_routes import get_streak as _  # just to ensure route exists
    # Calculate inline
    all_logs = list(db.daily_logs.find(
        {"user_id": ObjectId(user_id)}, {"_id": 0, "date": 1, "completion_pct": 1}
    ).sort("date", -1))
    good_days = {l["date"] for l in all_logs if l.get("completion_pct", 0) >= 80}

    from datetime import timedelta
    check_date = datetime.now(timezone.utc).date()
    if check_date.strftime("%Y-%m-%d") not in good_days:
        check_date -= timedelta(days=1)
    current_streak = 0
    while check_date.strftime("%Y-%m-%d") in good_days:
        current_streak += 1
        check_date -= timedelta(days=1)

    pred = user.get("prediction_result") if user else None
    goals = goals_doc.get("goals", []) if goals_doc else []
    completed_today = today_log.get("completed", []) if today_log else []
    missed_today = [g["label"] for g in goals if g["id"] not in completed_today]

    ctx = f"""User Profile:
- Name: {user.get('name', 'Unknown') if user else 'Unknown'}
- Heart Disease Prediction: {'HIGH RISK' if pred and pred.get('prediction') == 1 else 'LOW RISK' if pred else 'Not yet predicted'}
- Risk Probability: {pred.get('probability', 'N/A') if pred else 'N/A'}
- Risk Confidence: {pred.get('confidence', 'N/A') if pred else 'N/A'}%

Today's Progress ({today}):
- Completed: {', '.join(completed_today) if completed_today else 'None yet'}
- Missed: {', '.join(missed_today) if missed_today else 'All done!'}
- Completion: {today_log.get('completion_pct', 0) if today_log else 0}%

Streak: {current_streak} day(s)
Total Days Tracked: {len(all_logs)}

Recent 7 Days:"""

    for log in recent_logs:
        ctx += f"\n  {log['date']}: {log.get('completion_pct', 0)}% — completed: {', '.join(log.get('completed', []))}"

    if not recent_logs:
        ctx += "\n  No tracking data yet."

    return ctx


SYSTEM_PROMPT = """You are HeartGuard AI Coach — a friendly, knowledgeable health assistant specialized in cardiovascular health and lifestyle management. You're integrated into a heart disease prediction app.

Your personality:
- Warm, encouraging, and empathetic
- Evidence-based but accessible (no medical jargon)
- Concise — keep responses under 150 words unless asked for detail
- Use emojis sparingly for warmth (1-2 per response)

Important rules:
- NEVER diagnose or prescribe medication
- Always remind users to consult their doctor for medical decisions
- Focus on lifestyle: diet, exercise, sleep, stress management, hydration
- Personalize advice based on the user context provided
- If user is HIGH RISK, be more proactive with actionable suggestions
- Celebrate streaks and progress genuinely"""


@ai_bp.route("/api/ai/coach", methods=["POST"])
def coach():
    """Generate a personalized daily health tip."""
    user_id, err = require_auth()
    if err:
        return err

    client = _get_client()
    if not client:
        return jsonify({"error": "AI service not configured"}), 503

    context = _build_user_context(user_id)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""Here is my current health data:

{context}

Give me a personalized daily health tip based on my data. Focus on what I should do TODAY to improve my heart health. If I've missed some goals, give specific advice on those. If I'm doing well, encourage me and suggest the next improvement."""},
            ],
            temperature=0.8,
            max_tokens=300,
        )
        tip = response.choices[0].message.content
        return jsonify({"tip": tip, "model": MODEL})
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 500


@ai_bp.route("/api/ai/insights", methods=["POST"])
def insights():
    """Generate weekly analysis of tracking patterns."""
    user_id, err = require_auth()
    if err:
        return err

    client = _get_client()
    if not client:
        return jsonify({"error": "AI service not configured"}), 503

    context = _build_user_context(user_id)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""Here is my weekly health tracking data:

{context}

Analyze my tracking patterns. Give me:
1. 📊 Pattern Analysis — What goals do I consistently hit or miss?
2. 💡 Key Insight — One main observation about my behavior
3. 🎯 Top 3 Actionable Tips — Specific things I can do this week
4. 🌟 Encouragement — What am I doing well?

Format with clear headers and keep each section to 2-3 sentences max."""},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        analysis = response.choices[0].message.content
        return jsonify({"insights": analysis, "model": MODEL})
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 500


@ai_bp.route("/api/ai/chat", methods=["POST"])
def chat():
    """Conversational health chat with context."""
    user_id, err = require_auth()
    if err:
        return err

    client = _get_client()
    if not client:
        return jsonify({"error": "AI service not configured"}), 503

    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    history = data.get("history", [])  # list of {"role": "user"|"assistant", "content": "..."}

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    context = _build_user_context(user_id)

    messages = [
        {"role": "system", "content": f"""{SYSTEM_PROMPT}

Here is the user's current health data for reference:
{context}

Use this data to personalize your responses. When the user asks about diet, exercise, or lifestyle, relate it to their specific situation."""},
    ]

    # Add conversation history (last 10 messages max)
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=400,
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply, "model": MODEL})
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 500
