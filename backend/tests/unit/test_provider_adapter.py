import httpx
import pytest

from src.llm.openai_provider import OpenAIProvider
from src.llm.providers import ProviderMessage, ProviderRegistry, ProviderRequest


class _RecordingResponse:
    status_code = 200

    def json(self) -> dict:
        return {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": "Parsed assistant reply.",
                        }
                    ],
                }
            ]
        }


class _RecordingClient:
    last_request: dict | None = None

    def __init__(self, *args, **kwargs) -> None:
        self.timeout = kwargs.get("timeout")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def post(self, url: str, *, headers: dict, json: dict) -> _RecordingResponse:
        _RecordingClient.last_request = {
            "url": url,
            "headers": headers,
            "json": json,
            "timeout": self.timeout,
        }
        return _RecordingResponse()


class _TimeoutClient:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def post(self, url: str, *, headers: dict, json: dict):
        raise httpx.ReadTimeout("timed out")


class _StatusErrorResponse:
    status_code = 503

    def json(self) -> dict:
        return {"error": "service unavailable"}


class _StatusErrorClient:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def post(self, url: str, *, headers: dict, json: dict) -> _StatusErrorResponse:
        return _StatusErrorResponse()


class _InvalidJsonResponse:
    status_code = 200

    def json(self) -> dict:
        raise ValueError("invalid json")


class _InvalidJsonClient:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def post(self, url: str, *, headers: dict, json: dict) -> _InvalidJsonResponse:
        return _InvalidJsonResponse()


class TimeoutProvider:
    name = "timeout-provider"

    def generate(self, request: ProviderRequest) -> str:
        raise TimeoutError("provider timed out")


class ErrorProvider:
    name = "error-provider"

    def generate(self, request: ProviderRequest) -> str:
        raise RuntimeError("provider failed")


def test_provider_adapter_timeout_path_raises_timeout_error() -> None:
    registry = ProviderRegistry()
    registry.register(TimeoutProvider())
    provider = registry.get("timeout-provider")

    with pytest.raises(TimeoutError):
        provider.generate(
            ProviderRequest(
                prompt="Hello",
                system_prompt="Be sarcastic",
                sarcasm_level="medium",
            )
        )


def test_provider_adapter_error_path_raises_runtime_error() -> None:
    registry = ProviderRegistry()
    registry.register(ErrorProvider())
    provider = registry.get("error-provider")

    with pytest.raises(RuntimeError):
        provider.generate(
            ProviderRequest(
                prompt="Hello",
                system_prompt="Be sarcastic",
                sarcasm_level="medium",
            )
        )


def test_openai_provider_builds_responses_api_payload_and_parses_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _RecordingClient.last_request = None
    monkeypatch.setattr("src.llm.openai_provider.httpx.Client", _RecordingClient)
    provider = OpenAIProvider(
        timeout_seconds=7.5,
        model_name="gpt-4o-mini",
        api_key="test-key",
    )

    reply = provider.generate(
        ProviderRequest(
            prompt="legacy prompt",
            system_prompt="Base persona instructions.",
            sarcasm_level="medium",
            few_shot_examples=(
                'version: 1\n'
                "examples:\n"
                '  - sarcasm_level: low\n'
                '    user: "Low question"\n'
                '    assistant: "Low answer"\n'
                '  - sarcasm_level: medium\n'
                '    user: "Medium question"\n'
                '    assistant: "Medium answer"\n'
            ),
            conversation=(
                ProviderMessage(role="user", content="Earlier question"),
                ProviderMessage(role="assistant", content="Earlier answer"),
            ),
            latest_user_message="Newest question",
        )
    )

    assert reply == "Parsed assistant reply."
    assert _RecordingClient.last_request is not None
    assert _RecordingClient.last_request["url"] == "https://api.openai.com/v1/responses"
    assert _RecordingClient.last_request["headers"]["Authorization"] == "Bearer test-key"
    assert _RecordingClient.last_request["json"]["model"] == "gpt-4o-mini"
    assert _RecordingClient.last_request["timeout"] == 7.5
    assert _RecordingClient.last_request["json"]["input"] == [
        {"role": "system", "content": "Base persona instructions."},
        {
            "role": "developer",
            "content": "Style: medium sarcasm. Be sharper, use two to four short jabs, stay constructive.",
        },
        {"role": "user", "content": "Medium question"},
        {"role": "assistant", "content": "Medium answer"},
        {"role": "user", "content": "Earlier question"},
        {"role": "assistant", "content": "Earlier answer"},
        {"role": "user", "content": "Newest question"},
    ]


def test_openai_provider_timeout_path_raises_timeout_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.llm.openai_provider.httpx.Client", _TimeoutClient)
    provider = OpenAIProvider(timeout_seconds=3.0, api_key="test-key")

    with pytest.raises(TimeoutError):
        provider.generate(
            ProviderRequest(
                prompt="Hello",
                system_prompt="Be sarcastic",
                sarcasm_level="medium",
                latest_user_message="Hello",
            )
        )


def test_openai_provider_non_200_response_raises_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.llm.openai_provider.httpx.Client", _StatusErrorClient)
    provider = OpenAIProvider(timeout_seconds=3.0, api_key="test-key")

    with pytest.raises(RuntimeError):
        provider.generate(
            ProviderRequest(
                prompt="Hello",
                system_prompt="Be sarcastic",
                sarcasm_level="medium",
                latest_user_message="Hello",
            )
        )


def test_openai_provider_invalid_json_raises_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.llm.openai_provider.httpx.Client", _InvalidJsonClient)
    provider = OpenAIProvider(timeout_seconds=3.0, api_key="test-key")

    with pytest.raises(RuntimeError):
        provider.generate(
            ProviderRequest(
                prompt="Hello",
                system_prompt="Be sarcastic",
                sarcasm_level="medium",
                latest_user_message="Hello",
            )
        )
