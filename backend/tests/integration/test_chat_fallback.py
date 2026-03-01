import httpx
import pytest

from src.api.app import app


@pytest.mark.anyio
async def test_chat_returns_safe_fallback_when_provider_fails() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
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
