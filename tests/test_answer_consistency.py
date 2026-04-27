import pytest
from src.agent_wrapper import run_agent_wrapper

APPROVED_PLAN = "Remedy 02"
QUESTIONS = [
    "What is the annual limit for Remedy 02?",
    "What is the network for Remedy 02?",
    "Is direct billing available in Remedy 02?",
    "Is referral required for Remedy 02?",
    "What is the area of coverage for Remedy 02?",
    "What is the reimbursement rule for Remedy 02?",
    "Give me a summary of Remedy 02",
    "Tell me about Remedy 02",
    "Overview of Remedy 02",
    "Plan summary for Remedy 02"
]

@pytest.mark.parametrize("question", QUESTIONS)
def test_answer_consistency(question):
    # Run the same question multiple times
    results = [run_agent_wrapper(question) for _ in range(3)]
    # All outputs must be identical
    first = results[0]
    for r in results[1:]:
        assert r == first, f"Inconsistent output for question: {question}"
    # Check for no raw data leakage
    forbidden = ["source_trace", "raw", "unapproved", "internal", "debug", "json", "{", "}"]
    msg = first["message"] if "message" in first else ""
    for f in forbidden:
        assert f not in msg, f"Forbidden data leaked for question: {question}"
    # Check for no None/empty/broken strings
    assert first["ok"] is True
    assert first["plan_name"] == APPROVED_PLAN
    assert first["data"] is not None
    assert isinstance(first["message"], str) and first["message"].strip() != ""
    # Output structure consistency
    assert set(first.keys()) == set(results[1].keys())
    assert set(first["data"].keys()) == set(results[1]["data"].keys())
