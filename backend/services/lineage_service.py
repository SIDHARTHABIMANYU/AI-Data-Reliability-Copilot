DATASET_LINEAGE = {
    "sales": {
        "silver_output": "silver/sales/",
        "gold_outputs": [
            "gold/daily_revenue/"
        ],
        "business_metrics": [
            "Daily Revenue",
            "Transaction Count",
            "Sales Quantity"
        ]
    },

    "inventory": {
        "silver_output": "silver/inventory/",
        "gold_outputs": [
            "gold/stock_availability/"
        ],
        "business_metrics": [
            "Stock Availability",
            "Products In Stock",
            "Total Stock Quantity"
        ]
    },

    "suppliers": {
        "silver_output": "silver/suppliers/",
        "gold_outputs": [
            "gold/supplier_performance/"
        ],
        "business_metrics": [
            "Products Delivered",
            "Quantity Delivered",
            "Supplier Performance"
        ]
    }
}


def get_dataset_lineage(dataset: str) -> dict:

    lineage = DATASET_LINEAGE.get(dataset)

    if not lineage:
        return {
            "dataset": dataset,
            "found": False,
            "message": "No lineage definition found."
        }

    return {
        "dataset": dataset,
        "found": True,
        "silver_output": lineage["silver_output"],
        "gold_outputs": lineage["gold_outputs"],
        "business_metrics": lineage["business_metrics"]
    }