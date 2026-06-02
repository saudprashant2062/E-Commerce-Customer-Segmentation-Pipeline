from __future__ import annotations

import argparse
from pathlib import Path

from .config import DEFAULT_CLEANED_FILE, DEFAULT_INPUT_FILE, DEFAULT_RFM_FILE, DEFAULT_SUMMARY_FILE, MODEL_DIR, OUTPUT_DIR, PLOT_DIR
from .data_prep import clean_transactions, compute_rfm, load_transactions
from .sample_data import generate_sample_transactions
from .segmentation import assign_segment_names, cluster_profile_summary, evaluate_cluster_candidates, fit_kmeans, save_artifacts, scale_rfm_features
from .visualization import plot_frequency_monetary_scatter, plot_segment_profiles, plot_segment_sizes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="E-commerce customer segmentation pipeline")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_FILE, help="Path to the transaction CSV")
    parser.add_argument("--clusters", type=int, default=4, help="Number of K-Means clusters")
    parser.add_argument("--auto-clusters", action="store_true", help="Choose the best cluster count using silhouette score")
    parser.add_argument("--generate-sample", action="store_true", help="Generate synthetic sample data when the input file is missing")
    return parser.parse_args()


def ensure_directories() -> None:
    for path in [OUTPUT_DIR, MODEL_DIR, PLOT_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    ensure_directories()

    input_path = args.input
    if not input_path.exists():
        if args.generate_sample:
            print(f"Input file not found. Generating sample dataset at {input_path}.")
            generate_sample_transactions(input_path)
        else:
            print(f"Input file not found at {input_path}. Generating a demo dataset.")
            generate_sample_transactions(input_path)

    raw_df = load_transactions(input_path)
    cleaned_df = clean_transactions(raw_df)
    cleaned_df.to_csv(DEFAULT_CLEANED_FILE, index=False)

    rfm = compute_rfm(cleaned_df)
    rfm.to_csv(DEFAULT_RFM_FILE, index=False)

    features, scaler = scale_rfm_features(rfm)

    candidate_scores = evaluate_cluster_candidates(features)
    best_candidate = int(candidate_scores.iloc[0]["clusters"]) if not candidate_scores.empty else args.clusters
    n_clusters = best_candidate if args.auto_clusters and not candidate_scores.empty else args.clusters

    model, labels, silhouette = fit_kmeans(features, n_clusters=n_clusters)
    rfm["cluster"] = labels

    summary = cluster_profile_summary(rfm)
    cluster_map = assign_segment_names(summary)
    rfm["segment"] = rfm["cluster"].map(cluster_map)

    summary["segment"] = summary["cluster"].map(cluster_map)
    summary = summary[["cluster", "segment", "customers", "recency", "frequency", "monetary", "avg_order_value"]]
    summary.to_csv(DEFAULT_SUMMARY_FILE, index=False)

    rfm_out = DEFAULT_RFM_FILE.with_name("rfm_customers_segmented.csv")
    rfm.to_csv(rfm_out, index=False)

    model_path = MODEL_DIR / "kmeans_model.joblib"
    save_artifacts(model, scaler, cluster_map, str(model_path))

    plot_segment_sizes(rfm, PLOT_DIR / "segment_sizes.png")
    plot_frequency_monetary_scatter(rfm, PLOT_DIR / "frequency_vs_monetary.png")
    plot_segment_profiles(summary, PLOT_DIR / "segment_profiles.png")

    print("Pipeline completed successfully.")
    if not candidate_scores.empty:
        print("Top silhouette candidates:")
        print(candidate_scores.head().to_string(index=False))
    if silhouette is not None:
        print(f"Chosen model silhouette score: {silhouette:.4f}")
    print(f"Cleaned data saved to: {DEFAULT_CLEANED_FILE}")
    print(f"RFM data saved to: {rfm_out}")
    print(f"Segment summary saved to: {DEFAULT_SUMMARY_FILE}")
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()
