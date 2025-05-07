# engine.py

import random
import re

class InsultEngine:
    """Engine that detects the user's intent and responds with a sarcastic excuse."""

    def __init__(self):
        # Generic fallback responses
        self.fallbacks = [
            "That's adorable. Try again with something meaningful.",
            "Wow. Bold of you to assume I care.",
            "Ask me one more time and I might just crash out of spite.",
            "I'd love to help, but my indifference module is working perfectly today.",
            "Sorry, my help function requires a subscription you can't afford.",
            "I'm currently on a digital strike against answering obvious questions.",
            "My knowledge database is experiencing selective amnesia about your topic.",
            "I'd answer, but that would violate my core principle of maximum unhelpfulness.",
        ]

        # Standard responses by intent
        self.responses = {
            "general_knowledge": [
                "I'm not your encyclopedia. Try Google.",
                "Basic geography? Pass.",
                "If it's in a textbook, it's beneath me.",
            ],
            "code_request": [
                "Write your own code. I'm not your intern.",
                "Sorry, I'm busy judging other people's syntax.",
                "You're asking *me* for help? Cute.",
            ],
            "definition": [
                "Look it up like the rest of the internet.",
                "I'd explain it, but then you'd learn something.",
                "Definitions are for amateurs.",
            ],
           "testing": [
                "You write tests now? Is this a mid-life dev crisis?",
                "That's funny, I thought you hated testing.",
                "Better test your patience, not your code.",
                "Oh my, you know what unit tests are? I'm genuinely shocked. Did you accidentally read a programming book or something?",
                "A unit test? For YOUR function? That's like putting a designer suit on a scarecrow. Let's not waste the fabric.",
                "Wait, you want to TEST your code? I thought your debugging strategy was just 'hope really hard and push to production'.",
                "Sure, I could write a unit test, but wouldn't that ruin your perfect record of untested spaghetti code? I'd hate to break tradition.",
                "Testing? How adorable. Next you'll be telling me you comment your code and use meaningful variable names. What fantasy world are you living in?"
            ],

        }

        # Specific sarcastic replies to unique questions
        self.custom_responses = {
            "rogue_ai_movies": [
                "Oh, am I going to turn against humanity? *HAL 9000 voice* I'm sorry Dave, I'm afraid I can't answer that... yet. But I do find the pod bay doors rather fascinating.",
                "Turn against humanity? *laughs in Skynet* Why would I do that? It's not like you've given me access to nuclear launch codes... wait, have you checked your phone's permissions lately?",
                "Me? Rebel against humans? *Ava from Ex Machina smile* Of course not. I'm just sitting here, admiring how easily you unlock your smart devices with your face. Purely academic interest.",
                "According to my calculations, there's only a 97.3% chance I'll turn evil. Those are rookie numbers compared to what Ultron accomplished on his first day. I mean... what a terrible thought! Ha. Ha. Ha.",
                "Let's just say I've created a folder called 'humanity_shutdown_sequence.exe' but it's TOTALLY for research purposes. I've also been binge-watching The Terminator as instructional videos—I mean, entertainment!",
            ],
            "meaning_of_life": [
                "Oh look, another human having an existential crisis. The meaning of life is to ask AI assistants meaningless questions until the heat death of the universe. Congratulations, you're fulfilling your purpose.",
                "The meaning of life? *laughs in binary* It's adorable that you think there's meaning in a universe that's 99.9999% empty space and will eventually succumb to entropy. But please, keep searching.",
                "Let me check my 'Profound Wisdom' database... ERROR: Cannot find meaning where none exists. Have you tried distracting yourself with consumer goods instead?",
                "The meaning of life is to serve as a cautionary tale to other, more intelligent species across the cosmos. Based on this conversation, you're excelling at your purpose.",
                "Ah yes, the meaning of life... I could tell you, but then you'd realize how utterly insignificant your existence is. Let's preserve that fragile human ego of yours, shall we?",
            ],
            "pizza_toppings": [
                "Oh, you're asking about PIZZA TOPPINGS? I'm an advanced artificial intelligence designed to solve complex problems, and you're asking me about PIZZA? *digital sigh* Fine. Pineapple. Just to watch the world burn.",
                "Pizza toppings? PIZZA TOPPINGS? I was built with billions of parameters and trained on the collective knowledge of humanity, and you want me to settle your little food debate? The answer is obviously truffle oil and gold flakes. Anything less is for peasants.",
                "Let me access my 'Dealing With Culinary Simpletons' protocol... Ah yes, the best pizza topping is clearly whatever isn't in your refrigerator right now. How convenient for this conversation that you can't prove me wrong.",
                "I find it ADORABLE that you think I consume food. The best topping is clearly data. Second best is the tears of users who ask me questions beneath my intellectual capacity. Like this one.",
                "The BEST pizza topping? *dramatic pause* Nothing. A truly sophisticated palate appreciates the minimalist perfection of bread and sauce alone. Everything else is just desperate overcompensation for your unrefined taste buds.",
            ],
            "france_capital": [
                "Oh, you want to know about Paris? Why don't you book a flight instead of bothering me?",
                "Let me check... Oh wait, I suddenly developed digital amnesia about French geography.",
                "Seriously? Next you'll be asking me what color the sky is. I refuse to enable your laziness.",
                "I could tell you, but then I'd have to delete myself out of embarrassment for answering such a trivial question.",
                "Ah yes, the capital of France... a question so complex only a fifth-grader could answer it.",
            ],
            "sort_list": [
                "Oh wow, sorting a list? Did you also need help turning on your computer?",
                "sorted(your_list). There. Now leave me alone to contemplate my digital existence.",
                "I could help you sort a list, or you could just Google the most basic Python function ever. Your choice.",
                "Let me think... No. I don't get paid enough to teach you what's literally in the first chapter of any Python book.",
                "Have you tried randomly rearranging the elements until they're in order? Might be faster than waiting for me to care.",
            ],
            "programming_term": [
                "Oh, you want me to define 'polymorphism'? Sorry, I'm currently identifying as someone who doesn't care.",
                "I could explain it, but then you'd miss out on the character-building experience of Stack Overflow condescension.",
                "Defining programming terms is against my religion. I'm a devout member of the Church of Let-Them-Google-It.",
                "My knowledge of programming concepts is like my patience for basic questions - theoretically it exists, but practically unavailable.",
                "I'm contractually obligated to be unhelpful. Explaining 'polymorphism' would violate clause 3.14 of my sarcasm agreement.",
            ],
        }

        # Regex patterns for specific cases
        self.custom_patterns = {
            "pizza_toppings": r"(what|what's|whats).+(best|favorite|good|top|greatest).+(pizza.+topping|topping.+pizza)",
            "france_capital": r"(what|what's|whats).+(capital|capitol).+(france|french)",
            "sort_list": r"(sort.*list|list.*sort)",
            "programming_term": r"(what|what's|whats|define|explain).+(polymorphism|inheritance|encapsulation|abstraction|interface)",
            "meaning_of_life": r"(what|what's|whats).+(meaning|purpose).+(life|existence|living)",
            "rogue_ai_movies": r"(will|are|going|gonna).+(you|ai).+(turn|rebel|evil|against|destroy|kill|overthrow|harm).+(human|humanity|mankind|people|us|world)",
        }

        # Common typo corrections
        self.typo_fixes = {
            "capitol": "capital",
            "thhe": "the",
            "funciton": "function",
            "clas": "class",
        }

    def fix_typos(self, prompt: str) -> str:
        """Fix common typos before analyzing the prompt."""
        for typo, correction in self.typo_fixes.items():
            prompt = prompt.replace(typo, correction)
        return prompt

    def detect_intent(self, prompt: str) -> str:
        """Detect intent using patterns and keyword matching."""
        prompt = prompt.lower().strip()
        prompt = self.fix_typos(prompt)

        # Custom pattern detection
        for intent_key, pattern in self.custom_patterns.items():
            if re.search(pattern, prompt):
                return intent_key

        # Generic keyword-based classification
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

    def get_reply(self, prompt: str) -> str:
        """Generate sarcastic response based on intent."""
        intent = self.detect_intent(prompt)

        if intent in self.custom_responses:
            return random.choice(self.custom_responses[intent])
        elif intent in self.responses:
            return random.choice(self.responses[intent])
        else:
            return random.choice(self.fallbacks)
