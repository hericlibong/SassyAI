# responses.py

from engine import InsultEngine

engine = InsultEngine()

def get_sarcastic_reply(prompt: str) -> str:
    return engine.get_reply(prompt)


