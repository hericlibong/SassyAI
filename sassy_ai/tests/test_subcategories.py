# # sassy_ai/tests/test_subcategories.py
# import pytest

# from sassy_ai.sassy_core.subcategories import select_subcategory

# SPORTS_POOL = {
#     "general": ["G"],
#     "football": ["F"],
#     "basketball": ["B"],
#     "baseball": ["BA"],
# }
# NERD_POOL = {
#     "general": ["G"],
#     "sci-fi": ["SF"],
#     "comics": ["C"],
#     "gaming": ["GM"],
#     "anime": ["A"],
# }
# TV_POOL = {
#     "general": ["G"],
#     "preferences": ["P"],
#     "characters": ["CH"],
#     "finales": ["F"],
#     "spoilers": ["S"],
# }

# @pytest.mark.parametrize("prompt,expected", [
#     ("I love football highlights", ["F"]),
#     ("Tell me about NBA",          ["B"]),
#     ("Baseball stats please",      ["BA"]),
#     ("Random sport chat",          ["G"]),
# ])
# def test_select_sport(prompt, expected):
#     assert select_subcategory(prompt, SPORTS_POOL) == expected

# @pytest.mark.parametrize("prompt,expected", [
#     ("next Star Wars movie?",           ["SF"]),
#     ("Batman vs Superman",              ["C"]),
#     ("my Xbox broke",                   ["GM"]),
#     ("anime cosplay tips",              ["A"]),
#     ("just some nerd chatter",          ["G"]),
# ])
# def test_select_nerd(prompt, expected):
#     assert select_subcategory(prompt, NERD_POOL) == expected

# @pytest.mark.parametrize("prompt,expected", [
#     ("What’s your favorite show?",    ["P"]),
#     ("Which character died last week?",["CH"]),
#     ("I hate bad finales",            ["F"]),
#     ("No spoilers please",            ["S"]),
#     ("TV in general",                 ["G"]),
# ])
# def test_select_tv(prompt, expected):
#     assert select_subcategory(prompt, TV_POOL) == expected
