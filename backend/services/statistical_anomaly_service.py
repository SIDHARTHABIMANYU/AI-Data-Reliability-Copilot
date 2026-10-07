from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = BASE_DIR / "data" / "anomaly" / "features.csv"
OUTPUT_FILE = BASE_DIR / "data" / "anomaly" / "statistical_results.csv"

Z_SCORE_THRESHOLD = 3.0


def detect_statistical_anomalies() -> None:

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

    evaluated_count = valid_rows.sum()

    print("Statistical anomaly detection completed.")
    print(f"Evaluated rows: {evaluated_count}")
    print(f"Anomalies detected: {anomaly_count}")
    print(f"Z-score threshold: {Z_SCORE_THRESHOLD}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    detect_statistical_anomalies()