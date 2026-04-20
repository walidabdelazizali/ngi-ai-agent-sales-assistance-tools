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
    assert "تم عرض معلومات الخطة" in out["message"]

def test_plan_core_remedy03_english():
    out = run_agent_wrapper("What is the annual limit for Remedy 03?")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 03"
    assert out["tool_name"] == "get_plan_core"
    assert isinstance(out["data"], dict)
    assert "150,000" in out["data"]["annual_limit"]

def test_plan_core_remedy03_arabic():
    out = run_agent_wrapper("ما هو الحد السنوي لخطة ريميدي 03؟")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 03"
    assert out["tool_name"] == "get_plan_core"
    assert isinstance(out["data"], dict)
    assert "150,000" in out["data"]["annual_limit"]
    assert "تم عرض معلومات الخطة" in out["message"]

def test_plan_summary_remedy03_english():
    out = run_agent_wrapper("Give me a summary of Remedy 03")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 03"
    assert out["tool_name"] == "get_plan_summary"
    assert isinstance(out["data"], dict)
    assert "summary_text" in out["data"]

def test_plan_summary_remedy03_arabic():
    out = run_agent_wrapper("اعطني ملخص لخطة ريميدي 03")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 03"
    assert out["tool_name"] == "get_plan_summary"
    assert isinstance(out["data"], dict)
    assert "summary_text" in out["data"]
    assert "تم عرض ملخص الخطة" in out["message"]

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
    assert "تم عرض قواعد التعويض" in out["message"]

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
    assert "تم عرض ملخص الخطة" in out["message"]

def test_unsupported_intent():
    out = run_agent_wrapper("Show me the dental coverage for Remedy 04")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "not supported" in out["message"] or "supported plan" in out["message"]
    # Arabic unsupported
    out_ar = run_agent_wrapper("ما الفرق بين الريميدي 2 والريميدي 4؟")
    assert out_ar["ok"] is False
    assert out_ar["intent"] == "unsupported"
    assert out_ar["plan_name"] is None
    assert out_ar["tool_name"] is None
    assert out_ar["data"] is None
    assert "عذراً، النظام يدعم فقط الريميدي 03 والريميدي 04 والريميدي 05" in out_ar["message"]

def test_unknown_plan():
    out = run_agent_wrapper("What is the annual limit for Remedy 99?")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "supported plan" in out["message"] or "not supported" in out["message"]
