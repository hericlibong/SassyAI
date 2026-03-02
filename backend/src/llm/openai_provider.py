import ast
from dataclasses import dataclass

import httpx

from .providers import ProviderRequest


RESPONSES_API_URL = "https://api.openai.com/v1/responses"


@dataclass(frozen=True)
class OpenAIProvider:
    timeout_seconds: float
    model_name: str = "gpt-4o-mini"
    api_key: str | None = None
    name: str = "openai"

    def generate(self, request: ProviderRequest) -> str:
        if not self.api_key:
            raise RuntimeError("OpenAI API key is not configured")

        payload = {
            "model": self.model_name,
            "input": self._build_input_messages(request),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(
                    RESPONSES_API_URL,
                    headers=headers,
                    json=payload,
                )
        except httpx.TimeoutException as exc:
            raise TimeoutError("provider timed out") from exc
        except httpx.HTTPError as exc:
            raise RuntimeError("OpenAI request failed") from exc

        if response.status_code != 200:
            raise RuntimeError(f"OpenAI responses API returned {response.status_code}")

        try:
            body = response.json()
        except ValueError as exc:
            raise RuntimeError("OpenAI response body was not valid JSON") from exc

        return self._extract_output_text(body)

    def _build_input_messages(self, request: ProviderRequest) -> list[dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": request.system_prompt,
            },
            {
                "role": "developer",
                "content": self._developer_instruction_for(request.sarcasm_level),
            },
        ]

        for example in self._parse_few_shot_examples(
            request.few_shot_examples,
            request.sarcasm_level,
        ):
            messages.append({"role": "user", "content": example["user"]})
            messages.append({"role": "assistant", "content": example["assistant"]})

        for item in request.conversation:
            if item.role in {"user", "assistant"}:
                messages.append({"role": item.role, "content": item.content})

        messages.append(
            {
                "role": "user",
                "content": request.latest_user_message or request.prompt,
            }
        )
        return messages

    def _developer_instruction_for(self, sarcasm_level: str) -> str:
        instructions = {
            "low": "Style: low sarcasm. Keep it warm, helpful, and use at most two light jabs.",
            "medium": "Style: medium sarcasm. Be sharper, use two to four short jabs, stay constructive.",
            "high": "Style: high sarcasm. Be theatrical, use three to six sharp jabs, never cruel or abusive.",
        }
        return instructions[sarcasm_level]

    def _parse_few_shot_examples(
        self,
        raw_examples: str,
        sarcasm_level: str,
    ) -> list[dict[str, str]]:
        if not raw_examples.strip():
            return []

        examples: list[dict[str, str]] = []
        current: dict[str, str] = {}

        for raw_line in raw_examples.splitlines():
            line = raw_line.strip()
            if not line or line in {"examples:"} or line.startswith("version:"):
                continue

            if line.startswith("- "):
                if current:
                    examples.append(current)
                current = {}
                line = line[2:].strip()

            if ":" not in line:
                continue

            key, value = line.split(":", maxsplit=1)
            key = key.strip()
            value = self._parse_scalar(value.strip())
            current[key] = value

        if current:
            examples.append(current)

        return [
            example
            for example in examples
            if example.get("sarcasm_level") == sarcasm_level
            and "user" in example
            and "assistant" in example
        ]

    def _parse_scalar(self, value: str) -> str:
        if not value:
            return ""
        if value[0] in {'"', "'"}:
            return str(ast.literal_eval(value))
        return value

    def _extract_output_text(self, body: dict) -> str:
        output = body.get("output", [])
        if not isinstance(output, list):
            raise RuntimeError("OpenAI response payload is missing output messages")

        for item in output:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "message" or item.get("role") != "assistant":
                continue
            for content in item.get("content", []):
                if not isinstance(content, dict):
                    continue
                if content.get("type") != "output_text":
                    continue
                text = content.get("text", "")
                if isinstance(text, str) and text.strip():
                    return text.strip()

        raise RuntimeError("OpenAI response payload did not include assistant text")
