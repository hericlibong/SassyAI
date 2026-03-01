from fastapi.testclient import TestClient

from backend.src.api.app import app


client = TestClient(app)


def test_chat_endpoint_exists_for_contract() -> None:
    response = client.post(
        "/api/chat",
        json={
            "message": "Hello there",
            "sarcasm_level": "medium",
        },
    )

    assert response.status_code != 404
    if response.status_code == 200:
        payload = response.json()
        assert {
            "session_id",
            "reply",
            "classification",
            "sarcasm_level",
            "message_count",
        }.issubset(payload)
