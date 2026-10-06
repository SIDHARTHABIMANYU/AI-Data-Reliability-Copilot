from datetime import datetime

from backend.db.database import SessionLocal
from backend.db.models import RemediationAction

def create_pending_remediation(
    incident_id: int,
    proposed_change: str,
    risk: str
) -> int:

    db = SessionLocal()

    try:
        existing = (
            db.query(RemediationAction)
            .filter(
                RemediationAction.incident_id == incident_id,
                RemediationAction.status == "PENDING"
            )
            .order_by(
                RemediationAction.remediation_id.desc()
            )
            .first()
        )

        if existing:
            return existing.remediation_id

        remediation = RemediationAction(
            incident_id=incident_id,
            proposed_change=proposed_change,
            risk=risk,
            status="PENDING",
            created_at=datetime.now()
        )

        db.add(remediation)
        db.commit()
        db.refresh(remediation)

        return remediation.remediation_id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def approve_remediation(
    remediation_id: int,
    approved_by: str
) -> dict:

    db = SessionLocal()

    try:
        remediation = (
            db.query(RemediationAction)
            .filter(
                RemediationAction.remediation_id == remediation_id
            )
            .first()
        )

        if not remediation:
            return {"error": "Remediation not found"}

        if remediation.status != "PENDING":
            return {
                "error": (
                    f"Remediation is already "
                    f"{remediation.status}"
                )
            }

        remediation.status = "APPROVED"
        remediation.approved_by = approved_by
        remediation.approved_at = datetime.now()

        db.commit()
        db.refresh(remediation)

        return {
            "remediation_id": remediation.remediation_id,
            "incident_id": remediation.incident_id,
            "status": remediation.status,
            "approved_by": remediation.approved_by,
            "approved_at": remediation.approved_at,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def reject_remediation(
    remediation_id: int,
    rejected_by: str
) -> dict:

    db = SessionLocal()

    try:
        remediation = (
            db.query(RemediationAction)
            .filter(
                RemediationAction.remediation_id == remediation_id
            )
            .first()
        )

        if not remediation:
            return {"error": "Remediation not found"}

        if remediation.status != "PENDING":
            return {
                "error": (
                    f"Remediation is already "
                    f"{remediation.status}"
                )
            }

        remediation.status = "REJECTED"
        remediation.approved_by = rejected_by
        remediation.approved_at = datetime.now()

        db.commit()
        db.refresh(remediation)

        return {
            "remediation_id": remediation.remediation_id,
            "incident_id": remediation.incident_id,
            "status": remediation.status,
            "approved_by": remediation.approved_by,
            "approved_at": remediation.approved_at,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()