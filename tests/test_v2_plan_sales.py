import pytest
from src.v2_plan_loader import load_clean_plan
from src.v2_plan_normalizer import normalize_clean_plan
from src.v2_plan_compare import compare_two_plans
from src.v2_plan_sales import build_plan_sales_summary, build_plan_upgrade_pitch, build_plan_difference_pitch

def get_norm(plan_name):
    raw = load_clean_plan(plan_name)
    return normalize_clean_plan(raw)

def test_sales_summary_headline_and_lines():
    for plan_name in ["Remedy 02", "Remedy 04", "Remedy 05"]:
        norm = get_norm(plan_name)
        result = build_plan_sales_summary(norm)
        assert result["headline"].strip() != ""
        assert result["sales_lines"]
        assert all(isinstance(line, str) and line.strip() for line in result["sales_lines"])

def test_sales_summary_mentions():
    norm5 = get_norm("Remedy 05")
    norm4 = get_norm("Remedy 04")
    res5 = build_plan_sales_summary(norm5)
    res4 = build_plan_sales_summary(norm4)
    assert any("direct specialist access" in l.lower() for l in res5["sales_lines"])
    assert any("no lab or radiology co-pay" in l.lower() for l in res4["sales_lines"])

def test_upgrade_pitch_lines():
    norm2 = get_norm("Remedy 02")
    norm4 = get_norm("Remedy 04")
    norm5 = get_norm("Remedy 05")
    up_2_5 = build_plan_upgrade_pitch(norm2, norm5)
    up_2_4 = build_plan_upgrade_pitch(norm2, norm4)
    up_4_5 = build_plan_upgrade_pitch(norm4, norm5)
    assert any("direct specialist access" in l.lower() for l in up_2_5["upgrade_lines"])
    assert any("pharmacy" in l.lower() for l in up_2_5["upgrade_lines"])
    assert up_2_5["headline"] and up_2_5["upgrade_lines"]
    assert up_2_4["headline"] and up_2_4["upgrade_lines"]
    assert up_4_5["headline"] and up_4_5["upgrade_lines"]

def test_difference_pitch_lines():
    norm2 = get_norm("Remedy 02")
    norm4 = get_norm("Remedy 04")
    norm5 = get_norm("Remedy 05")
    cmp_2_4 = compare_two_plans(norm2, norm4)
    cmp_2_5 = compare_two_plans(norm2, norm5)
    cmp_4_5 = compare_two_plans(norm4, norm5)
    diff_2_4 = build_plan_difference_pitch(cmp_2_4)
    diff_2_5 = build_plan_difference_pitch(cmp_2_5)
    diff_4_5 = build_plan_difference_pitch(cmp_4_5)
    for diff in [diff_2_4, diff_2_5, diff_4_5]:
        assert diff["headline"]
        assert diff["pitch_lines"]
        assert all(isinstance(line, str) and line.strip() for line in diff["pitch_lines"])
        # No raw field names
        forbidden = ["specialist_access_model", "pharmacy_limit_and_cost_share", "laboratory_cost_share", "radiology_cost_share"]
        for f in forbidden:
            assert not any(f in l for l in diff["pitch_lines"])


def test_remedy_03_06_expansion():
    from src.v2_plan_loader import load_clean_plan
    from src.v2_plan_normalizer import normalize_clean_plan
    from src.v2_plan_answers import answer_plan_core
    from src.v2_plan_compare import compare_two_plans
    from src.v2_plan_sales import build_plan_sales_summary, build_plan_upgrade_pitch, build_plan_difference_pitch
    norm3 = normalize_clean_plan(load_clean_plan("Remedy 03"))
    norm6 = normalize_clean_plan(load_clean_plan("Remedy 06"))
    # Remedy 03 assertions
    assert norm3["specialist_access_model"] == "referral"
    assert "5,000" in norm3["pharmacy_limit_and_cost_share"]
    assert "20%" in norm3["pharmacy_limit_and_cost_share"]
    # Remedy 06 assertions
    assert norm6["specialist_access_model"] == "direct"
    assert "20 sessions" in norm6["physiotherapy_limit_and_cost_share"].lower()
    assert "nil" in norm6["physiotherapy_limit_and_cost_share"].lower()
    assert "10,000" in norm6["pharmacy_limit_and_cost_share"]
    assert "20%" in norm6["pharmacy_limit_and_cost_share"]
    # Sales summary outputs
    sales3 = build_plan_sales_summary(norm3)
    sales6 = build_plan_sales_summary(norm6)
    assert sales3["headline"] and sales3["sales_lines"]
    assert sales6["headline"] and sales6["sales_lines"]
    # Compare and sales mode outputs
    norm5 = normalize_clean_plan(load_clean_plan("Remedy 05"))
    cmp_3_5 = compare_two_plans(norm3, norm5)
    cmp_5_6 = compare_two_plans(norm5, norm6)
    diff_3_5 = build_plan_difference_pitch(cmp_3_5)
    diff_5_6 = build_plan_difference_pitch(cmp_5_6)
    assert diff_3_5["headline"] and diff_3_5["pitch_lines"]
    assert diff_5_6["headline"] and diff_5_6["pitch_lines"]
