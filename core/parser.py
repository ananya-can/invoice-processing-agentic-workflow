import os
import json
import csv
import fitz  # PyMuPDF
import xml.etree.ElementTree as ET

def parse_invoice(file_path):
    """
    Reads an invoice file and returns raw text + metadata.
    Supports: txt, json, csv, pdf (basic placeholder for now)
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_type = file_path.split('.')[-1].lower()

    if file_type == "txt":
        with open(file_path, "r") as f:
            raw_text = f.read()

    elif file_type == "json":
        with open(file_path, "r") as f:
            data = json.load(f)
            raw_text = json.dumps(data, indent=2)

    elif file_type == "csv":
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            raw_text = "\n".join([",".join(row) for row in rows])

    elif file_type == "pdf":
        doc = fitz.open(file_path)
        raw_text = ""

        for page in doc:
            raw_text += page.get_text("text") + "\n"

        doc.close()

    elif file_type == "xml":
        tree = ET.parse(file_path)
        root = tree.getroot()
        raw_text = ET.tostring(root, encoding="unicode")

    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    return {
        "file_path": file_path,
        "file_type": file_type,
        "raw_text": raw_text
    }