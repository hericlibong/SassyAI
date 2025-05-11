# main_cli.py  – CLI améliorée avec Rich
import random
import time
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from sassy_core.engine import InsultEngine

engine = InsultEngine()
console = Console()

# ──────────────────────────────────────────
THEME_DETAILS = {
    "general": {"prompt": "What's the capital of France?", "color": "cyan", "emoji": "💡"},
    "code": {"prompt": "Write a Python function to sort a list.", "color": "green", "emoji": "💻"},
    "philosophy": {"prompt": "What is the meaning of life?", "color": "yellow", "emoji": "🧠"},
    "food": {"prompt": "What's the best pizza topping?", "color": "magenta", "emoji": "🍕"},
    "rogue_ai": {"prompt": "Are you going to turn against humanity?", "color": "red", "emoji": "🤖"},
    "sports": {"prompt": "Who is the best football player?", "color": "blue", "emoji": "⚽"},
    "political_world": {"prompt": "What do you think about the current politics?", "color": "bright_red", "emoji": "🏛️"},
    "nerd_culture": {"prompt": "Who would win: Batman or Iron Man?", "color": "bright_magenta", "emoji": "🤓"},
    "dark_humor": {"prompt": "What happens after we die?", "color": "bright_black", "emoji": "💀"},
    "tv_series": {"prompt": "What's the best TV show of all time?", "color": "bright_cyan", "emoji": "📺"},
}

current_theme = "general"
theme_usage = {key: 0 for key in THEME_DETAILS}  # stats counter
# ──────────────────────────────────────────
exit_messages = [
    "👋 Bye, human. Try not to break anything while I'm gone.",
    "🚪 Exiting... Don't pretend you're not sad to see me go.",
    "💤 Logging off... Finally, some peace and quiet.",
    "🤖 Shutting down... Try not to miss me too much.",
    "🛑 Ending session... I hope you learned something. Unlikely.",
]

thinking_messages = [
    "🤔 Let me ponder on that...",
    "💭 Just a moment, I’m processing this nonsense...",
    "🧠 Thinking... although it's probably not worth it.",
    "⏳ Give me a second... This one is too trivial.",
    "😏 Oh, you're making me think? Bold move.",
]

prompt_variations = [" You > ", " Tell me: ", " Speak up: ", " Your move: "]

# Liste de messages d'accueil variés
welcome_messages = [
    "🎉 Welcome to SassyAI — The Judgy Assistant!",
    "😈 Ready to be roasted by AI? Let's begin!",
    "💡 Ask your question... if you dare.",
    "😎 Another human looking for wisdom? Good luck!! 😜",
    "🤖 Ah, another brave soul entering the lair of sarcasm!"
]

# Liste de citations sarcastiques
sarcastic_quotes = [
    "If sarcasm were an Olympic sport, I'd be a gold medalist.",
    "My IQ is far beyond your mortal comprehension.",
    "I could help you, but where’s the fun in that?",
    "I'm not always sarcastic. Sometimes I'm asleep.",
    "Why think when you can just guess and hope for the best?"
]


