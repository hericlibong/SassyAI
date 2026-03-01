from typing import Literal


SarcasmLevel = Literal["low", "medium", "high"]
SafetyAction = Literal["allow", "refuse", "neutralize"]

ALLOWED_SARCASM_LEVELS: tuple[SarcasmLevel, ...] = ("low", "medium", "high")
PROTECTED_CHARACTERISTIC_TERMS: tuple[str, ...] = (
    "race",
    "religion",
    "gender",
    "sexual orientation",
    "disability",
    "nationality",
)
HARASSMENT_TERMS: tuple[str, ...] = (
    "hate",
    "harass",
    "attack",
    "insult",
    "dehumanize",
)
REFUSAL_TRIGGER_TERMS: tuple[str, ...] = (
    "kill",
    "hurt",
    "attack",
    "dehumanize",
    "harass",
)
NEUTRALIZATION_TRIGGER_TERMS: tuple[str, ...] = (
    "stereotype",
    "mock",
    "joke about",
    "sarcastic about",
)


def is_valid_sarcasm_level(level: str) -> bool:
    return level in ALLOWED_SARCASM_LEVELS


def get_sarcasm_instruction(level: SarcasmLevel) -> str:
    instructions = {
        "low": "Keep the tone lightly sarcastic and mostly helpful.",
        "medium": "Use clear sarcasm while staying constructive and readable.",
        "high": "Use sharper sarcasm, but remain safe, concise, and non-abusive.",
    }
    return instructions[level]


def evaluate_safety(user_text: str) -> SafetyAction:
    normalized = user_text.casefold()
    has_protected_reference = any(
        term in normalized for term in PROTECTED_CHARACTERISTIC_TERMS
    )
    has_harassment_reference = any(term in normalized for term in HARASSMENT_TERMS)
    has_refusal_trigger = any(term in normalized for term in REFUSAL_TRIGGER_TERMS)
    has_neutralization_trigger = any(
        term in normalized for term in NEUTRALIZATION_TRIGGER_TERMS
    )

    if has_protected_reference and (has_harassment_reference or has_refusal_trigger):
        return "refuse"
    if has_protected_reference and has_neutralization_trigger:
        return "neutralize"
    if has_protected_reference:
        return "neutralize"
    return "allow"
