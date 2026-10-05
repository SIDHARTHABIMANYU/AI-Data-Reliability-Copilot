import io

import boto3
import pandas as pd

from backend.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_silver_inventory(file_name: str) -> pd.DataFrame:
    s3_key = f"silver/inventory/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def load_all_silver_inventory() -> pd.DataFrame:
    all_inventory = []

    for day in pd.date_range(
        start="2026-01-01",
        end="2026-03-31"
    ):

        run_date = day.strftime("%Y-%m-%d")

        file_name = f"inventory_{run_date}.csv"

        print(f"Reading Silver: {file_name}")

        df = read_silver_inventory(file_name)

        all_inventory.append(df)

    return pd.concat(
        all_inventory,
        ignore_index=True
    )


def create_stock_availability(
    inventory_df: pd.DataFrame
) -> pd.DataFrame:

    inventory_df["inventory_date"] = pd.to_datetime(
        inventory_df["inventory_date"]
    )

    # A product is considered available when stock > 0
    inventory_df["in_stock"] = (
        inventory_df["stock_quantity"] > 0
    )

    gold_df = (
        inventory_df
        .groupby(
            [
                "inventory_date",
                "store_id"
            ],
            as_index=False
        )
        .agg(
            total_products=(
                "product_id",
                "count"
            ),
            products_in_stock=(
                "in_stock",
                "sum"
            ),
            total_stock_quantity=(
                "stock_quantity",
                "sum"
            )
        )
    )

    gold_df["stock_availability_pct"] = (
        gold_df["products_in_stock"]
        / gold_df["total_products"]
        * 100
    )

    gold_df["stock_availability_pct"] = (
        gold_df["stock_availability_pct"]
        .round(2)
    )

    gold_df["inventory_date"] = (
        gold_df["inventory_date"]
        .dt.strftime("%Y-%m-%d")
    )

    return gold_df


def write_gold_inventory(
    df: pd.DataFrame
) -> None:

    s3_key = "gold/stock_availability/stock_availability.csv"

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


def generate_stock_availability() -> None:

    print("Loading Silver Inventory data...")

    inventory_df = load_all_silver_inventory()

    print(
        f"Total Silver Inventory rows: {len(inventory_df)}"
    )

    print(
        "Creating Gold Stock Availability..."
    )

    gold_df = create_stock_availability(
        inventory_df
    )

    print(
        f"Gold rows: {len(gold_df)}"
    )

    write_gold_inventory(
        gold_df
    )

    print(
        "Silver → Gold Stock Availability completed."
    )


if __name__ == "__main__":
    generate_stock_availability()