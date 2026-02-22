from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DEFAULT_FEATURES = ["thall", "caa", "cp", "oldpeak", "exng", "chol", "thalachh"]


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
        default="logistic_model.joblib",
        help="Output model artifact path (default: logistic_model.joblib)",
    )
    parser.add_argument(
        "--all-features",
        action="store_true",
        help="Use all numeric feature columns except target",
    )
    return parser.parse_args()


def read_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def select_features(df: pd.DataFrame, target_col: str, use_all_features: bool) -> list[str]:
    if use_all_features:
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        return [c for c in numeric_cols if c != target_col]

    missing = [col for col in DEFAULT_FEATURES if col not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing expected columns for app compatibility: {missing}. "
            f"Use --all-features only if you also update app inputs."
        )
    return DEFAULT_FEATURES


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)

    df = read_dataset(data_path)
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in dataset")

    feature_columns = select_features(df, args.target, args.all_features)

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
    print(f"Features used: {feature_columns}")
    print("Metrics:")
    for metric_name, value in artifact["metrics"].items():
        print(f"  {metric_name}: {value:.4f}")


if __name__ == "__main__":
    main()
