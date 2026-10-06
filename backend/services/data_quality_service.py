from datetime import datetime

from backend.db.database import SessionLocal
from backend.db.models import DataQualityResult


def record_quality_result(
    dataset: str,
    file_name: str,
    check_name: str,
    check_status: str,
    expected_value: str | None = None,
    actual_value: str | None = None,
) -> None:

    db = SessionLocal()

    try:
        result = DataQualityResult(
            dataset=dataset,
            file_name=file_name,
            check_name=check_name,
            check_status=check_status,
            expected_value=expected_value,
            actual_value=actual_value,
            checked_at=datetime.now(),
        )

        db.add(result)
        db.commit()

        print(
            f"Quality result recorded: "
            f"{check_name} -> {check_status}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()