import argparse
from core.orchestrator import run_pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoice Processing Pipeline")
    parser.add_argument(
        "--invoice",
        type=str,
        required=True,
        help="Path to invoice file"
    )

    args = parser.parse_args()

    result = run_pipeline(args.invoice)

    print("\n==============================")
    print("INVOICE PROCESSING RESULT")
    print("==============================\n")

    invoice = result["invoice"]
    validation = result["validation"]
    approval = result["approval"]
    payment = result["payment"]

    print(f"Invoice ID   : {invoice['invoice_id']}")
    print(f"Vendor       : {invoice['vendor']}")
    print(f"Amount       : {invoice['amount']}")

    # Validation
    status = "PASS" if validation["is_valid"] else "FAIL"

    print("\nVALIDATION")
    print("------------------------------")
    print(f"Status       : {status}")

    if validation["issues"]:
        print("Issues:")
        for issue in validation["issues"]:
            print(f"  - {issue}")
    else:
        print("  No issues found")

    # Decision
    print("\nDECISION")
    print("------------------------------")
    print(f"Decision     : {approval['decision'].upper()}")
    print(f"Reason       : {approval['reasoning']}")

    # Payment
    status = "PAID" if payment["status"] == "paid" else "NOT PAID"

    print("\nPAYMENT")
    print("------------------------------")
    print(f"Status       : {status}")

    print("\n==============================")

    print("\n--- FULL DEBUG OUTPUT ---\n")
    print(result)