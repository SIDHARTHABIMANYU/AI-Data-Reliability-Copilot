from backend.services.silver_pipeline import process_all_silver_data
from backend.services.gold_revenue_service import generate_daily_revenue
from backend.services.gold_inventory_service import generate_stock_availability
from backend.services.gold_supplier_service import generate_supplier_performance


def run_retail_pipeline() -> None:

    print("\n" + "=" * 70)
    print("RETAIL DATA RELIABILITY PIPELINE")
    print("=" * 70)

    # Bronze → Silver
    print("\n[1/4] Processing Bronze → Silver...")
    process_all_silver_data()

    # Silver → Gold: Revenue
    print("\n[2/4] Creating Gold Daily Revenue...")
    generate_daily_revenue()

    # Silver → Gold: Inventory
    print("\n[3/4] Creating Gold Stock Availability...")
    generate_stock_availability()

    # Silver → Gold: Suppliers
    print("\n[4/4] Creating Gold Supplier Performance...")
    generate_supplier_performance()

    print("\n" + "=" * 70)
    print("RETAIL DATA PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_retail_pipeline()