import datetime
import json

def sanitize(details: dict) -> dict:
    # Şifrə, token, email kimi sahələri maskala
    masked = {}
    for key, value in details.items():
        if key.lower() in ["password", "token", "secret"]:
            masked[key] = "***"
        else:
            masked[key] = value
    return masked

def log_event(event_type: str, details: dict, filepath: str = "audit.log"):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": sanitize(details)
    }
    with open(filepath, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


