"""Tests for src.tools.io."""

import glob
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.tools.io import atomic_write_text


def test_writes_file_successfully(tmp_path):
    target = tmp_path / "out.json"
    atomic_write_text(target, '{"ok": true}')
    assert target.read_text(encoding="utf-8") == '{"ok": true}'


def test_no_temp_files_left_on_success(tmp_path):
    target = tmp_path / "out.json"
    atomic_write_text(target, "content")
    tmp_files = glob.glob(str(tmp_path / "*.tmp"))
    assert tmp_files == []


def test_creates_parent_dirs(tmp_path):
    target = tmp_path / "sub" / "deep" / "out.json"
    atomic_write_text(target, "nested")
    assert target.read_text(encoding="utf-8") == "nested"


def test_overwrites_existing_file_atomically(tmp_path):
    target = tmp_path / "out.json"
    target.write_text("old", encoding="utf-8")
    atomic_write_text(target, "new")
    assert target.read_text(encoding="utf-8") == "new"


def test_original_untouched_on_replace_failure(tmp_path):
    target = tmp_path / "out.json"
    target.write_text("original", encoding="utf-8")

    with patch("src.tools.io.os.replace", side_effect=OSError("mock fail")):
        with pytest.raises(OSError, match="mock fail"):
            atomic_write_text(target, "bad content")

    # Original file should be intact.
    assert target.read_text(encoding="utf-8") == "original"


def test_no_temp_left_on_replace_failure(tmp_path):
    target = tmp_path / "out.json"

    with patch("src.tools.io.os.replace", side_effect=OSError("mock fail")):
        with pytest.raises(OSError):
            atomic_write_text(target, "bad content")

    tmp_files = glob.glob(str(tmp_path / "*.tmp"))
    assert tmp_files == []


def test_no_final_file_on_write_failure(tmp_path):
    """If no original exists and write fails, nothing should remain."""
    target = tmp_path / "out.json"

    with patch("src.tools.io.os.replace", side_effect=OSError("mock fail")):
        with pytest.raises(OSError):
            atomic_write_text(target, "content")

    assert not target.exists()
    tmp_files = glob.glob(str(tmp_path / "*.tmp"))
    assert tmp_files == []
