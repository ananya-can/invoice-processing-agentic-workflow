import sqlite3
from core.schema import find_missing_fields


def validate_invoice(invoice_data, db_path="inventory.db"):
    """
    Validates extracted invoice data against:
    - required fields
    - item quantity rules
    - inventory database
    """

    result = {
        "is_valid": True,
        "issues": [],
        "item_checks": []
    }

    # 1. Check missing required fields
    missing_fields = find_missing_fields(invoice_data)
    if missing_fields:
        result["is_valid"] = False
        result["issues"].append(f"Missing required fields: {', '.join(missing_fields)}")

    items = invoice_data.get("items", [])

    # If items is not a list, fail early
    if not isinstance(items, list):
        result["is_valid"] = False
        result["issues"].append("Items field must be a list.")
        return result

    # 2. Connect to inventory DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for entry in items:
        item_name = entry.get("item")
        quantity = entry.get("quantity")

        item_result = {
            "item": item_name,
            "requested": quantity,
            "available": None,
            "status": "unknown"
        }

        # Validate item presence
        if not item_name:
            result["is_valid"] = False
            result["issues"].append("Item name is missing.")
            item_result["status"] = "missing_item_name"
            result["item_checks"].append(item_result)
            continue

        # Validate quantity
        if quantity is None or not isinstance(quantity, int):
            result["is_valid"] = False
            result["issues"].append(f"Invalid quantity for item {item_name}.")
            item_result["status"] = "invalid_quantity"
            result["item_checks"].append(item_result)
            continue

        if quantity <= 0:
            result["is_valid"] = False
            result["issues"].append(f"Quantity must be positive for item {item_name}.")
            item_result["status"] = "non_positive_quantity"
            result["item_checks"].append(item_result)
            continue

        # Check inventory database
        cursor.execute("SELECT stock FROM inventory WHERE item = ?", (item_name,))
        row = cursor.fetchone()

        if row is None:
            result["is_valid"] = False
            result["issues"].append(f"Unknown item: {item_name}.")
            item_result["status"] = "unknown_item"
            result["item_checks"].append(item_result)
            continue

        available_stock = row[0]
        item_result["available"] = available_stock

        if quantity > available_stock:
            result["is_valid"] = False
            result["issues"].append(
                f"Requested quantity {quantity} exceeds available stock {available_stock} for item {item_name}."
            )
            item_result["status"] = "stock_mismatch"
        elif available_stock == 0:
            result["is_valid"] = False
            result["issues"].append(f"Item {item_name} is out of stock.")
            item_result["status"] = "out_of_stock"
        else:
            item_result["status"] = "ok"

        result["item_checks"].append(item_result)

    conn.close()
    return result
