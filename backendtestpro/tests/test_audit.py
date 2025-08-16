import os
import json
from backend.services.audit import log_event

def test_log_event_creates_entry(tmp_path):
    log_file = tmp_path / "audit.log"
    log_event("test_event", {"key": "value"}, str(log_file))

    content = log_file.read_text().strip()
    log_data = json.loads(content)
    assert log_data["event_type"] == "test_event"
    assert log_data["details"]["key"] == "value"
