from datetime import datetime
from pathlib import Path

import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import Incident


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ML_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "ml_results.csv"
)

FEATURE_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "features.csv"
)

Z_SCORE_CONFIRMATION_THRESHOLD = 2.5


def create_anomaly_incidents() -> None:

    ml_df = pd.read_csv(ML_FILE)
    feature_df = pd.read_csv(FEATURE_FILE)

    print("ML columns:")
    print(list(ml_df.columns))

    print("\nFeature columns:")
    print(list(feature_df.columns))

    # Only take the columns we actually need
    statistical_df = feature_df[
        [
            "transaction_date",
            "store_id",
            "revenue_z_score"
        ]
    ].copy()

    # Make sure both join columns use the same format
    ml_df["transaction_date"] = (
        pd.to_datetime(
            ml_df["transaction_date"]
        ).dt.strftime("%Y-%m-%d")
    )

    statistical_df["transaction_date"] = (
        pd.to_datetime(
            statistical_df["transaction_date"]
        ).dt.strftime("%Y-%m-%d")
    )

    # Remove any possible existing z-score column
    # from the ML dataframe before merging.
    if "revenue_z_score" in ml_df.columns:
        ml_df = ml_df.drop(
            columns=["revenue_z_score"]
        )

    df = ml_df.merge(
        statistical_df,
        on=[
            "transaction_date",
            "store_id"
        ],
        how="left"
    )

    print("\nMerged columns:")
    print(list(df.columns))

    # Safety check
    if "revenue_z_score" not in df.columns:
        raise ValueError(
            "revenue_z_score was not created after merge."
        )

    db = SessionLocal()
    created_count = 0

    try:

        for _, row in df.iterrows():

            # Only ML anomalies continue
            if row["ml_anomaly_status"] != "ANOMALY":
                continue

            z_score = row["revenue_z_score"]

            # No statistical evidence
            if pd.isna(z_score):
                continue

            # Require statistical confirmation
            if abs(z_score) < Z_SCORE_CONFIRMATION_THRESHOLD:
                continue

            transaction_date = pd.to_datetime(
                row["transaction_date"]
            ).date()

            file_name = (
                f"daily_revenue_{transaction_date}.csv"
            )

            existing = (
                db.query(Incident)
                .filter(
                    Incident.dataset == "daily_revenue",
                    Incident.file_name == file_name,
                    Incident.incident_type == "ANOMALY"
                )
                .first()
            )

            if existing:
                continue

            incident = Incident(
                dataset="daily_revenue",
                file_name=file_name,
                incident_type="ANOMALY",
                severity="MEDIUM",
                description=(
                    f"ML anomaly detected for "
                    f"{row['store_id']} on "
                    f"{transaction_date}. "
                    f"Revenue: "
                    f"{row['total_revenue']:.2f}. "
                    f"Revenue z-score: "
                    f"{z_score:.2f}."
                ),
                status="OPEN",
                detected_at=datetime.now()
            )

            db.add(incident)
            created_count += 1

        db.commit()

        print(
            f"\nAnomaly incidents created: "
            f"{created_count}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_anomaly_incidents()