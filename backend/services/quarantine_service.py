import io
from datetime import datetime

import boto3
import pandas as pd

from backend.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def write_quarantine_records(
    df: pd.DataFrame,
    dataset: str,
    file_name: str,
    reason: str
) -> None:

    if df.empty:
        print("No records to quarantine.")
        return

    df = df.copy()

    df["quarantine_reason"] = reason
    df["quarantined_at"] = datetime.now().isoformat()

    csv_buffer = io.StringIO()

    df.to_csv(
        csv_buffer,
        index=False
    )

    s3_key = (
        f"quarantine/"
        f"{dataset}/"
        f"{file_name}"
    )

    s3.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key,
        Body=csv_buffer.getvalue()
    )

    print(f"Quarantine file created: {s3_key}")
    print(f"Quarantined rows: {len(df)}")