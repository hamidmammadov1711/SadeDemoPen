from datetime import datetime

def log_request(request, action: str, details: dict):
    ip = request.client.host
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "ip": ip,
        "timestamp": timestamp,
        "action": action,
        "details": details
    }
    print(f"[AUDIT] {log_entry}")  # Sonra fayla yazmaq və ya DB-ə salmaq olar
