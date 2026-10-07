from fastapi import APIRouter

from backend.db.database import SessionLocal
from backend.db.models import AnomalyResult


router = APIRouter(
    prefix="/anomalies",
    tags=["Anomalies"]
)


@router.get("/")
def get_anomalies():

    db = SessionLocal()

    try:
        anomalies = (
            db.query(AnomalyResult)
            .filter(
                AnomalyResult.anomaly_status == "ANOMALY"
            )
            .order_by(
                AnomalyResult.transaction_date.desc()
            )
            .all()
        )

        return [
            {
                "anomaly_id": anomaly.anomaly_id,
                "transaction_date": anomaly.transaction_date,
                "store_id": anomaly.store_id,
                "total_revenue": float(
                    anomaly.total_revenue
                )
                if anomaly.total_revenue is not None
                else None,
                "total_transactions": (
                    anomaly.total_transactions
                ),
                "total_quantity": (
                    anomaly.total_quantity
                ),
                "anomaly_score": float(
                    anomaly.anomaly_score
                )
                if anomaly.anomaly_score is not None
                else None,
                "anomaly_status": (
                    anomaly.anomaly_status
                ),
                "detection_method": (
                    anomaly.detection_method
                ),
                "detected_at": anomaly.detected_at
            }
            for anomaly in anomalies
        ]

    finally:
        db.close()