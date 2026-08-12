"""
=========================================================
OmniMind AI Assistant
Agent Unit Tests
=========================================================

Tests for AI Agents.
"""

from unittest.mock import MagicMock, patch

import pytest

# ==========================================================
# DUMMY AGENT
# ==========================================================


class DummyAgent:
    """
    Dummy agent used for testing.
    """

    def __init__(self, name="Assistant"):

        self.name = name

        self.history = []

    def respond(self, message):

        self.history.append(message)

        return f"Echo: {message}"


# ==========================================================
# INITIALIZATION
# ==========================================================


def test_agent_initialization():

    agent = DummyAgent()

    assert agent.name == "Assistant"

    assert agent.history == []


# ==========================================================
# RESPONSE
# ==========================================================


def test_agent_response():

    agent = DummyAgent()

    response = agent.respond("Hello")

    assert response == "Echo: Hello"

    assert len(agent.history) == 1


# ==========================================================
# HISTORY
# ==========================================================


def test_history_storage():

    agent = DummyAgent()

    agent.respond("Hi")

    agent.respond("How are you?")

    assert len(agent.history) == 2

    assert agent.history[0] == "Hi"

    assert agent.history[1] == "How are you?"


# ==========================================================
# EMPTY MESSAGE
# ==========================================================


def test_empty_message():

    agent = DummyAgent()

    response = agent.respond("")

    assert response == "Echo: "


# ==========================================================
# LONG MESSAGE
# ==========================================================


def test_long_message():

    text = "A" * 10000

    agent = DummyAgent()

    response = agent.respond(text)

    assert response.startswith("Echo:")


# ==========================================================
# MOCKED LLM
# ==========================================================


@patch("builtins.print")
def test_mocked_llm(mock_print):

    llm = MagicMock()

    llm.generate.return_value = "AI Response"

    result = llm.generate("Hello")

    assert result == "AI Response"

    llm.generate.assert_called_once()


# ==========================================================
# MULTIPLE REQUESTS
# ==========================================================


def test_multiple_requests():

    agent = DummyAgent()

    for i in range(100):

        response = agent.respond(str(i))

        assert response.startswith("Echo")


# ==========================================================
# INVALID INPUT
# ==========================================================


def test_invalid_input():

    agent = DummyAgent()

    response = agent.respond(None)

    assert response == "Echo: None"


# ==========================================================
# AGENT NAME
# ==========================================================


@pytest.mark.parametrize(
    "name",
    [
        "ChatGPT",
        "Research",
        "Vision",
        "Voice",
        "Planner",
    ],
)
def test_agent_names(name):

    agent = DummyAgent(name)

    assert agent.name == name


# ==========================================================
# CONVERSATION
# ==========================================================


def test_conversation():

    agent = DummyAgent()

    messages = [
        "Hello",
        "Who are you?",
        "Explain AI",
        "Bye",
    ]

    for msg in messages:

        agent.respond(msg)

    assert len(agent.history) == 4


# ==========================================================
# STRESS TEST
# ==========================================================


def test_large_history():

    agent = DummyAgent()

    for i in range(1000):

        agent.respond(f"Message {i}")

    assert len(agent.history) == 1000
