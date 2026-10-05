import io

import boto3
import pandas as pd

from backend.config.settings import settings
from backend.schemas.data_contracts import SALES_COLUMNS
from backend.services.incident_service import create_incident

from backend.services.quarantine_service import (
    write_quarantine_records
)


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_bronze_sales(file_name: str) -> pd.DataFrame:
    """
    Read a sales CSV file from the Bronze S3 layer.
    """

    s3_key = f"bronze/sales/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def validate_sales_schema(df: pd.DataFrame) -> None:
    """
    Validate that the sales dataset contains the expected columns.
    """

    actual_columns = list(df.columns)

    if actual_columns != SALES_COLUMNS:
        raise ValueError(
            f"Invalid sales schema.\n"
            f"Expected: {SALES_COLUMNS}\n"
            f"Received: {actual_columns}"
        )


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate sales records.
    """

    df = df.copy()

    # Remove unnecessary whitespace from string columns
    string_columns = [
        "transaction_id",
        "store_id",
        "product_id"
    ]

    for column in string_columns:
        df[column] = df[column].astype(str).str.strip()

    # Convert data types
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["sales_amount"] = pd.to_numeric(
        df["sales_amount"],
        errors="coerce"
    )

    # Remove records with missing required values
    df = df.dropna(
        subset=[
            "transaction_id",
            "transaction_date",
            "store_id",
            "product_id",
            "quantity",
            "sales_amount"
        ]
    )

    # Business validation rules
    df = df[df["quantity"] > 0]
    df = df[df["sales_amount"] >= 0]

    # Remove duplicate transactions
    df = df.drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )

    # Convert date back to YYYY-MM-DD
    df["transaction_date"] = (
        df["transaction_date"].dt.strftime("%Y-%m-%d")
    )

    return df


def write_silver_sales(
    df: pd.DataFrame,
    file_name: str
) -> None:
    """
    Write cleaned sales data to the Silver S3 layer.
    """

    s3_key = f"silver/sales/{file_name}"

    csv_buffer = io.StringIO()

    df.to_csv(
        csv_buffer,
        index=False
    )

    s3.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key,
        Body=csv_buffer.getvalue()
    )

    print(f"Silver file created: {s3_key}")
def process_sales_file(file_name: str) -> None:

    print(f"Processing: {file_name}")

    df = read_bronze_sales(file_name)

    print(f"Bronze rows: {len(df)}")

    try:
        validate_sales_schema(df)

    except ValueError as error:

        print("❌ Sales schema validation failed.")

        create_incident(
            dataset="sales",
            file_name=file_name,
            incident_type="SCHEMA_CHANGE",
            severity="HIGH",
            description=str(error)
        )

        print("Sales file moved to incident tracking.")
        return

    # Detect duplicate transactions
    duplicate_mask = df.duplicated(
        subset=["transaction_id"],
        keep="first"
    )

    duplicate_rows = df[duplicate_mask].copy()

    if not duplicate_rows.empty:

        print(
            f"⚠️ Duplicate transactions detected: "
            f"{len(duplicate_rows)}"
        )

        create_incident(
            dataset="sales",
            file_name=file_name,
            incident_type="DUPLICATE_TRANSACTIONS",
            severity="MEDIUM",
            description=(
                f"Detected {len(duplicate_rows)} "
                f"duplicate transaction records."
            )
        )

        write_quarantine_records(
            df=duplicate_rows,
            dataset="sales",
            file_name=file_name,
            reason="Duplicate transaction"
        )

    # Remove duplicates from Silver
    clean_df = clean_sales_data(df)

    print(f"Silver rows: {len(clean_df)}")

    write_silver_sales(
        df=clean_df,
        file_name=file_name
    )

    print("Sales Bronze → Silver completed.")