import io

import boto3
import pandas as pd

from backend.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_silver_suppliers(file_name: str) -> pd.DataFrame:
    s3_key = f"silver/suppliers/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def load_all_silver_suppliers() -> pd.DataFrame:
    all_suppliers = []

    for day in pd.date_range(
        start="2026-01-01",
        end="2026-03-31"
    ):

        run_date = day.strftime("%Y-%m-%d")

        file_name = f"suppliers_{run_date}.csv"

        print(f"Reading Silver: {file_name}")

        df = read_silver_suppliers(file_name)

        all_suppliers.append(df)

    return pd.concat(
        all_suppliers,
        ignore_index=True
    )


def create_supplier_performance(
    supplier_df: pd.DataFrame
) -> pd.DataFrame:

    supplier_df["delivery_date"] = pd.to_datetime(
        supplier_df["delivery_date"]
    )

    gold_df = (
        supplier_df
        .groupby(
            [
                "delivery_date",
                "supplier_id",
                "supplier_name"
            ],
            as_index=False
        )
        .agg(
            total_products_delivered=(
                "product_id",
                "nunique"
            ),
            total_quantity_delivered=(
                "quantity_delivered",
                "sum"
            )
        )
    )

    gold_df["delivery_date"] = (
        gold_df["delivery_date"]
        .dt.strftime("%Y-%m-%d")
    )

    return gold_df


def write_gold_supplier_performance(
    df: pd.DataFrame
) -> None:

    s3_key = (
        "gold/"
        "supplier_performance/"
        "supplier_performance.csv"
    )

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
        f"Gold file created: {s3_key}"
    )


def generate_supplier_performance() -> None:

    print("Loading Silver Supplier data...")

    supplier_df = load_all_silver_suppliers()

    print(
        f"Total Silver Supplier rows: "
        f"{len(supplier_df)}"
    )

    print(
        "Creating Gold Supplier Performance..."
    )

    gold_df = create_supplier_performance(
        supplier_df
    )

    print(
        f"Gold rows: {len(gold_df)}"
    )

    write_gold_supplier_performance(
        gold_df
    )

    print(
        "Silver → Gold Supplier Performance "
        "completed."
    )


if __name__ == "__main__":
    generate_supplier_performance()