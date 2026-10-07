from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = BASE_DIR / "data" / "anomaly" / "features.csv"
OUTPUT_FILE = BASE_DIR / "data" / "anomaly" / "test_features.csv"


def create_test_data() -> None:

    df = pd.read_csv(INPUT_FILE)

    # Select a record that already has enough historical data.
    target_index = (
        df["revenue_7d_mean"]
        .notna()
        & df["revenue_7d_std"].notna()
    ).idxmax()

    original_revenue = df.loc[
        target_index,
        "total_revenue"
    ]

    # Inject an artificial business anomaly.
    df.loc[
        target_index,
        "total_revenue"
    ] = original_revenue * 3

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Controlled anomaly dataset created.")
    print(
        f"Store: {df.loc[target_index, 'store_id']}"
    )
    print(
        f"Date: {df.loc[target_index, 'transaction_date']}"
    )
    print(
        f"Original revenue: {original_revenue:.2f}"
    )
    print(
        f"Injected revenue: "
        f"{df.loc[target_index, 'total_revenue']:.2f}"
    )
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_test_data()