import pytest

from backend.src.llm.providers import ProviderRegistry, ProviderRequest


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
