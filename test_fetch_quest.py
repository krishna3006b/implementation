import requests
import jwt
from datetime import datetime, timedelta, timezone
import os
from pymongo import MongoClient

JWT_SECRET = "super-secret-key-123"

# Connect to DB and get krishna
client = MongoClient('mongodb://localhost:27017/')
user = client.heartguard.users.find_one({"name": {"$regex": "krishna", "$options": "i"}})
if not user:
    user = client.heartguard.users.find_one()

user_id = str(user["_id"])

# Make token
payload = {
    "sub": user_id,
    "exp": datetime.now(timezone.utc) + timedelta(hours=72),
    "iat": datetime.now(timezone.utc),
}
token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# Test fetch
print("Fetching /api/ai/quest...")
try:
    res = requests.post("http://localhost:5001/api/ai/quest", headers={"Authorization": f"Bearer {token}"})
    print("Status:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", e)
