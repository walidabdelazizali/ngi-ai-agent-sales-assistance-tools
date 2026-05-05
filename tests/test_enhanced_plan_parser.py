import pytest
from src.parsers.enhanced_plan_parser import parse_enhanced_plan, REQUIRED_FIELDS

def sample_table():
    # Simulated table as list of [label, value] rows
    return [
        ["Plan Name", "Classic Plan-2"],
        ["Provider Network", "HN Standard Plus"],
        ["Maximum Benefit Per Year", "AED 250,000"],
        ["Area of Coverage", "Worldwide Excluding USA and Canada"],
        ["Direct Billing Available", "Yes"],
        ["Claims Settlement", "Direct Billing Available"],
    ]

def test_parse_enhanced_plan_all_fields():
    table = sample_table()
    result = parse_enhanced_plan(table)
    # All required fields present
    for field in REQUIRED_FIELDS:
        assert field in result, f"Missing field: {field}"
        assert result[field] is not None, f"Field {field} is None"
    assert result["plan_name"] == "Classic 2"
    assert result["plan_code"] == "HN_CLASSIC_2"
    assert result["network_name"] == "Standard Plus"
    assert result["annual_limit"] == "AED 250,000"
    assert result["area_of_coverage"] == "Worldwide Excluding USA and Canada"
    assert result["direct_billing"] is True
    assert result["referral_required"] is False

def test_parse_enhanced_plan_missing_direct_billing():
    table = [
        ["Plan Name", "Classic Plan-2"],
        ["Provider Network", "HN Standard Plus"],
        ["Maximum Benefit Per Year", "AED 250,000"],
        ["Area of Coverage", "Worldwide Excluding USA and Canada"],
    ]
    result = parse_enhanced_plan(table)
    assert result["direct_billing"] is False

def test_parse_enhanced_plan_label_variants():
    table = [
        ["plan name", "Classic Plan-2"],
        ["provider network", "Standard Plus"],
        ["annual limit", "AED 250,000"],
        ["area of coverage", "Worldwide Excluding USA and Canada"],
        ["claims settlement", "Direct Billing available"],
    ]
    result = parse_enhanced_plan(table)
    assert result["plan_name"] == "Classic 2"
    assert result["network_name"] == "Standard Plus"
    assert result["direct_billing"] is True
