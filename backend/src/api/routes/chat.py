from fastapi import APIRouter

from ..schemas import ChatRequest, ChatResponse
from ...chat.service import ChatService
from ...chat.session_store import InMemorySessionStore
from ...config.settings import load_settings
from ...llm.openai_provider import OpenAIProvider
from ...llm.providers import ProviderRegistry


router = APIRouter()

_settings = load_settings()
_session_store = InMemorySessionStore()
_provider_registry = ProviderRegistry()
_provider_registry.register(
    OpenAIProvider(timeout_seconds=_settings.provider_timeout_seconds),
)
_chat_service = ChatService(
    session_store=_session_store,
    provider_registry=_provider_registry,
)


@router.post("/api/chat", response_model=ChatResponse)
async def create_chat_reply(payload: ChatRequest) -> ChatResponse:
    result = _chat_service.create_reply(
        provider_name=_settings.llm_provider,
        message=payload.message,
        sarcasm_level=payload.sarcasm_level,
        session_id=payload.session_id,
    )
    return ChatResponse(
        session_id=result.session_id,
        reply=result.reply,
        classification=result.classification,
        sarcasm_level=result.sarcasm_level,
        message_count=result.message_count,
    )
