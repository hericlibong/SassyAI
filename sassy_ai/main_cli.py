# main_cli.py
import click
from engine import InsultEngine
import random
import time


engine = InsultEngine()

THEMES = {
    "general": "What's the capital of France?",
    "code": "Write a Python function to sort a list.",
    "philosophy": "What is the meaning of life?",
    "food": "What's the best pizza topping?",
    "rogue_ai": "Are you going to turn against humanity?"
}

OPENINGS = [
    "🎭 Let the sarcasm begin...",
    "🧠 Preparing a deeply unhelpful answer...",
    "🙄 Booting up my sarcasm core...",
    "👁️‍🗨️ Running diagnostics on your intelligence level...",
    "🎬 Lights, sarcasm, action!"
]

CLOSINGS = [
    "💀 That was emotionally exhausting.",
    "🚪 I'm off to judge someone else's questions now.",
    "🎤 And *that's* how you answer a question you never should've asked.",
    "🫠 Try harder next time.",
    "🥴 Is that the best you’ve got?"
]

@click.command()
@click.argument("prompt", required=False)
@click.option("--mode", type=click.Choice(list(THEMES.keys())), help="Pick a sarcastic theme")
def ask(prompt, mode):
    """SassyAI - Ask your question and get judged."""
    click.secho("🤖 SassyAI is online.", fg="cyan")
    click.secho(random.choice(OPENINGS), fg="bright_blue")

    if not prompt:
        if mode:
            prompt = THEMES[mode]
            click.secho(f"💡 Using sarcastic theme: {mode}", fg="blue")
        else:
            click.secho("🧐 No question? Let me guess, decision fatigue?", fg="yellow")
            click.echo("Try one of these lovely sarcastic themes:")
            for key in THEMES:
                click.secho(f"  --mode={key}", fg="magenta")
            click.echo("\nOr just type your question directly. If you dare.")
            return

    if prompt:
        click.secho("🧠 Let me get this straight... You just asked:", fg="bright_yellow")
        click.secho(f"❓ “{prompt}”\n", fg="white")
        reply = engine.get_reply(prompt)
        time.sleep(1.2)
        click.secho(f"💬 SassyAI: {reply}", fg="green")
        click.secho(random.choice(CLOSINGS), fg="bright_black")

if __name__ == "__main__":
    ask()
