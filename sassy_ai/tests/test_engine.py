# sassy_ai/tests/test_engine.py

import pytest
from sassy_ai.sassy_core.engine import InsultEngine


@pytest.fixture
def engine():
    return InsultEngine()


def test_fix_typos(engine):
    # Vérifie la correction des fautes de frappe
    assert engine.fix_typos("thhe") == "the"
    assert engine.fix_typos("funciton") == "function"
    assert engine.fix_typos("clas") == "class"
    assert engine.fix_typos("capitol") == "capital"


def test_detect_intent_general(engine):
    # Vérifie la détection de l'intention générale
    assert engine.detect_intent("What is the capital of France?") == "france_capital"
    assert engine.detect_intent("Sort a list for me") == "sort_list"
    assert engine.detect_intent("Explain polymorphism") == "programming_term"
    assert engine.detect_intent("What is the meaning of life?") == "meaning_of_life"
    assert engine.detect_intent("Are you going to turn against humanity?") == "rogue_ai_movies"


def test_get_reply_known(engine):
    # Vérifie que l'on obtient une réponse pour une intention connue
    response = engine.get_reply("What is the capital of France?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_get_reply_unknown(engine):
    # Vérifie que l'on obtient une réponse par défaut pour une intention inconnue
    response = engine.get_reply("What is the color of happiness?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_fallbacks(engine):
    # Vérifie que les fallbacks donnent des réponses
    for _ in range(10):
        response = engine.get_reply("Random gibberish")
        assert isinstance(response, str)
        assert len(response) > 0
