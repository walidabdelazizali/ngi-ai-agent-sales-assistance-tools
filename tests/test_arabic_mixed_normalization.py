from src.agent_wrapper import run_agent_wrapper


def test_classic_number_spacing_variants():
    for q in [
        "classic2 referral?",
        "classic 2 referral",
        "كلاسيك٢ ريفرال",
        "كلاسيك ٢ ريفرال",
    ]:
        out = run_agent_wrapper(q)
        assert out["ok"] is True
        assert out["intent"] == "plan_core"
        assert out["plan_name"] == "Classic 2"


def test_mixed_direct_billing_query_routes_core():
    out = run_agent_wrapper("direct billing في classic 3")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Classic 3"


def test_arabic_shorthand_limit_normalization():
    out = run_agent_wrapper("ليمت كلاسيك 2R")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Classic 2R"
    assert "Annual limit" in out["message"]


def test_network_arabic_basic_plus_phrase():
    out = run_agent_wrapper("هل ACCURACY PLUS MEDICAL LABORATORY في بيسك بلس؟")
    assert out["intent"] == "network_lookup"
    assert out["tool_name"] == "network_lookup"


def test_network_arabic_shorthand_provider_alias():
    out = run_agent_wrapper("هل برجيل ابوظبي داخل الشبكة؟")
    assert out["intent"] == "network_lookup"
    assert out["tool_name"] == "network_lookup"


def test_network_city_type_shorthand_queries():
    for q in ["show hospitals in sharjah", "عيادات في دبي", "هاتلي مستشفيات في الشارقة"]:
        out = run_agent_wrapper(q)
        assert out["intent"] in ("network_lookup", "plan_network_city_type")


def test_blocked_comparison_still_blocked():
    out = run_agent_wrapper("compare all plans")
    assert out["ok"] is False
    assert out["intent"] in ("unsupported", "plan_comparison")
