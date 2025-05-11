# sassy_ai/tests/test_main_cli.py

import pytest
from click.testing import CliRunner
from sassy_ai.main_cli import chat_loop, exit_messages, THEME_DETAILS
import re


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


def test_change_theme(runner):
    result = runner.invoke(chat_loop, input="User\n:mode philosophy\n:exit\n")
    assert result.exit_code == 0
    assert "Current theme: philosophy" in result.output


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


def test_ask_question(runner):
    result = runner.invoke(chat_loop, input="User\nWhat is the capital of France?\n:exit\n")
    assert result.exit_code == 0
    assert "SassyAI:" in result.output


def test_themes_and_mode_and_info_and_stats(runner):
    result = runner.invoke(chat_loop, input="User\n:themes\n:mode philosophy\n:info\n:stats\n:exit\n")
    assert result.exit_code == 0
    assert "Available themes" in result.output
    assert "Current theme: philosophy" in result.output
    assert "Theme usage stats:" in result.output


def test_random_changes_theme(runner):
    # plusieurs :random puis :exit
    cmds = "\n".join([":random"] * 3 + [":exit\n"])
    result = runner.invoke(chat_loop, input=cmds)
    # extraire les lignes de règle qui contiennent "Current theme:"
    themes = {
        line.split("Current theme: ")[1]
        for line in result.output.splitlines()
        if "Current theme:" in line
    }
    # on devrait voir au moins deux thèmes différents
    assert len(themes) >= 2
