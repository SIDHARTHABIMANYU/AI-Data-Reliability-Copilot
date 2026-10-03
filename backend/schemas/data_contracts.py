from typing import Final


SALES_COLUMNS: Final = [
    "transaction_id",
    "transaction_date",
    "store_id",
    "product_id",
    "quantity",
    "sales_amount",
]

INVENTORY_COLUMNS: Final = [
    "inventory_date",
    "store_id",
    "product_id",
    "stock_quantity",
]

SUPPLIER_COLUMNS: Final = [
    "supplier_id",
    "supplier_name",
    "product_id",
    "delivery_date",
    "quantity_delivered",
]