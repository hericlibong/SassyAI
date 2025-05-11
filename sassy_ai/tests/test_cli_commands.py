# sassy_ai/tests/test_cli_commands.py

import pytest
from click.testing import CliRunner
from sassy_ai.main_cli import chat_loop
from sassy_ai.main_cli import exit_messages, THEME_DETAILS


@pytest.fixture
def runner():
    """Fixture to provide a Click test runner."""
    return CliRunner()


def test_help_command(runner):
    result = runner.invoke(chat_loop, input="User\n:help\n:exit\n")
    assert result.exit_code == 0
    assert "📝 Available commands:" in result.output


def test_themes_command(runner):
    result = runner.invoke(chat_loop, input="User\n:themes\n:exit\n")
    assert result.exit_code == 0
    assert "🧩 Available themes:" in result.output


def test_change_theme_valid(runner):
    result = runner.invoke(chat_loop, input="User\n:mode philosophy\n:exit\n")
    assert result.exit_code == 0
    assert "Current theme: philosophy" in result.output


def test_change_theme_invalid(runner):
    result = runner.invoke(chat_loop, input="User\n:mode unknown_theme\n:exit\n")
    assert result.exit_code == 0
    assert "❌ Unknown theme" in result.output


def test_exit_command(runner):
    result = runner.invoke(chat_loop, input="User\n:exit\n")
    assert result.exit_code == 0
    assert any(exit_msg in result.output for exit_msg in [
        "👋 Bye, human.",
        "🚪 Exiting...",
        "💤 Logging off...",
        "🤖 Shutting down...",
        "🛑 Ending session..."
    ])


def test_invalid_command(runner):
    result = runner.invoke(chat_loop, input="User\n:unknown\n:exit\n")
    assert result.exit_code == 0
    assert "❗ Unknown command" in result.output
