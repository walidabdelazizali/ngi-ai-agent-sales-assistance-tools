from src.agent_wrapper import run_agent_wrapper


def test_recommendation_style_comparison_blocked_english():
    out = run_agent_wrapper("Which is better, Remedy 02 or Remedy 05?")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert "Recommendation-style plan selection is not supported" in out["message"]


def test_recommendation_style_comparison_blocked_arabic():
    out = run_agent_wrapper("أفضل خطة بين Remedy 02 و Remedy 05؟")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert "غير مدعوم" in out["message"] or "اختيار الخطة" in out["message"]


def test_factual_comparison_still_allowed():
    out = run_agent_wrapper("Compare Remedy 02 and Remedy 05")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert out["tool_name"] == "compare_plans"
    assert "Comparison between Remedy 02 and Remedy 05" in out["message"]
    assert "Recommendation:" not in out["message"]


def test_enhanced_baseline_unsupported_benefit_still_blocked():
    out = run_agent_wrapper("pharmacy Classic 2R")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
