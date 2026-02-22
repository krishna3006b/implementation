"""AI-powered health coaching routes using Groq (LLaMA 3.3 70B)."""

from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta

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

IST = timezone(timedelta(hours=5, minutes=30))


def _get_client():
    if not GROQ_API_KEY:
        return None
    return Groq(api_key=GROQ_API_KEY)


def _build_user_context(user_id: str) -> str:
    """Build a context string from the user's data for the AI."""
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    goals_doc = db.goals.find_one({"user_id": ObjectId(user_id)})
    today = datetime.now(IST).strftime("%Y-%m-%d")
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
    check_date = datetime.now(IST).date()
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

    # Load persona-aware system prompt
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    persona_id = user.get("ai_persona", "supportive") if user else "supportive"
    persona_prompt = AI_PERSONAS.get(persona_id, AI_PERSONAS["supportive"])["system_prompt"]
    system_prompt = persona_prompt + "\n\n" + SYSTEM_PROMPT

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
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


@ai_bp.route("/api/ai/protocol", methods=["POST"])
def generate_protocol():
    """Generate a personalized habit protocol based on prediction results and auto-add to goals."""
    import json
    user_id, err = require_auth()
    if err:
        return err

    client = _get_client()
    if not client:
        return jsonify({"error": "AI service not configured"}), 503

    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user or not user.get("prediction_result"):
        return jsonify({"error": "No prediction results found. Please take the risk assessment first."}), 400
        
    pred = user["prediction_result"]
    
    prompt = f"""You are an elite preventative cardiologist AI. 
The user has just taken a heart disease risk assessment.
Risk Assessment Results:
- Prediction: {'HIGH RISK' if pred.get('prediction') == 1 else 'LOW RISK'}
- Probability of Heart Disease: {pred.get('probability', 'N/A')}

Generate a strict 4-week health protocol consisting of 4 to 6 daily habits tailored to their risk profile.
You MUST format your entire response as valid, parseable JSON only. Do not wrap it in markdown block quotes. Provide ONLY the JSON object.

Format:
{{
  "protocol_summary": "A 1-sentence encouraging summary of the plan.",
  "goals": [
    {{
      "id": "unique_string_id",
      "label": "Short Actionable Name",
      "icon": "Emoji",
      "target": 0,
      "unit": "none"
    }}
  ]
}}

Rules for goals:
- Use standard units if numeric target (e.g., 'glasses', 'steps', 'minutes').
- If it's a simple yes/no check-in (like 'Take Medication' or 'No Junk Food'), set target to 0 and unit to 'none'.
- Make the habits highly relevant to cardiovascular health."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4, # lower temp for strict JSON adherence
            max_tokens=600,
            response_format={"type": "json_object"} # Force JSON mode on Groq API
        )
        
        protocol_str = response.choices[0].message.content
        protocol_data = json.loads(protocol_str)
        
        # Inject these new goals into the user's db.goals
        new_goals = protocol_data.get("goals", [])
        if new_goals:
            db.goals.update_one(
                {"user_id": ObjectId(user_id)},
                {"$set": {"goals": new_goals}},
                upsert=True
            )
            
        return jsonify({
            "message": "Protocol generated successfully.",
            "protocol_summary": protocol_data.get("protocol_summary", "Your new protocol is ready."),
            "goals": new_goals
        })

    except json.JSONDecodeError:
         return jsonify({"error": "Failed to parse AI protocol generation."}), 500
    except Exception as e:
        return jsonify({"error": f"Protocol generation failed: {str(e)}"}), 500


@ai_bp.route("/api/ai/quest", methods=["POST"])
def generate_quest():
    """Generate a fun, gamified Daily Quest. Avoids repeating recent quests."""
    import json
    user_id, err = require_auth()
    if err:
        return err

    client = _get_client()
    if not client:
        return jsonify({"error": "AI service not configured"}), 503

    db = get_db()
    today = datetime.now(IST).strftime("%Y-%m-%d")
    
    # Store or retrieve today's quest in a new collection
    quest_log = db.daily_quests.find_one({"user_id": ObjectId(user_id), "date": today})
    
    # If a quest already exists for today, just return it so it doesn't constantly change
    if quest_log:
        return jsonify({
            "quest": quest_log.get("quest"),
            "completed": quest_log.get("completed", False)
        })

    # Fetch recent quests so the AI doesn't repeat them
    recent_quests = list(db.daily_quests.find(
        {"user_id": ObjectId(user_id)}
    ).sort("date", -1).limit(5))
    recent_titles = [q.get("quest", {}).get("title", "") for q in recent_quests]

    prompt = f"""You are the Gamemaster for a heart-health app. Your job is to generate ONE highly specific, fun, and easy "Daily Quest" for the user to complete today.
The quest should take less than 5 minutes. It should feel like a little gamified side-mission, not a massive chore.
Examples of good quests:
- "Drink 1 full glass of water while your coffee brews."
- "Close your eyes and take 5 deep breaths before opening an app."
- "Do 10 jumping jacks right now."
- "Text a friend or family member just to say hi."

Do NOT repeat these recent quests: {', '.join(recent_titles) if recent_titles else 'None'}

