from src.agent_wrapper import run_agent_wrapper


def test_arabic_pharmacy_limit_query_classic1r_routes_plan_field():
    out = run_agent_wrapper("حد الصيدلية Classic 1R")
    assert out["ok"] is True
    assert out["intent"] == "plan_field"
    assert out["plan_name"] == "Classic 1R"
    assert "Pharmacy Cover" in out["message"]


def test_arabic_maternity_query_classic1r_routes_plan_field():
    out = run_agent_wrapper("الولادة Classic 1R")
    assert out["ok"] is True
    assert out["intent"] == "plan_field"
    assert out["plan_name"] == "Classic 1R"
    assert "Maternity Cover" in out["message"]


def test_arabic_network_query_classic1r_routes_plan_field():
    out = run_agent_wrapper("شبكة Classic 1R")
    assert out["ok"] is True
    assert out["intent"] == "plan_field"
    assert out["plan_name"] == "Classic 1R"
    assert "Network:" in out["message"]


def test_mixed_shorthand_provider_listing_remedy5_dubai():
    out = run_agent_wrapper("remedy 5 hospitals dubai")
    assert out["ok"] is True
    assert out["intent"] == "plan_network_city_type"
    assert out["plan_name"] == "Remedy 05"
    assert "[PROVIDER LIST]" in out["message"]


def test_arabic_provider_listing_without_city_gets_safe_clarification():
    out = run_agent_wrapper("مستشفيات remedy 6")
    assert out["ok"] is False
    assert out["intent"] == "plan_network_city_type"
    assert out["plan_name"] == "Remedy 06"
    assert "City is unknown" in out["message"]


def test_unsupported_arabic_recommendation_comparison_is_blocked():
    out = run_agent_wrapper("ايه افضل classic 1r ولا classic 3")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
    assert out["tool_name"] is None
