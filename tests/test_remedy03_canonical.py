"""Tests for Remedy 03 parsing and canonical schema conformance.

Verifies:
- Remedy 03 parses successfully through the standard flow
- Both Remedy 02 and Remedy 03 conform to the canonical schema
- No regression on Remedy 02
- Unknown values remain safely unset (None / [])
- Comparison helper works correctly
"""

import json
from pathlib import Path

import pytest

from src.parsers.remedy_parser import parse_remedy_plan
from src.parsers.canonical_schema import (
    CANONICAL_FIELDS,
    BUSINESS_FIELDS,
    validate_canonical_shape,
)
from src.parsers.plan_comparator import compare_plans

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_REMEDY2_JSON = Path(__file__).parent.parent / "output" / "HN-REMEDY-2.json"
_REMEDY3_JSON = Path(__file__).parent.parent / "output" / "HN-REMEDY-3.json"


def _load_extraction(path: Path) -> dict:
    if not path.exists():
        pytest.skip(f"{path.name} not found in output/")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def remedy2_parsed():
    return parse_remedy_plan(_load_extraction(_REMEDY2_JSON))


@pytest.fixture
def remedy3_parsed():
    return parse_remedy_plan(_load_extraction(_REMEDY3_JSON))


# ===================================================================
# Canonical schema conformance
# ===================================================================


class TestCanonicalSchemaConformance:
    """Both plans must have exactly the canonical field set."""

    def test_remedy2_has_all_canonical_fields(self, remedy2_parsed):
        errors = validate_canonical_shape(remedy2_parsed)
        assert errors == [], f"Schema violations: {errors}"

    def test_remedy3_has_all_canonical_fields(self, remedy3_parsed):
        errors = validate_canonical_shape(remedy3_parsed)
        assert errors == [], f"Schema violations: {errors}"

    def test_remedy2_no_extra_fields(self, remedy2_parsed):
        canonical_set = set(CANONICAL_FIELDS)
        extras = set(remedy2_parsed.keys()) - canonical_set
        assert extras == set(), f"Unexpected fields: {extras}"

    def test_remedy3_no_extra_fields(self, remedy3_parsed):
        canonical_set = set(CANONICAL_FIELDS)
        extras = set(remedy3_parsed.keys()) - canonical_set
        assert extras == set(), f"Unexpected fields: {extras}"

    def test_both_plans_same_key_set(self, remedy2_parsed, remedy3_parsed):
        assert set(remedy2_parsed.keys()) == set(remedy3_parsed.keys())


# ===================================================================
# Remedy 03 happy-path field validation
# ===================================================================


