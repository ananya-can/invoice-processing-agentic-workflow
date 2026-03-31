from core.validator import validate_invoice

def test_valid_invoice_passes():
    invoice = {
        "invoice_id": "1001",
        "vendor": "Test Vendor",
        "amount": 500.0,
        "due_date": "2026-01-01",
        "items": [{"item": "WidgetA", "quantity": 2}]
    }

    result = validate_invoice(invoice)

    assert result["is_valid"] is True
    assert result["issues"] == []


def test_missing_fields_fails():
    invoice = {
        "invoice_id": "1002",
        "vendor": None,
        "amount": 500.0,
        "due_date": None,
        "items": [{"item": "WidgetA", "quantity": 2}]
    }

    result = validate_invoice(invoice)

    assert result["is_valid"] is False
    assert any("Missing required fields" in issue for issue in result["issues"])


def test_negative_quantity_fails():
    invoice = {
        "invoice_id": "1003",
        "vendor": "Test Vendor",
        "amount": 500.0,
        "due_date": "2026-01-01",
        "items": [{"item": "WidgetA", "quantity": -1}]
    }

    result = validate_invoice(invoice)

    assert result["is_valid"] is False
    assert any("Quantity must be positive" in issue for issue in result["issues"])


def test_stock_mismatch_fails():
    invoice = {
        "invoice_id": "1004",
        "vendor": "Test Vendor",
        "amount": 500.0,
        "due_date": "2026-01-01",
        "items": [{"item": "GadgetX", "quantity": 100}]  # exceeds stock (5)
    }

    result = validate_invoice(invoice)

    assert result["is_valid"] is False
    assert any("exceeds available stock" in issue for issue in result["issues"])


def test_unknown_item_fails():
    invoice = {
        "invoice_id": "1005",
        "vendor": "Test Vendor",
        "amount": 500.0,
        "due_date": "2026-01-01",
        "items": [{"item": "WidgetC", "quantity": 1}]  # not in DB
    }

    result = validate_invoice(invoice)

    assert result["is_valid"] is False
    assert any("not found in inventory" in issue.lower() for issue in result["issues"])
