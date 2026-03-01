from src.observability.logger import (
    build_latency_event,
    build_provider_error_event,
)


def test_latency_event_contains_only_redacted_operational_metadata() -> None:
    event = build_latency_event(
        path="/api/chat",
        duration_ms=123.456,
        provider="openai",
    )

    assert event.event_type == "latency"
    assert event.metadata == {
        "path": "/api/chat",
        "duration_ms": 123.46,
        "provider": "openai",
    }


def test_provider_error_event_excludes_prompt_or_secret_fields() -> None:
    event = build_provider_error_event(
        provider="openai",
        error_type="timeout",
        status="fallback",
    )

    assert event.event_type == "provider_error"
    assert event.metadata == {
        "provider": "openai",
        "error_type": "timeout",
        "status": "fallback",
    }
    assert "prompt" not in event.metadata
    assert "api_key" not in event.metadata
