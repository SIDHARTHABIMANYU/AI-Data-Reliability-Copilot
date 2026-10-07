from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "scenario_features.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "scenario_ml_results.csv"
)

FEATURE_COLUMNS = [
    "total_revenue",
    "total_transactions",
    "total_quantity",
    "revenue_change_pct",
    "transaction_change_pct",
    "quantity_change_pct",
    "revenue_deviation_pct",
]


def detect_scenario_ml_anomalies() -> None:

    df = pd.read_csv(INPUT_FILE)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    model_df = df.dropna(
        subset=FEATURE_COLUMNS
    ).copy()

    X = model_df[FEATURE_COLUMNS]

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(X)

    scores = model.decision_function(X)

    model_df["ml_prediction"] = predictions

    model_df["ml_anomaly_score"] = scores

    model_df["ml_anomaly_status"] = "NORMAL"

    model_df.loc[
        model_df["ml_prediction"] == -1,
        "ml_anomaly_status"
    ] = "ANOMALY"

    model_df["detection_method"] = (
        "ISOLATION_FOREST"
    )

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

    print("Scenario ML anomaly detection completed.")
    print(f"Evaluated rows: {len(model_df)}")
    print(f"ML anomalies detected: {anomaly_count}")
    print(f"Output: {OUTPUT_FILE}")

    target = model_df[
        (model_df["transaction_date"] == "2026-02-15")
        & (model_df["store_id"] == "STORE05")
    ]

    print("\nTarget scenario:")

    if target.empty:
        print("Target scenario was not evaluated.")
    else:
        print(
            target[
                [
                    "transaction_date",
                    "store_id",
                    "total_revenue",
                    "revenue_deviation_pct",
                    "ml_anomaly_score",
                    "ml_anomaly_status"
                ]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    detect_scenario_ml_anomalies()