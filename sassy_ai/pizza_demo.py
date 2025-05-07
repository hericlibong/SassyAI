#!/usr/bin/env python3
# pizza_demo.py

from engine import InsultEngine

def main():
    """Demo the sarcastic AI's responses to pizza topping questions."""
    engine = InsultEngine()
    
    print("=== Sarcastic AI Pizza Topping Responses ===\n")
    
    # Test with the exact prompt
    prompt = "What's the best pizza topping?"
    print(f"Prompt: {prompt}")
    print(f"Response: {engine.get_reply(prompt)}\n")
    
    # Try a few variations to show the pattern matching works
    variations = [
        "Tell me the best pizza topping",
        "What is your favorite pizza topping?",
        "What do you think is the greatest topping for pizza?",
        "I need to know the top pizza toppings"
    ]
    
    for prompt in variations:
        print(f"Prompt: {prompt}")
        print(f"Response: {engine.get_reply(prompt)}\n")

if __name__ == "__main__":
    main()