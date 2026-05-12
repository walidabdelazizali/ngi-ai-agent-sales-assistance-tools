from src.agent_wrapper import run_agent_wrapper
from src.query.plan_network_lookup import resolve_plan_network
from src.query.plan_query import get_plan_field


def test_summarize_hn_classic_4():
    out = run_agent_wrapper("Summarize HN_CLASSIC_4")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Classic 4"
    assert out["data"]["plan_code"] == "HN_CLASSIC_4"


def test_summarize_classic_4():
    out = run_agent_wrapper("Summarize Classic 4")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["data"]["network_name"] == "Basic Plus"
    assert out["data"]["annual_limit"] == "AED 150,000"


def test_summarize_classic_plan_4_alias():
    out = run_agent_wrapper("Summarize Classic Plan-4")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Classic 4"
    assert out["data"]["plan_code"] == "HN_CLASSIC_4"


def test_network_lookup_classic_4_basic_plus():
    out = run_agent_wrapper("What is the network for Classic 4?")
    assert out["ok"] is True
    assert out["intent"] in ("plan_core", "plan_field")
    assert out["data"]["network_name"] == "Basic Plus"


def test_network_resolver_classic_4():
    result = resolve_plan_network("Classic 4")
    assert result["found"] is True
    assert result["medical_network"] == "hn_basic_plus"


def test_annual_limit_lookup_classic_4():
    out = run_agent_wrapper("What is the annual limit for Classic 4?")
    assert out["ok"] is True
    assert out["intent"] in ("plan_core", "plan_field")
    assert out["data"]["annual_limit"] == "AED 150,000"


def test_area_of_coverage_lookup_classic_4():
    out = run_agent_wrapper("What is the area of coverage for Classic 4?")
    assert out["ok"] is True
    assert out["intent"] in ("plan_core", "plan_field")
    assert out["data"]["area_of_coverage"] == "UAE + Home Country"
    assert "worldwide" not in out["data"]["area_of_coverage"].lower()


def test_maternity_extraction_classic_4():
    out = get_plan_field("Classic 4", "maternity_cover")
    assert out["ok"] is True
    assert "AED 10,000" in out["value"]


def test_pharmacy_extraction_classic_4():
    out = get_plan_field("Classic 4", "pharmacy_cover_summary")
    assert out["ok"] is True
    assert "AED 10,000" in out["value"]


def test_classic_4_summary_no_internal_leakage():
    out = run_agent_wrapper("Summarize Classic 4")
    msg = (out.get("message") or "").lower()
    assert "source_trace" not in msg
    assert "approval_status" not in msg
    assert "tests_passed" not in msg


def test_comparison_boundary_classic_4_with_prime_1():
    out = run_agent_wrapper("Compare Classic 4 and Prime 1")
    assert out["intent"] == "plan_comparison"
    assert out["ok"] is False
    assert "not supported" in (out.get("message") or "").lower()


def test_comparison_boundary_classic_4_with_classic_2():
    out = run_agent_wrapper("Compare Classic 4 and Classic 2")
    assert out["intent"] == "plan_comparison"
    assert out["ok"] is False
    assert "not supported" in (out.get("message") or "").lower()


def test_comparison_boundary_classic_4_with_classic_3():
    out = run_agent_wrapper("Compare Classic 4 and Classic 3")
    assert out["intent"] == "plan_comparison"
    assert out["ok"] is False
    assert "not supported" in (out.get("message") or "").lower()
