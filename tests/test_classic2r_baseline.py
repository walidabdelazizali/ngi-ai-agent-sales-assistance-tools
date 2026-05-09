"""
Regression tests for Classic 2R (HN_CLASSIC_2R) baseline plan.

Scope:
  - All 6 core field values from source_table_HN_CLASSIC_2R.json
  - End-to-end agent routing via run_agent_wrapper (plan_summary / plan_core)
  - Data dict field values returned in agent response
  - Arabic alias routing
  - Safe blocking of unsupported benefits (maternity, pharmacy, dental, optical)
"""
import pytest
from src.tool_contract import get_plan_core, get_plan_summary
from src.agent_wrapper import run_agent_wrapper

# ---------------------------------------------------------------------------
# Tool-contract level — core field values
# ---------------------------------------------------------------------------

def test_classic2r_core_network_name():
    core = get_plan_core("Classic 2R")
    assert core["network_name"] == "Standard Plus"


def test_classic2r_core_annual_limit():
    core = get_plan_core("Classic 2R")
    assert core["annual_limit"] == "AED 250,000"


def test_classic2r_core_area_of_coverage():
    core = get_plan_core("Classic 2R")
    assert core["area_of_coverage"] == "Worldwide Excluding USA and Canada"


def test_classic2r_core_direct_billing():
    core = get_plan_core("Classic 2R")
    assert core["direct_billing"] is True


def test_classic2r_core_referral_required():
    core = get_plan_core("Classic 2R")
    assert core["referral_required"] is False


def test_classic2r_summary_network_name():
    summary = get_plan_summary("Classic 2R")
    assert summary["network_name"] == "Standard Plus"


def test_classic2r_summary_area_of_coverage():
    summary = get_plan_summary("Classic 2R")
    assert summary["area_of_coverage"] == "Worldwide Excluding USA and Canada"


def test_classic2r_summary_direct_billing():
    summary = get_plan_summary("Classic 2R")
    assert summary["direct_billing"] is True


def test_classic2r_summary_referral_required():
    summary = get_plan_summary("Classic 2R")
    assert summary["referral_required"] is False


def test_classic2r_summary_text_contains_network():
    summary = get_plan_summary("Classic 2R")
    assert "Standard Plus" in summary.get("summary_text", "")


# ---------------------------------------------------------------------------
# End-to-end agent wrapper — data dict field values
# ---------------------------------------------------------------------------

def test_classic2r_agent_summary_data_fields():
    out = run_agent_wrapper("Summarize Classic 2R")
    assert out["ok"] is True
    assert out["intent"] == "plan_summary"
    data = out["data"]
    assert data["plan_name"] == "Classic 2R"
    assert data["plan_code"] == "HN_CLASSIC_2R"
    assert data["network_name"] == "Standard Plus"
    assert data["annual_limit"] == "AED 250,000"
    assert data["area_of_coverage"] == "Worldwide Excluding USA and Canada"
    assert data["direct_billing"] is True
    assert data["referral_required"] is False
    assert data["field_count"] == 7


def test_classic2r_agent_core_data_fields():
    out = run_agent_wrapper("classic 2r limit")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    data = out["data"]
    assert data["plan_name"] == "Classic 2R"
    assert data["plan_code"] == "HN_CLASSIC_2R"
    assert data["annual_limit"] == "AED 250,000"
    assert data["network_name"] == "Standard Plus"


# ---------------------------------------------------------------------------
# Arabic alias routing
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query", [
    "ملخص كلاسيك 2r",
    "شبكة كلاسيك 2r",
    "شبكة كلاسيك 2R",
])
def test_classic2r_arabic_alias_routes_correctly(query):
    out = run_agent_wrapper(query)
    assert out["ok"] is True
    assert out["plan_name"] == "Classic 2R"
    assert out["intent"] in ("plan_summary", "plan_core")


# ---------------------------------------------------------------------------
# Safe blocking — unsupported benefits must never expose data
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query", [
    "pharmacy Classic 2R",
    "maternity Classic 2R",
    "dental Classic 2R",
    "optical Classic 2R",
])
def test_classic2r_unsupported_benefits_blocked(query):
    out = run_agent_wrapper(query)
    # These benefits are not in the Classic 2R baseline scope.
    # The agent must return 'unsupported' intent — never expose internal data.
    assert out.get("intent") == "unsupported", (
        f"Expected intent='unsupported' for query '{query}', got '{out.get('intent')}'"
    )
