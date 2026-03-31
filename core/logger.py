import json
from datetime import datetime


def log_result(result_data, log_file="run_log.jsonl"):
    """
    Appends a structured result log to a local JSONL file.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "result": result_data
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\nResult logged to {log_file}")
