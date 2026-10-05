import io

import boto3
import pandas as pd

from backend.config.settings import settings
from backend.schemas.data_contracts import SUPPLIER_COLUMNS


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_bronze_suppliers(file_name: str) -> pd.DataFrame:
    s3_key = f"bronze/suppliers/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def validate_supplier_schema(df: pd.DataFrame) -> None:
    actual_columns = list(df.columns)

    if actual_columns != SUPPLIER_COLUMNS:
        raise ValueError(
            f"Invalid supplier schema.\n"
            f"Expected: {SUPPLIER_COLUMNS}\n"
            f"Received: {actual_columns}"
        )


def clean_supplier_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Clean string fields
    for column in [
        "supplier_id",
        "supplier_name",
        "product_id"
    ]:
        df[column] = df[column].astype(str).str.strip()

    # Convert data types
    df["delivery_date"] = pd.to_datetime(
        df["delivery_date"],
        errors="coerce"
    )

    df["quantity_delivered"] = pd.to_numeric(
        df["quantity_delivered"],
        errors="coerce"
    )

    # Remove records with missing required values
    df = df.dropna(
        subset=[
            "supplier_id",
            "supplier_name",
            "product_id",
            "delivery_date",
            "quantity_delivered"
        ]
    )

    # Business rule
    df = df[df["quantity_delivered"] > 0]

    # Remove duplicate delivery records
    df = df.drop_duplicates(
        subset=[
            "supplier_id",
            "product_id",
            "delivery_date"
        ],
        keep="first"
    )

    # Standardize date
    df["delivery_date"] = (
        df["delivery_date"].dt.strftime("%Y-%m-%d")
    )

    return df


def write_silver_suppliers(
    df: pd.DataFrame,
    file_name: str
) -> None:

    s3_key = f"silver/suppliers/{file_name}"

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


def process_supplier_file(file_name: str) -> None:

    print(f"Processing: {file_name}")

    # 1. Read Bronze
    df = read_bronze_suppliers(file_name)

    print(f"Bronze rows: {len(df)}")

    # 2. Validate schema
    validate_supplier_schema(df)

    # 3. Clean data
    clean_df = clean_supplier_data(df)

    print(f"Silver rows: {len(clean_df)}")

    # 4. Write Silver
    write_silver_suppliers(
        df=clean_df,
        file_name=file_name
    )

    print("Supplier Bronze → Silver completed.")


if __name__ == "__main__":

    process_supplier_file(
        "suppliers_2026-01-01.csv"
    )