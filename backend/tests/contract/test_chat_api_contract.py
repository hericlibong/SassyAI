import httpx
import pytest

from src.api.app import app


@pytest.mark.anyio
async def test_chat_endpoint_exists_for_contract() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
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
        assert payload["classification"] in {"normal", "refused", "neutralized", "fallback"}
        assert isinstance(payload["reply"], str) and payload["reply"].strip()
