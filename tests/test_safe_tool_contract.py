import pytest
from src.tool_contract import get_plan_core, get_plan_summary

def test_get_plan_core_blocks_invalid():
    # Simulate an unapproved/invalid plan (Remedy 99 is not approved)
    out = get_plan_core("Remedy 99")
    assert all(out[k] is None for k in ["plan_name", "plan_code", "network_name", "annual_limit", "area_of_coverage", "direct_billing", "referral_required", "maternity_cover"])

def test_get_plan_summary_blocks_invalid():
    out = get_plan_summary("Remedy 99")
    assert out["plan_name"] is None and out["summary_text"] is None

def test_get_plan_core_approved_remedy():
    out = get_plan_core("Remedy 03")
    assert out["plan_name"] == "NGI Healthnet –Remedy 03"
    assert out["plan_code"] is not None
    assert out["network_name"] is not None

def test_get_plan_summary_approved_remedy():
    out = get_plan_summary("Remedy 03")
    assert out["plan_name"] == "NGI Healthnet –Remedy 03"
    assert out["summary_text"] is not None

def test_get_plan_core_classic2():
    out = get_plan_core("Classic 2")
    assert out["plan_name"] is not None
    assert out["plan_code"] is not None

def test_get_plan_summary_classic2():
    out = get_plan_summary("Classic 2")
    assert out["plan_name"] is not None
    assert out["summary_text"] is not None
