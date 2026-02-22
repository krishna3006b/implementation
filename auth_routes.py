"""Authentication routes for HeartGuard."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from bson import ObjectId
from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)

JWT_SECRET = os.environ.get("JWT_SECRET", "heartguard-dev-secret-change-me")
JWT_EXPIRY_HOURS = 72


def get_db():
    from api import get_mongo_db
    return get_mongo_db()


def make_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def require_auth():
    """Extract and verify JWT from Authorization header. Returns user_id or aborts."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, (jsonify({"error": "Missing or invalid token"}), 401)
    token = auth_header.split(" ", 1)[1]
    user_id = verify_token(token)
    if not user_id:
        return None, (jsonify({"error": "Invalid or expired token"}), 401)
    return user_id, None


@auth_bp.route("/api/auth/signup", methods=["POST"])
def signup():
    db = get_db()
    data = request.get_json(force=True)

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc),
        "prediction_result": None,
    }
    result = db.users.insert_one(user)
    user_id = str(result.inserted_id)
    token = make_token(user_id)

    return jsonify({"token": token, "user": {"id": user_id, "name": name, "email": email}}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    db = get_db()
    data = request.get_json(force=True)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = db.users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"error": "Invalid email or password"}), 401

    user_id = str(user["_id"])
    token = make_token(user_id)

    return jsonify({
        "token": token,
        "user": {
            "id": user_id,
            "name": user["name"],
            "email": user["email"],
            "prediction_result": user.get("prediction_result"),
        },
    })


@auth_bp.route("/api/auth/me", methods=["GET"])
def me():
    user_id, err = require_auth()
    if err:
        return err

    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "prediction_result": user.get("prediction_result"),
    })
