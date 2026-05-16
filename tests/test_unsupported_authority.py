import pytest

from src.agent_adapter import handle_user_query
from src.agent_wrapper import run_agent_wrapper
from src.constrained_planner import execute_planned_query


@pytest.mark.parametrize(
    "query",
    [
        "Tell me about Remedy 99",
        "Show me the dental coverage for Remedy 04",
        "كيف أحصل على خصم؟",
    ],
)
def test_wrapper_unsupported_signal_is_structured(query):
    result = run_agent_wrapper(query)

    assert isinstance(result, dict)
    assert result["ok"] is False
    assert result["intent"] == "unsupported"
    assert getattr(result, "is_unsupported", False) is True
    assert result["normalized"]["status"] == "not_found"
    assert result["message"]


@pytest.mark.parametrize(
    "query",
    [
        "Tell me about Remedy 99",
        "Show me the dental coverage for Remedy 04",
        "كيف أحصل على خصم؟",
    ],
)
def test_adapter_preserves_structured_unsupported_signal(query):
    result = handle_user_query(query, "dict")

    assert isinstance(result, dict)
    assert result["ok"] is False
    assert result["intent"] == "unsupported"
    assert getattr(result, "is_unsupported", False) is True
    assert result["normalized"]["status"] == "not_found"
    assert result["message"]


def test_constrained_planner_uses_same_unsupported_authority():
    result = execute_planned_query("Tell me about Remedy 99", "dict")

    assert isinstance(result, dict)
    assert result["ok"] is False
    assert result["intent"] == "unsupported"
    assert getattr(result, "is_unsupported", False) is True
    assert result["message"]
