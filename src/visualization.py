from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


sns.set_theme(style="whitegrid")


def _prepare_output(path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def plot_segment_sizes(rfm: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = _prepare_output(output_path)
    counts = rfm["segment"].value_counts().sort_values(ascending=False).reset_index()
    counts.columns = ["segment", "customers"]

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=counts, x="segment", y="customers", palette="viridis")
    ax.set_title("Customer Count by Segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Customers")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    return output_path


def plot_frequency_monetary_scatter(rfm: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = _prepare_output(output_path)

    plt.figure(figsize=(10, 7))
    ax = sns.scatterplot(
        data=rfm,
        x="frequency",
        y="monetary",
        hue="segment",
        size="recency",
        sizes=(40, 240),
        alpha=0.8,
        palette="tab10",
    )
    ax.set_title("Customer Segments: Frequency vs Monetary")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Monetary Value")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    return output_path


def plot_segment_profiles(summary: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = _prepare_output(output_path)
    plot_df = summary.melt(
        id_vars=["segment"],
        value_vars=["recency", "frequency", "monetary"],
        var_name="metric",
        value_name="value",
    )

    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(data=plot_df, x="metric", y="value", hue="segment", marker="o")
    ax.set_title("Average RFM Profile by Segment")
    ax.set_xlabel("Metric")
    ax.set_ylabel("Average Value")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    return output_path
