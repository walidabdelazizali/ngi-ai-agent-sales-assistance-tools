"""Tests for src.extractors.docx_extractor."""

import json
import shutil
from pathlib import Path

import pytest

from src.extractors.docx_extractor import (
    extract_docx,
    run_ingestion,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_DOCX = FIXTURES_DIR / "sample.docx"


# --- extract_docx unit tests ---


def test_extract_docx_returns_expected_fields():
    result = extract_docx(SAMPLE_DOCX)
    assert result["schema_version"] == "1.0"
    assert result["source_filename"] == "sample.docx"
    assert result["paragraph_count"] == 2
    assert result["table_count"] == 1


def test_extract_docx_paragraphs_content():
    result = extract_docx(SAMPLE_DOCX)
    assert result["paragraphs"] == ["First paragraph.", "Second paragraph."]


def test_extract_docx_tables_content():
    result = extract_docx(SAMPLE_DOCX)
    assert len(result["tables"]) == 1
    assert result["tables"][0] == [["A1", "B1"], ["A2", "B2"]]


def test_extract_docx_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_docx(Path("nonexistent.docx"))


def test_extract_docx_unsupported_extension(tmp_path):
    txt_file = tmp_path / "readme.txt"
    txt_file.write_text("hello")
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_docx(txt_file)


# --- run_ingestion integration tests ---


def test_run_ingestion_produces_json(tmp_path, monkeypatch):
    """Copy fixture to a temp input dir, run ingestion, check output."""
    input_dir = tmp_path / "input_docs"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    shutil.copy(SAMPLE_DOCX, input_dir / "sample.docx")

    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", input_dir)
    monkeypatch.setattr("src.extractors.docx_extractor.OUTPUT_DIR", output_dir)

    written = run_ingestion()
    assert len(written) == 1
    assert written[0].name == "sample.json"

    data = json.loads(written[0].read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert data["source_filename"] == "sample.docx"
    assert data["paragraph_count"] == 2
    assert data["table_count"] == 1


def test_run_ingestion_empty_dir(tmp_path, monkeypatch):
    input_dir = tmp_path / "input_docs"
    input_dir.mkdir()
    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", input_dir)

    written = run_ingestion()
    assert written == []


def test_run_ingestion_missing_input_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", tmp_path / "nope")
    with pytest.raises(FileNotFoundError):
        run_ingestion()
