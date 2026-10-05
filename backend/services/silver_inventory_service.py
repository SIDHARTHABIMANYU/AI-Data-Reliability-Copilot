import io

import boto3
import pandas as pd

from backend.config.settings import settings
from backend.schemas.data_contracts import INVENTORY_COLUMNS


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_bronze_inventory(file_name: str) -> pd.DataFrame:
    s3_key = f"bronze/inventory/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def validate_inventory_schema(df: pd.DataFrame) -> None:
    actual_columns = list(df.columns)

    if actual_columns != INVENTORY_COLUMNS:
        raise ValueError(
            f"Invalid inventory schema.\n"
            f"Expected: {INVENTORY_COLUMNS}\n"
            f"Received: {actual_columns}"
        )


def clean_inventory_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Clean string fields
    for column in ["store_id", "product_id"]:
        df[column] = df[column].astype(str).str.strip()

    # Convert data types
    df["inventory_date"] = pd.to_datetime(
        df["inventory_date"],
        errors="coerce"
    )

    df["stock_quantity"] = pd.to_numeric(
        df["stock_quantity"],
        errors="coerce"
    )

    # Remove records with missing required values
    df = df.dropna(
        subset=[
            "inventory_date",
            "store_id",
            "product_id",
            "stock_quantity"
        ]
    )

    # Business rule
    df = df[df["stock_quantity"] >= 0]

    # Remove duplicate inventory records
    df = df.drop_duplicates(
        subset=[
            "inventory_date",
            "store_id",
            "product_id"
        ],
        keep="first"
    )

    # Standardize date format
    df["inventory_date"] = (
        df["inventory_date"].dt.strftime("%Y-%m-%d")
    )

    return df


def write_silver_inventory(
    df: pd.DataFrame,
    file_name: str
) -> None:

    s3_key = f"silver/inventory/{file_name}"

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


def process_inventory_file(file_name: str) -> None:

    print(f"Processing: {file_name}")

    # 1. Read Bronze
    df = read_bronze_inventory(file_name)

    print(f"Bronze rows: {len(df)}")

    # 2. Validate schema
    validate_inventory_schema(df)

    # 3. Clean data
    clean_df = clean_inventory_data(df)

    print(f"Silver rows: {len(clean_df)}")

    # 4. Write Silver
    write_silver_inventory(
        df=clean_df,
        file_name=file_name
    )

    print("Inventory Bronze → Silver completed.")


if __name__ == "__main__":

    process_inventory_file(
        "inventory_2026-01-01.csv"
    )