from src.agent_wrapper import run_agent_wrapper
from src.query.plan_network_lookup import resolve_plan_network
from src.query.plan_query import get_plan_field


def test_summarize_hn_prime_1():
    out = run_agent_wrapper("Summarize HN_PRIME_1")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Prime 1"
    assert out["data"]["plan_code"] == "HN_PRIME_1"


def test_summarize_prime_1():
    out = run_agent_wrapper("Summarize Prime 1")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["data"]["plan_name"] == "Prime 1"
    assert out["data"]["network_name"] == "Advantage Plus"


def test_summarize_classic_plan_1_alias():
    out = run_agent_wrapper("Summarize Classic Plan-1")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    assert out["plan_name"] == "Prime 1"
    assert out["data"]["plan_code"] == "HN_PRIME_1"


def test_network_lookup_prime_1_advantage_plus():
    out = run_agent_wrapper("What is the network for Prime 1?")
    assert out["ok"] is True
    assert out["intent"] in ("plan_core", "plan_field")
    assert out["data"]["network_name"] == "Advantage Plus"


def test_network_resolver_prime_1():
    result = resolve_plan_network("Prime 1")
    assert result["found"] is True
    assert result["medical_network"] == "hn_advantage_plus"


def test_annual_limit_lookup_prime_1():
    out = run_agent_wrapper("What is the annual limit for Prime 1?")
    assert out["ok"] is True
    assert out["intent"] in ("plan_core", "plan_field")
    assert out["data"]["annual_limit"] == "AED 300,000"


def test_maternity_extraction_prime_1():
    out = get_plan_field("Prime 1", "maternity_cover")
    assert out["ok"] is True
    assert "AED 15,000" in out["value"]


def test_pharmacy_extraction_prime_1():
    out = get_plan_field("Prime 1", "pharmacy_cover_summary")
    assert out["ok"] is True
    assert "AED 10,000" in out["value"]


def test_compare_prime_1_deterministic_boundary():
    out = run_agent_wrapper("Compare Prime 1 and Prime 2")
    assert out["intent"] == "plan_comparison"
    # Enhanced-only comparison remains safely blocked by current boundary.
    assert out["ok"] is False
    assert "not supported" in (out.get("message") or "").lower()


def test_prime_1_summary_no_internal_leakage():
    out = run_agent_wrapper("Summarize Prime 1")
    msg = (out.get("message") or "").lower()
    assert "source_trace" not in msg
    assert "approval_status" not in msg
    assert "tests_passed" not in msg
