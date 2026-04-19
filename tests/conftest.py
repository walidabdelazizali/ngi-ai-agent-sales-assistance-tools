"""Shared pytest configuration — auto-generate fixtures before test collection."""

from pathlib import Path


# Only add workspace root for src imports if needed
import sys
from pathlib import Path
workspace_root = str(Path(__file__).parent.parent.resolve())
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
from tests.create_fixture import create_fixture

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_DOCX = FIXTURES_DIR / "sample.docx"


def pytest_configure(config):
    """Ensure the sample .docx fixture exists before any test runs."""
    if not SAMPLE_DOCX.exists():
        create_fixture(SAMPLE_DOCX)
