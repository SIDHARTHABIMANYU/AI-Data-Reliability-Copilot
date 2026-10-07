from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = BASE_DIR / "data" / "daily_revenue.csv"
OUTPUT_FILE = BASE_DIR / "data" / "anomaly" / "scenario_revenue.csv"


def create_revenue_drop_scenario() -> None:

    df = pd.read_csv(INPUT_FILE)

    target_date = "2026-02-15"
    target_store = "STORE05"

    mask = (
        (df["transaction_date"] == target_date)
        & (df["store_id"] == target_store)
    )

    if not mask.any():
        raise ValueError(
            "Target store/date combination not found."
        )

    original_revenue = df.loc[
        mask,
        "total_revenue"
    ].iloc[0]

    # Simulate a 70% revenue drop.
    df.loc[
        mask,
        "total_revenue"
    ] = original_revenue * 0.30

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    new_revenue = df.loc[
        mask,
        "total_revenue"
    ].iloc[0]

    print("Deliberate anomaly scenario created.")
    print(f"Store: {target_store}")
    print(f"Date: {target_date}")
    print(f"Original revenue: {original_revenue:.2f}")
    print(f"Scenario revenue: {new_revenue:.2f}")
    print("Simulated event: 70% revenue drop")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_revenue_drop_scenario()