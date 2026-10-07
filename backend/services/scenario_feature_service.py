from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "scenario_revenue.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "anomaly"
    / "scenario_features.csv"
)


def build_scenario_features() -> None:

    df = pd.read_csv(INPUT_FILE)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    df = df.sort_values(
        ["store_id", "transaction_date"]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # Day-over-day changes
    # ---------------------------------------------------------

    df["revenue_change_pct"] = (
        df.groupby("store_id")["total_revenue"]
        .pct_change()
        * 100
    )

    df["transaction_change_pct"] = (
        df.groupby("store_id")["total_transactions"]
        .pct_change()
        * 100
    )

    df["quantity_change_pct"] = (
        df.groupby("store_id")["total_quantity"]
        .pct_change()
        * 100
    )

    # ---------------------------------------------------------
    # Leakage-free 7-day baseline
    #
    # Today's value is excluded from the baseline.
    # ---------------------------------------------------------

    df["revenue_7d_mean"] = (
        df.groupby("store_id")["total_revenue"]
        .transform(
            lambda series: (
                series
                .shift(1)
                .rolling(
                    window=7,
                    min_periods=3
                )
                .mean()
            )
        )
    )

    df["revenue_7d_std"] = (
        df.groupby("store_id")["total_revenue"]
        .transform(
            lambda series: (
                series
                .shift(1)
                .rolling(
                    window=7,
                    min_periods=3
                )
                .std()
            )
        )
    )

    # ---------------------------------------------------------
    # Revenue deviation
    # ---------------------------------------------------------

    df["revenue_deviation_pct"] = (
        (
            df["total_revenue"]
            - df["revenue_7d_mean"]
        )
        / df["revenue_7d_mean"]
    ) * 100

    # ---------------------------------------------------------
    # Z-score
    # ---------------------------------------------------------

    df["revenue_z_score"] = (
        (
            df["total_revenue"]
            - df["revenue_7d_mean"]
        )
        / df["revenue_7d_std"]
    )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Scenario features created.")
    print(f"Rows: {len(df)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_scenario_features()