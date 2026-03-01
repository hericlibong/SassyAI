from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SessionMessage:
    role: str
    content: str
    classification: str = "normal"
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class ChatSession:
    session_id: str
    sarcasm_level: str
    messages: list[SessionMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    status: str = "active"

    def add_message(
        self,
        *,
        role: str,
        content: str,
        classification: str = "normal",
    ) -> SessionMessage:
        message = SessionMessage(
            role=role,
            content=content,
            classification=classification,
        )
        self.messages.append(message)
        self.updated_at = utc_now()
        return message


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, ChatSession] = {}

    def create(self, sarcasm_level: str) -> ChatSession:
        session = ChatSession(
            session_id=str(uuid4()),
            sarcasm_level=sarcasm_level,
        )
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> ChatSession | None:
        return self._sessions.get(session_id)

    def get_or_create(self, session_id: str | None, sarcasm_level: str) -> ChatSession:
        if session_id:
            session = self.get(session_id)
            if session is not None:
                session.sarcasm_level = sarcasm_level
                session.updated_at = utc_now()
                return session
        return self.create(sarcasm_level)

    def clear(self, session_id: str) -> None:
        session = self._sessions.pop(session_id, None)
        if session is not None:
            session.status = "expired"