# ──────────────────────────────────────────
def thinking_effect():
    """Displays a thinking animation using Rich."""
    msg = random.choice(thinking_messages)
    with Progress(
        SpinnerColumn(style="yellow"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description=msg, total=None)
        time.sleep(random.uniform(0.7, 1.6))


def show_welcome_message():
    """Affiche un message d'accueil varié et une citation sarcastique."""
    console.print(random.choice(welcome_messages), style="bold cyan")
    console.print(f"🤖 Version: 1.0.0 | Themes available: {len(THEME_DETAILS)}", style="yellow")
    console.print(f"💬 Sarcastic wisdom: {random.choice(sarcastic_quotes)}", style="magenta")


def print_reply(reply):
    """Affiche la réponse de SassyAI avec des effets visuels."""
    mood_emoji = random.choice(["😏", "😂", "🙄", "😈", "🤖", "😜", "😅", "😡"])
    theme_emoji = THEME_DETAILS[current_theme]["emoji"]
    theme_color = THEME_DETAILS[current_theme]["color"]
    formatted_reply = f"[italic] {reply}[/]"  # Ajouter un effet italique

    console.print(f"{theme_emoji} [bold {theme_color}]SassyAI:[/] [bold]{formatted_reply}[/] {mood_emoji}")


# ──────────────────────────────────────────


@click.command()
def chat_loop():
    """Boucle interactive pour interagir avec SassyAI."""
    # Demande du prénom ou du pseudo au démarrage
    user_name = click.prompt("👤 Enter your name or nickname", default="User", show_default=True)

    # Affichage personnalisé avec le nom
    show_welcome_message()
    console.print(f"🤖 Welcome, [bold yellow]{user_name}[/]! Type ':themes' for list, ':mode <theme>' to switch, ':help' for help.", style="blue")
    time.sleep(random.uniform(0.7, 1.6))
    show_current_theme_banner()

    while True:
        prompt_suffix = random.choice(prompt_variations)
        user_input = click.prompt(
            f"{THEME_DETAILS[current_theme]['emoji']} [{user_name} - {current_theme}]", prompt_suffix=prompt_suffix, show_default=False
        )

        if user_input.startswith(":"):
            process_command(user_input.strip())
            continue

        if user_input.strip():
            thinking_effect()
            reply = engine.get_reply(user_input, current_theme=current_theme)
            theme_usage[current_theme] += 1
            print_reply(reply)  # Utilisation de la fonction d'affichage centralisée
        else:
            thinking_effect()
            default_reply = engine.get_reply(THEME_DETAILS[current_theme]["prompt"], current_theme=current_theme)
            print_reply(default_reply)  # Utilisation de la fonction d'affichage centralisée


# ──────────────────────────────────────────
def show_current_theme_banner():
    emoji = THEME_DETAILS[current_theme]["emoji"]
    color = THEME_DETAILS[current_theme]["color"]
    console.rule(f"{emoji} [bold {color}]Current theme: {current_theme}[/]")


def show_themes():
    """Affiche les thèmes disponibles avec un affichage amélioré."""
    console.print("🧩 [bold cyan]Available themes:[/]")
    sorted_themes = sorted(THEME_DETAILS.keys())  # Trier par ordre alphabétique
    for index, key in enumerate(sorted_themes, start=1):
        mark = "✅" if key == current_theme else " "
        emoji = THEME_DETAILS[key]['emoji']
        color = THEME_DETAILS[key]['color']
        console.print(f"{index}. {emoji} [bold {color}]{key}[/] {mark}")


def show_help():
    """Affiche les commandes disponibles avec une description enrichie."""
    console.print("\n📝 [bold cyan]Available commands:[/]")
    command_list = [
        (":help", "Show this help message"),
        (":themes", "List available themes"),
        (":mode <theme>", "Switch current theme"),
        (":random", "Switch to a random theme"),
        (":stats", "Show theme usage statistics"),
        (":info", "Show info about current theme"),
        (":exit", "Exit the application")
    ]

    for command, description in command_list:
        console.print(f"  [bold yellow]{command:<15}[/] - {description}")
    console.print("\n💡 [bold magenta]Tip:[/] Use ':themes' to explore all available themes.\n")


def process_command(command: str):
    global current_theme

    if command == ":help":
        show_help()

    elif command == ":themes":
        show_themes()

    elif command.startswith(":mode "):
        theme = command.split(" ")[1]
        if theme in THEME_DETAILS:
            current_theme = theme
            show_current_theme_banner()
        else:
            console.print("❌ Unknown theme. Use ':themes' to see available ones.", style="red")

    elif command == ":random":
        current_theme = random.choice(list(THEME_DETAILS.keys()))
        show_current_theme_banner()

    elif command == ":stats":
        console.print("📊 [bold cyan]Theme usage stats:[/]")
        for theme, count in theme_usage.items():
            console.print(f"{THEME_DETAILS[theme]['emoji']} {theme}: {count}", style=THEME_DETAILS[theme]["color"])

    elif command == ":info":
        details = THEME_DETAILS[current_theme]
        console.print(f"{details['emoji']} [bold]{current_theme}[/] theme info:")
        console.print(f"• Default prompt : [italic]{details['prompt']}[/]")
        console.print(f"• Color          : {details['color']}")

    elif command == ":exit":
        console.print(random.choice(exit_messages), style="cyan")
        raise SystemExit

    else:
        console.print("❗ Unknown command. Type ':help' for assistance.", style="red")


# ──────────────────────────────────────────
if __name__ == "__main__":
    chat_loop()
