# test_api.py
# API testleri
# backend/tests/test_api.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_run_test(client, sample_target):
    response = client.post("/run-test", json=sample_target)
    assert response.status_code == 200
    assert "status" in response.json()
    assert "details" in response.json()

def test_get_report(client, sample_target):
    response = client.post("/report", json=sample_target)
    assert response.status_code == 200
    assert "score" in response.json()
    assert "recommendation" in response.json()
    assert response.json()["status"] in ["SAFE", "WARNING", "CRITICAL"]

