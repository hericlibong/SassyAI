# main_cli.py
import click
import time
import random
from engine import InsultEngine

engine = InsultEngine()

THEMES = {
    "general": {"prompt": "What's the capital of France?", "color": "cyan"},
    "code": {"prompt": "Write a Python function to sort a list.", "color": "green"},
    "philosophy": {"prompt": "What is the meaning of life?", "color": "yellow"},
    "food": {"prompt": "What's the best pizza topping?", "color": "magenta"},
    "rogue_ai": {"prompt": "Are you going to turn against humanity?", "color": "red"},
}

current_theme = "general"

# Messages de sortie variés
exit_messages = [
    "👋 Bye, human. Try not to break anything while I'm gone.",
    "🚪 Exiting... Don't pretend you're not sad to see me go.",
    "💤 Logging off... Finally, some peace and quiet.",
    "🤖 Shutting down... Try not to miss me too much.",
    "🛑 Ending session... I hope you learned something. Unlikely.",
]

# Messages de réflexion (thinking)
thinking_messages = [
    "🤔 Let me ponder on that...",
    "💭 Just a moment, I’m processing this nonsense...",
    "🧠 Thinking... although it's probably not worth it.",
    "⏳ Give me a second... This one is too trivial.",
    "😏 Oh, you're making me think? Bold move.",
]

# Variations du prompt
prompt_variations = [
    " You > ",
    " Tell me: ",
    " Speak up: ",
    " Your move: ",
]


def thinking_effect():
    """Simuler une réflexion avec un message aléatoire et un délai."""
    message = random.choice(thinking_messages)
    click.secho(message, fg="yellow")
    time.sleep(random.uniform(0.5, 1.5))  # Délai aléatoire pour simuler la réflexion


@click.command()
def chat_loop():
    """Boucle interactive pour interagir avec SassyAI."""
    click.secho("🎉 Welcome to SassyAI — The Judgy Assistant", fg="cyan")
    click.secho("🤖 Type ':themes' if you need to see available themes.", fg="blue")
    click.secho("🤖 Type ':mode <theme>' to change theme.", fg="blue")
    click.secho("💡 Type ':help' to see available commands.", fg="yellow")
    click.secho(f"🤖 Current theme: {current_theme}\n", fg=THEMES[current_theme]["color"])

    while True:
        # Variation aléatoire du prompt
        prompt_suffix = random.choice(prompt_variations)
        # Récupérer la question ou commande de l'utilisateur
        user_input = click.prompt(
            f"🗨️ [{current_theme}]", prompt_suffix=prompt_suffix, show_default=False
        )

        # Gérer les commandes spéciales
        if user_input.startswith(":"):
            process_command(user_input)
            continue

        # Gestion des questions ou des réponses par défaut si aucune question n'est donnée
        if user_input.strip():
            thinking_effect()  # Simuler la réflexion avant de répondre
            reply = engine.get_reply(user_input)
            click.secho(f"💬 SassyAI: {reply}", fg=THEMES[current_theme]["color"])
        else:
            # Réponse par défaut basée sur le thème courant
            thinking_effect()
            default_reply = engine.get_reply(THEMES[current_theme]["prompt"])
            click.secho(f"💬 SassyAI (by theme): {default_reply}", fg=THEMES[current_theme]["color"])


def process_command(command):
    """Gérer les commandes spéciales."""
    global current_theme

    if command == ":help":
        click.secho("📝 Available commands:", fg="cyan")
        click.echo(" - :help         Show this help message")
        click.echo(" - :themes       Show available themes")
        click.echo(" - :mode <theme> Change the current theme")
        click.echo(" - :exit         Exit the application")
    elif command == ":themes":
        click.secho("🧩 Available themes:", fg="cyan")
        for key in THEMES:
            theme_indicator = "✅" if key == current_theme else " "
            click.secho(f" {theme_indicator} {key}", fg=THEMES[key]["color"])
    elif command.startswith(":mode "):
        theme = command.split(" ")[1]
        if theme in THEMES:
            current_theme = theme
            click.secho(f"🍕 Theme changed to: {theme}", fg=THEMES[current_theme]["color"])
        else:
            click.secho("❌ Unknown theme. Use ':themes' to see available ones.", fg="red")
    elif command == ":exit":
        # Afficher un message de sortie aléatoire
        exit_message = random.choice(exit_messages)
        click.secho(exit_message, fg="cyan")
        exit()
    else:
        click.secho("❗ Unknown command. Type ':help' for assistance.", fg="red")


if __name__ == "__main__":
    chat_loop()
