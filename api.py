"""Flask API backend for HeartGuard React frontend."""

from __future__ import annotations

import os
from pathlib import Path

import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------------------------
# MongoDB
# ---------------------------------------------------------------------------
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/heartguard")
_mongo_client = None
_mongo_db = None


def get_mongo_db():
    global _mongo_client, _mongo_db
    if _mongo_db is None:
        _mongo_client = MongoClient(MONGO_URI)
        db_name = MONGO_URI.rsplit("/", 1)[-1].split("?")[0] or "heartguard"
        _mongo_db = _mongo_client[db_name]
    return _mongo_db


# ---------------------------------------------------------------------------
# ML Model
# ---------------------------------------------------------------------------
MODEL_PATH = Path(__file__).resolve().parent / "logistic_model.joblib"
_artifact = None


def get_artifact():
    global _artifact
    if _artifact is None:
        if not MODEL_PATH.exists():
            return None
        _artifact = joblib.load(MODEL_PATH)
    return _artifact


# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------
from auth_routes import auth_bp
from goals_routes import goals_bp
from tracker_routes import tracker_bp
from ai_routes import ai_bp

app.register_blueprint(auth_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(tracker_bp)
app.register_blueprint(ai_bp)


# ---------------------------------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------------------------------
@app.route("/api/predict", methods=["POST"])
def predict():
    artifact = get_artifact()
    if artifact is None:
        return jsonify({"error": "Model not found. Train the model first."}), 500

    data = request.get_json(force=True)

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    try:
        row = {col: float(data[col]) for col in feature_columns}
    except KeyError as e:
        return jsonify({"error": f"Missing feature: {e}"}), 400

    import pandas as pd

    df = pd.DataFrame([row])[feature_columns]
    prob = float(model.predict_proba(df)[0][1])
    prediction = 1 if prob >= 0.5 else 0
    confidence = abs(0.5 - prob) * 200

    # If user is authenticated, save prediction result
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        from auth_routes import verify_token
        from bson import ObjectId

        token = auth_header.split(" ", 1)[1]
        user_id = verify_token(token)
        if user_id:
            db = get_mongo_db()
            db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"prediction_result": {
                    "prediction": prediction,
                    "probability": round(prob, 4),
                    "confidence": round(confidence, 1),
                }}},
            )

    return jsonify(
        {
            "prediction": prediction,
            "probability": round(prob, 4),
            "confidence": round(confidence, 1),
            "model_name": artifact.get("model_name", "Logistic Regression"),
            "features_used": feature_columns,
        }
    )


@app.route("/api/health", methods=["GET"])
def health():
    artifact = get_artifact()

    # Check MongoDB connection
    mongo_ok = False
    try:
        db = get_mongo_db()
        db.command("ping")
        mongo_ok = True
    except Exception:
        pass

    return jsonify(
        {
            "status": "ok",
            "model_loaded": artifact is not None,
            "model_name": artifact.get("model_name") if artifact else None,
            "features": artifact.get("feature_columns") if artifact else None,
            "database": "connected" if mongo_ok else "disconnected",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
