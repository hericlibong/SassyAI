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
    result = runner.invoke(chat_loop, input=":help\n:exit\n")
    assert "📝 Available commands:" in result.output


def test_themes_command(runner):
    result = runner.invoke(chat_loop, input=":themes\n:exit\n")
    assert "🧩 Available themes:" in result.output


def test_change_theme(runner):
    result = runner.invoke(chat_loop, input=":mode philosophy\n:exit\n")
    assert "Current theme: philosophy" in result.output


def test_exit_command(runner):
    result = runner.invoke(chat_loop, input=":exit\n")
    assert any(msg in result.output for msg in exit_messages)


def test_ask_question(runner):
    result = runner.invoke(chat_loop, input="What is the meaning of life?\n:exit\n")
    assert re.search(r"💬 .*SassyAI:", result.output)


def test_themes_and_mode_and_info_and_stats(runner):
    # 1) :themes  2) :mode code  3) :info  4) :stats  5) :exit
    cmds = ":themes\n:mode code\n:info\n:stats\n:exit\n"
    result = runner.invoke(chat_loop, input=cmds)
    # on liste bien les thèmes
    assert "Available themes" in result.output
    # on change bien de thème (via la règle Rich)
    assert "Current theme: code" in result.output
    # on affiche les infos du thème
    assert THEME_DETAILS["code"]["prompt"] in result.output
    # on affiche les stats
    assert "Theme usage stats" in result.output


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
