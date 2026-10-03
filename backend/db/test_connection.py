from datetime import date

from backend.db.database import SessionLocal
from backend.db.models import PipelineRun


db = SessionLocal()

try:
    test_run = PipelineRun(
        dataset="sales",
        file_name="sales_2026-01-01.csv",
        run_date=date(2026, 1, 1),
        row_count=100,
        status="SUCCESS"
    )

    db.add(test_run)
    db.commit()
    db.refresh(test_run)

    print("Pipeline run inserted successfully!")
    print("Run ID:", test_run.run_id)

finally:
    db.close()