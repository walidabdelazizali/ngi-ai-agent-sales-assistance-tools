"""Smoke tests: verify project structure and imports."""

from pathlib import Path

from src.config.settings import (
    PROJECT_ROOT,
    INPUT_DIR,
    OUTPUT_DIR,
    DATA_DIR,
    RUNTIME_CSV_DIR,
    RUNTIME_WORKBOOK_DIR,
)


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir()


def test_required_directories_exist():
    for d in (INPUT_DIR, OUTPUT_DIR, DATA_DIR, RUNTIME_CSV_DIR, RUNTIME_WORKBOOK_DIR):
        assert d.is_dir(), f"Missing directory: {d}"


def test_src_subpackages_importable():
    import src.extractors
    import src.normalizers
    import src.validators
    import src.db
    import src.tools
    import src.agent
    import src.config
