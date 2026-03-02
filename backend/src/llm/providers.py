from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    system_prompt: str
    sarcasm_level: str
    few_shot_examples: str = ""
    conversation: tuple[ProviderMessage, ...] = ()
    latest_user_message: str = ""


class ProviderAdapter(Protocol):
    name: str

    def generate(self, request: ProviderRequest) -> str:
        ...


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderAdapter] = {}

    def register(self, provider: ProviderAdapter) -> None:
        self._providers[provider.name] = provider

    def get(self, provider_name: str) -> ProviderAdapter:
        try:
            return self._providers[provider_name]
        except KeyError as exc:
            raise KeyError(f"Unknown provider: {provider_name}") from exc

    def available(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))
