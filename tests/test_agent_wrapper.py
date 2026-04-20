import pytest
from src.agent_wrapper import run_agent_wrapper

def test_plan_core_english():
    out = run_agent_wrapper("What is the annual limit for Remedy 04?")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 04"
    assert out["tool_name"] == "get_plan_core"
    assert isinstance(out["data"], dict)
    assert out["data"]["annual_limit"] == "500,000"

def test_plan_core_arabic():
    out = run_agent_wrapper("ما هو الحد السنوي لخطة ريميدي 04؟")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 04"
    assert out["tool_name"] == "get_plan_core"
    assert isinstance(out["data"], dict)
    assert out["data"]["annual_limit"] == "500,000"

def test_reimbursement_rules_english():
    out = run_agent_wrapper("What are the reimbursement rules for Remedy 05?")
    assert out["ok"] is True
    assert out["intent"] == "reimbursement_rules"
    assert out["plan_name"] == "Remedy 05"
    assert out["tool_name"] == "get_reimbursement_rules"
    assert isinstance(out["data"], dict)
    assert out["data"]["reimbursement_allowed"] is True

def test_reimbursement_rules_arabic():
    out = run_agent_wrapper("ما هي شروط التعويض لخطة ريميدي 05؟")
    assert out["ok"] is True
    assert out["intent"] == "reimbursement_rules"
    assert out["plan_name"] == "Remedy 05"
    assert out["tool_name"] == "get_reimbursement_rules"
    assert isinstance(out["data"], dict)
    assert out["data"]["reimbursement_allowed"] is True

def test_plan_summary_english():
    out = run_agent_wrapper("Give me a summary of Remedy 04")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 04"
    assert out["tool_name"] == "get_plan_summary"
    assert isinstance(out["data"], dict)
    assert "summary_text" in out["data"]

def test_plan_summary_arabic():
    out = run_agent_wrapper("اعطني ملخص لخطة ريميدي 04")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 04"
    assert out["tool_name"] == "get_plan_summary"
    assert isinstance(out["data"], dict)
    assert "summary_text" in out["data"]

def test_unsupported_intent():
    out = run_agent_wrapper("Show me the dental coverage for Remedy 04")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "not supported" in out["message"] or "supported plan" in out["message"]

def test_unknown_plan():
    out = run_agent_wrapper("What is the annual limit for Remedy 99?")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "supported plan" in out["message"]

def test_unsupported_query():
    out = run_agent_wrapper("How do I get a discount?")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "supported plan" in out["message"] or "not supported" in out["message"]
def test_unsupported_plan_summary():
    out = run_agent_wrapper("Tell me about Remedy 99")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "supported plan" in out["message"]
