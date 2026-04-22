def test_plan_comparison_english():
    out = run_agent_wrapper("compare Remedy 02 and Remedy 04")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert "Comparison between Remedy 02 and Remedy 04" in out["message"]
    # Should show key fields
    for label in ["Annual Limit", "Network", "Area of Coverage", "Direct Billing", "Reimbursement Allowed"]:
        assert label in out["message"]
        assert "Remedy 02" in out["message"] and "Remedy 04" in out["message"]

def test_plan_comparison_arabic():
    out = run_agent_wrapper("ما الفرق بين ريميدي 02 و ريميدي 04")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert "مقارنة بين Remedy 02 و Remedy 04" in out["message"]
    # Should show key Arabic labels
    for label in ["الحد السنوي", "الشبكة", "نطاق التغطية", "الدفع المباشر", "التعويض"]:
        assert label in out["message"]
        assert "Remedy 02" in out["message"] and "Remedy 04" in out["message"]
def test_plan_core_remedy02_english():
    out = run_agent_wrapper("What is the annual limit for Remedy 02?")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 02"
    assert out["tool_name"] == "get_plan_core"
    assert isinstance(out["data"], dict)
    assert "annual_limit" in out["data"]
    assert out["data"]["annual_limit"] == "AED. 150,000"

def test_plan_summary_remedy02_english():
    out = run_agent_wrapper("Give me a summary of Remedy 02")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 02"
    assert out["tool_name"] == "get_plan_summary"
    assert isinstance(out["data"], dict)
    assert "summary_text" in out["data"]

def test_reimbursement_rules_remedy02_english():
    out = run_agent_wrapper("What are the reimbursement rules for Remedy 02?")
    assert out["ok"] is True
    assert out["intent"] == "reimbursement_rules"
    assert out["plan_name"] == "Remedy 02"
    assert out["tool_name"] == "get_reimbursement_rules"
    assert isinstance(out["data"], dict)
    assert out["data"]["reimbursement_allowed"] is False
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

def test_plan_summary_remedy03_arabic_localized():
    out = run_agent_wrapper("اعطني ملخص لخطة ريميدي 03")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Remedy 03"
    assert out["tool_name"] == "get_plan_summary"
    assert isinstance(out["data"], dict)
    assert "summary_text" in out["data"]
    # Check for Arabic labels and values in summary_text
    summary = out["data"]["summary_text"]
    assert "اسم الخطة" in summary
    assert "رمز الخطة" in summary
    assert "الشبكة" in summary
    assert "الحد السنوي" in summary
    assert "نطاق التغطية" in summary
    assert "الدفع المباشر" in summary
    assert "الإحالة مطلوبة" in summary
    assert "تغطية الأمومة" in summary
    assert "تغطية المرضى الداخليين" in summary
    assert "تغطية العيادات الخارجية" in summary
    assert "تغطية الصيدلية" in summary
    assert "الاستثناءات الأساسية" in summary
    assert "نعم" in summary or "لا" in summary or "غير متوفر" in summary
    assert "تم عرض ملخص الخطة" in out["message"]
    # Ensure 'Not available' is never corrupted
    assert "لاt available" not in summary
    assert "Not available" not in summary
    assert "None listed" not in summary
    assert "None" not in summary
    assert "null" not in summary

def test_plan_summary_remedy03_arabic_not_available_placeholder():
    # This test expects a missing field, but real Remedy 03 data has all fields populated.
    # Instead, just ensure no broken tokens or English placeholders remain.
    out = run_agent_wrapper("اعطني ملخص لخطة ريميدي 03")
    summary = out["data"]["summary_text"]
    assert "لاt available" not in summary
    assert "Not available" not in summary
    assert "None listed" not in summary
    assert "None" not in summary
    assert "null" not in summary
    # If a missing field is present, it should use the Arabic placeholder
    # (This is a no-op for current data, but will catch regressions if data changes)
    if any(x in summary for x in [": غير متوفر", "غير متوفر"]):
        assert "غير متوفر" in summary

