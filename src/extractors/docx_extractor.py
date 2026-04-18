"""Extract structured data from .docx files."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from docx import Document

from src.config.settings import INPUT_DIR, OUTPUT_DIR
from src.extractors.schema import SCHEMA_VERSION
from src.normalizers.extraction_normalizer import normalize_extraction
from src.tools.io import atomic_write_text
from src.validators.extraction_validator import validate_or_raise

SUPPORTED_EXTENSIONS = {".docx"}


class ExtractionError(Exception):
    """Raised when a .docx file cannot be parsed."""

    def __init__(self, path: Path, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to extract {path.name}: {reason}")


@dataclass
class IngestionResult:
    """Summary of a batch ingestion run."""

    succeeded: list[Path] = field(default_factory=list)
    failed: list[tuple[Path, str]] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.succeeded) + len(self.failed)

    def print_summary(self) -> None:
        print(f"\nIngestion summary: {len(self.succeeded)} succeeded, "
              f"{len(self.failed)} failed, {self.total} total.")
        for path, reason in self.failed:
            print(f"  FAILED: {path.name} — {reason}")


def extract_paragraphs(doc: Document) -> list[str]:
    """Return non-empty paragraph texts."""
    return [p.text for p in doc.paragraphs if p.text.strip()]


def extract_tables(doc: Document) -> list[list[list[str]]]:
    """Return tables as list of rows, each row a list of cell texts."""
    tables = []
    for table in doc.tables:
        rows = []
        for row in table.rows:
            rows.append([cell.text.strip() for cell in row.cells])
        tables.append(rows)
    return tables


def extract_docx(file_path: Path) -> dict[str, Any]:
    """Extract paragraphs and tables from a single .docx file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    try:
        doc = Document(str(file_path))
    except Exception as exc:
        raise ExtractionError(file_path, str(exc)) from exc

    paragraphs = extract_paragraphs(doc)
    tables = extract_tables(doc)

    return {
        "schema_version": SCHEMA_VERSION,
        "source_filename": file_path.name,
        "source_path": str(file_path),
        "paragraph_count": len(paragraphs),
        "table_count": len(tables),
        "paragraphs": paragraphs,
        "tables": tables,
    }


def run_ingestion() -> IngestionResult:
    """Process all .docx files in INPUT_DIR, write JSON to OUTPUT_DIR.

    Returns an IngestionResult with per-file success/failure details.
    """
    if not INPUT_DIR.is_dir():
        raise FileNotFoundError(f"Input directory missing: {INPUT_DIR}")

    docx_files = sorted(INPUT_DIR.glob("*.docx"))
    if not docx_files:
        print(f"No .docx files found in {INPUT_DIR}")
        return IngestionResult()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result = IngestionResult()
    for docx_path in docx_files:
        try:
            data = extract_docx(docx_path)
            data = normalize_extraction(data)
            validate_or_raise(data)
            out_path = OUTPUT_DIR / f"{docx_path.stem}.json"
            atomic_write_text(
                out_path, json.dumps(data, indent=2, ensure_ascii=False)
            )
            print(f"  {docx_path.name} -> {out_path.name}")
            result.succeeded.append(out_path)
        except Exception as exc:
            print(f"  {docx_path.name} FAILED: {exc}")
            result.failed.append((docx_path, str(exc)))

    return result
