"""Flask API backend for HeartGuard React frontend."""

from __future__ import annotations

import os
from pathlib import Path

import joblib
import numpy as np
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)


def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


app.after_request(add_cors_headers)

MODEL_PATH = Path(__file__).resolve().parent / "logistic_model.joblib"

_artifact = None


def get_artifact():
    global _artifact
    if _artifact is None:
        if not MODEL_PATH.exists():
            return None
        _artifact = joblib.load(MODEL_PATH)
    return _artifact


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
    return jsonify(
        {
            "status": "ok",
            "model_loaded": artifact is not None,
            "model_name": artifact.get("model_name") if artifact else None,
            "features": artifact.get("feature_columns") if artifact else None,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host="0.0.0.0", port=port)
