"""Visualization helpers for EDA and model performance."""

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server environments

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path


def plot_class_distribution(
    df: pd.DataFrame,
    target_col: str = "match_compatibility",
    output_path: str = "data/processed/class_distribution.png",
) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df[target_col].value_counts().sort_index()
    labels = {0: "Low", 1: "Mid", 2: "High"}
    ax.bar(
        [labels.get(k, str(k)) for k in counts.index],
        counts.values,
        color=["#ef4444", "#f59e0b", "#22c55e"],
    )
    ax.set_title("Matchmaking Compatibility Class Distribution")
    ax.set_xlabel("Compatibility Class")
    ax.set_ylabel("Count")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 5, str(v), ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close()
    print(f"[viz] Saved class distribution → {output_path}")


def plot_confusion_matrix(
    cm: list[list[int]],
    output_path: str = "data/processed/confusion_matrix.png",
) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    labels = ["Low", "Mid", "High"]
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        ax=ax,
    )
    ax.set_title("Confusion Matrix — Match Compatibility")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close()
    print(f"[viz] Saved confusion matrix → {output_path}")


def plot_feature_importance(
    importances: np.ndarray,
    feature_names: list[str],
    output_path: str = "data/processed/feature_importance.png",
    top_n: int = 10,
) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    indices = np.argsort(importances)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(
        [feature_names[i] for i in reversed(indices)],
        [importances[i] for i in reversed(indices)],
        color="#6366f1",
    )
    ax.set_title("Feature Importances (Top 10)")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close()
    print(f"[viz] Saved feature importance → {output_path}")
