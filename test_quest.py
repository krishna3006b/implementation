import os
from datetime import datetime, timezone
from bson import ObjectId
from groq import Groq
from pymongo import MongoClient
import json

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = MongoClient('mongodb://localhost:27017/')
db = client.heartguard

# Get a random user
user = db.users.find_one()
if not user:
    print("No users found.")
    exit(1)
user_id = str(user['_id'])
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

recent_quests = list(db.daily_quests.find({"user_id": ObjectId(user_id)}).sort("date", -1).limit(5))
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
    groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else Groq()
    print("Calling Groq...")
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200,
        response_format={"type": "json_object"}
    )
    print("Response choice:")
    print(response.choices[0].message.content)
    quest_data = json.loads(response.choices[0].message.content)
    print("Parsed Quest:", quest_data)
except Exception as e:
    import traceback
    traceback.print_exc()
