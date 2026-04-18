"""Tests for src.validators.extraction_validator."""

import copy
from pathlib import Path

import pytest

from src.extractors.docx_extractor import extract_docx
from src.extractors.schema import SCHEMA_VERSION
from src.validators.extraction_validator import (
    ValidationError,
    validate_extraction,
    validate_or_raise,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_DOCX = FIXTURES_DIR / "sample.docx"


def _valid_payload() -> dict:
    """Return a known-good extraction result."""
    return extract_docx(SAMPLE_DOCX)


# --- valid output ---


def test_valid_output_has_no_errors():
    errors = validate_extraction(_valid_payload())
    assert errors == []


def test_validate_or_raise_passes_for_valid():
    validate_or_raise(_valid_payload())  # should not raise


# --- missing required fields ---


@pytest.mark.parametrize(
    "field",
    [
        "schema_version",
        "source_filename",
        "source_path",
        "paragraph_count",
        "table_count",
        "paragraphs",
        "tables",
    ],
)
def test_missing_required_field(field):
    data = _valid_payload()
    del data[field]
    errors = validate_extraction(data)
    assert any(field in e for e in errors)


# --- wrong field types ---


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("schema_version", 999),
        ("source_filename", 123),
        ("source_path", None),
        ("paragraph_count", "two"),
        ("table_count", 1.5),
        ("paragraphs", "not a list"),
        ("tables", {}),
    ],
)
def test_wrong_field_type(field, bad_value):
    data = _valid_payload()
    data[field] = bad_value
    errors = validate_extraction(data)
    assert any(field in e and "expected" in e for e in errors)


# --- count consistency ---


def test_paragraph_count_mismatch():
    data = _valid_payload()
    data["paragraph_count"] = 999
    errors = validate_extraction(data)
    assert any("paragraph_count" in e for e in errors)


def test_table_count_mismatch():
    data = _valid_payload()
    data["table_count"] = 999
    errors = validate_extraction(data)
    assert any("table_count" in e for e in errors)


# --- malformed paragraphs ---


def test_paragraphs_contains_non_string():
    data = _valid_payload()
    data["paragraphs"] = ["ok", 42]
    data["paragraph_count"] = 2
    errors = validate_extraction(data)
    assert any("paragraphs[1]" in e for e in errors)


# --- malformed tables ---


def test_table_is_not_list_of_rows():
    data = _valid_payload()
    data["tables"] = ["not a table"]
    data["table_count"] = 1
    errors = validate_extraction(data)
    assert any("tables[0]" in e for e in errors)


def test_table_row_is_not_list():
    data = _valid_payload()
    data["tables"] = [["not a row"]]
    data["table_count"] = 1
    errors = validate_extraction(data)
    assert any("tables[0][0]" in e for e in errors)


def test_table_cell_is_not_string():
    data = _valid_payload()
    data["tables"] = [[[99]]]
    data["table_count"] = 1
    errors = validate_extraction(data)
    assert any("tables[0][0][0]" in e for e in errors)


# --- validate_or_raise ---


def test_validate_or_raise_raises_on_invalid():
    with pytest.raises(ValidationError) as exc_info:
        validate_or_raise({})
    assert len(exc_info.value.errors) > 0


# --- schema_version value ---


def test_schema_version_value():
    data = _valid_payload()
    assert data["schema_version"] == SCHEMA_VERSION


def test_schema_version_wrong_value():
    data = _valid_payload()
    data["schema_version"] = "0.0"
    errors = validate_extraction(data)
    assert any("schema_version" in e for e in errors)
