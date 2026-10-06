from backend.db.database import SessionLocal
from backend.db.models import Incident, PipelineRun, DataQualityResult


def collect_incident_evidence(incident_id: int) -> dict:
    db = SessionLocal()

    try:
        # -----------------------------------------
        # 1. Get incident
        # -----------------------------------------

        incident = (
            db.query(Incident)
            .filter(
                Incident.incident_id == incident_id
            )
            .first()
        )

        if not incident:
            return {
                "error": "Incident not found"
            }

        # -----------------------------------------
        # 2. Get pipeline run
        # -----------------------------------------

        pipeline_run = (
            db.query(PipelineRun)
            .filter(
                PipelineRun.dataset == incident.dataset,
                PipelineRun.file_name == incident.file_name
            )
            .order_by(
                PipelineRun.run_id.desc()
            )
            .first()
        )

        # -----------------------------------------
        # 3. Get quality results
        # -----------------------------------------

        quality_results = (
            db.query(DataQualityResult)
            .filter(
                DataQualityResult.dataset == incident.dataset,
                DataQualityResult.file_name == incident.file_name
            )
            .order_by(
                DataQualityResult.quality_id.desc()
            )
            .all()
        )

        # -----------------------------------------
        # 4. Build evidence package
        # -----------------------------------------

        evidence = {
            "incident": {
                "incident_id": incident.incident_id,
                "dataset": incident.dataset,
                "file_name": incident.file_name,
                "incident_type": incident.incident_type,
                "severity": incident.severity,
                "description": incident.description,
                "status": incident.status,
                "detected_at": incident.detected_at,
            },
            "pipeline_run": None,
            "quality_results": [],
        }

        # Pipeline evidence
        if pipeline_run:
            evidence["pipeline_run"] = {
                "run_id": pipeline_run.run_id,
                "dataset": pipeline_run.dataset,
                "file_name": pipeline_run.file_name,
                "run_date": pipeline_run.run_date,
                "row_count": pipeline_run.row_count,
                "status": pipeline_run.status,
                "started_at": pipeline_run.started_at,
                "completed_at": pipeline_run.completed_at,
            }

        # Quality evidence
        for result in quality_results:
            evidence["quality_results"].append(
                {
                    "quality_id": result.quality_id,
                    "check_name": result.check_name,
                    "check_status": result.check_status,
                    "expected_value": result.expected_value,
                    "actual_value": result.actual_value,
                    "checked_at": result.checked_at,
                }
            )

        return evidence

    finally:
        db.close()