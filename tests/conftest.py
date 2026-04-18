"""Shared pytest configuration — auto-generate fixtures before test collection."""

from pathlib import Path

from tests.create_fixture import create_fixture

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_DOCX = FIXTURES_DIR / "sample.docx"


def pytest_configure(config):
    """Ensure the sample .docx fixture exists before any test runs."""
    if not SAMPLE_DOCX.exists():
        create_fixture(SAMPLE_DOCX)
