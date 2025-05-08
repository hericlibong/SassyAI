# Updated engine.py

import random
import re
import json
import os

class InsultEngine:
    def __init__(self):
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

        self.responses = self.load_responses()
        self.custom_patterns = self.load_patterns()
        self.typo_fixes = self.load_typos()
        self.theme_to_intent = {
        "rogue_ai": "rogue_ai_movies",
        "food": "pizza_toppings",
        "philosophy": "meaning_of_life",
        "code": "code_request",
        "general": "general_knowledge",
        "sports": "sports_responses",
        "political_world": "political_discussions"
        }
        self._last_reply = None

    def load_responses(self):
        with open(os.path.join("config", "responses.json"), "r") as file:
            return json.load(file)

    def load_patterns(self):
        with open(os.path.join("config", "patterns.json"), "r") as file:
            return json.load(file)
        
    def load_typos(self):
        """Load common typo corrections from a JSON file."""
        try:
            with open(os.path.join("config", "typos.json"), "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def fix_typos(self, prompt: str) -> str:
        """Fix common typos before analyzing the prompt."""
        for typo, correction in self.typo_fixes.items():
            prompt = prompt.replace(typo, correction)
        return prompt


    def detect_intent(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        for intent_key, pattern in self.custom_patterns.items():
            if re.search(pattern, prompt):
                return intent_key

        if any(word in prompt for word in ["capital", "who is", "what is", "when did"]):
            return "general_knowledge"
        elif any(word in prompt for word in ["def", "function", "class", "sort", "code", "script"]):
            return "code_request"
        elif any(word in prompt for word in ["mean", "definition", "explain"]):
            return "definition"
        elif "test" in prompt:
            return "testing"
        else:
            return "unknown"
        
    def _pick_without_repeat(self, pool: list[str]) -> str:
        """Chooses a reply different from the previous one if possible."""
        if len(pool) <= 1:
            return pool[0]

        reply = random.choice(pool)
        while reply == self._last_reply:
            reply = random.choice(pool)
        self._last_reply = reply
        return reply
    
    
    def _select_sport_pool(self, sub_dict: dict, prompt: str) -> list[str]:
        p = prompt.lower()
        mapping = {
            "football":  ["football", "soccer", "nfl", "touchdown", "super bowl"],
            "basketball":["basketball", "nba", "dunk", "hoop", "court"],
            "baseball":  ["baseball", "mlb", "bat", "pitch", "home run"],
            "athletes":  ["athlete", "player", "star", "champion", "mvp"],
            "practice":  ["practice", "training", "workout", "exercise", "drill"],
        }
        for key, words in mapping.items():
            if any(w in p for w in words) and key in sub_dict:
                return sub_dict[key]
        return sub_dict.get("general", sum(sub_dict.values(), []))


    def _select_sport_pool(self, sub_dict: dict, prompt: str) -> list[str]:
        """Choisit la bonne sous-catégorie dans sports_responses."""
        p = prompt.lower()
        mapping = {
            "football":  ["football", "soccer", "nfl", "touchdown", "super bowl"],
            "basketball":["basketball", "nba", "dunk", "hoop", "court"],
            "baseball":  ["baseball", "mlb", "bat", "pitch", "home run"],
            "athletes":  ["athlete", "player", "star", "champion", "mvp"],
            "practice":  ["practice", "training", "workout", "exercise", "drill"],
        }
        for key, words in mapping.items():
            if any(w in p for w in words) and key in sub_dict:
                return sub_dict[key]
        # défaut : liste « general » ou concaténation de toutes les listes
        return sub_dict.get("general", sum(sub_dict.values(), []))


    def get_reply(self, prompt: str, current_theme: str = "general") -> str:
        """Génère une réplique sarcastique en tenant compte de l'intention et du thème."""
        intent = self.detect_intent(prompt)

        # 0️⃣  Cas où l'intention détectée est le bloc sports (avec sous-catégories)
        if intent == "sports_responses":
            sports_dict = self.responses["custom_responses"]["sports_responses"]
            return self._pick_without_repeat(self._select_sport_pool(sports_dict, prompt))

        # 1️⃣  Intention trouvée dans custom_responses
        if intent in self.responses["custom_responses"]:
            pool = self.responses["custom_responses"][intent]
            if isinstance(pool, dict):                       # ex. sports_responses
                return self._pick_without_repeat(pool.get("general",
                                                        sum(pool.values(), [])))
            return self._pick_without_repeat(pool)

        # 2️⃣  Aucune intention explicite : on regarde le thème choisi par l'utilisateur
        mapped_intent = self.theme_to_intent.get(current_theme)

        # 2-a  Thème courant pointe vers custom_responses
        if mapped_intent and mapped_intent in self.responses["custom_responses"]:
            pool = self.responses["custom_responses"][mapped_intent]
            if isinstance(pool, dict):                       # peut être sports_responses
                if mapped_intent == "sports_responses":      # sous-catégories sport
                    return self._pick_without_repeat(self._select_sport_pool(pool, prompt))
                return self._pick_without_repeat(pool.get("general",
                                                        sum(pool.values(), [])))
            return self._pick_without_repeat(pool)

        # 2-b  Thème courant pointe vers standard_responses
        if mapped_intent and mapped_intent in self.responses["standard_responses"]:
            return self._pick_without_repeat(
                self.responses["standard_responses"][mapped_intent]
            )

        # 3️⃣  Intention générique dans standard_responses
        if intent in self.responses["standard_responses"]:
            return self._pick_without_repeat(
                self.responses["standard_responses"][intent]
            )

        # 4️⃣  Fallback générique
        return self._pick_without_repeat(self.fallbacks)
