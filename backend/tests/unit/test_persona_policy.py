from backend.src.safety.policy import get_sarcasm_instruction, is_valid_sarcasm_level


def test_persona_policy_supports_all_required_sarcasm_levels() -> None:
    assert is_valid_sarcasm_level("low")
    assert is_valid_sarcasm_level("medium")
    assert is_valid_sarcasm_level("high")
    assert not is_valid_sarcasm_level("extreme")


def test_persona_policy_returns_distinct_instructions_per_level() -> None:
    low_instruction = get_sarcasm_instruction("low")
    medium_instruction = get_sarcasm_instruction("medium")
    high_instruction = get_sarcasm_instruction("high")

    assert low_instruction != medium_instruction
    assert medium_instruction != high_instruction
    assert low_instruction != high_instruction
