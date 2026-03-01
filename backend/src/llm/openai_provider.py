from dataclasses import dataclass

from .providers import ProviderRequest


@dataclass(frozen=True)
class OpenAIProvider:
    timeout_seconds: float
    name: str = "openai"

    def generate(self, request: ProviderRequest) -> str:
        if self.timeout_seconds <= 0:
            raise TimeoutError("provider timed out")

        user_message = request.prompt.split("Latest user message:", maxsplit=1)[-1].strip()
        return (
            f"[{request.sarcasm_level}] Sure, because that apparently needed a model. "
            f"You said: {user_message}"
        )
