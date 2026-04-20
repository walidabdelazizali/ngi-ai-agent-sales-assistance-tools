from src.constrained_planner import plan_user_query, execute_planned_query

def test_plan_core():
    out = plan_user_query("Tell me the annual limit for Remedy 04")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 04"
    assert "Supported plan" in out["reason"]

def test_reimbursement_rules():
    out = plan_user_query("What are the reimbursement rules for Remedy 05?")
    assert out["ok"] is True
    assert out["intent"] == "reimbursement_rules"
    assert out["plan_name"] == "Remedy 05"

def test_plan_summary():
    out = plan_user_query("Give me a summary of Remedy 04")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 04"

def test_unsupported_plan():
    out = plan_user_query("Tell me about Remedy 99")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert "No supported plan" in out["reason"]

def test_ambiguous_query():
    out = plan_user_query("How do I get a discount?")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert "No supported plan" in out["reason"]

def test_execute_planned_query_dict():
    out = execute_planned_query("Tell me the annual limit for Remedy 04", "dict")
    assert isinstance(out, dict)
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 04"

def test_execute_planned_query_text():
    out = execute_planned_query("What are the reimbursement rules for Remedy 05?", "text")
    assert isinstance(out, str)
    assert "Intent: reimbursement_rules" in out
    assert "Plan: Remedy 05" in out

def test_execute_planned_query_unsupported():
    out = execute_planned_query("Tell me about Remedy 99", "dict")
    assert isinstance(out, dict)
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert "Supported plans" in out["message"]

def test_regression_safe():
    queries = [
        ("Tell me the annual limit for Remedy 04", "dict"),
        ("What are the reimbursement rules for Remedy 05?", "text"),
        ("Give me a summary of Remedy 04", "dict"),
        ("Tell me about Remedy 99", "dict"),
        ("How do I get a discount?", "dict"),
        ("Tell me the annual limit for Remedy 04", "invalid"),
    ]
    for q, mode in queries:
        out = execute_planned_query(q, mode)
        assert out is not None
