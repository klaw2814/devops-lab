from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

def test_create_ticket():
    response = client.post(
        "/tickets",
        json={
            "title": "Network Outage",
            "priority": "critical",
            "description": "Entire office offline"
        }
    )

    assert response.status_code == 200
