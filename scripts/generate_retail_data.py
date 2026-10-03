import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

SALES_DIR = RAW_DIR / "sales"
INVENTORY_DIR = RAW_DIR / "inventory"
SUPPLIERS_DIR = RAW_DIR / "suppliers"

NUM_STORES = 10
NUM_PRODUCTS = 50
NUM_SUPPLIERS = 10
NUM_DAYS = 90

START_DATE = date(2026, 1, 1)

random.seed(42)


# -----------------------------
# Create directories
# -----------------------------

SALES_DIR.mkdir(parents=True, exist_ok=True)
INVENTORY_DIR.mkdir(parents=True, exist_ok=True)
SUPPLIERS_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Master data
# -----------------------------

stores = [
    f"STORE{i:02d}"
    for i in range(1, NUM_STORES + 1)
]

products = [
    f"P{i:03d}"
    for i in range(1, NUM_PRODUCTS + 1)
]

suppliers = [
    {
        "supplier_id": f"SUP{i:03d}",
        "supplier_name": f"Supplier {i:02d}"
    }
    for i in range(1, NUM_SUPPLIERS + 1)
]


# Assign each product to a supplier
product_supplier = {
    product: random.choice(suppliers)
    for product in products
}


# Assign a base price to each product
product_price = {
    product: round(random.uniform(100, 5000), 2)
    for product in products
}


# -----------------------------
# Generate daily data
# -----------------------------

transaction_counter = 1

for day_number in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day_number)

    date_string = current_date.isoformat()

    sales_records = []
    inventory_records = []
    supplier_records = []


    # -------------------------
    # Sales
    # -------------------------

    for store in stores:

        number_of_transactions = random.randint(80, 150)

        for _ in range(number_of_transactions):

            product = random.choice(products)

            quantity = random.randint(1, 5)

            price = product_price[product]

            sales_amount = round(quantity * price, 2)

            sales_records.append(
                {
                    "transaction_id": f"TXN{transaction_counter:07d}",
                    "transaction_date": date_string,
                    "store_id": store,
                    "product_id": product,
                    "quantity": quantity,
                    "sales_amount": sales_amount,
                }
            )

            transaction_counter += 1


    # -------------------------
    # Inventory
    # -------------------------

    for store in stores:

        for product in products:

            stock_quantity = random.randint(0, 500)

            inventory_records.append(
                {
                    "inventory_date": date_string,
                    "store_id": store,
                    "product_id": product,
                    "stock_quantity": stock_quantity,
                }
            )


    # -------------------------
    # Supplier deliveries
    # -------------------------

    for supplier in suppliers:

        supplier_products = [
            product
            for product in products
            if product_supplier[product]["supplier_id"]
            == supplier["supplier_id"]
        ]

        for product in supplier_products:

            if random.random() < 0.35:

                quantity_delivered = random.randint(50, 500)

                supplier_records.append(
                    {
                        "supplier_id": supplier["supplier_id"],
                        "supplier_name": supplier["supplier_name"],
                        "product_id": product,
                        "delivery_date": date_string,
                        "quantity_delivered": quantity_delivered,
                    }
                )


    # -------------------------
    # Save daily files
    # -------------------------

    sales_df = pd.DataFrame(sales_records)

    inventory_df = pd.DataFrame(inventory_records)

    suppliers_df = pd.DataFrame(supplier_records)


    sales_df.to_csv(
        SALES_DIR / f"sales_{date_string}.csv",
        index=False
    )

    inventory_df.to_csv(
        INVENTORY_DIR / f"inventory_{date_string}.csv",
        index=False
    )

    suppliers_df.to_csv(
        SUPPLIERS_DIR / f"suppliers_{date_string}.csv",
        index=False
    )


print("Retail synthetic data generation completed.")

print(f"Sales files: {len(list(SALES_DIR.glob('*.csv')))}")
print(f"Inventory files: {len(list(INVENTORY_DIR.glob('*.csv')))}")
print(f"Supplier files: {len(list(SUPPLIERS_DIR.glob('*.csv')))}")