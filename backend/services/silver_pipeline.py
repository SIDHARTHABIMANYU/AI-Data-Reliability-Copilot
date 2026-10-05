from datetime import date, timedelta

from backend.services.silver_sales_service import process_sales_file
from backend.services.silver_inventory_service import process_inventory_file
from backend.services.silver_supplier_service import process_supplier_file


START_DATE = date(2026, 1, 1)
NUMBER_OF_DAYS = 90


def process_all_silver_data() -> None:

    for day_number in range(NUMBER_OF_DAYS):

        current_date = START_DATE + timedelta(days=day_number)
        run_date = current_date.isoformat()

        sales_file = f"sales_{run_date}.csv"
        inventory_file = f"inventory_{run_date}.csv"
        supplier_file = f"suppliers_{run_date}.csv"

        print("\n" + "=" * 60)
        print(f"Processing Silver data for: {run_date}")
        print("=" * 60)

        # Sales
        process_sales_file(sales_file)

        # Inventory
        process_inventory_file(inventory_file)

        # Suppliers
        process_supplier_file(supplier_file)

    print("\n" + "=" * 60)
    print("ALL SILVER PROCESSING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    process_all_silver_data()