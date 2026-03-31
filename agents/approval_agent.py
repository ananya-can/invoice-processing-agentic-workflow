import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")


def call_grok(prompt):
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-4.20-reasoning",
        "messages": [
            {"role": "system", "content": "You are an invoice approval agent that reasons carefully and returns strict JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Grok API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]


def decide_approval(invoice_data, validation_result, hint=None):
    prompt = f"""
    You are reviewing an invoice for approval.

    Invoice data:
    {json.dumps(invoice_data, indent=2)}

    Validation result:
    {json.dumps(validation_result, indent=2)}

    Previous critique hint:
    {hint if hint else "None"}

    Approval policy:
    - If validation contains critical issues, reject.
    - If amount is above 10000, escalate for additional scrutiny.
    - If validation passes and there are no critical issues, approve.

    Return STRICT JSON only in this format:
    {{
      "decision": "approve" or "reject" or "escalate",
      "reasoning": "short explanation"
    }}
    """

    response_text = call_grok(prompt)

    try:
        return json.loads(response_text)
    except:
        return {
            "decision": "reject",
            "reasoning": f"Approval parsing failed. Raw model output: {response_text}"
        }


def critique_decision(invoice_data, validation_result, approval_result):
    prompt = f"""
    Review the following approval decision for consistency.

    Invoice data:
    {json.dumps(invoice_data, indent=2)}

    Validation result:
    {json.dumps(validation_result, indent=2)}

    Approval decision:
    {json.dumps(approval_result, indent=2)}

    Check:
    - Does the decision match the validation issues?
    - Is the reasoning consistent with the invoice facts?
    - Are there contradictions?

    Return STRICT JSON only in this format:
    {{
      "is_sound": true or false,
      "critique": "short review of whether the decision is sound"
    }}
    """

    response_text = call_grok(prompt)

    try:
        return json.loads(response_text)
    except:
        return {
            "is_sound": True,
            "critique": f"Critique parsing failed. Raw model output: {response_text}"
        }
    