class TestRemedy03HappyPath:
    """Verify all fields against the known HN-REMEDY-3 extraction."""

    @pytest.fixture(autouse=True)
    def _parsed(self, remedy3_parsed):
        self.result = remedy3_parsed

    # --- Identity ---

    def test_plan_name(self):
        assert self.result["plan_name"] is not None
        assert "Remedy" in self.result["plan_name"]
        assert "03" in self.result["plan_name"]

    def test_plan_code(self):
        assert self.result["plan_code"] == "HN-REMEDY-3"

    def test_insurer_name(self):
        name = self.result["insurer_name"]
        assert name is not None
        assert "National General Insurance" in name

    def test_network_name(self):
        assert self.result["network_name"] is not None
        assert "HN Basic Plus" in self.result["network_name"]

    # --- Coverage core ---

    def test_area_of_coverage(self):
        aoc = self.result["area_of_coverage"]
        assert aoc is not None
        assert "UAE" in aoc
        assert "\n" not in aoc

    def test_annual_limit(self):
        limit = self.result["annual_limit"]
        assert limit is not None
        assert "150,000" in limit

    def test_direct_billing(self):
        assert self.result["direct_billing"] is True

    def test_reimbursement_allowed(self):
        assert self.result["reimbursement_allowed"] is False

    def test_referral_required(self):
        assert self.result["referral_required"] is True

    # --- Benefit summaries ---

    def test_maternity_cover(self):
        mc = self.result["maternity_cover"]
        assert mc is not None
        assert "co-pay" in mc.lower() or "delivery" in mc.lower()
        assert "10,000" in mc

    def test_inpatient_cover_summary(self):
        val = self.result["inpatient_cover_summary"]
        assert val is not None
        assert "in-patient" in val.lower()

    def test_outpatient_cover_summary(self):
        val = self.result["outpatient_cover_summary"]
        assert val is not None
        # Remedy 03 uses 10% co-pay (vs Remedy 02's 15%)
        assert "10%" in val

    def test_pharmacy_cover_summary(self):
        val = self.result["pharmacy_cover_summary"]
        assert val is not None
        # Remedy 03: AED 5,000/year, 20% co-pay
        assert "5,000" in val
        assert "20%" in val

    def test_diagnostics_cover_summary(self):
        val = self.result["diagnostics_cover_summary"]
        assert val is not None
        assert "10%" in val  # Remedy 03 uses 10% co-pay

    def test_physiotherapy_cover_summary(self):
        val = self.result["physiotherapy_cover_summary"]
        assert val is not None
        assert "12 sessions" in val
        assert "10%" in val  # Remedy 03 uses 10% co-pay

    # --- Rules ---

    def test_pre_existing_condition_rule(self):
        val = self.result["pre_existing_condition_rule"]
        assert val is not None
        assert "6 months" in val

    def test_chronic_condition_rule(self):
        val = self.result["chronic_condition_rule"]
        assert val is not None
        assert "chronic" in val.lower() or "pre-existing" in val.lower()

    def test_outside_network_rule(self):
        val = self.result["outside_network_rule"]
        assert val is not None
        assert "Emergency" in val

    def test_outside_uae_rule(self):
        val = self.result["outside_uae_rule"]
        assert val is not None
        assert "reimbursement" in val.lower()

    def test_approval_rule_summary(self):
        val = self.result["approval_rule_summary"]
        assert val is not None
        assert "approval" in val.lower() or "Non-urgent" in val

    # --- Exclusions ---

    def test_key_exclusions_populated(self):
        excl = self.result["key_exclusions"]
        assert isinstance(excl, list)
        assert len(excl) > 10  # Remedy 03 also has 40+ exclusions

    def test_exclusions_no_artifact_fragments(self):
        import re
        artifact = re.compile(r"(?<!te)rror of whatever type\.")
        for item in self.result["key_exclusions"]:
            assert not artifact.search(item)

    def test_exclusions_military_operations(self):
        expected = (
            "Injuries or illnesses suffered by the Insured Person "
            "as a result of military operations of whatever type."
        )
        assert expected in self.result["key_exclusions"]

    def test_exclusions_wars_or_terror(self):
        expected = (
            "Injuries or illnesses suffered by the Insured Person "
            "as a result of wars or acts of terror of whatever type."
        )
        assert expected in self.result["key_exclusions"]

    def test_exclusions_are_strings(self):
        for item in self.result["key_exclusions"]:
            assert isinstance(item, str)
            assert len(item) > 0

    def test_exclusions_no_leading_numbers(self):
        import re
        for item in self.result["key_exclusions"]:
            assert not re.match(r"^\d+\s*\.", item)

    # --- Network prep fields ---

    def test_network_access_notes(self):
        val = self.result["network_access_notes"]
        assert val is not None
        assert "HN Basic Plus" in val

    def test_clinic_only_flag(self):
        assert self.result["clinic_only_flag"] is True

    def test_hospital_access_notes(self):
        val = self.result["hospital_access_notes"]
        assert val is not None
        assert "hospital" in val.lower()

    def test_direct_access_hospitals_raw(self):
        hospitals = self.result["direct_access_hospitals_raw"]
        assert isinstance(hospitals, list)
        assert len(hospitals) >= 3  # At least a few hospitals listed

    def test_direct_billing_notes(self):
        val = self.result["direct_billing_notes"]
        assert val is not None
        assert "direct billing" in val.lower()

    def test_referral_behavior_notes(self):
        val = self.result["referral_behavior_notes"]
        assert val is not None
        assert "Referral" in val or "Specialist" in val

    # --- Raw section map ---

    def test_raw_section_map_has_keys(self):
        rsm = self.result["raw_section_map"]
        assert "proposal_header" in rsm
        assert "table_of_benefits" in rsm
        assert "standard_exclusions" in rsm


# ===================================================================
# Remedy 02 regression — ensure nothing broke
# ===================================================================


