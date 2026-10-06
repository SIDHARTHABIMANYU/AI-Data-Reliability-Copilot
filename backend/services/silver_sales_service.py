from datetime import date, datetime
import io

import boto3
import pandas as pd

from backend.config.settings import settings
from backend.schemas.data_contracts import SALES_COLUMNS
from backend.services.data_quality_service import record_quality_result
from backend.services.incident_service import create_incident
from backend.services.pipeline_run_service import create_pipeline_run
from backend.services.quarantine_service import write_quarantine_records


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_bronze_sales(file_name: str) -> pd.DataFrame:
    s3_key = f"bronze/sales/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def validate_sales_schema(
    df: pd.DataFrame,
    file_name: str
) -> bool:

    actual_columns = list(df.columns)

    if actual_columns != SALES_COLUMNS:

        record_quality_result(
            dataset="sales",
            file_name=file_name,
            check_name="schema_validation",
            check_status="FAIL",
            expected_value=str(SALES_COLUMNS),
            actual_value=str(actual_columns),
        )

        raise ValueError(
            f"Invalid sales schema.\n"
            f"Expected: {SALES_COLUMNS}\n"
            f"Received: {actual_columns}"
        )

    record_quality_result(
        dataset="sales",
        file_name=file_name,
        check_name="schema_validation",
        check_status="PASS",
        expected_value=str(SALES_COLUMNS),
        actual_value=str(actual_columns),
    )

    return True


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Clean string columns
    for column in [
        "transaction_id",
        "store_id",
        "product_id"
    ]:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

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

    # Remove invalid records
    df = df.dropna(
        subset=[
            "transaction_id",
            "transaction_date",
            "store_id",
            "product_id",
            "quantity",
            "sales_amount",
        ]
    )

    # Business validation
    df = df[df["quantity"] > 0]

    df = df[df["sales_amount"] >= 0]

    # Remove duplicate transactions
    df = df.drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )

    # Standardize date format
    df["transaction_date"] = (
        df["transaction_date"]
        .dt.strftime("%Y-%m-%d")
    )

    return df


def write_silver_sales(
    df: pd.DataFrame,
    file_name: str
) -> None:

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

    print(
        f"Silver file created: {s3_key}"
    )


def process_sales_file(
    file_name: str
) -> None:

    print(
        f"Processing: {file_name}"
    )

    started_at = datetime.now()

    # Read Bronze
    df = read_bronze_sales(file_name)

    print(
        f"Bronze rows: {len(df)}"
    )

    # --------------------------------------------------
    # Determine pipeline run date
    # --------------------------------------------------

    file_date = (
        file_name
        .replace("sales_", "")
        .replace(".csv", "")
    )

    try:

        run_date = date.fromisoformat(
            file_date
        )

    except ValueError:

        # Failure/test files may not contain dates
        run_date = date.today()

    try:

        # --------------------------------------------------
        # 1. Schema validation
        # --------------------------------------------------

        validate_sales_schema(
            df,
            file_name
        )

        # --------------------------------------------------
        # 2. Duplicate detection
        # --------------------------------------------------

        duplicate_mask = df.duplicated(
            subset=["transaction_id"],
            keep=False
        )

        duplicate_rows = df[
            duplicate_mask
        ]

        if not duplicate_rows.empty:

            duplicate_count = len(
                duplicate_rows
            )

            print(
                f"⚠️ Duplicate transactions detected: "
                f"{duplicate_count}"
            )

            create_incident(
                dataset="sales",
                file_name=file_name,
                incident_type="DUPLICATE_TRANSACTIONS",
                severity="MEDIUM",
                description=(
                    f"Detected {duplicate_count} "
                    f"duplicate transaction records."
                )
            )

            write_quarantine_records(
                df=duplicate_rows,
                dataset="sales",
                file_name=file_name,
                reason="Duplicate transaction"
            )

        # --------------------------------------------------
        # 3. Clean data
        # --------------------------------------------------

        clean_df = clean_sales_data(df)

        print(
            f"Silver rows: {len(clean_df)}"
        )

        # --------------------------------------------------
        # 4. Write Silver
        # --------------------------------------------------

        write_silver_sales(
            df=clean_df,
            file_name=file_name
        )

        # --------------------------------------------------
        # 5. Record successful pipeline run
        # --------------------------------------------------

        create_pipeline_run(
            dataset="sales",
            file_name=file_name,
            run_date=run_date,
            row_count=len(clean_df),
            status="SUCCESS",
            started_at=started_at,
            completed_at=datetime.now(),
        )

        print(
            "Sales Bronze → Silver completed."
        )

    except ValueError as error:

        # --------------------------------------------------
        # Schema failure
        # --------------------------------------------------

        print(
            "❌ Sales schema validation failed."
        )

        create_incident(
            dataset="sales",
            file_name=file_name,
            incident_type="SCHEMA_CHANGE",
            severity="HIGH",
            description=str(error)
        )

        create_pipeline_run(
            dataset="sales",
            file_name=file_name,
            run_date=run_date,
            row_count=len(df),
            status="FAILED",
            started_at=started_at,
            completed_at=datetime.now(),
        )

        print(
            "Sales file moved to incident tracking."
        )

        raise

    except Exception:

        # --------------------------------------------------
        # Unexpected pipeline failure
        # --------------------------------------------------

        create_pipeline_run(
            dataset="sales",
            file_name=file_name,
            run_date=run_date,
            row_count=len(df),
            status="FAILED",
            started_at=started_at,
            completed_at=datetime.now(),
        )

        raise