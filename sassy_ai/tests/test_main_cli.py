# sassy_ai/tests/test_main_cli.py

import pytest
from click.testing import CliRunner
from sassy_ai.main_cli import chat_loop, exit_messages, thinking_messages


@pytest.fixture
def runner():
    """Fixture to provide a Click test runner."""
    return CliRunner()

# def test_app_launch(runner):
#     result = runner.invoke(chat_loop, [])
#     assert result.exit_code == 0
#     assert "🎉 Welcome to SassyAI" in result.output


def test_help_command(runner):
    result = runner.invoke(chat_loop, input=":help\n:exit\n")
    assert "📝 Available commands:" in result.output


def test_themes_command(runner):
    result = runner.invoke(chat_loop, input=":themes\n:exit\n")
    assert "🧩 Available themes:" in result.output


def test_change_theme(runner):
    result = runner.invoke(chat_loop, input=":mode philosophy\n:exit\n")
    assert "🍕 Theme changed to: philosophy" in result.output


def test_exit_command(runner):
    result = runner.invoke(chat_loop, input=":exit\n")
    assert any(msg in result.output for msg in exit_messages)


def test_ask_question(runner):
    result = runner.invoke(chat_loop, input="What is the meaning of life?\n:exit\n")
    assert "💬 SassyAI:" in result.output


def test_thinking_message(runner):
    result = runner.invoke(chat_loop, input="What is Python?\n:exit\n")
    assert any(msg in result.output for msg in thinking_messages)
