"""Frozen schema for extracted DOCX JSON output.

This is the single source of truth for the expected shape of
extraction results. Validators and downstream consumers reference
this module.
"""

SCHEMA_VERSION = "1.0"

# Required top-level fields and their expected Python types.
REQUIRED_FIELDS: dict[str, type] = {
    "schema_version": str,
    "source_filename": str,
    "source_path": str,
    "paragraph_count": int,
    "table_count": int,
    "paragraphs": list,
    "tables": list,
}
