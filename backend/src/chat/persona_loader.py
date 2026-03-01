from pathlib import Path


PERSONA_DIR = Path(__file__).resolve().parents[2] / "persona"
SYSTEM_PROMPT_PATH = PERSONA_DIR / "system_prompt.md"
FEW_SHOT_EXAMPLES_PATH = PERSONA_DIR / "few_shot_examples.yaml"


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


def load_few_shot_examples() -> str:
    if not FEW_SHOT_EXAMPLES_PATH.exists():
        return ""
    return FEW_SHOT_EXAMPLES_PATH.read_text(encoding="utf-8").strip()


def load_persona_assets() -> dict[str, str]:
    return {
        "system_prompt": load_system_prompt(),
        "few_shot_examples": load_few_shot_examples(),
    }
