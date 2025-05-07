# sassy_ai/tests/test_cli_commands.py

import pytest
from click.testing import CliRunner
from sassy_ai.main_cli import chat_loop
from sassy_ai.main_cli import exit_messages, THEMES


@pytest.fixture
def runner():
    """Fixture to provide a Click test runner."""
    return CliRunner()


def test_help_command(runner):
    """Test the help command displays available commands."""
    result = runner.invoke(chat_loop, input=":help\n:exit\n")
    assert result.exit_code == 0
    assert "📝 Available commands:" in result.output
    assert ":help" in result.output
    assert ":themes" in result.output
    assert ":mode <theme>" in result.output
    assert ":exit" in result.output


def test_themes_command(runner):
    """Test the themes command displays all themes."""
    result = runner.invoke(chat_loop, input=":themes\n:exit\n")
    assert result.exit_code == 0
    assert "🧩 Available themes:" in result.output
    for theme in THEMES.keys():
        assert theme in result.output


def test_change_theme_valid(runner):
    """Test changing theme to a valid option."""
    result = runner.invoke(chat_loop, input=":mode philosophy\n:exit\n")
    assert result.exit_code == 0
    assert "🍕 Theme changed to: philosophy" in result.output


def test_change_theme_invalid(runner):
    """Test changing theme to an invalid option."""
    result = runner.invoke(chat_loop, input=":mode unknown_theme\n:exit\n")
    assert result.exit_code == 0
    assert "❌ Unknown theme" in result.output


def test_exit_command(runner):
    """Test the exit command with random exit message."""
    result = runner.invoke(chat_loop, input=":exit\n")
    assert result.exit_code == 0
    assert any(msg in result.output for msg in exit_messages)


def test_invalid_command(runner):
    """Test an unknown command."""
    result = runner.invoke(chat_loop, input=":unknown\n:exit\n")
    assert result.exit_code == 0
    assert "❗ Unknown command" in result.output
