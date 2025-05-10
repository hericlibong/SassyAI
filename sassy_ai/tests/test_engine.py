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

# def test_theme_priority_over_intent(monkeypatch):
#     """
#     Même si le prompt matche un autre intent, on doit d'abord
#     piocher dans le thème actif.
#     """
#     engine = InsultEngine()
#     # On force la réponse du thème 'food'
#     engine.responses["custom_responses"]["pizza_toppings"] = ["🍕FOOD"]
#     # Prompt qui matche sort_list
#     reply = engine.get_reply("please sort this list", current_theme="food")
#     assert reply == "🍕FOOD"

# def test_get_reply_tv_subcategory(monkeypatch):
#     engine = InsultEngine()
#     # on fixe un pool simple
#     engine.responses["custom_responses"]["tv_series_responses"] = {
#         "general":     ["GEN"],
#         "preferences": ["PREF"],
#         "characters":  ["CHAR"],
#         "finales":     ["FIN"],
#         "spoilers":    ["SP"],
#     }
#     # Override patterns pour forcer le cas
#     engine.custom_patterns["tv_series_responses"] = r"tv|series"
#     # Prompt sur personnages
#     out = engine.get_reply("Tell me about the main character in that tv show", current_theme="tv_series")
#     assert out in ["CHAR"]

# def test_detect_standard_vs_fallback():
#     engine = InsultEngine()
#     # mot-clé 'capital' => standard_responses['general_knowledge']
#     r1 = engine.get_reply("What is the capital of France?", current_theme="general")
#     assert r1 in engine.responses["standard_responses"]["general_knowledge"]
#     # phrase sans aucun mot connu => fallback
#     r2 = engine.get_reply("qwertyuiop", current_theme="general")
#     assert r2 in engine.fallbacks
