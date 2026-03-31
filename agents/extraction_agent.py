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
            {"role": "system", "content": "You extract structured data from invoices."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Grok API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]


def extract_invoice_data(raw_text):
    prompt = f"""
    Extract the following fields from this invoice text and return STRICT JSON only.

    Required fields:
    - invoice_id (preserve the original invoice number exactly as written, including prefixes like INV-)
    - vendor
    - amount (as a number, remove currency symbols and commas, return as float like 5000.0)
    - due_date
    - items (list of objects with 'item' and 'quantity')

    If something is missing, set it to null.
    Preserve invoice_id exactly as written in the source text. Do not remove prefixes, letters, or hyphens.
    Do NOT add extra text. Only return JSON.

    Invoice:
    {raw_text}
    """

    response_text = call_grok(prompt)

    try:
        data = json.loads(response_text)
    except:
        print("Initial JSON parsing failed. Retrying with correction prompt...")

        retry_prompt = f"""
    Your previous output was not valid JSON.

    Fix it and return ONLY valid JSON.
    Do not add any explanation or extra text.

    Original output:
    {response_text}
    """

        retry_response = call_grok(retry_prompt)

        try:
            data = json.loads(retry_response)
        except:
            print("Retry also failed. Returning empty structured object.")
            data = {
                "invoice_id": None,
                "vendor": None,
                "amount": None,
                "due_date": None,
                "items": [],
                "missing_fields": ["parsing_error"],
                "extraction_notes": retry_response
            }

    return data