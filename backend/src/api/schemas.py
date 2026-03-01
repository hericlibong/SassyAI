from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


SarcasmLevel = Literal["low", "medium", "high"]
ResponseClassification = Literal["normal", "refused", "neutralized", "fallback"]
ErrorCode = Literal["invalid_request"]


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(min_length=1)
    sarcasm_level: SarcasmLevel

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("message must not be empty")
        return trimmed


class ChatResponse(BaseModel):
    session_id: str
    reply: str = Field(min_length=1)
    classification: ResponseClassification
    sarcasm_level: SarcasmLevel
    message_count: int = Field(ge=1)


class ErrorResponse(BaseModel):
    error: ErrorCode = "invalid_request"
    message: str = Field(min_length=1)
