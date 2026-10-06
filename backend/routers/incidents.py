from fastapi import APIRouter, HTTPException

from backend.db.database import SessionLocal
from backend.db.models import Incident


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.get("/")
def get_incidents():
    db = SessionLocal()

    try:
        incidents = (
            db.query(Incident)
            .order_by(Incident.detected_at.desc())
            .all()
        )

        return [
            {
                "incident_id": incident.incident_id,
                "dataset": incident.dataset,
                "file_name": incident.file_name,
                "incident_type": incident.incident_type,
                "severity": incident.severity,
                "description": incident.description,
                "status": incident.status,
                "detected_at": incident.detected_at,
                "resolved_at": incident.resolved_at,
            }
            for incident in incidents
        ]

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve incidents."
        )

    finally:
        db.close()