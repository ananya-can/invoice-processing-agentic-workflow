from core.parser import parse_invoice
from agents.extraction_agent import extract_invoice_data
from core.validator import validate_invoice
from agents.approval_agent import decide_approval, critique_decision
from core.payment import process_payment
from core.logger import log_result


def run_pipeline(invoice_path):
    print("\n--- STARTING PIPELINE ---\n")

    # 1. Parse
    parsed = parse_invoice(invoice_path)

    # 2. Extract
    extracted = extract_invoice_data(parsed["raw_text"])

    # 3. Validate
    validation = validate_invoice(extracted)

    # 4. Approval
    approval = decide_approval(extracted, validation)

    # 5. Critique
    critique = critique_decision(extracted, validation, approval)

    # 6. Retry approval once if critique says the decision is not sound
    if critique.get("is_sound") is False:
        print("\n🔁 Critique flagged the decision as unsound. Retrying approval once...\n")
        approval = decide_approval(
            extracted,
            validation,
            hint=critique.get("critique")
        )
        critique = critique_decision(extracted, validation, approval)

    # 7. Execute
    if approval.get("decision") == "approve":
        payment = process_payment(extracted)
    else:
        payment = {
            "status": "not_paid",
            "message": "Invoice not approved"
        }

    # 8. Final result
    final_result = {
        "invoice": extracted,
        "validation": validation,
        "approval": approval,
        "critique": critique,
        "payment": payment
    }

    # 9. Log
    log_result(final_result)

    return final_result