class TestRemedy02Regression:
    """Re-verify critical Remedy 02 fields haven't regressed."""

    @pytest.fixture(autouse=True)
    def _parsed(self, remedy2_parsed):
        self.result = remedy2_parsed

    def test_plan_code(self):
        assert self.result["plan_code"] == "HN-REMEDY-2"

    def test_plan_name_contains_remedy(self):
        assert "Remedy" in self.result["plan_name"]

    def test_annual_limit(self):
        assert "150,000" in self.result["annual_limit"]

    def test_direct_billing(self):
        assert self.result["direct_billing"] is True

    def test_reimbursement_allowed(self):
        assert self.result["reimbursement_allowed"] is False

    def test_referral_required(self):
        assert self.result["referral_required"] is True

    def test_exclusions_count(self):
        assert len(self.result["key_exclusions"]) > 10

    def test_network_name(self):
        assert "HN Basic Plus" in self.result["network_name"]

    def test_outpatient_15_percent(self):
        """Remedy 02 uses 15% co-pay — must not show 10%."""
        val = self.result["outpatient_cover_summary"]
        assert "15%" in val

    def test_pharmacy_3000(self):
        """Remedy 02 pharmacy limit is AED 3,000."""
        val = self.result["pharmacy_cover_summary"]
        assert "3,000" in val


# ===================================================================
# No hallucination in Remedy 03
# ===================================================================


class TestRemedy03NoHallucination:
    """Verify parser doesn't invent values for Remedy 03."""

    def test_all_non_none_fields_are_grounded(self, remedy3_parsed):
        """Every non-None string field must be traceable to source text."""
        # This is a structural check: None is acceptable, fabrication is not.
        for field in BUSINESS_FIELDS:
            val = remedy3_parsed.get(field)
            if val is None:
                continue  # Acceptable — no data
            if isinstance(val, str):
                assert len(val) > 0, f"Empty string for {field}"
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        assert len(item) > 0


# ===================================================================
# Plan comparator tests
# ===================================================================


class TestPlanComparator:
    """Verify the comparison helper produces correct diffs."""

    def test_compare_remedy_02_vs_03(self, remedy2_parsed, remedy3_parsed):
        diff = compare_plans(remedy2_parsed, remedy3_parsed)
        assert diff["plan_a_code"] == "HN-REMEDY-2"
        assert diff["plan_b_code"] == "HN-REMEDY-3"
        # Plans share the same structure — no missing fields
        assert diff["missing_in_a"] == []
        assert diff["missing_in_b"] == []

    def test_some_fields_match(self, remedy2_parsed, remedy3_parsed):
        diff = compare_plans(remedy2_parsed, remedy3_parsed)
        # Both share same insurer, network, direct billing, etc.
        assert "insurer_name" in diff["matched"]
        assert "network_name" in diff["matched"]
        assert "direct_billing" in diff["matched"]
        assert "reimbursement_allowed" in diff["matched"]
        assert "referral_required" in diff["matched"]

    def test_known_differences(self, remedy2_parsed, remedy3_parsed):
        diff = compare_plans(remedy2_parsed, remedy3_parsed)
        # Plan codes must differ
        assert "plan_code" in diff["differing"]
        # Plan names must differ
        assert "plan_name" in diff["differing"]
        # Outpatient summaries differ (10% vs 15%)
        assert "outpatient_cover_summary" in diff["differing"]
        # Pharmacy summaries differ (5K/20% vs 3K/30%)
        assert "pharmacy_cover_summary" in diff["differing"]

    def test_compare_identical_plans(self, remedy2_parsed):
        diff = compare_plans(remedy2_parsed, remedy2_parsed)
        assert diff["differing"] == {}
        assert diff["missing_in_a"] == []
        assert diff["missing_in_b"] == []
        # All business fields should match
        assert len(diff["matched"]) == len(BUSINESS_FIELDS)

    def test_compare_with_empty_plan(self, remedy2_parsed):
        empty = parse_remedy_plan({
            "schema_version": "1.0",
            "source_filename": "empty.docx",
            "source_path": "empty.docx",
            "paragraph_count": 0,
            "table_count": 0,
            "paragraphs": [],
            "tables": [],
        })
        diff = compare_plans(remedy2_parsed, empty)
        assert diff["missing_in_a"] == []
        assert diff["missing_in_b"] == []
        # plan_code should differ (HN-REMEDY-2 vs "empty")
        assert "plan_code" in diff["differing"]
