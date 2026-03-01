from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class LogEvent:
    event_type: str
    message: str
    metadata: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)


def build_latency_event(*, path: str, duration_ms: float, provider: str) -> LogEvent:
    return LogEvent(
        event_type="latency",
        message="Chat request completed",
        metadata={
            "path": path,
            "duration_ms": round(duration_ms, 2),
            "provider": provider,
        },
    )


def build_provider_error_event(
    *,
    provider: str,
    error_type: str,
    status: str,
) -> LogEvent:
    return LogEvent(
        event_type="provider_error",
        message="Provider request failed",
        metadata={
            "provider": provider,
            "error_type": error_type,
            "status": status,
        },
    )
