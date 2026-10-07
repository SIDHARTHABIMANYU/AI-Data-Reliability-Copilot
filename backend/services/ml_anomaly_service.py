from pathlib import Path

import pandas as pd

from sklearn.ensemble import IsolationForest


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = BASE_DIR / "data" / "anomaly" / "features.csv"
OUTPUT_FILE = BASE_DIR / "data" / "anomaly" / "ml_results.csv"


FEATURE_COLUMNS = [
    "total_revenue",
    "total_transactions",
    "total_quantity",
    "revenue_change_pct",
    "transaction_change_pct",
    "quantity_change_pct",
    "revenue_deviation_pct",
]


def detect_ml_anomalies() -> None:

    df = pd.read_csv(INPUT_FILE)

    # Remove rows where rolling features are not available.
    model_df = df.dropna(
        subset=FEATURE_COLUMNS
    ).copy()

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(
        model_df[FEATURE_COLUMNS]
    )

    # Isolation Forest:
    # 1  = normal
    # -1 = anomaly
    model_df["ml_prediction"] = model.predict(
        model_df[FEATURE_COLUMNS]
    )

    model_df["ml_anomaly_score"] = (
        model.decision_function(
            model_df[FEATURE_COLUMNS]
        )
    )

    model_df["ml_anomaly_status"] = (
        model_df["ml_prediction"]
        .map({
            1: "NORMAL",
            -1: "ANOMALY"
        })
    )

    model_df["detection_method"] = "ISOLATION_FOREST"

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    model_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    anomaly_count = (
        model_df["ml_anomaly_status"] == "ANOMALY"
    ).sum()

    print("ML anomaly detection completed.")
    print(f"Rows evaluated: {len(model_df)}")
    print(f"Anomalies detected: {anomaly_count}")
    print("Model: Isolation Forest")
    print("Contamination: 0.05")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    detect_ml_anomalies()