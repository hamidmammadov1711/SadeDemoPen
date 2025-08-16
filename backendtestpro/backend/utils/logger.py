# backend/utils/logger.py
import logging
import json
from datetime import datetime

logging.basicConfig(filename="audit.log", level=logging.INFO)

def sanitize(details: dict) -> dict:
    masked = {}
    for key, value in details.items():
        if key.lower() in ["password", "token", "secret"]:
            masked[key] = "***"
        else:
            masked[key] = value
    return masked

def log_scan(target: str, status: str, details: str):
    logging.info(f"{target} → {status}: {details}")

def log_event(event_type: str, details: dict, filepath: str = "audit.log"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": sanitize(details)
    }
    with open(filepath, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
