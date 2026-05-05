"""
Test for internal loader of HN_CLASSIC_2 (not customer-facing)
"""
import pytest
from src.tools.internal_loader_hn_classic_2 import load_internal_hn_classic_2
from src.schema.plan_schema import REQUIRED_FIELDS
from src.validation.plan_validator import validate_plan_ready

def test_internal_loader_hn_classic_2():
    plan = load_internal_hn_classic_2()
    # Required fields exist
    for field in REQUIRED_FIELDS:
        assert field in plan, f"Missing required field: {field}"
        assert plan[field] not in (None, ""), f"Empty value for field: {field}"
    # Validate plan ready
    ok, reason = validate_plan_ready(plan)
    assert ok, f"Plan not ready: {reason}"
    # Approval metadata
    assert plan["approval_status"] == "approved"
    assert plan["tests_passed"] is True
    # source_trace must be a dict per required field, all values point to correct file and field
    assert isinstance(plan["source_trace"], dict)
    for field, trace in plan["source_trace"].items():
        assert trace.startswith("data/plans/raw/HN_CLASSIC_2/source_table.json:"), f"Bad trace for {field}: {trace}"
        assert "output/" not in trace
    # Not customer-facing: plan_code must be HN_CLASSIC_2, not exposed in PLAN_DOCX_MAP
    assert plan["plan_code"] == "HN_CLASSIC_2"
