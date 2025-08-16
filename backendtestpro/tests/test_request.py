from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_run_test():
    response = client.post("/run-test", json={"target": "example.com"})
    assert response.status_code == 200
    assert "status" in response.json()
    assert "details" in response.json()
