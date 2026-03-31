def process_payment(invoice_data):
    """
    Simulates payment processing.
    """

    print("\nProcessing Payment...")
    print(f"Invoice ID: {invoice_data.get('invoice_id')}")
    print(f"Vendor: {invoice_data.get('vendor')}")
    print(f"Amount: ${invoice_data.get('amount')}")

    return {
        "status": "paid",
        "message": "Payment processed successfully"
    }
