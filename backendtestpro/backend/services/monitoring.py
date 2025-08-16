from datetime import datetime
from random import randint

def get_server_status(server_id: int) -> dict:
    # Demo: random status
    return {
        "server_id": server_id,
        "cpu": randint(10, 90),
        "memory": randint(20, 95),
        "uptime": f"{randint(1, 365)} gün",
        "last_checked": datetime.now().isoformat(),
        "status": "OK" if randint(0, 1) else "WARNING"
    }

def get_web_status(site: str) -> dict:
    # Demo: random response time
    return {
        "site": site,
        "response_time_ms": randint(100, 2000),
        "status": "OK" if randint(0, 1) else "CRITICAL",
        "last_checked": datetime.now().isoformat()
    }
