"""Tests for src.__main__ CLI exit code behavior."""

import shutil
from pathlib import Path

from src.__main__ import main

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_DOCX = FIXTURES_DIR / "sample.docx"


def _setup_batch(tmp_path, monkeypatch, valid_names=(), corrupt_names=()):
    input_dir = tmp_path / "input_docs"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    monkeypatch.setattr("src.extractors.docx_extractor.INPUT_DIR", input_dir)
    monkeypatch.setattr("src.extractors.docx_extractor.OUTPUT_DIR", output_dir)
    for name in valid_names:
        shutil.copy(SAMPLE_DOCX, input_dir / name)
    for name in corrupt_names:
        (input_dir / name).write_bytes(b"not a docx")


def test_main_returns_zero_on_all_success(tmp_path, monkeypatch):
    _setup_batch(tmp_path, monkeypatch, valid_names=["a.docx", "b.docx"])
    assert main() == 0


def test_main_returns_nonzero_on_partial_failure(tmp_path, monkeypatch):
    _setup_batch(tmp_path, monkeypatch, valid_names=["good.docx"], corrupt_names=["bad.docx"])
    assert main() == 1


def test_main_returns_nonzero_on_all_failure(tmp_path, monkeypatch):
    _setup_batch(tmp_path, monkeypatch, corrupt_names=["bad1.docx", "bad2.docx"])
    assert main() == 1


def test_main_returns_zero_on_empty_input(tmp_path, monkeypatch):
    _setup_batch(tmp_path, monkeypatch)
    assert main() == 0
