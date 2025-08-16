def test_run_test_endpoint(client):
    response = client.post("/run-test", json={"target": "example.com"})
    assert response.status_code == 200
    assert "status" in response.json()
