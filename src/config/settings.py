"""Centralized path constants for the project."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

INPUT_DIR = PROJECT_ROOT / "input_docs"
OUTPUT_DIR = PROJECT_ROOT / "output"
DATA_DIR = PROJECT_ROOT / "data"
RUNTIME_CSV_DIR = PROJECT_ROOT / "runtime_data" / "csv"
RUNTIME_WORKBOOK_DIR = PROJECT_ROOT / "runtime_data" / "workbook"
