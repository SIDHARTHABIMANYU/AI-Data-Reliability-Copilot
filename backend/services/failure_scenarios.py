import io

import boto3
import pandas as pd

from backend.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def create_duplicate_failure() -> None:

    source_key = "bronze/sales/sales_2026-03-30.csv"

    target_key = "bronze/sales/failure_duplicates.csv"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=source_key
    )

    df = pd.read_csv(response["Body"])

    # Select a few existing transactions
    duplicate_rows = df.head(5).copy()

    # Add the same transactions again
    df_with_duplicates = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    csv_buffer = io.StringIO()

    df_with_duplicates.to_csv(
        csv_buffer,
        index=False
    )

    s3.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=target_key,
        Body=csv_buffer.getvalue()
    )

    print("Duplicate transaction failure created:")
    print(target_key)

    print(f"Original rows: {len(df)}")
    print(f"Rows after duplicates: {len(df_with_duplicates)}")
    print(f"Duplicate rows added: {len(duplicate_rows)}")


if __name__ == "__main__":
    create_duplicate_failure()