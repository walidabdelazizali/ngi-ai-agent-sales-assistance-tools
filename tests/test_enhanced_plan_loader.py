import pytest
from src.tools.enhanced_plan_loader import (
    is_enhanced_plan, resolve_enhanced_plan_name, load_enhanced_plan
)
from src.tools.internal_loader_hn_classic_2 import load_internal_hn_classic_2
from src.tool_contract import get_plan_core, get_plan_summary
from src.query.plan_query import load_plan

def test_is_enhanced_plan_classic2():
    assert is_enhanced_plan("Classic 2")
    assert is_enhanced_plan("hn_classic_2")
    assert is_enhanced_plan("hn classic 2")
    assert is_enhanced_plan("Classic 3")
    assert is_enhanced_plan("hn_classic_3")
    assert is_enhanced_plan("hn classic 3")
    assert not is_enhanced_plan("Remedy 03")

def test_resolve_enhanced_plan_name_aliases():
    assert resolve_enhanced_plan_name("Classic 2") == "Classic 2"
    assert resolve_enhanced_plan_name("hn_classic_2") == "Classic 2"
    assert resolve_enhanced_plan_name("hn classic 2") == "Classic 2"
    assert resolve_enhanced_plan_name("Classic 3") == "Classic 3"
    assert resolve_enhanced_plan_name("hn_classic_3") == "Classic 3"
    assert resolve_enhanced_plan_name("hn classic 3") == "Classic 3"
    assert resolve_enhanced_plan_name("Remedy 03") is None

def test_load_enhanced_plan_classic2():
    plan = load_enhanced_plan("Classic 2")
    assert plan["plan_name"] == "Classic 2"
    assert plan["plan_code"] == "HN_CLASSIC_2"
    assert plan["approval_status"] == "approved"
    assert plan["tests_passed"] is True
    assert isinstance(plan["source_trace"], dict)
    assert plan["network_name"]
    assert plan["annual_limit"]
    assert plan["area_of_coverage"]
    assert plan["direct_billing"] is not None
    assert plan["referral_required"] is not None

def test_load_enhanced_plan_classic3():
    plan = load_enhanced_plan("Classic 3")
    assert plan["plan_name"] == "Classic 3"
    assert plan["plan_code"] == "HN_CLASSIC_3"
    assert plan["approval_status"] == "approved"
    assert plan["tests_passed"] is True
    assert isinstance(plan["source_trace"], dict)
    assert plan["network_name"] == "Standard"
    assert plan["annual_limit"] == "AED 250,000"
    assert plan["area_of_coverage"] == "UAE+Home country"
    assert plan["direct_billing"] is True
    assert plan["referral_required"] is False

def test_load_internal_loader_hn_classic_2():
    plan = load_internal_hn_classic_2()
    assert plan["plan_name"] == "Classic 2"
    assert plan["plan_code"] == "HN_CLASSIC_2"
    assert plan["approval_status"] == "approved"
    assert plan["tests_passed"] is True
    assert isinstance(plan["source_trace"], dict)

def test_tool_contract_classic2_no_leak():
    core = get_plan_core("Classic 2")
    summary = get_plan_summary("Classic 2")
    forbidden = ["approval_status", "tests_passed", "source_trace"]
    for k in forbidden:
        assert k not in core
        assert k not in summary
    assert core["plan_name"] == "Classic 2"
    assert summary["plan_name"] == "Classic 2"

def test_load_plan_classic3_uses_enhanced_loader():
    plan = load_plan("Classic 3")
    assert plan["plan_name"] == "Classic 3"
    assert plan["plan_code"] == "HN_CLASSIC_3"
    assert plan["approval_status"] == "approved"
    for field, trace in plan["source_trace"].items():
        assert trace.startswith("data/plans/raw/HN_CLASSIC_3/source_table.json:")
        assert "output/" not in trace

def test_tool_contract_classic3_core_and_summary_no_leak():
    core = get_plan_core("Classic 3")
    summary = get_plan_summary("Classic 3")
    forbidden = ["approval_status", "tests_passed", "source_trace"]
    for k in forbidden:
        assert k not in core
        assert k not in summary
    assert core["plan_name"] == "Classic 3"
    assert core["plan_code"] == "HN_CLASSIC_3"
    assert core["network_name"] == "Standard"
    assert summary["plan_name"] == "Classic 3"
    assert summary["plan_code"] == "HN_CLASSIC_3"
    assert summary["network_name"] == "Standard"
    assert summary["summary_text"]

def test_classic3_benefit_extraction_contract_values():
    core = get_plan_core("Classic 3")
    summary = get_plan_summary("Classic 3")

    assert core["annual_limit"] == "AED 250,000"
    assert core["network_name"] == "Standard"
    assert core["area_of_coverage"] == "UAE+Home country"
    assert core["direct_billing"] is True
    assert core["referral_required"] is False

    # Stabilization guard: do not synthesize missing maternity normalization.
    assert core.get("maternity_cover") is None
    assert "maternity_cover" not in summary
    assert "pharmacy_cover_summary" not in core
    assert "physiotherapy_cover_summary" not in core

def test_classic3_summary_output_no_duplicate_core_labels():
    summary = get_plan_summary("Classic 3")
    text = summary["summary_text"]
    assert text
    assert text.count("Plan:") == 1
    assert text.count("Code:") == 1
    assert text.count("Network:") == 1
    assert text.count("Annual limit:") == 1
    assert text.count("Area:") == 1
    assert text.count("Direct billing:") == 1
    assert text.count("Referral required:") == 1
