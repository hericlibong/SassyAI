import os
import sys
from pathlib import Path

import pytest


BACKEND_ROOT = Path(__file__).resolve().parents[1]

os.environ.setdefault("SASSYAI_OPENAI_API_KEY", "test-openai-key")

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


class _FakeOpenAIResponse:
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
                            "text": "Stubbed OpenAI response for tests.",
                        }
                    ],
                }
            ]
        }


class _FakeOpenAIClient:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def post(self, url: str, *, headers: dict, json: dict) -> _FakeOpenAIResponse:
        return _FakeOpenAIResponse()


@pytest.fixture(autouse=True)
def _stub_openai_http_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.llm.openai_provider.httpx.Client", _FakeOpenAIClient)
