from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = ["recency", "frequency", "monetary"]


@dataclass
class SegmentationArtifacts:
    scaler: StandardScaler
    model: KMeans
    cluster_map: dict[int, str]
    silhouette: float | None


def scale_rfm_features(rfm: pd.DataFrame) -> tuple[np.ndarray, StandardScaler]:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(rfm[FEATURE_COLUMNS])
    return scaled, scaler


def evaluate_cluster_candidates(features: np.ndarray, candidate_clusters: range = range(2, 7)) -> pd.DataFrame:
    records = []
    for clusters in candidate_clusters:
        if clusters >= len(features):
            continue
        model = KMeans(n_clusters=clusters, random_state=42, n_init=10)
        labels = model.fit_predict(features)
        score = silhouette_score(features, labels)
        records.append({"clusters": clusters, "silhouette": score, "inertia": model.inertia_})
    return pd.DataFrame(records).sort_values(["silhouette", "clusters"], ascending=[False, True]).reset_index(drop=True)


def fit_kmeans(features: np.ndarray, n_clusters: int = 4) -> tuple[KMeans, np.ndarray, float | None]:
    if len(features) < 2:
        raise ValueError("At least two customers are required for clustering.")

    n_clusters = max(2, min(int(n_clusters), len(features)))
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = model.fit_predict(features)
    silhouette = None
    if len(set(labels)) > 1:
        silhouette = silhouette_score(features, labels)
    return model, labels, silhouette


def cluster_profile_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    summary = (
        rfm.groupby("cluster")
        .agg(
            customers=("customer_id", "count"),
            recency=("recency", "mean"),
            frequency=("frequency", "mean"),
            monetary=("monetary", "mean"),
            avg_order_value=("avg_order_value", "mean"),
        )
        .reset_index()
    )
    return summary


def assign_segment_names(summary: pd.DataFrame) -> dict[int, str]:
    ranked = summary.copy()
    ranked["recency_rank"] = ranked["recency"].rank(ascending=True, method="dense")
    ranked["frequency_rank"] = ranked["frequency"].rank(ascending=False, method="dense")
    ranked["monetary_rank"] = ranked["monetary"].rank(ascending=False, method="dense")
    ranked["score"] = ranked[["recency_rank", "frequency_rank", "monetary_rank"]].sum(axis=1)
    ranked = ranked.sort_values(["score", "customers"], ascending=[True, False])

    labels = ["High Value", "Loyal", "Promising", "At Risk", "Needs Attention"]
    mapping: dict[int, str] = {}
    for index, cluster_id in enumerate(ranked["cluster"].tolist()):
        mapping[int(cluster_id)] = labels[index] if index < len(labels) else f"Segment {index + 1}"
    return mapping


def save_artifacts(model: KMeans, scaler: StandardScaler, cluster_map: dict[int, str], output_path: str) -> None:
    dump({"model": model, "scaler": scaler, "cluster_map": cluster_map}, output_path)
