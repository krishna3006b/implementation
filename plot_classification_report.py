"""
Visualise the classification report of the trained logistic-regression model.

Usage:
    python3 plot_classification_report.py --data "heart (4).csv"

The script loads the saved model artifact, generates predictions on the
test split, and creates a matplotlib figure with:
  1. A heatmap of precision / recall / F1-score per class
  2. A bar chart comparing per-class F1 scores
  3. Overall accuracy & ROC-AUC annotated on the figure
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

# ── same outlier treatment as the training script ──────────────────────
def treat_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["trtbps", "chol", "oldpeak"]:
        if col in df.columns:
            upper = df[col].quantile(0.90)
            df[col] = np.where(df[col] > upper, upper, df[col])
    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot classification report for the trained model."
    )
    parser.add_argument("--data", required=True, help="Path to heart disease CSV file")
    parser.add_argument(
        "--model",
        default=str(Path(__file__).resolve().parent / "logistic_model.joblib"),
        help="Path to saved model artifact (.joblib)",
    )
    parser.add_argument(
        "--save",
        default="",
        help="If provided, save the figure to this path instead of showing it",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # ── load model artifact ────────────────────────────────────────────
    artifact = joblib.load(args.model)
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    target_col = artifact["target_column"]
    risk_label = artifact["risk_label"]

    # ── recreate the same test split ───────────────────────────────────
    df = pd.read_csv(args.data)
    df = treat_outliers(df)

    target_series = df[target_col]
    try:
        risk_label = target_series.dtype.type(risk_label)
    except Exception:
        pass

    y = (target_series == risk_label).astype(int)
    x = df[feature_columns]

    _, x_test, _, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    y_proba = model.predict_proba(x_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    # ── compute metrics ────────────────────────────────────────────────
    class_names = ["No Risk (0)", "Risk (1)"]
    report = classification_report(
        y_test, y_pred, target_names=class_names, output_dict=True
    )
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    # ── build figure ───────────────────────────────────────────────────
    fig = plt.figure(figsize=(20, 6), facecolor="#0f0f1a")
    fig.suptitle(
        "Logistic Regression — Classification Report",
        fontsize=18,
        fontweight="bold",
        color="white",
        y=0.97,
    )

    # custom colour-map (dark purple → teal → gold)
    cmap = LinearSegmentedColormap.from_list(
        "report_cmap", ["#1a1a2e", "#16213e", "#0f3460", "#00b4d8", "#f9c74f"]
    )

    # ── subplot 1: heatmap ─────────────────────────────────────────────
    ax1 = fig.add_subplot(1, 3, 1)

    metrics_labels = ["precision", "recall", "f1-score"]
    rows = class_names + ["macro avg", "weighted avg"]
    data = np.array([[report[r][m] for m in metrics_labels] for r in rows])

    im = ax1.imshow(data, cmap=cmap, aspect="auto", vmin=0.5, vmax=1.0)
    ax1.set_xticks(range(len(metrics_labels)))
    ax1.set_xticklabels(
        [m.capitalize() for m in metrics_labels], color="white", fontsize=11
    )
    ax1.set_yticks(range(len(rows)))
    ax1.set_yticklabels(rows, color="white", fontsize=11)

    for i in range(len(rows)):
        for j in range(len(metrics_labels)):
            val = data[i, j]
            text_color = "black" if val > 0.85 else "white"
            ax1.text(
                j, i, f"{val:.2f}",
                ha="center", va="center",
                fontsize=13, fontweight="bold", color=text_color,
            )

    ax1.set_title("Per-Class Metrics", color="white", fontsize=13, pad=10)
    ax1.tick_params(colors="white")
    ax1.set_facecolor("#0f0f1a")
    plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)

    # ── subplot 2: bar chart of F1 + accuracy / AUC annotation ────────
    ax2 = fig.add_subplot(1, 3, 2)
    f1_scores = [report[c]["f1-score"] for c in class_names]
    bar_colours = ["#00b4d8", "#f9c74f"]

    bars = ax2.barh(class_names, f1_scores, color=bar_colours, height=0.45, edgecolor="white", linewidth=0.6)
    for bar, score in zip(bars, f1_scores):
        ax2.text(
            bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
            f"{score:.2f}", va="center", fontsize=13, fontweight="bold", color="white",
        )

    ax2.set_xlim(0, 1.1)
    ax2.set_title("F1-Score by Class", color="white", fontsize=13, pad=10)
    ax2.set_facecolor("#0f0f1a")
    ax2.tick_params(colors="white")
    ax2.spines["bottom"].set_color("white")
    ax2.spines["left"].set_color("white")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.xaxis.label.set_color("white")

    # annotate overall metrics
    summary_text = (
        f"Accuracy : {acc:.4f}\n"
        f"ROC-AUC  : {auc:.4f}\n"
        f"Macro F1 : {report['macro avg']['f1-score']:.4f}"
    )
    ax2.text(
        0.60, 0.15, summary_text,
        transform=ax2.transAxes,
        fontsize=12, fontfamily="monospace", color="#a3f7bf",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#1a1a2e", edgecolor="#00b4d8"),
    )

    # ── subplot 3: confusion matrix ───────────────────────────────────
    ax3 = fig.add_subplot(1, 3, 3)
    cm = confusion_matrix(y_test, y_pred)
    im3 = ax3.imshow(cm, cmap=cmap, aspect="auto")

    ax3.set_xticks(range(len(class_names)))
    ax3.set_xticklabels(class_names, color="white", fontsize=10, rotation=20, ha="right")
    ax3.set_yticks(range(len(class_names)))
    ax3.set_yticklabels(class_names, color="white", fontsize=10)
    ax3.set_xlabel("Predicted", color="white", fontsize=11)
    ax3.set_ylabel("Actual", color="white", fontsize=11)
    ax3.set_title("Confusion Matrix", color="white", fontsize=13, pad=10)
    ax3.set_facecolor("#0f0f1a")
    ax3.tick_params(colors="white")

    for i in range(len(class_names)):
        for j in range(len(class_names)):
            val = cm[i, j]
            text_color = "black" if val > cm.max() * 0.7 else "white"
            ax3.text(
                j, i, str(val),
                ha="center", va="center",
                fontsize=16, fontweight="bold", color=text_color,
            )

    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    if args.save:
        fig.savefig(args.save, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"Figure saved to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
