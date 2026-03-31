REQUIRED_FIELDS = ["invoice_id", "vendor", "amount", "due_date", "items"]


def empty_invoice_schema():
    """
    Returns the default invoice structure expected from the extraction agent.
    """
    return {
        "invoice_id": None,
        "vendor": None,
        "amount": None,
        "due_date": None,
        "items": [],
        "missing_fields": [],
        "extraction_notes": ""
    }


def find_missing_fields(invoice_data):
    """
    Checks which required fields are missing or empty.
    """
    missing = []

    for field in REQUIRED_FIELDS:
        value = invoice_data.get(field)

        if value is None:
            missing.append(field)
        elif isinstance(value, str) and value.strip() == "":
            missing.append(field)
        elif field == "items" and (not isinstance(value, list) or len(value) == 0):
            missing.append(field)

    return missing
