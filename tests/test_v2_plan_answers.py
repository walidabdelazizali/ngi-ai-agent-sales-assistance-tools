
import pytest
from src.v2_plan_answers import answer_plan_core, answer_reimbursement, answer_plan_summary
from src.v2_plan_loader import load_clean_plan
from src.v2_plan_normalizer import normalize_clean_plan

def test_remedy_02_core_fields():
    raw = load_clean_plan("Remedy 02")
    norm = normalize_clean_plan(raw)
    core = answer_plan_core(norm)
    assert core["specialist_access_model"].lower() == "referral"
    assert core["annual_limit"] is not None
    assert core["pharmacy_limit_and_cost_share"] is not None
    assert None not in core.values()

def test_remedy_05_core_fields():
    raw = load_clean_plan("Remedy 05")
    norm = normalize_clean_plan(raw)
    core = answer_plan_core(norm)
    assert core["specialist_access_model"].lower() == "direct"
    assert core["annual_limit"] is not None
    assert core["pharmacy_limit_and_cost_share"] is not None
    assert None not in core.values()

def test_all_summary_and_fields():
    for plan_name in ["Remedy 02", "Remedy 04", "Remedy 05"]:
        raw = load_clean_plan(plan_name)
        norm = normalize_clean_plan(raw)
        summary = answer_plan_summary(norm)
        assert summary["plan_name"]
        assert summary["summary_lines"]
        assert isinstance(summary["summary_lines"], list)
        assert len(summary["summary_lines"]) > 0
        assert None not in summary["summary_lines"]
        core = answer_plan_core(norm)
        assert core["annual_limit"] is not None
        assert core["pharmacy_limit_and_cost_share"] is not None
        assert None not in core.values()
        reimb = answer_reimbursement(norm)
        assert None not in reimb.values()
