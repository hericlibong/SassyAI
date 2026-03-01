from fastapi.testclient import TestClient

from backend.src.api.app import app


client = TestClient(app)


def test_chat_flow_preserves_session_across_turns() -> None:
    first_response = client.post(
        "/api/chat",
        json={
            "message": "Hello there",
            "sarcasm_level": "medium",
        },
    )

    assert first_response.status_code == 200
    first_payload = first_response.json()
    assert {
        "session_id",
        "reply",
        "classification",
        "sarcasm_level",
        "message_count",
    }.issubset(first_payload)

    second_response = client.post(
        "/api/chat",
        json={
            "session_id": first_payload["session_id"],
            "message": "Follow up question",
            "sarcasm_level": "medium",
        },
    )

    assert second_response.status_code == 200
    second_payload = second_response.json()
    assert second_payload["session_id"] == first_payload["session_id"]
    assert second_payload["message_count"] > first_payload["message_count"]
