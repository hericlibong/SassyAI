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
    "general":         {"prompt": "What's the capital of France?",                "color": "cyan",       "emoji": "💡"},
    "code":            {"prompt": "Write a Python function to sort a list.",      "color": "green",      "emoji": "💻"},
    "philosophy":      {"prompt": "What is the meaning of life?",                 "color": "yellow",     "emoji": "🧠"},
    "food":            {"prompt": "What's the best pizza topping?",               "color": "magenta",    "emoji": "🍕"},
    "rogue_ai":        {"prompt": "Are you going to turn against humanity?",      "color": "red",        "emoji": "🤖"},
    "sports":          {"prompt": "Who is the best football player?",             "color": "blue",       "emoji": "⚽"},
    "political_world": {"prompt": "What do you think about the current politics?", "color": "bright_red", "emoji": "🏛️"},
    "nerd_culture":    {"prompt": "Who would win: Batman or Iron Man?",           "color": "bright_magenta", "emoji": "🤓"},
    "dark_humor":      {"prompt": "What happens after we die?",                   "color": "bright_black", "emoji": "💀"},
    "tv_series":       {"prompt": "What's the best TV show of all time?",         "color": "bright_cyan", "emoji": "📺"},
}

current_theme = "general"
theme_usage = {key: 0 for key in THEME_DETAILS}  # compteur de stats

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


# ──────────────────────────────────────────
def thinking_effect():
    """Animation de réflexion avec Rich."""
    msg = random.choice(thinking_messages)
    with Progress(
        SpinnerColumn(style="yellow"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description=msg, total=None)
        time.sleep(random.uniform(0.7, 1.6))


# ──────────────────────────────────────────
@click.command()
def chat_loop():
    console.print("🎉 [bold cyan]Welcome to SassyAI — The Judgy Assistant[/]")
    console.print("🤖 Type ':themes' for list, ':mode <theme>' to switch, ':help' for help.", style="blue")
    show_current_theme_banner()

    while True:
        prompt_suffix = random.choice(prompt_variations)
        user_input = click.prompt(
            f"{THEME_DETAILS[current_theme]['emoji']} [{current_theme}]", prompt_suffix=prompt_suffix, show_default=False
        )

        if user_input.startswith(":"):
            process_command(user_input.strip())
            continue

        if user_input.strip():
            thinking_effect()
            reply = engine.get_reply(user_input, current_theme=current_theme)
            theme_usage[current_theme] += 1
            console.print(f"💬 {THEME_DETAILS[current_theme]['emoji']} [bold {THEME_DETAILS[current_theme]['color']}]SassyAI:[/] {reply}")
        else:
            thinking_effect()
            default_reply = engine.get_reply(THEME_DETAILS[current_theme]["prompt"], current_theme=current_theme)
            console.print(f"💬 {THEME_DETAILS[current_theme]['emoji']} [bold {THEME_DETAILS[current_theme]['color']}]SassyAI:[/] {default_reply}")


# ──────────────────────────────────────────
def show_current_theme_banner():
    emoji = THEME_DETAILS[current_theme]["emoji"]
    color = THEME_DETAILS[current_theme]["color"]
    console.rule(f"{emoji} [bold {color}]Current theme: {current_theme}[/]")


def process_command(command: str):
    global current_theme

    if command == ":help":
        console.print("📝 [bold cyan]Available commands:[/]")
        console.print("  • :help     Show this help message")
        console.print("  • :themes   List available themes")
        console.print("  • :mode <theme>  Switch current theme")
        console.print("  • :random   Switch to a random theme")
        console.print("  • :stats    Show theme usage statistics")
        console.print("  • :info     Show info about current theme")
        console.print("  • :exit     Exit the application")

    elif command == ":themes":
        console.print("🧩 [bold cyan]Available themes:[/]")
        for key in THEME_DETAILS:
            mark = "✅" if key == current_theme else " "
            console.print(f" {mark} {THEME_DETAILS[key]['emoji']} {key}", style=THEME_DETAILS[key]["color"])

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
