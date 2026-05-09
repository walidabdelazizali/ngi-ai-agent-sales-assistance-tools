from src.agent_wrapper import run_agent_wrapper


def test_arabic_mixed_comparison_remedy():
    out = run_agent_wrapper("قارن بين Remedy 4 و Remedy 5")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert out["plan_name"] == "Remedy 04 vs Remedy 05"
    assert "Comparison between Remedy 04 and Remedy 05" in out["message"] or "مقارنة بين Remedy 04 و Remedy 05" in out["message"]


def test_arabic_comparison_classic():
    out = run_agent_wrapper("الفرق بين Classic 2 و Classic 3")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert out["plan_name"] == "Classic 2 vs Classic 3"
    assert "Comparison between Classic 2 and Classic 3" in out["message"] or "مقارنة بين Classic 2 و Classic 3" in out["message"]


def test_arabic_comparison_alias_phrase():
    out = run_agent_wrapper("مقارنة بين Remedy 04 و Remedy 05")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert out["plan_name"] == "Remedy 04 vs Remedy 05"


def test_arabic_core_annual_limit_classic3():
    out = run_agent_wrapper("ما هو الحد السنوي ل Classic 3")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Classic 3"
    assert "Annual limit: AED 250,000" in out["message"]


def test_arabic_mixed_referral_classic2():
    out = run_agent_wrapper("هل Classic 2 يحتاج referral")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Classic 2"
    assert "Referral required: No" in out["message"]


def test_unknown_plan_safe_failure_arabic_compare():
    out = run_agent_wrapper("قارن بين Remedy 4 و Plan X")
    assert out["ok"] is False
    assert out["intent"] == "plan_comparison"
    assert out["tool_name"] is None
    assert out["data"] is None
    assert "not supported" in out["message"].lower() or "يرجى تحديد خطتين مدعومتين" in out["message"]


def test_english_regression_comparison_still_works():
    out = run_agent_wrapper("Compare Remedy 04 and Remedy 05")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert out["plan_name"] == "Remedy 04 vs Remedy 05"
