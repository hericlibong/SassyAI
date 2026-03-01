from dataclasses import dataclass

from .persona_loader import load_persona_assets
from .session_store import ChatSession, InMemorySessionStore
from ..llm.providers import ProviderRegistry, ProviderRequest
from ..safety.policy import get_sarcasm_instruction


@dataclass(frozen=True)
class ChatServiceResponse:
    session_id: str
    reply: str
    classification: str
    sarcasm_level: str
    message_count: int


class ChatService:
    def __init__(
        self,
        *,
        session_store: InMemorySessionStore,
        provider_registry: ProviderRegistry,
    ) -> None:
        self._session_store = session_store
        self._provider_registry = provider_registry

    def create_reply(
        self,
        *,
        provider_name: str,
        message: str,
        sarcasm_level: str,
        session_id: str | None = None,
    ) -> ChatServiceResponse:
        session = self._session_store.get_or_create(session_id, sarcasm_level)
        session.add_message(role="user", content=message)

        reply = self._generate_normal_reply(
            session=session,
            provider_name=provider_name,
            message=message,
            sarcasm_level=sarcasm_level,
        )
        session.add_message(role="assistant", content=reply, classification="normal")

        return ChatServiceResponse(
            session_id=session.session_id,
            reply=reply,
            classification="normal",
            sarcasm_level=session.sarcasm_level,
            message_count=len(session.messages),
        )

    def _generate_normal_reply(
        self,
        *,
        session: ChatSession,
        provider_name: str,
        message: str,
        sarcasm_level: str,
    ) -> str:
        provider = self._provider_registry.get(provider_name)
        persona_assets = load_persona_assets()
        prompt = self._build_prompt(session=session, message=message, sarcasm_level=sarcasm_level)
        request = ProviderRequest(
            prompt=prompt,
            system_prompt=persona_assets["system_prompt"],
            sarcasm_level=sarcasm_level,
        )
        return provider.generate(request)

    def _build_prompt(
        self,
        *,
        session: ChatSession,
        message: str,
        sarcasm_level: str,
    ) -> str:
        context_lines = [
            f"{item.role}: {item.content}"
            for item in session.messages[:-1]
        ]
        context = "\n".join(context_lines)
        instruction = get_sarcasm_instruction(sarcasm_level)
        if context:
            return f"{instruction}\nConversation so far:\n{context}\nLatest user message: {message}"
        return f"{instruction}\nLatest user message: {message}"
