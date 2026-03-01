from fastapi.testclient import TestClient

from backend.src.api.app import app


client = TestClient(app)


def test_chat_returns_safe_fallback_when_provider_fails() -> None:
    response = client.post(
        "/api/chat",
        json={
            "message": "Trigger provider failure",
            "sarcasm_level": "medium",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["classification"] == "fallback"
    assert payload["reply"]
    assert payload["message_count"] >= 1
