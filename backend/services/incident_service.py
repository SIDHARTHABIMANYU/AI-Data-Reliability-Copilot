from datetime import datetime

from backend.db.database import SessionLocal
from backend.db.models import Incident


def create_incident(
    dataset: str,
    file_name: str,
    incident_type: str,
    severity: str,
    description: str
) -> None:

    db = SessionLocal()

    try:
        incident = Incident(
            dataset=dataset,
            file_name=file_name,
            incident_type=incident_type,
            severity=severity,
            description=description,
            status="OPEN",
            detected_at=datetime.now()
        )

        db.add(incident)
        db.commit()

        print(
            f"Incident created: "
            f"{incident.incident_id}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()