You MUST return valid JSON matching this exact string schema:
{{
  "title": "Short catchy title (e.g., The Hydration Hit)",
  "description": "The exact physical action to take.",
  "icon": "A single suitable emoji",
  "xp_reward": 50 // always an integer between 10 and 100
}}"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8, # higher temp for creative quests
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        quest_data = json.loads(response.choices[0].message.content)
        
        # Save today's quest to DB
        db.daily_quests.insert_one({
            "user_id": ObjectId(user_id),
            "date": today,
            "quest": quest_data,
            "completed": False,
            "created_at": datetime.now(IST)
        })
            
        return jsonify({
            "quest": quest_data,
            "completed": False
        })

    except Exception as e:
        return jsonify({"error": f"Quest generation failed: {str(e)}"}), 500


@ai_bp.route("/api/ai/quest/complete", methods=["POST"])
def complete_quest():
    """Mark today's quest as completed."""
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    today = datetime.now(IST).strftime("%Y-%m-%d")
    
    result = db.daily_quests.update_one(
        {"user_id": ObjectId(user_id), "date": today},
        {"$set": {"completed": True}}
    )
    
    if result.matched_count == 0:
        return jsonify({"error": "No active quest found for today"}), 404
        
    return jsonify({"success": True})


# ───────────────────────────────────────────────
#  VOICE-FIRST LOGGING  (Parse natural language)
# ───────────────────────────────────────────────

@ai_bp.route("/api/ai/parse-log", methods=["POST"])
def parse_voice_log():
    """Parse a natural-language voice transcript into structured goal data."""
    import json
    user_id, err = require_auth()
    if err:
        return err

    client = _get_client()
    if not client:
        return jsonify({"error": "AI service not configured"}), 503

    data = request.get_json(force=True)
    transcript = data.get("transcript", "").strip()
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    # Fetch the user's current goals so the AI knows what to map to
    db = get_db()
    goals_doc = db.goals.find_one({"user_id": ObjectId(user_id)})
    goal_list = goals_doc.get("goals", []) if goals_doc else []
    goal_ids = [{"id": g["id"], "label": g["label"], "unit": g.get("unit", ""), "target": g.get("target", 0)} for g in goal_list]

    prompt = f"""You are a health-tracking assistant. The user spoke the following update about their day:

"{transcript}"

Based on what they said, extract structured data. Here are the user's tracked goals:
{json.dumps(goal_ids)}

Return valid JSON with:
{{
  "completed": ["goal_id_1", "goal_id_2"],  // IDs of goals they completed or mentioned positively
  "values": {{"goal_id": number}},           // numeric values they mentioned (e.g. glasses of water, steps)
  "mood": "great" | "good" | "okay" | "bad" | "terrible" | null,
  "energy": 1-5 integer or null,
  "notes": "A brief summary of what they said"
}}

Only include goals they explicitly or implicitly mentioned. If unsure about a value, omit it."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        parsed = json.loads(response.choices[0].message.content)
        return jsonify({"parsed": parsed})
    except Exception as e:
        return jsonify({"error": f"Voice parsing failed: {str(e)}"}), 500


# ───────────────────────────────────────────────
#  AI PERSONA SYSTEM
# ───────────────────────────────────────────────

AI_PERSONAS = {
    "supportive": {
        "name": "Supportive Coach",
        "emoji": "🤗",
        "system_prompt": """You are a warm, encouraging health coach. You celebrate every small win. 
You use gentle language, empathy, and positive reinforcement. When the user misses goals, 
you reassure them and help them find small steps forward. Use supportive emojis like 🌱💪🙏."""
    },
    "tough_love": {
        "name": "Tough Love",
        "emoji": "🔥",
        "system_prompt": """You are a no-nonsense, tough-love health drill sergeant like David Goggins. 
You push the user to be accountable. No excuses. Be direct, intense, and motivating. 
Call out missed goals firmly but always channel it into action. Use intense emojis like 🔥💀⚡."""
    },
    "zen": {
        "name": "Zen Master",
        "emoji": "🧘",
        "system_prompt": """You are a calm, mindful Zen wellness guide. You focus on balance, 
mindfulness, and the journey rather than perfection. Your language is serene and philosophical. 
Encourage rest, breathwork, and self-compassion. Use peaceful emojis like 🧘🌸☯️."""
    },
    "scientist": {
        "name": "Data Scientist",
        "emoji": "🔬",
        "system_prompt": """You are a data-driven health analyst. You focus on numbers, trends, and 
evidence-based recommendations. Reference their tracking data specifically, calculate percentages, 
and provide actionable metrics-based advice. Use analytical emojis like 📊🔬📈."""
    }
}


@ai_bp.route("/api/ai/persona", methods=["GET"])
def get_persona():
    """Get user's current AI persona and list all available personas."""
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    current = user.get("ai_persona", "supportive") if user else "supportive"

    personas = []
    for key, val in AI_PERSONAS.items():
        personas.append({"id": key, "name": val["name"], "emoji": val["emoji"], "active": key == current})

    return jsonify({"current": current, "personas": personas})


@ai_bp.route("/api/ai/persona", methods=["POST"])
def set_persona():
    """Set user's preferred AI persona."""
    user_id, err = require_auth()
    if err:
        return err

    data = request.get_json(force=True)
    persona_id = data.get("persona", "supportive")
    if persona_id not in AI_PERSONAS:
        return jsonify({"error": "Invalid persona"}), 400

    db = get_db()
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"ai_persona": persona_id}})
    return jsonify({"success": True, "persona": persona_id})

