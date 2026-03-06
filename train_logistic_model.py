from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# All 13 feature columns from heart.csv (excluding the target 'output')
ALL_FEATURES = [
    "age",
    "sex",
    "cp",
    "trtbps",
    "chol",
    "fbs",
    "restecg",
    "thalachh",
    "exng",
    "oldpeak",
    "slp",
    "caa",
    "thall",
]

# Top 7 features identified via mutual information in the notebook
TOP7_FEATURES = ["thall", "caa", "cp", "oldpeak", "exng", "chol", "thalachh"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a Logistic Regression model for heart disease risk prediction."
    )
    parser.add_argument("--data", required=True, help="Path to heart disease CSV file")
    parser.add_argument("--target", default="output", help="Target column name")
    parser.add_argument(
        "--risk-label",
        default="1",
        help="Target value that represents elevated heart disease risk (default: 1)",
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parent / "logistic_model.joblib"),
        help="Output model artifact path (default: <project_dir>/logistic_model.joblib)",
    )
    parser.add_argument(
        "--top7-only",
        action="store_true",
        help="Use only the top 7 MI-selected features instead of all 13",
    )
    return parser.parse_args()


def read_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def select_features(df: pd.DataFrame, target_col: str, top7_only: bool) -> list[str]:
    if top7_only:
        chosen = TOP7_FEATURES
    else:
        chosen = ALL_FEATURES

    missing = [col for col in chosen if col not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing expected columns: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )
    return chosen


def treat_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Cap upper outliers at the 90th percentile (same as the notebook)."""
    import numpy as np

    df = df.copy()
    for col in ["trtbps", "chol", "oldpeak"]:
        if col in df.columns:
            upper = df[col].quantile(0.90)
            df[col] = np.where(df[col] > upper, upper, df[col])
    return df


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)

    df = read_dataset(data_path)
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in dataset")

    # Apply the same outlier treatment used in the notebook
    df = treat_outliers(df)

    feature_columns = select_features(df, args.target, args.top7_only)

    target_series = df[args.target]
    risk_label = args.risk_label
    try:
        risk_label = target_series.dtype.type(risk_label)
    except Exception:
        pass

    y = (target_series == risk_label).astype(int)
    x = df[feature_columns]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_auc = cross_val_score(model, x_train, y_train, cv=cv, scoring="roc_auc")

    model.fit(x_train, y_train)
    y_proba = model.predict_proba(x_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    artifact = {
        "model_name": "Logistic Regression",
        "model": model,
        "feature_columns": feature_columns,
        "target_column": args.target,
        "risk_label": args.risk_label,
        "metrics": {
            "cv_roc_auc_mean": float(cv_auc.mean()),
            "cv_roc_auc_std": float(cv_auc.std()),
            "test_roc_auc": float(roc_auc_score(y_test, y_proba)),
            "test_accuracy": float(accuracy_score(y_test, y_pred)),
        },
    }

    output_path = Path(args.output)
    joblib.dump(artifact, output_path)

    print(f"Saved model to: {output_path}")
    print(f"Features used ({len(feature_columns)}): {feature_columns}")
    print("Metrics:")
    for metric_name, value in artifact["metrics"].items():
        print(f"  {metric_name}: {value:.4f}")

    print("\n" + "=" * 60)
    print("Classification Report")
    print("=" * 60)
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["No Risk (0)", "Risk (1)"],
        )
    )


if __name__ == "__main__":
    main()
