import io

import boto3
import pandas as pd

from backend.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def read_silver_sales(file_name: str) -> pd.DataFrame:
    s3_key = f"silver/sales/{file_name}"

    response = s3.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key
    )

    return pd.read_csv(response["Body"])


def load_all_silver_sales() -> pd.DataFrame:
    all_sales = []

    for day in pd.date_range(
        start="2026-01-01",
        end="2026-03-31"
    ):

        run_date = day.strftime("%Y-%m-%d")

        file_name = f"sales_{run_date}.csv"

        print(f"Reading Silver: {file_name}")

        df = read_silver_sales(file_name)

        all_sales.append(df)

    return pd.concat(
        all_sales,
        ignore_index=True
    )


def create_daily_revenue(
    sales_df: pd.DataFrame
) -> pd.DataFrame:

    sales_df["transaction_date"] = pd.to_datetime(
        sales_df["transaction_date"]
    )

    gold_df = (
        sales_df
        .groupby(
            [
                "transaction_date",
                "store_id"
            ],
            as_index=False
        )
        .agg(
            total_revenue=(
                "sales_amount",
                "sum"
            ),
            total_transactions=(
                "transaction_id",
                "count"
            ),
            total_quantity=(
                "quantity",
                "sum"
            )
        )
    )

    gold_df["transaction_date"] = (
        gold_df["transaction_date"]
        .dt.strftime("%Y-%m-%d")
    )

    return gold_df


def write_gold_revenue(
    df: pd.DataFrame
) -> None:

    s3_key = "gold/daily_revenue/daily_revenue.csv"

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


def generate_daily_revenue() -> None:

    print("Loading Silver Sales data...")

    sales_df = load_all_silver_sales()

    print(
        f"Total Silver Sales rows: {len(sales_df)}"
    )

    print("Creating Gold Daily Revenue...")

    gold_df = create_daily_revenue(
        sales_df
    )

    print(
        f"Gold rows: {len(gold_df)}"
    )

    write_gold_revenue(
        gold_df
    )

    print(
        "Silver → Gold Daily Revenue completed."
    )


if __name__ == "__main__":
    generate_daily_revenue()