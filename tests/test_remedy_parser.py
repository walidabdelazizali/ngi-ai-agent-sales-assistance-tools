"""Tests for src.parsers.remedy_parser."""

import json
from pathlib import Path

import pytest

from src.parsers.remedy_parser import detect_sections, parse_remedy_plan

# ---------------------------------------------------------------------------
# Fixture: realistic extraction payload based on HN-REMEDY-2
# ---------------------------------------------------------------------------

_REMEDY_JSON = Path(__file__).parent.parent / "output" / "HN-REMEDY-2.json"


def _load_remedy_extraction() -> dict:
    """Load the real HN-REMEDY-2 extracted JSON if available."""
    if not _REMEDY_JSON.exists():
        pytest.skip("HN-REMEDY-2.json not found in output/")
    return json.loads(_REMEDY_JSON.read_text(encoding="utf-8"))


def _minimal_extraction(**overrides) -> dict:
    """Return a bare-minimum extraction dict."""
    data = {
        "schema_version": "1.0",
        "source_filename": "test.docx",
        "source_path": "test.docx",
        "paragraph_count": 0,
        "table_count": 0,
        "paragraphs": [],
        "tables": [],
    }
    data.update(overrides)
    return data


# ===================================================================
# Happy-path tests against the real HN-REMEDY-2 payload
# ===================================================================


class TestRemedyHappyPath:
    """Verify all fields against the known HN-REMEDY-2 extraction."""

    @pytest.fixture(autouse=True)
    def _parsed(self):
        self.extraction = _load_remedy_extraction()
        self.result = parse_remedy_plan(self.extraction)

    def test_plan_name(self):
        assert "Remedy" in self.result["plan_name"]

    def test_plan_code(self):
        assert self.result["plan_code"] == "HN-REMEDY-2"

    def test_insurer_name(self):
        name = self.result["insurer_name"]
        assert name is not None
        assert "National General Insurance" in name

    def test_network_name(self):
        assert self.result["network_name"] is not None
        assert "HN Basic Plus" in self.result["network_name"]

    def test_area_of_coverage(self):
        aoc = self.result["area_of_coverage"]
        assert aoc is not None
        assert "UAE" in aoc

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

    def test_maternity_cover(self):
        mc = self.result["maternity_cover"]
        assert mc is not None
        assert "co-pay" in mc.lower() or "delivery" in mc.lower()

    def test_key_exclusions_populated(self):
        excl = self.result["key_exclusions"]
        assert isinstance(excl, list)
        assert len(excl) > 10  # HN-REMEDY-2 has 40+ exclusions

    def test_exclusions_are_strings(self):
        for item in self.result["key_exclusions"]:
            assert isinstance(item, str)
            assert len(item) > 0

    def test_exclusions_no_leading_numbers(self):
        """Numbered prefixes should be stripped."""
        import re
        for item in self.result["key_exclusions"]:
            assert not re.match(r"^\d+\s*\.", item)

    def test_raw_section_map_has_keys(self):
        rsm = self.result["raw_section_map"]
        assert "proposal_header" in rsm
        assert "table_of_benefits" in rsm
        assert "terms_and_conditions" in rsm
        assert "standard_exclusions" in rsm

    def test_no_mutation_of_input(self):
        """Parser must not modify the extraction dict."""
        original = json.loads(json.dumps(self.extraction))
        parse_remedy_plan(self.extraction)
        assert self.extraction == original


# ===================================================================
# Section detection tests
# ===================================================================


