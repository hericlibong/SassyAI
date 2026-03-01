from fastapi.testclient import TestClient

from backend.src.api.app import app


client = TestClient(app)


def test_health_endpoint_returns_ok_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
