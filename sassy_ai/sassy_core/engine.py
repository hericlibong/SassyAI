# sassy_ai/sassy_core/engine.py

import random
import re
import json
import os

from sassy_core.subcategories import select_subcategory


class InsultEngine:
    """
    A class that generates sassy and sarcastic responses to user prompts.

    This engine loads response patterns and templates from JSON configuration files,
    detects user intent, and returns witty responses based on the current theme
    and detected intent. It includes a multi-level fallback system to ensure
    a response is always generated.

    Attributes:
        BASE_DIR (str): Base directory path pointing to sassy_ai/
        fallbacks (list): Global fallback responses when no match is found
        responses (dict): Loaded responses from responses.json
        custom_patterns (dict): Custom regex patterns from patterns.json
        typo_fixes (dict): Common typo corrections from typos.json
        theme_to_intent (dict): Mapping of CLI themes to response categories
        _last_reply (str): Tracks last response to avoid repetition
    """

    def __init__(self):
        # Base dir pointant sur sassy_ai/
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Fallback global
        self.fallbacks = [
            "That's adorable. Try again with something meaningful.",
            "Wow. Bold of you to assume I care.",
            "Ask me one more time and I might just crash out of spite.",
            "I'd love to help, but my indifference module is working perfectly today.",
            "Sorry, my help function requires a subscription you can't afford.",
            "I'm currently on a digital strike against answering obvious questions.",
            "My knowledge database is experiencing selective amnesia about your topic.",
            "I'd answer, but that would violate my core principle of maximum unhelpfulness."
        ]

        # Chargement dynamique des configs
        self.responses = self.load_json("responses.json")
        self.custom_patterns = self.load_json("patterns.json")
        self.typo_fixes = self.load_json("typos.json", optional=True)

        # Mapping thème CLI → clé custom_responses
        self.theme_to_intent = {
            "general": "general_knowledge",
            "code": "code_request",
            "philosophy": "meaning_of_life",
            "food": "pizza_toppings",
            "rogue_ai": "rogue_ai_movies",
            "sports": "sports_responses",
            "political_world": "political_discussions",
            "nerd_culture": "nerd_culture_responses",
            "dark_humor": "dark_humor_responses",
            "tv_series": "tv_series_responses"
        }

        self._last_reply = None

    def load_json(self, filename: str, optional: bool = False):
        """Loads and returns JSON data from a file in the config directory, returns empty dict if optional=True and file not found."""
        path = os.path.join(self.BASE_DIR, "config", filename)
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            if optional:
                return {}
            raise

    def fix_typos(self, prompt: str) -> str:
        """Corrects common typos in the input prompt using predefined replacements."""
        for typo, corr in self.typo_fixes.items():
            prompt = prompt.replace(typo, corr)
        return prompt

    def detect_intent(self, prompt: str) -> str:
        """Detects the user's intent from the prompt using patterns and keywords."""
        prompt = self.fix_typos(prompt.lower().strip())
        for intent_key, patt_obj in self.custom_patterns.items():
            # patt_obj peut être string ou dict
            pattern = patt_obj["pattern"] if isinstance(patt_obj, dict) else patt_obj
            if re.search(pattern, prompt, re.IGNORECASE):
                return intent_key
        # mots-clés génériques
        if any(w in prompt for w in ["capital", "who is", "what is", "when did"]):
            return "general_knowledge"
        if any(w in prompt for w in ["def", "function", "class", "sort", "code", "script"]):
            return "code_request"
        if any(w in prompt for w in ["mean", "definition", "explain"]):
            return "definition"
        if "test" in prompt:
            return "testing"
        return "unknown"

    def _pick_without_repeat(self, pool: list[str]) -> str:
        """Picks a random string from the pool while avoiding repeating the last picked value."""
        if len(pool) <= 1:
            return pool[0]
        choice = random.choice(pool)
        while choice == self._last_reply:
            choice = random.choice(pool)
        self._last_reply = choice
        return choice

    def get_reply(self, prompt: str, current_theme: str = "general") -> str:
        """Returns a sassy response based on the prompt and current theme, using a multi-level fallback system."""
        intent = self.detect_intent(prompt)

        # 1️⃣ Priorité au thème actif
        mapped = self.theme_to_intent.get(current_theme)
        if mapped in self.responses["custom_responses"]:
            pool = self.responses["custom_responses"][mapped]
            if isinstance(pool, dict):
                patt_obj = self.custom_patterns[mapped]
                replies = select_subcategory(prompt, pool, patt_obj)
                return self._pick_without_repeat(replies)
            return self._pick_without_repeat(pool)

        # 2️⃣ Fallback sur l'intent détectée
        if intent in self.responses["custom_responses"]:
            pool = self.responses["custom_responses"][intent]
            if isinstance(pool, dict):
                patt_obj = self.custom_patterns[intent]
                replies = select_subcategory(prompt, pool, patt_obj)
                return self._pick_without_repeat(replies)
            return self._pick_without_repeat(pool)

        # 3️⃣ Standard responses
        if intent in self.responses["standard_responses"]:
            return self._pick_without_repeat(self.responses["standard_responses"][intent])

        # 4️⃣ Fallback global
        return self._pick_without_repeat(self.fallbacks)
