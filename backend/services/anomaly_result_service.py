from datetime import datetime

import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import AnomalyResult


def save_anomaly_results(
    file_path: str
) -> None:

    df = pd.read_csv(file_path)

    db = SessionLocal()

    try:

        for _, row in df.iterrows():

            result = AnomalyResult(
                transaction_date=pd.to_datetime(
                    row["transaction_date"]
                ).date(),

                store_id=row["store_id"],

                total_revenue=row["total_revenue"],

                total_transactions=int(
                    row["total_transactions"]
                ),

                total_quantity=int(
                    row["total_quantity"]
                ),

                anomaly_score=row[
                    "ml_anomaly_score"
                ],

                anomaly_status=row[
                    "ml_anomaly_status"
                ],

                detection_method=row[
                    "detection_method"
                ],

                detected_at=datetime.now()
            )

            db.add(result)

        db.commit()

        print(
            f"Saved {len(df)} anomaly results."
        )

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":

    save_anomaly_results(
        "data/anomaly/ml_results.csv"
    )