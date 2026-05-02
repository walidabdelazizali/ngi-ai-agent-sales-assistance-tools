from src.query.output_packaging import format_whatsapp_client_message

def test_whatsapp_client_message_summary():
    d = {"plan_name": "Remedy 04", "summary_text": "Annual limit: AED 1,000,000\nNetwork: Gold"}
    msg = format_whatsapp_client_message(d, "summary")
    assert msg.startswith("Hello,")
    assert "Remedy 04: Annual limit: AED 1,000,000" in msg
    assert msg.strip().endswith("proceed?")

def test_whatsapp_client_message_comparison():
    d = {"summary_text": "Annual limit: AED 500,000 | AED 1,000,000\nNetwork: Silver | Gold"}
    msg = format_whatsapp_client_message(d, "comparison")
    assert msg.startswith("Hello,")
    assert "Annual limit: AED 500,000 | AED 1,000,000" in msg
    assert msg.strip().endswith("proceed?")

def test_whatsapp_client_message_recommendation():
    d = {"plan_name": "Remedy 05", "recommendation": "Best for family coverage."}
    msg = format_whatsapp_client_message(d, "recommendation")
    assert msg.startswith("Hello,")
    assert "Our recommendation: Remedy 05 — Best for family coverage." in msg
    assert msg.strip().endswith("proceed?")

def test_whatsapp_client_message_str_input():
    s = "Comparison between Remedy 02 and Remedy 03: Annual limit: AED 500,000 | AED 1,000,000"
    msg = format_whatsapp_client_message(s, "comparison")
    assert msg.startswith("Hello,")
    assert "Comparison between Remedy 02 and Remedy 03" in msg

def test_whatsapp_client_message_invalid_mode():
    d = {"plan_name": "Remedy 04", "summary_text": "Annual limit: AED 1,000,000"}
    msg = format_whatsapp_client_message(d, "invalid")
    assert "not available" in msg

def test_whatsapp_client_message_no_leakage():
    d = {"plan_name": "Remedy 04", "summary_text": "Annual limit: AED 1,000,000", "_debug": "should not appear"}
    msg = format_whatsapp_client_message(d, "summary")
    assert "_debug" not in msg
    assert "{" not in msg and "}" not in msg and "[" not in msg and "]" not in msg
    assert "raw" not in msg.lower()
    assert "traceback" not in msg.lower()
from src.agent_adapter import handle_user_query

def test_plan_core_dict():
    out = handle_user_query("What is the annual limit for Remedy 04?", "dict")
    assert isinstance(out, dict)
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 04"
    assert out["tool_name"] == "get_plan_core"
    assert isinstance(out["data"], dict)
    assert "annual_limit" in out["data"]

def test_reimbursement_rules_dict():
    out = handle_user_query("What are the reimbursement rules for Remedy 05?", "dict")
    assert isinstance(out, dict)
    assert out["ok"] is True
    assert out["intent"] == "reimbursement_rules"
    assert out["plan_name"] == "Remedy 05"
    assert out["tool_name"] == "get_reimbursement_rules"
    assert isinstance(out["data"], dict)
    assert "reimbursement allowed" in out["message"].lower() or "تعويض" in out["message"]

def test_plan_summary_text():
    out = handle_user_query("Give me a summary of Remedy 04", "text")
    assert isinstance(out, str)
    assert "Remedy 04" in out or "summary" in out.lower()

def test_unsupported_query_dict():
    out = handle_user_query("Tell me about Remedy 99", "dict")
    assert isinstance(out, dict)
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["plan_name"] is None or out["plan_name"] == "Remedy 99"
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "not available" in out["message"].lower() or "غير متاحة" in out["message"]

def test_unsupported_query_text():
    out = handle_user_query("Tell me about Remedy 99", "text")
    assert isinstance(out, str)
    assert "not available" in out.lower() or "غير متاحة" in out

def test_invalid_output_mode():
    out = handle_user_query("What is the annual limit for Remedy 04?", "invalid")
    assert isinstance(out, dict)
    assert out["ok"] is False
    # Accept either plan_core or unsupported for intent
    assert out["intent"] in ("plan_core", "unsupported")
    # Accept None or Remedy 04 for plan_name
    assert out["plan_name"] is None or out["plan_name"] == "Remedy 04"
    assert out["tool_name"] is None or out["tool_name"] == "get_plan_core"
    assert out["data"] is None
    assert "invalid output_mode" in out["message"].lower() or "not available" in out["message"].lower() or "غير متاحة" in out["message"]

def test_regression_safe():
    # Should not crash or throw for any input/output_mode
    queries = [
        ("What is the annual limit for Remedy 04?", "dict"),
        ("What are the reimbursement rules for Remedy 05?", "dict"),
        ("Give me a summary of Remedy 04", "text"),
        ("Tell me about Remedy 99", "dict"),
        ("Tell me about Remedy 99", "text"),
        ("What is the annual limit for Remedy 04?", "invalid"),
    ]
    for q, mode in queries:
        out = handle_user_query(q, mode)
        assert out is not None
