import pytest

from src.agent_wrapper import normalize_query as wrapper_normalize_query
from src.agent_wrapper import run_agent_wrapper
from src.runtime_hardening import normalize_query as runtime_normalize_query


@pytest.mark.parametrize(
    "query",
    [
        "  Remedy ٠٥  ",
        "قارن بين Remedy 4 و Remedy 5",
        "هل ACCURACY PLUS MEDICAL LABORATORY في بيسك بلس؟",
        "What is the annual limit for Remedy 04?",
    ],
)
def test_wrapper_is_canonical_normalization_authority(query):
    normalized = wrapper_normalize_query(query)

    assert runtime_normalize_query(query) == normalized
    assert wrapper_normalize_query(normalized) == normalized


@pytest.mark.parametrize(
    "query",
    [
        "قارن بين Remedy 4 و Remedy 5",
        "هل ACCURACY PLUS MEDICAL LABORATORY في بيسك بلس؟",
        "What is the annual limit for Remedy 04?",
        "Show me something unsupported",
    ],
)
def test_raw_and_normalized_queries_keep_same_routing(query):
    normalized = wrapper_normalize_query(query)

    raw_result = run_agent_wrapper(query)
    normalized_result = run_agent_wrapper(normalized)

    assert raw_result["ok"] == normalized_result["ok"]
    assert raw_result["intent"] == normalized_result["intent"]
    assert raw_result["plan_name"] == normalized_result["plan_name"]
    assert raw_result["tool_name"] == normalized_result["tool_name"]
