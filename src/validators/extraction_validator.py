"""Validate extracted DOCX JSON output against the frozen schema."""

from typing import Any

from src.extractors.schema import REQUIRED_FIELDS, SCHEMA_VERSION


class ValidationError(Exception):
    """Raised when extracted output fails schema validation."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(f"Validation failed ({len(errors)} error(s)): {'; '.join(errors)}")


def validate_extraction(data: dict[str, Any]) -> list[str]:
    """Check *data* against the DOCX extraction schema.

    Returns a list of error strings (empty means valid).
    """
    errors: list[str] = []

    # --- required fields & types ---
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
        elif not isinstance(data[field], expected_type):
            errors.append(
                f"Field '{field}' expected {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )

    # Stop early if basic structure is broken.
    if errors:
        return errors

    # --- schema_version value ---
    if data["schema_version"] != SCHEMA_VERSION:
        errors.append(
            f"schema_version expected '{SCHEMA_VERSION}', got '{data['schema_version']}'"
        )

    # --- count consistency ---
    if data["paragraph_count"] != len(data["paragraphs"]):
        errors.append(
            f"paragraph_count ({data['paragraph_count']}) "
            f"does not match len(paragraphs) ({len(data['paragraphs'])})"
        )
    if data["table_count"] != len(data["tables"]):
        errors.append(
            f"table_count ({data['table_count']}) "
            f"does not match len(tables) ({len(data['tables'])})"
        )

    # --- paragraphs shape: list[str] ---
    for i, item in enumerate(data["paragraphs"]):
        if not isinstance(item, str):
            errors.append(f"paragraphs[{i}] expected str, got {type(item).__name__}")

    # --- tables shape: list[list[list[str]]] ---
    for t_idx, table in enumerate(data["tables"]):
        if not isinstance(table, list):
            errors.append(f"tables[{t_idx}] expected list (rows), got {type(table).__name__}")
            continue
        for r_idx, row in enumerate(table):
            if not isinstance(row, list):
                errors.append(
                    f"tables[{t_idx}][{r_idx}] expected list (cells), "
                    f"got {type(row).__name__}"
                )
                continue
            for c_idx, cell in enumerate(row):
                if not isinstance(cell, str):
                    errors.append(
                        f"tables[{t_idx}][{r_idx}][{c_idx}] expected str, "
                        f"got {type(cell).__name__}"
                    )

    return errors


def validate_or_raise(data: dict[str, Any]) -> None:
    """Validate and raise :class:`ValidationError` if invalid."""
    errors = validate_extraction(data)
    if errors:
        raise ValidationError(errors)
