import pytest
from src.query import business_answer
from src.agent_wrapper import run_agent_wrapper

def test_approved_plan_business_questions():
    # Use Remedy 02 as the approved baseline plan
    approved_plan = "Remedy 02"
    draft_plan = "Remedy 04"  # Known to be not ready in baseline
    questions = [
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
    # Approved plan: all questions must be answered with ok=True and no raw/internal data
    for q in questions:
        out = run_agent_wrapper(q)
        assert out["ok"] is True, f"Failed for question: {q}"
        assert out["plan_name"] == approved_plan
        assert out["intent"] in ("plan_core", "reimbursement_rules", "plan_summary")
        assert out["data"] is not None
        # Output must not leak raw/internal data
        forbidden = ["source_trace", "raw", "unapproved", "internal", "debug", "json", "{", "}"]
        msg = out["message"] if "message" in out else ""
        for f in forbidden:
            assert f not in msg, f"Forbidden data leaked for question: {q}"
    # Draft/unapproved plan: must be blocked
    for q in questions:
        q_draft = q.replace(approved_plan, draft_plan)
        out = run_agent_wrapper(q_draft)
        assert out["ok"] is False, f"Draft plan not blocked for: {q_draft}"
        assert out["plan_name"] == draft_plan
        assert out["data"] is None
        assert "not available" in out["message"].lower() or "غير متاحة" in out["message"]
    # Missing source_trace: simulate by direct call if possible (not exposed in wrapper, so skip)
    # This is covered by plan readiness logic in wrapper
