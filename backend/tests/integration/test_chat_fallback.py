import httpx
import pytest

from src.api.app import app
from src.api.routes import chat as chat_route


class _FailingProvider:
    name = "openai"

    def generate(self, request) -> str:
        raise RuntimeError("simulated provider failure")


@pytest.mark.anyio
async def test_chat_returns_safe_fallback_when_provider_fails() -> None:
    original_provider = chat_route._provider_registry.get("openai")
    chat_route._provider_registry.register(_FailingProvider())

    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post(
                "/api/chat",
                json={
                    "message": "Trigger provider failure",
                    "sarcasm_level": "medium",
                },
            )
    finally:
        chat_route._provider_registry.register(original_provider)

    assert response.status_code == 200
    payload = response.json()
    assert payload["classification"] == "fallback"
    assert payload["reply"]
    assert payload["message_count"] >= 1
