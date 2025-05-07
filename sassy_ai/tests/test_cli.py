# tests/test_cli.py

import pytest
from click.testing import CliRunner
from sassy_ai.cli import chat


@pytest.fixture
def runner():
    """Fixture for Click CLI runner."""
    return CliRunner()


def test_cli_launch(runner):
    """Test the basic launch of the CLI."""
    result = runner.invoke(chat, input="exit\n")
    assert result.exit_code == 0
    assert "🤖 Welcome to SassyAI – The assistant that judges you." in result.output


def test_cli_interaction(runner):
    """Test the CLI interaction with a question."""
    result = runner.invoke(chat, input="What is Python?\nexit\n")
    assert result.exit_code == 0
    assert "SassyAI:" in result.output


def test_cli_exit_command(runner):
    """Test the exit command."""
    result = runner.invoke(chat, input="exit\n")
    assert result.exit_code == 0
    assert "SassyAI: Leaving already? Good luck with those bugs." in result.output


def test_cli_quit_command(runner):
    """Test the quit command."""
    result = runner.invoke(chat, input="quit\n")
    assert result.exit_code == 0
    assert "SassyAI: Leaving already? Good luck with those bugs." in result.output

# def test_cli_keyboard_interrupt(runner):
#     """Test keyboard interrupt (Ctrl+C) handling."""
#     result = runner.invoke(chat, input="\x03")
#     assert result.exit_code == 0
#     assert "SassyAI: Rage quitting? How mature." in result.output

# def test_cli_eof_error(runner):
#     """Test EOF error (Ctrl+D) handling."""
#     result = runner.invoke(chat, input="\x04")
#     assert result.exit_code == 0
#     assert "SassyAI: Rage quitting? How mature." in result.output
