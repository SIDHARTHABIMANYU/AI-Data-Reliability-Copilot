from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATISTICAL_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "statistical_results.csv"
)

ML_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "ml_results.csv"
)


def evaluate_anomaly_detection() -> None:

    statistical_df = pd.read_csv(
        STATISTICAL_FILE
    )

    ml_df = pd.read_csv(
        ML_FILE
    )

    # --------------------------------------------------
    # Statistical detection
    # --------------------------------------------------

    statistical_anomalies = (
        statistical_df[
            statistical_df["anomaly_status"] == "ANOMALY"
        ]
    )

    statistical_count = len(
        statistical_anomalies
    )

    statistical_evaluated = (
        statistical_df["revenue_z_score"]
        .notna()
        .sum()
    )

    statistical_rate = (
        statistical_count
        / statistical_evaluated
        * 100
    )

    # --------------------------------------------------
    # ML detection
    # --------------------------------------------------

    ml_anomalies = (
        ml_df[
            ml_df["ml_anomaly_status"] == "ANOMALY"
        ]
    )

    ml_count = len(ml_anomalies)

    ml_evaluated = len(ml_df)

    ml_rate = (
        ml_count
        / ml_evaluated
        * 100
    )

    # --------------------------------------------------
    # Agreement between detectors
    # --------------------------------------------------

    statistical_keys = set(
        zip(
            statistical_anomalies[
                "transaction_date"
            ],
            statistical_anomalies[
                "store_id"
            ]
        )
    )

    ml_keys = set(
        zip(
            ml_anomalies[
                "transaction_date"
            ],
            ml_anomalies[
                "store_id"
            ]
        )
    )

    agreement = (
        statistical_keys
        & ml_keys
    )

    ml_only = (
        ml_keys
        - statistical_keys
    )

    statistical_only = (
        statistical_keys
        - ml_keys
    )

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    print()
    print("=" * 55)
    print("V7 ANOMALY DETECTION EVALUATION")
    print("=" * 55)

    print()
    print("STATISTICAL DETECTOR")
    print("-" * 30)
    print(
        f"Evaluated rows: "
        f"{statistical_evaluated}"
    )
    print(
        f"Anomalies: "
        f"{statistical_count}"
    )
    print(
        f"Anomaly rate: "
        f"{statistical_rate:.2f}%"
    )

    print()
    print("ISOLATION FOREST")
    print("-" * 30)
    print(
        f"Evaluated rows: "
        f"{ml_evaluated}"
    )
    print(
        f"Anomalies: "
        f"{ml_count}"
    )
    print(
        f"Anomaly rate: "
        f"{ml_rate:.2f}%"
    )

    print()
    print("DETECTOR AGREEMENT")
    print("-" * 30)
    print(
        f"Both detected: "
        f"{len(agreement)}"
    )
    print(
        f"ML only: "
        f"{len(ml_only)}"
    )
    print(
        f"Statistical only: "
        f"{len(statistical_only)}"
    )

    print()
    print("=" * 55)


if __name__ == "__main__":
    evaluate_anomaly_detection()