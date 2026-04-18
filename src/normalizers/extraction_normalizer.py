"""Normalize raw extracted DOCX content before validation.

Operates on the extraction dict in-place and returns it.
Does not alter the schema shape — only cleans string values,
removes empty paragraphs, and strips empty table rows.
Counts are recomputed after cleanup.
"""

import re
from typing import Any

_MULTI_SPACE = re.compile(r"[ \t]+")


def _clean_string(value: str) -> str:
    """Strip leading/trailing whitespace and collapse internal runs of spaces/tabs."""
    return _MULTI_SPACE.sub(" ", value.strip())


def _normalize_paragraphs(paragraphs: list[str]) -> list[str]:
    """Clean each paragraph and drop any that become empty."""
    cleaned = [_clean_string(p) for p in paragraphs]
    return [p for p in cleaned if p]


def _normalize_table(table: list[list[str]]) -> list[list[str]]:
    """Clean every cell and drop rows where all cells are empty."""
    cleaned_rows: list[list[str]] = []
    for row in table:
        cleaned_row = [_clean_string(cell) for cell in row]
        if any(cell for cell in cleaned_row):
            cleaned_rows.append(cleaned_row)
    return cleaned_rows


def _normalize_tables(tables: list[list[list[str]]]) -> list[list[list[str]]]:
    """Normalize each table; drop tables that become empty after cleanup."""
    result: list[list[list[str]]] = []
    for table in tables:
        cleaned = _normalize_table(table)
        if cleaned:
            result.append(cleaned)
    return result


def normalize_extraction(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize an extraction payload in-place and return it.

    - Cleans paragraph and table-cell strings
    - Removes empty paragraphs and all-empty table rows
    - Removes tables that become empty after row cleanup
    - Recomputes paragraph_count and table_count
    """
    data["paragraphs"] = _normalize_paragraphs(data["paragraphs"])
    data["tables"] = _normalize_tables(data["tables"])
    data["paragraph_count"] = len(data["paragraphs"])
    data["table_count"] = len(data["tables"])
    return data
