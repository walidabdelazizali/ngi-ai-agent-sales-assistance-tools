"""Tests for the owner-facing query and comparison layer.

Covers:
- Single-field retrieval for both plans
- Full and filtered comparison
- Summary generation
- Deterministic intent routing via answer_owner_query
- Safe fallback for unsupported queries
- Regression: existing parser/comparator behavior unchanged
"""

import json
from pathlib import Path

import pytest

from src.query.plan_query import (
    answer_owner_query,
    clear_cache,
    compare_plans,
    get_plan_field,
    load_plan,
    summarize_plan,
    available_plans,
    OWNER_FIELDS,
    _SAFE_FALLBACK,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_OUTPUT = Path(__file__).parent.parent / "output"


@pytest.fixture(autouse=True)
def _clear():
    """Clear plan cache between tests."""
    clear_cache()
    yield
    clear_cache()


def _skip_if_missing(name: str):
    path = _OUTPUT / name
    if not path.exists():
        pytest.skip(f"{name} not found")


@pytest.fixture
def r02():
    _skip_if_missing("HN-REMEDY-2.json")
    return load_plan("Remedy 02")


@pytest.fixture
def r03():
    _skip_if_missing("HN-REMEDY-3.json")
    return load_plan("Remedy 03")


# ===================================================================
# Plan loading
# ===================================================================


class TestPlanLoading:

    def test_load_remedy_02(self, r02):
        assert r02["plan_code"] == "HN-REMEDY-2"

    def test_load_remedy_03(self, r03):
        assert r03["plan_code"] == "HN-REMEDY-3"

    def test_load_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown plan"):
            load_plan("Remedy 99")

    def test_alias_case_insensitive(self):
        _skip_if_missing("HN-REMEDY-2.json")
        p = load_plan("REMEDY 02")
        assert p["plan_code"] == "HN-REMEDY-2"

    def test_alias_no_space(self):
        _skip_if_missing("HN-REMEDY-3.json")
        p = load_plan("remedy3")
        assert p["plan_code"] == "HN-REMEDY-3"

    def test_available_plans(self):
        plans = available_plans()
        assert "HN-REMEDY-2.json" in plans
        assert "HN-REMEDY-3.json" in plans


# ===================================================================
# Single-field retrieval
# ===================================================================


class TestGetPlanField:

    def test_annual_limit_r03(self, r03):
        result = get_plan_field("Remedy 03", "annual limit")
        assert result["field"] == "annual_limit"
        assert "150,000" in result["formatted"]

    def test_annual_limit_r02(self, r02):
        result = get_plan_field("Remedy 02", "annual_limit")
        assert "150,000" in result["formatted"]

    def test_network_name_r03(self, r03):
        result = get_plan_field("Remedy 03", "network")
        assert "HN Basic Plus" in result["formatted"]

    def test_maternity_r02(self, r02):
        result = get_plan_field("Remedy 02", "maternity")
        assert result["value"] is not None

    def test_direct_billing_bool(self, r03):
        result = get_plan_field("Remedy 03", "direct billing")
        assert result["value"] is True
        assert result["formatted"] == "Yes"

    def test_reimbursement_bool(self, r02):
        result = get_plan_field("Remedy 02", "reimbursement")
        assert result["value"] is False
        assert result["formatted"] == "No"

    def test_referral_required(self, r03):
        result = get_plan_field("Remedy 03", "referral")
        assert result["value"] is True

    def test_pharmacy_r03(self, r03):
        result = get_plan_field("Remedy 03", "pharmacy")
        assert "5,000" in result["formatted"]
        assert "20%" in result["formatted"]

    def test_outpatient_r02(self, r02):
        result = get_plan_field("Remedy 02", "outpatient")
        assert "15%" in result["formatted"]

    def test_diagnostics_r03(self, r03):
        result = get_plan_field("Remedy 03", "diagnostics")
        assert "10%" in result["formatted"]

    def test_physiotherapy_r03(self, r03):
        result = get_plan_field("Remedy 03", "physio")
        assert "10%" in result["formatted"]
        assert "12 sessions" in result["formatted"]

    def test_pre_existing_rule(self, r03):
        result = get_plan_field("Remedy 03", "pre-existing")
        assert "6 months" in result["formatted"]

    def test_outside_network_rule(self, r02):
        result = get_plan_field("Remedy 02", "outside network")
        assert result["value"] is not None

    def test_outside_uae_rule(self, r03):
        result = get_plan_field("Remedy 03", "outside uae")
        assert result["value"] is not None

    def test_exclusions_r03(self, r03):
        result = get_plan_field("Remedy 03", "exclusions")
        assert isinstance(result["value"], list)
        assert len(result["value"]) > 10

    def test_unknown_field_fallback(self, r02):
        result = get_plan_field("Remedy 02", "nonsense_field_xyz")
        assert result["formatted"] == _SAFE_FALLBACK

    def test_plan_code_field(self, r03):
        result = get_plan_field("Remedy 03", "plan code")
        assert result["value"] == "HN-REMEDY-3"

    def test_plan_name_field(self, r02):
        result = get_plan_field("Remedy 02", "plan name")
        assert "Remedy" in result["value"]


# ===================================================================
# Comparison
# ===================================================================


class TestComparePlans:

    def test_full_compare_structure(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03")
        assert result["plan_a_code"] == "HN-REMEDY-2"
        assert result["plan_b_code"] == "HN-REMEDY-3"
        assert "matched" in result
        assert "differing" in result

    def test_known_matching_fields(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03")
        matched_fields = [m["field"] for m in result["matched"]]
        assert "network_name" in matched_fields
        assert "direct_billing" in matched_fields
        assert "referral_required" in matched_fields

    def test_known_differing_fields(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03")
        assert "plan_code" in result["differing"]
        assert "plan_name" in result["differing"]
        assert "outpatient_cover_summary" in result["differing"]
        assert "pharmacy_cover_summary" in result["differing"]

    def test_single_field_compare_matching(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03",
                               field_name="network")
        assert result["match"] is True
        assert "HN Basic Plus" in result["plan_a_formatted"]

    def test_single_field_compare_differing(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03",
                               field_name="outpatient")
        assert result["match"] is False
        assert "15%" in result["plan_a_formatted"]
        assert "10%" in result["plan_b_formatted"]

    def test_pharmacy_field_compare(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03",
                               field_name="pharmacy")
        assert result["match"] is False
        assert "3,000" in result["plan_a_formatted"]
        assert "5,000" in result["plan_b_formatted"]

    def test_differences_only(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03",
                               differences_only=True)
        assert result["differences_only"] is True
        assert "plan_code" in result["differing"]
        assert "matched" not in result

    def test_unknown_field_compare_fallback(self, r02, r03):
        result = compare_plans("Remedy 02", "Remedy 03",
                               field_name="nonsense_xyz")
        assert "error" in result
        assert result["error"] == _SAFE_FALLBACK

    def test_identical_plan_no_diff(self, r02):
        result = compare_plans("Remedy 02", "Remedy 02")
        assert result["differing"] == {}


# ===================================================================
# Summary
# ===================================================================


class TestSummarizePlan:

    def test_r02_summary(self, r02):
        result = summarize_plan("Remedy 02")
        assert result["plan_code"] == "HN-REMEDY-2"
        assert "150,000" in result["summary_text"]
        assert "HN Basic Plus" in result["summary_text"]

    def test_r03_summary(self, r03):
        result = summarize_plan("Remedy 03")
        assert result["plan_code"] == "HN-REMEDY-3"
        assert "150,000" in result["summary_text"]

    def test_summary_has_key_fields(self, r03):
        result = summarize_plan("Remedy 03")
        text = result["summary_text"]
        assert "Plan Name:" in text
        assert "Annual Limit:" in text
        assert "Network:" in text
        assert "Direct Billing:" in text
        assert "Key Exclusions:" in text


# ===================================================================
# Natural-language intent routing
# ===================================================================


class TestAnswerOwnerQuery:

    def test_field_query(self, r03):
        result = answer_owner_query(
            "What is the annual limit for Remedy 03?")
        assert result["type"] == "field"
        assert "150,000" in result["result"]["formatted"]

    def test_field_maternity(self, r02):
        result = answer_owner_query("Show maternity for Remedy 02")
        assert result["type"] == "field"
        assert result["result"]["field"] == "maternity_cover"

    def test_field_network(self, r03):
        result = answer_owner_query(
            "What is the network name for Remedy 03?")
        assert result["type"] == "field"
        assert "HN Basic Plus" in result["result"]["formatted"]

    def test_compare_full(self, r02, r03):
        result = answer_owner_query(
            "Compare Remedy 02 vs Remedy 03")
        assert result["type"] == "compare"
        assert "plan_a_code" in result["result"]

    def test_compare_field(self, r02, r03):
        result = answer_owner_query(
            "Compare pharmacy for Remedy 02 vs Remedy 03")
        assert result["type"] == "compare"
        assert result["result"]["field"] == "pharmacy_cover_summary"

    def test_compare_differences(self, r02, r03):
        result = answer_owner_query(
            "Show differences between Remedy 02 and Remedy 03")
        assert result["type"] == "compare"
        assert result["result"].get("differences_only") is True

    def test_summary_query(self, r03):
        result = answer_owner_query("Remedy 03 summary")
        assert result["type"] == "summary"
        assert "HN-REMEDY-3" in result["result"]["plan_code"]

    def test_plan_name_only_gives_summary(self, r02):
        result = answer_owner_query("Remedy 02")
        assert result["type"] == "summary"

    def test_unsupported_query(self):
        result = answer_owner_query(
            "Who is the CEO of the insurance company?")
        assert result["type"] == "unsupported"
        assert result["message"] == _SAFE_FALLBACK

    def test_empty_query(self):
        result = answer_owner_query("")
        assert result["type"] == "unsupported"

    def test_pharmacy_query_r03(self, r03):
        result = answer_owner_query(
            "What is the pharmacy cover for Remedy 03?")
        assert result["type"] == "field"
        assert "5,000" in result["result"]["formatted"]

    def test_pre_existing_rule_query(self, r03):
        result = answer_owner_query(
            "What is the pre-existing condition rule for Remedy 03?")
        assert result["type"] == "field"
        assert "6 months" in result["result"]["formatted"]

    def test_outside_uae_query(self, r03):
        result = answer_owner_query(
            "outside UAE rule for Remedy 03")
        assert result["type"] == "field"

    def test_exclusions_query(self, r02):
        result = answer_owner_query(
            "Show exclusions for Remedy 02")
        assert result["type"] == "field"
        assert isinstance(result["result"]["value"], list)


# ===================================================================
# Regression: parser + comparator still work correctly
# ===================================================================


class TestRegression:

    def test_r02_canonical_shape(self, r02):
        from src.parsers.canonical_schema import validate_canonical_shape
        errors = validate_canonical_shape(r02)
        assert errors == []

    def test_r03_canonical_shape(self, r03):
        from src.parsers.canonical_schema import validate_canonical_shape
        errors = validate_canonical_shape(r03)
        assert errors == []

    def test_raw_comparator_still_works(self, r02, r03):
        from src.parsers.plan_comparator import compare_plans as raw_cmp
        raw = raw_cmp(r02, r03)
        assert raw["plan_a_code"] == "HN-REMEDY-2"
        assert raw["plan_b_code"] == "HN-REMEDY-3"
        assert raw["missing_in_a"] == []
        assert raw["missing_in_b"] == []

    def test_r02_outpatient_15(self, r02):
        assert "15%" in r02["outpatient_cover_summary"]

    def test_r03_outpatient_10(self, r03):
        assert "10%" in r03["outpatient_cover_summary"]

    def test_r02_pharmacy_3k(self, r02):
        assert "3,000" in r02["pharmacy_cover_summary"]

    def test_r03_pharmacy_5k(self, r03):
        assert "5,000" in r03["pharmacy_cover_summary"]

    def test_owner_fields_subset_of_business(self):
        from src.parsers.canonical_schema import BUSINESS_FIELDS
        assert set(OWNER_FIELDS).issubset(set(BUSINESS_FIELDS))
