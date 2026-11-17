from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_demo_sos_never_claims_real_dispatch():
    response = client.post("/demo/sos")
    assert response.status_code == 200
    assert response.json()["mode"] == "demo"
    assert "No contacts" in response.json()["message"]

def test_notification_outcome_validation():
    assert client.post("/demo/notification", json={"outcome": "failed"}).status_code == 200
    assert client.post("/demo/notification", json={"outcome": "delivered"}).status_code == 422
