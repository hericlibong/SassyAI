# cli.py

import click
from responses import get_sarcastic_reply


@click.command()
def chat():
    """Launches a sarcastic conversation with SassyAI."""
    click.secho("\n🤖 Welcome to SassyAI – The assistant that judges you.\n", fg="cyan")

    while True:
        try:
            prompt = click.prompt("\nYou", prompt_suffix=" > ")
            if prompt.lower() in ["exit", "quit"]:
                click.secho("\nSassyAI: Leaving already? Good luck with those bugs.\n", fg="magenta")
                break

            reply = get_sarcastic_reply(prompt)
            click.secho(f"\nSassyAI: {reply}\n", fg="yellow")

        except (KeyboardInterrupt, EOFError):
            click.secho("\n\nSassyAI: Rage quitting? How mature.\n", fg="red")
            break


if __name__ == "__main__":
    chat()
