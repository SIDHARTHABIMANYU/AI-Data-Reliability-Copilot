from fastapi import APIRouter, HTTPException

from backend.db.database import SessionLocal
from backend.db.models import (
    Incident,
    RemediationAction,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary():

    db = SessionLocal()

    try:
        incidents = (
            db.query(Incident)
            .order_by(Incident.detected_at.desc())
            .all()
        )

        total_incidents = len(incidents)

        open_incidents = sum(
            1
            for incident in incidents
            if incident.status == "OPEN"
        )

        resolved_incidents = sum(
            1
            for incident in incidents
            if incident.status == "RESOLVED"
        )

        high_severity_incidents = sum(
            1
            for incident in incidents
            if incident.severity == "HIGH"
        )

        pending_remediations = (
            db.query(RemediationAction)
            .filter(
                RemediationAction.status == "PENDING"
            )
            .count()
        )

        approved_remediations = (
            db.query(RemediationAction)
            .filter(
                RemediationAction.status == "APPROVED"
            )
            .count()
        )

        return {
            "total_incidents": total_incidents,
            "open_incidents": open_incidents,
            "resolved_incidents": resolved_incidents,
            "high_severity_incidents": high_severity_incidents,
            "pending_remediations": pending_remediations,
            "approved_remediations": approved_remediations,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve dashboard summary."
        )

    finally:
        db.close()