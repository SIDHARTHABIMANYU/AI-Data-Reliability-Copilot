from pathlib import Path

import pandas as pd


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
    / "scenario_statistical_results.csv"
)

Z_SCORE_THRESHOLD = 3.0


def detect_scenario_anomalies() -> None:

    df = pd.read_csv(INPUT_FILE)

    df["revenue_z_score"] = (
        (
            df["total_revenue"]
            - df["revenue_7d_mean"]
        )
        / df["revenue_7d_std"]
    )

    df["anomaly_status"] = "NORMAL"

    valid_rows = df["revenue_z_score"].notna()

    df.loc[
        valid_rows
        & (
            df["revenue_z_score"].abs()
            > Z_SCORE_THRESHOLD
        ),
        "anomaly_status"
    ] = "ANOMALY"

    df["detection_method"] = "ROLLING_Z_SCORE"

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    anomaly_count = (
        df["anomaly_status"] == "ANOMALY"
    ).sum()

    print("Scenario statistical detection completed.")
    print(f"Evaluated rows: {valid_rows.sum()}")
    print(f"Anomalies detected: {anomaly_count}")
    print(f"Output: {OUTPUT_FILE}")

    target = df[
        (df["transaction_date"] == "2026-02-15")
        & (df["store_id"] == "STORE05")
    ]

    print("\nTarget scenario:")
    print(
        target[
            [
                "transaction_date",
                "store_id",
                "total_revenue",
                "revenue_z_score",
                "anomaly_status"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    detect_scenario_anomalies()