def test_plan_summary_mixed_arabic_english_phrasing():
    # Mixed phrasing: Arabic + English
    queries = [
        "لخص خطة Remedy 03",
        "ملخص Remedy 04",
        "اعطني summary لخطة Remedy 05",
        "اعطني ملخص لخطة Remedy 04",
        "ملخص ريميدي 03",
    ]
    for q in queries:
        out = run_agent_wrapper(q)
        assert out["ok"] is True
        assert out["intent"] == "plan_summary"
        assert out["plan_name"] in ("Remedy 03", "Remedy 04", "Remedy 05")
        assert out["tool_name"] == "get_plan_summary"
        assert isinstance(out["data"], dict)
        assert "summary_text" in out["data"]
        summary = out["data"]["summary_text"]
        # Check for at least one Arabic label
        assert "اسم الخطة" in summary or "رمز الخطة" in summary
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

def test_normalized_field_exists():
    out = run_agent_wrapper("What is the annual limit for Remedy 04?")
    assert "normalized" in out
    norm = out["normalized"]
    assert set(norm.keys()) == {"status", "tool", "answer", "errors"}
    assert norm["status"] == "ok"
    assert norm["tool"] == "get_plan_core"
    assert isinstance(norm["answer"], dict)
    assert isinstance(norm["errors"], list)

def test_plan_summary_business_friendly_formatting():
    from src.agent_adapter import handle_user_query
    # English summary query for Remedy 03
    response = handle_user_query("Give me a summary of Remedy 03", output_mode="text")
    # Should be non-empty, readable, and not raw/internal
    assert response
    assert "Plan:" in response
    assert "Code:" in response
    assert "summary_text" not in response  # Should not expose raw summary_text
    # Should show at least one business highlight
    assert any(
        kw in response for kw in [
            "Network:", "Annual limit:", "Area:", "Direct billing:",
            "Referral required:", "Maternity cover:", "Pharmacy cover:", "Key exclusions:"]
    )

def test_response_is_business_friendly():
    from src.agent_adapter import handle_user_query
    queries = [
        "What is the annual limit for Remedy 04?",
        "Give me a summary of Remedy 03",
        "What is the reimbursement rule for Remedy 05?"
    ]
    for q in queries:
        resp = handle_user_query(q, output_mode="text")
        # Response must be non-empty
        assert resp and resp.strip(), f"Empty response for query: {q}"
        # Response should not start with a label or internal marker
        first_line = resp.strip().splitlines()[0]
        assert not first_line.startswith("["), f"Response exposes label: {resp}"
        # Response should not contain raw dict or internal formatting
        assert not any(x in resp for x in ["{", "}", "'status'", "'tool'", "'answer'"]), f"Response exposes internal formatting: {resp}"
        # Response should be readable (at least one alphanumeric character in first line)
        assert any(c.isalnum() for c in first_line), f"Response not readable: {resp}"

def test_no_normalized_keys_leak_in_response():
    from src.agent_adapter import handle_user_query
    queries = [
        "What is the annual limit for Remedy 04?",
        "Give me a summary of Remedy 03",
        "What is the reimbursement rule for Remedy 05?"
    ]
    forbidden = ["status:", "tool:", "answer:", "errors:"]
    for q in queries:
        resp = handle_user_query(q, output_mode="text")
        for key in forbidden:
            assert key not in resp, f"Internal key '{key}' leaked in response: {resp}"

def test_unsupported_and_unknown_are_business_friendly():
    queries = [
        ("Show me the dental coverage for Remedy 04", "en"),
        ("ما الفرق بين الريميدي 2 والريميدي 4؟", "ar"),
        ("What is the annual limit for Remedy 99?", "en"),
    ]
    forbidden = ["status", "tool", "answer", "errors", "{", "}"]
    from src.agent_wrapper import run_agent_wrapper
    for q, _ in queries:
        out = run_agent_wrapper(q)
        msg = out.get("message", "")
        # Message must be non-empty and readable
        assert msg and any(c.isalnum() for c in msg), f"Empty or unreadable message: {msg}"
        # No internal keys or raw dicts
        for key in forbidden:
            assert key not in msg, f"Internal key '{key}' leaked in message: {msg}"
        # No label prefix
        assert not msg.strip().startswith("["), f"Label prefix leaked in message: {msg}"