class TestDetectSections:

    def test_detects_known_headings(self):
        paragraphs = [
            "Some intro text",
            "Table of Benefits",
            "benefit row 1",
            "benefit row 2",
            "Summary of Premiums",
            "premium info",
            "Terms and Conditions",
            "some term",
        ]
        sections = detect_sections(paragraphs)
        assert "table_of_benefits" in sections
        assert sections["table_of_benefits"] == ["benefit row 1", "benefit row 2"]
        assert "summary_of_premiums" in sections
        assert sections["summary_of_premiums"] == ["premium info"]
        assert "terms_and_conditions" in sections
        assert sections["terms_and_conditions"] == ["some term"]

    def test_no_headings_returns_empty(self):
        paragraphs = ["random text", "more text"]
        assert detect_sections(paragraphs) == {}

    def test_empty_paragraphs(self):
        assert detect_sections([]) == {}

    def test_heading_at_end_captures_nothing(self):
        paragraphs = ["intro", "Table of Benefits"]
        sections = detect_sections(paragraphs)
        assert sections["table_of_benefits"] == []


# ===================================================================
# Missing-section / partial-parse behaviour
# ===================================================================


class TestMissingSections:

    def test_empty_extraction_returns_all_none_or_empty(self):
        result = parse_remedy_plan(_minimal_extraction())
        assert result["plan_name"] is None
        assert result["insurer_name"] is None
        assert result["network_name"] is None
        assert result["area_of_coverage"] is None
        assert result["annual_limit"] is None
        assert result["direct_billing"] is None
        assert result["reimbursement_allowed"] is None
        assert result["referral_required"] is None
        assert result["maternity_cover"] is None
        assert result["key_exclusions"] == []
        assert result["raw_section_map"] == {}

    def test_plan_code_from_filename(self):
        ext = _minimal_extraction(source_filename="HN-REMEDY-5.docx")
        result = parse_remedy_plan(ext)
        assert result["plan_code"] == "HN-REMEDY-5"

    def test_plan_code_none_when_empty_filename(self):
        ext = _minimal_extraction(source_filename="")
        result = parse_remedy_plan(ext)
        assert result["plan_code"] is None or result["plan_code"] == ""

    def test_only_paragraphs_no_tables(self):
        ext = _minimal_extraction(paragraphs=[
            "National General Insurance Company (NGI) welcomes you.",
            "Treatment within the applicable NGI Healthnet Network will be settled on a direct billing basis.",
            "No reimbursement is allowed under this plan.",
        ])
        result = parse_remedy_plan(ext)
        assert result["insurer_name"] is not None
        assert result["direct_billing"] is True
        assert result["reimbursement_allowed"] is False
        # Table-derived fields must be None.
        assert result["plan_name"] is None
        assert result["annual_limit"] is None

    def test_only_tables_no_paragraphs(self):
        ext = _minimal_extraction(tables=[
            [["Plan", "NGI Remedy 03"],
             ["Maximum Benefit Per Year\n(some note)", "AED. 250,000"]],
        ])
        result = parse_remedy_plan(ext)
        assert result["plan_name"] == "NGI Remedy 03"
        assert "250,000" in result["annual_limit"]
        # Paragraph-derived fields must be None.
        assert result["insurer_name"] is None
        assert result["direct_billing"] is None


# ===================================================================
# No hallucinated values
# ===================================================================


class TestNoHallucination:
    """Parser must never fabricate data."""

    def test_no_invented_exclusions(self):
        ext = _minimal_extraction(paragraphs=[
            "Standard Policy Exclusions",
            "This is a description, not an exclusion.",
        ])
        result = parse_remedy_plan(ext)
        # The description does not match "N ." pattern — should be empty.
        assert result["key_exclusions"] == []

    def test_reimbursement_unknown_without_signal(self):
        ext = _minimal_extraction(paragraphs=["Some unrelated paragraph."])
        result = parse_remedy_plan(ext)
        assert result["reimbursement_allowed"] is None

    def test_direct_billing_unknown_without_signal(self):
        ext = _minimal_extraction(paragraphs=["Nothing about billing here."])
        result = parse_remedy_plan(ext)
        assert result["direct_billing"] is None

    def test_referral_unknown_without_signal(self):
        ext = _minimal_extraction(paragraphs=["General text."], tables=[])
        result = parse_remedy_plan(ext)
        assert result["referral_required"] is None
