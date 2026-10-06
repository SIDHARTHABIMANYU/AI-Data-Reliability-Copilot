from datetime import datetime, date

from backend.db.database import SessionLocal
from backend.db.models import PipelineRun


def create_pipeline_run(
    dataset: str,
    file_name: str,
    run_date: date,
    row_count: int | None,
    status: str,
    started_at: datetime,
    completed_at: datetime | None = None,
) -> None:

    db = SessionLocal()

    try:
        pipeline_run = PipelineRun(
            dataset=dataset,
            file_name=file_name,
            run_date=run_date,
            row_count=row_count,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
        )

        db.add(pipeline_run)
        db.commit()

        print(
            f"Pipeline run recorded: "
            f"{dataset} | {file_name} | {status}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()