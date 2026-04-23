import pytest
from src.v2_plan_loader import load_clean_plan
from src.v2_plan_normalizer import normalize_clean_plan
from src.v2_plan_compare import compare_two_plans

def get_norm(plan_name):
    raw = load_clean_plan(plan_name)
    return normalize_clean_plan(raw)

def test_specialist_access_difference():
    norm2 = get_norm("Remedy 02")
    norm5 = get_norm("Remedy 05")
    result = compare_two_plans(norm2, norm5)
    fields = [d["field"] for d in result["field_differences"]]
    assert "specialist_access_model" in fields
    assert any("specialist access" in s.lower() for s in result["summary_lines"])

def test_pharmacy_difference():
    norm2 = get_norm("Remedy 02")
    norm5 = get_norm("Remedy 05")
    result = compare_two_plans(norm2, norm5)
    fields = [d["field"] for d in result["field_differences"]]
    assert "pharmacy_limit_and_cost_share" in fields
    assert any("pharmacy" in s.lower() for s in result["summary_lines"])

def test_lab_radiology_pharmacy_outpatient_difference():
    norm2 = get_norm("Remedy 02")
    norm4 = get_norm("Remedy 04")
    result = compare_two_plans(norm2, norm4)
    fields = [d["field"] for d in result["field_differences"]]
    assert "laboratory_cost_share" in fields
    assert "radiology_cost_share" in fields
    assert "pharmacy_limit_and_cost_share" in fields
    assert any("lab" in s.lower() or "radiology" in s.lower() or "pharmacy" in s.lower() for s in result["summary_lines"])
    assert result["summary_lines"]

def test_no_identical_fields_in_differences():
    norm2 = get_norm("Remedy 02")
    norm4 = get_norm("Remedy 04")
    result = compare_two_plans(norm2, norm4)
    for d in result["field_differences"]:
        assert d["plan_a"] != d["plan_b"]

def test_summary_lines_not_empty_when_differences():
    norm2 = get_norm("Remedy 02")
    norm5 = get_norm("Remedy 05")
    result = compare_two_plans(norm2, norm5)
    assert result["summary_lines"]

def test_summary_lines_empty_when_no_differences():
    norm2 = get_norm("Remedy 02")
    result = compare_two_plans(norm2, norm2)
    assert result["summary_lines"] == ["Compared fields are the same."]
