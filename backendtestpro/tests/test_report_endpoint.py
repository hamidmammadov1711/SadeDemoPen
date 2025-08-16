from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_generate_report_endpoint():
    dummy = {
        "details": "22/tcp open ssh\n80/tcp open http\n443/tcp open https"
    }
    response = client.post("/generate-report", json=dummy)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] == 6
    assert data["category"] == "High Risk"
    assert "recommendation" in data
