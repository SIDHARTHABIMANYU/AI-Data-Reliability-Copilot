from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import PipelineRun


BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def ingest_retail_file(dataset: str, file_name: str) -> None:
    file_path = RAW_DIR / dataset / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    started_at = datetime.now()

    db = SessionLocal()

    existing_run = (
        db.query(PipelineRun)
        .filter(
            PipelineRun.dataset == dataset,
            PipelineRun.file_name == file_name,
            PipelineRun.status == "SUCCESS"
        )
        .first()
    )

    if existing_run:
        print(
            f"Already ingested: {dataset} | {file_name}"
        )
        db.close()
        return

    try:
        df = pd.read_csv(file_path)

        run_date = date.fromisoformat(
            file_path.stem.split("_")[-1]
        )

        pipeline_run = PipelineRun(
            dataset=dataset,
            file_name=file_name,
            run_date=run_date,
            row_count=len(df),
            status="SUCCESS",
            started_at=started_at,
            completed_at=datetime.now()
        )

        db.add(pipeline_run)
        db.commit()
        db.refresh(pipeline_run)

        print(f"Dataset: {dataset}")
        print(f"File: {file_name}")
        print(f"Rows: {len(df)}")
        print(f"Status: {pipeline_run.status}")
        print(f"Run ID: {pipeline_run.run_id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def ingest_daily_data(run_date: str) -> None:
    datasets = {
        "sales": f"sales_{run_date}.csv",
        "inventory": f"inventory_{run_date}.csv",
        "suppliers": f"suppliers_{run_date}.csv",
    }

    for dataset, file_name in datasets.items():
        ingest_retail_file(
            dataset=dataset,
            file_name=file_name
        )

def ingest_all_days(start_date: str, number_of_days: int) -> None:
    start = date.fromisoformat(start_date)

    for day_number in range(number_of_days):
        current_date = start + timedelta(days=day_number)
        run_date = current_date.isoformat()

        print(f"\nProcessing date: {run_date}")

        ingest_daily_data(run_date)

if __name__ == "__main__":
    ingest_all_days(
        start_date="2026-01-01",
        number_of_days=90
    )