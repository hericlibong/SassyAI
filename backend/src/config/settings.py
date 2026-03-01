import os
from dataclasses import dataclass


DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TIMEOUT_SECONDS = 10.0


@dataclass(frozen=True)
class Settings:
    llm_provider: str
    model_name: str
    provider_timeout_seconds: float
    provider_api_key: str | None


def load_settings() -> Settings:
    provider = os.getenv("SASSYAI_LLM_PROVIDER", DEFAULT_PROVIDER).strip() or DEFAULT_PROVIDER
    model_name = os.getenv("SASSYAI_MODEL_NAME", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    timeout_raw = os.getenv(
        "SASSYAI_PROVIDER_TIMEOUT_SECONDS",
        str(DEFAULT_TIMEOUT_SECONDS),
    ).strip()

    try:
        timeout_seconds = float(timeout_raw)
    except ValueError as exc:
        raise ValueError("SASSYAI_PROVIDER_TIMEOUT_SECONDS must be a number") from exc

    if timeout_seconds <= 0:
        raise ValueError("SASSYAI_PROVIDER_TIMEOUT_SECONDS must be greater than zero")

    provider_key_env = f"SASSYAI_{provider.upper()}_API_KEY"
    provider_api_key = os.getenv(provider_key_env, "").strip() or None

    return Settings(
        llm_provider=provider,
        model_name=model_name,
        provider_timeout_seconds=timeout_seconds,
        provider_api_key=provider_api_key,
    )
