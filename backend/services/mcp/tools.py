
from datetime import date, datetime
from typing import Any
from backend.db.database import SessionLocal
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from backend.db.models import (
    AnomalyResult,
    DataQualityResult,
    Incident,
    PipelineRun,
    RemediationAction,
)
from decimal import Decimal


def _serialize_datetime(value: datetime | date | None) -> str | None:
    """Convert date and datetime values to ISO-formatted strings."""
    if value is None:
        return None
    return value.isoformat()


def get_pipeline_runs(
    dataset: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Return recent pipeline runs, optionally filtered by dataset."""
    if not 1 <= limit <= 100:
        return {"error": "limit must be between 1 and 100"}

    db = SessionLocal()

    try:
        query = select(PipelineRun)

        if dataset:
            query = query.where(PipelineRun.dataset == dataset)

        query = query.order_by(
            PipelineRun.run_id.desc()
        ).limit(limit)

        runs = db.execute(query).scalars().all()

        return {
            "count": len(runs),
            "runs": [
                {
                    "run_id": run.run_id,
                    "dataset": run.dataset,
                    "file_name": run.file_name,
                    "run_date": _serialize_datetime(run.run_date),
                    "row_count": run.row_count,
                    "status": run.status,
                    "started_at": _serialize_datetime(run.started_at),
                    "completed_at": _serialize_datetime(run.completed_at),
                }
                for run in runs
            ],
        }

    except SQLAlchemyError:
        return {"error": "Database query failed"}

    finally:
        db.close()


def get_data_quality_results(
    dataset: str | None = None,
    check_status: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Return recent data-quality results with optional filters."""
    if not 1 <= limit <= 100:
        return {"error": "limit must be between 1 and 100"}

    db = SessionLocal()

    try:
        query = select(DataQualityResult)

        if dataset:
            query = query.where(
                DataQualityResult.dataset == dataset
            )

        if check_status:
            query = query.where(
                DataQualityResult.check_status == check_status
            )

        query = query.order_by(
            DataQualityResult.quality_id.desc()
        ).limit(limit)

        results = db.execute(query).scalars().all()

        return {
            "count": len(results),
            "results": [
                {
                    "quality_id": result.quality_id,
                    "dataset": result.dataset,
                    "file_name": result.file_name,
                    "check_name": result.check_name,
                    "check_status": result.check_status,
                    "expected_value": result.expected_value,
                    "actual_value": result.actual_value,
                    "checked_at": _serialize_datetime(
                        result.checked_at
                    ),
                }
                for result in results
            ],
        }

    except SQLAlchemyError:
        return {"error": "Database query failed"}

    finally:
        db.close()


def get_incidents(
    dataset: str | None = None,
    status: str | None = None,
    severity: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Retrieve recent incidents with optional filters."""
    if not 1 <= limit <= 100:
        return {"error": "limit must be between 1 and 100"}

    db = SessionLocal()
    try:
        query = select(Incident)

        if dataset:
            query = query.where(Incident.dataset == dataset)
        if status:
            query = query.where(Incident.status == status)
        if severity:
            query = query.where(Incident.severity == severity)

        query = query.order_by(Incident.incident_id.desc()).limit(limit)
        incidents = db.execute(query).scalars().all()

        return {
            "count": len(incidents),
            "incidents": [
                {
                    "incident_id": incident.incident_id,
                    "dataset": incident.dataset,
                    "file_name": incident.file_name,
                    "incident_type": incident.incident_type,
                    "severity": incident.severity,
                    "description": incident.description,
                    "status": incident.status,
                    "detected_at": _serialize_datetime(incident.detected_at),
                    "resolved_at": _serialize_datetime(incident.resolved_at),
                }
                for incident in incidents
            ],
        }
    except SQLAlchemyError:
        return {"error": "Database query failed"}
    finally:
        db.close()


def get_anomaly_results(
    store_id: str | None = None,
    anomaly_status: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Retrieve recent anomaly results with optional filters."""
    if not 1 <= limit <= 100:
        return {"error": "limit must be between 1 and 100"}

    db = SessionLocal()
    try:
        query = select(AnomalyResult)

        if store_id:
            query = query.where(AnomalyResult.store_id == store_id)
        if anomaly_status:
            query = query.where(
                AnomalyResult.anomaly_status == anomaly_status
            )

        query = query.order_by(
            AnomalyResult.anomaly_id.desc()
        ).limit(limit)

        rows = db.execute(query).scalars().all()

        def number(value):
            if value is None:
                return None
            return float(value) if isinstance(value, Decimal) else value

        return {
            "count": len(rows),
            "anomalies": [
                {
                    "anomaly_id": row.anomaly_id,
                    "transaction_date": _serialize_datetime(
                        row.transaction_date
                    ),
                    "store_id": row.store_id,
                    "total_revenue": number(row.total_revenue),
                    "total_transactions": row.total_transactions,
                    "total_quantity": row.total_quantity,
                    "anomaly_score": number(row.anomaly_score),
                    "anomaly_status": row.anomaly_status,
                    "detection_method": row.detection_method,
                    "detected_at": _serialize_datetime(row.detected_at),
                }
                for row in rows
            ],
        }
    except SQLAlchemyError:
        return {"error": "Database query failed"}
    finally:
        db.close()


def get_remediation_status(
    remediation_id: int,
) -> dict[str, Any]:
    """Retrieve a remediation record without changing its state."""
    if remediation_id < 1:
        return {
            "error": "remediation_id must be a positive integer"
        }

    db = SessionLocal()
    try:
        query = select(RemediationAction).where(
            RemediationAction.remediation_id == remediation_id
        )
        remediation = db.execute(query).scalar_one_or_none()

        if remediation is None:
            return {"error": "Remediation not found"}

        return {
            "remediation_id": remediation.remediation_id,
            "incident_id": remediation.incident_id,
            "proposed_change": remediation.proposed_change,
            "risk": remediation.risk,
            "status": remediation.status,
            "approved_by": remediation.approved_by,
            "approved_at": _serialize_datetime(remediation.approved_at),
            "rejected_by": remediation.rejected_by,
            "rejected_at": _serialize_datetime(remediation.rejected_at),
            "created_at": _serialize_datetime(remediation.created_at),
        }
    except SQLAlchemyError:
        return {"error": "Database query failed"}
    finally:
        db.close()
