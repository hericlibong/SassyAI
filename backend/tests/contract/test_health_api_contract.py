import httpx
import pytest

from src.api.app import app


@pytest.mark.anyio
async def test_health_endpoint_returns_ok_status() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
