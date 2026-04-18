"""Tests for src.extractors.docx_extractor."""

import json
import shutil
from pathlib import Path

import pytest

from src.extractors.docx_extractor import (
    ExtractionError,
    IngestionResult,
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


# --- corrupted / unreadable .docx ---


def test_extract_docx_corrupted_file(tmp_path):
    bad_file = tmp_path / "corrupted.docx"
    bad_file.write_bytes(b"this is not a valid docx")
    with pytest.raises(ExtractionError, match="corrupted.docx") as exc_info:
        extract_docx(bad_file)
    assert exc_info.value.path == bad_file
    assert exc_info.value.reason  # non-empty reason string


def test_extract_docx_empty_file(tmp_path):
    empty_file = tmp_path / "empty.docx"
    empty_file.write_bytes(b"")
    with pytest.raises(ExtractionError, match="empty.docx"):
        extract_docx(empty_file)


def test_extract_docx_truncated_zip(tmp_path):
    """A file that starts like a ZIP but is truncated."""
    truncated = tmp_path / "truncated.docx"
    truncated.write_bytes(b"PK\x03\x04" + b"\x00" * 20)
    with pytest.raises(ExtractionError, match="truncated.docx"):
        extract_docx(truncated)


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

    result = run_ingestion()
    assert len(result.succeeded) == 1
    assert result.succeeded[0].name == "sample.json"
    assert result.failed == []

    data = json.loads(result.succeeded[0].read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert data["source_filename"] == "sample.docx"
    assert data["paragraph_count"] == 2
    assert data["table_count"] == 1


def test_run_ingestion_empty_dir(tmp_path, monkeypatch):
    input_dir = tmp_path / "input_docs"
    input_dir.mkdir()
    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", input_dir)

    result = run_ingestion()
    assert result.succeeded == []
    assert result.failed == []
    assert result.total == 0


def test_run_ingestion_missing_input_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", tmp_path / "nope")
    with pytest.raises(FileNotFoundError):
        run_ingestion()


# --- batch error reporting ---


def _setup_batch(tmp_path, monkeypatch, valid_names=(), corrupt_names=()):
    """Helper: populate temp input dir with valid copies and corrupt files."""
    input_dir = tmp_path / "input_docs"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", input_dir)
    monkeypatch.setattr("src.extractors.docx_extractor.OUTPUT_DIR", output_dir)
    for name in valid_names:
        shutil.copy(SAMPLE_DOCX, input_dir / name)
    for name in corrupt_names:
        (input_dir / name).write_bytes(b"not a docx")
    return input_dir, output_dir


def test_batch_mixed_valid_and_corrupted(tmp_path, monkeypatch):
    _setup_batch(
        tmp_path, monkeypatch,
        valid_names=["good1.docx", "good2.docx"],
        corrupt_names=["bad.docx"],
    )
    result = run_ingestion()
    assert len(result.succeeded) == 2
    assert len(result.failed) == 1
    assert result.failed[0][0].name == "bad.docx"
    assert result.failed[0][1]  # non-empty reason
    assert result.total == 3


def test_batch_all_corrupted(tmp_path, monkeypatch):
    _setup_batch(
        tmp_path, monkeypatch,
        corrupt_names=["bad1.docx", "bad2.docx"],
    )
    result = run_ingestion()
    assert result.succeeded == []
    assert len(result.failed) == 2


def test_batch_all_valid(tmp_path, monkeypatch):
    _setup_batch(
        tmp_path, monkeypatch,
        valid_names=["a.docx", "b.docx", "c.docx"],
    )
    result = run_ingestion()
    assert len(result.succeeded) == 3
    assert result.failed == []


def test_batch_valid_files_still_written_when_others_fail(tmp_path, monkeypatch):
    _, output_dir = _setup_batch(
        tmp_path, monkeypatch,
        valid_names=["good.docx"],
        corrupt_names=["bad.docx"],
    )
    result = run_ingestion()
    assert (output_dir / "good.json").exists()
    assert not (output_dir / "bad.json").exists()
    assert len(result.succeeded) == 1
    assert len(result.failed) == 1


def test_ingestion_result_print_summary(capsys):
    r = IngestionResult(
        succeeded=[Path("a.json")],
        failed=[(Path("b.docx"), "corrupt")],
    )
    r.print_summary()
    out = capsys.readouterr().out
    assert "1 succeeded" in out
    assert "1 failed" in out
    assert "b.docx" in out
