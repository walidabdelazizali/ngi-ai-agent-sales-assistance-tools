"""Structured parser for NGI Remedy plan extraction output.

Reads the raw extraction dict produced by ``extract_docx`` and maps
known sections / table rows into normalised insurance-plan fields.

Design rules
------------
* Never invent values — return ``None`` or ``[]`` when data is absent.
* Purely deterministic; no AI, no network calls.
* Does **not** modify the incoming extraction dict.
"""

from __future__ import annotations

import re
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Section heading patterns (case-insensitive)
# ---------------------------------------------------------------------------

_SECTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("proposal_header", re.compile(
        r"medical\s+insurance\s+program", re.IGNORECASE)),
    ("table_of_benefits", re.compile(
        r"^table\s+of\s+benefits$", re.IGNORECASE)),
    ("summary_of_premiums", re.compile(
        r"^summary\s+of\s+premiums$", re.IGNORECASE)),
    ("terms_and_conditions", re.compile(
        r"^terms\s+and\s+conditions$", re.IGNORECASE)),
    ("standard_exclusions", re.compile(
        r"standard\s+policy\s+exclusions", re.IGNORECASE)),
    ("out_of_scope_exclusions", re.compile(
        r"healthcare\s+services\s+outside\s+the\s+scope", re.IGNORECASE)),
    ("client_approval", re.compile(
        r"^client\s+approval\s+form$", re.IGNORECASE)),
]

# Ordered list of section keys so we know when a section ends.
_SECTION_ORDER = [key for key, _ in _SECTION_PATTERNS]


# ---------------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------------

def detect_sections(paragraphs: list[str]) -> dict[str, list[str]]:
    """Map section headings to their paragraph content.

    Returns a dict keyed by section name (see ``_SECTION_PATTERNS``)
    whose values are the list of paragraphs between that heading and
    the next detected heading.
    """
    # Build list of (index, section_key) for every detected heading.
    markers: list[tuple[int, str]] = []
    for idx, para in enumerate(paragraphs):
        text = para.strip()
        for key, pattern in _SECTION_PATTERNS:
            if pattern.search(text):
                markers.append((idx, key))
                break  # first match wins

    sections: dict[str, list[str]] = {}
    for pos, (start_idx, key) in enumerate(markers):
        # Content starts on the line *after* the heading.
        content_start = start_idx + 1
        # Content ends at the next marker (or end of paragraphs).
        if pos + 1 < len(markers):
            content_end = markers[pos + 1][0]
        else:
            content_end = len(paragraphs)
        sections[key] = paragraphs[content_start:content_end]

    return sections


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

_RE_WHITESPACE = re.compile(r"\s+")


def _clean_scalar(value: Optional[str]) -> Optional[str]:
    """Collapse newlines and repeated whitespace into single spaces."""
    if value is None:
        return None
    cleaned = _RE_WHITESPACE.sub(" ", value).strip()
    return cleaned if cleaned else None


# ---------------------------------------------------------------------------
# Table helpers
# ---------------------------------------------------------------------------

def _cell(table: list[list[str]], row: int, col: int) -> Optional[str]:
    """Safely retrieve a cell value, returning ``None`` on index error."""
    try:
        val = table[row][col].strip()
        return val if val else None
    except (IndexError, AttributeError):
        return None


def _find_row(table: list[list[str]], label_pattern: re.Pattern[str],
              col: int = 0) -> Optional[int]:
    """Return the first row index whose *col* matches *label_pattern*."""
    for idx, row in enumerate(table):
        try:
            if label_pattern.search(row[col]):
                return idx
        except (IndexError, AttributeError):
            continue
    return None


def _find_table_with_row(tables: list[list[list[str]]],
                         label_pattern: re.Pattern[str],
                         col: int = 0) -> Optional[list[list[str]]]:
    """Return the first table containing a row matching *label_pattern*."""
    for table in tables:
        if _find_row(table, label_pattern, col) is not None:
            return table
    return None


# ---------------------------------------------------------------------------
# Field extractors — each returns a single parsed value
# ---------------------------------------------------------------------------

_RE_PLAN = re.compile(r"^Plan$", re.IGNORECASE)
_RE_MAX_BENEFIT = re.compile(r"Maximum Benefit Per Year", re.IGNORECASE)
_RE_AREA = re.compile(r"^Area of Coverage$", re.IGNORECASE)
_RE_NETWORK = re.compile(r"^Provider Network$", re.IGNORECASE)
_RE_MATERNITY = re.compile(r"^MATERNITY$", re.IGNORECASE)
_RE_REIMBURSE_OUTSIDE = re.compile(r"Reimbursement Outside Network", re.IGNORECASE)


def _extract_plan_name(tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_PLAN)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_PLAN)
    return _cell(tbl, row_idx, 1) if row_idx is not None else None


def _extract_plan_code(source_filename: str,
                       plan_name: Optional[str]) -> Optional[str]:
    """Derive a plan code from the filename or plan name."""
    # Try filename first: "HN-REMEDY-2.docx" -> "HN-REMEDY-2"
    stem = re.sub(r"\.\w+$", "", source_filename).strip()
    if stem:
        return stem
    # Fallback: extract from plan_name if present
    if plan_name:
        m = re.search(r"Remedy\s*[-–]?\s*\d+", plan_name, re.IGNORECASE)
        if m:
            return m.group(0).replace(" ", "-").replace("–", "-")
    return None


def _extract_insurer_name(paragraphs: list[str]) -> Optional[str]:
    for para in paragraphs:
        m = re.search(
            r"(National General Insurance(?:\s+Company)?(?:\s*\(NGI\))?)",
            para, re.IGNORECASE,
        )
        if m:
            return m.group(1).strip()
    return None


def _extract_network_name(tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_NETWORK)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_NETWORK)
    if row_idx is None:
        return None
    raw = _cell(tbl, row_idx, 1)
    if raw is None:
        return None
    # Extract the network brand from the first line.
    first_line = raw.split("\n")[0].strip()
    # e.g. "HN Basic Plus (OP Restricted to Clinics) with direct access..."
    m = re.match(r"(HN\s+\S+(?:\s+\S+)?)", first_line, re.IGNORECASE)
    return m.group(1).strip() if m else first_line


def _extract_area_of_coverage(tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_AREA)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_AREA)
    return _cell(tbl, row_idx, 1) if row_idx is not None else None


def _extract_annual_limit(tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_MAX_BENEFIT)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_MAX_BENEFIT)
    return _cell(tbl, row_idx, 1) if row_idx is not None else None


def _extract_direct_billing(paragraphs: list[str]) -> Optional[bool]:
    for para in paragraphs:
        if re.search(r"direct\s+billing\s+basis", para, re.IGNORECASE):
            return True
    return None


def _extract_reimbursement_allowed(paragraphs: list[str]) -> Optional[bool]:
    for para in paragraphs:
        if re.search(r"no\s+reimbursement\s+is\s+allowed", para, re.IGNORECASE):
            return False
    # Check for positive reimbursement mentions
    for para in paragraphs:
        if re.search(r"reimbursement\s+(?:is\s+)?allowed", para, re.IGNORECASE):
            return True
    return None


def _extract_referral_required(paragraphs: list[str],
                               tables: list[list[list[str]]]) -> Optional[bool]:
    for para in paragraphs:
        if re.search(r"referral", para, re.IGNORECASE):
            return True
    for table in tables:
        for row in table:
            for cell in row:
                if re.search(r"Subject\s+to\s+GP\s+Referral", cell, re.IGNORECASE):
                    return True
    return None


def _extract_maternity_cover(tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_MATERNITY)
    if tbl is None:
        return None
    # Find the in-patient maternity row which has the cover details.
    pat = re.compile(r"in-patient\s+maternity", re.IGNORECASE)
    row_idx = _find_row(tbl, pat)
    if row_idx is not None:
        # The coverage description is typically in col 2.
        return _cell(tbl, row_idx, 2)
    return None


_RE_ITEM_START = re.compile(r"^\s*(\d+)\s*\.\s*(.+)$")


def _extract_exclusions(sections: dict[str, list[str]]) -> list[str]:
    """Parse numbered exclusion items structurally from section content.

    Each paragraph is split into lines.  A line matching ``N . text``
    starts a new exclusion item; subsequent non-numbered lines are
    appended as continuations of the current item.  Final items are
    whitespace-collapsed and stripped of their leading number.
    """
    exclusions: list[str] = []
    current: list[str] = []

    def _flush() -> None:
        if current:
            merged = _RE_WHITESPACE.sub(" ", " ".join(current)).strip()
            if merged:
                exclusions.append(merged)
            current.clear()

    for key in ("standard_exclusions", "out_of_scope_exclusions"):
        for para in sections.get(key, []):
            for line in para.split("\n"):
                line = line.strip()
                if not line:
                    continue
                m = _RE_ITEM_START.match(line)
                if m:
                    _flush()
                    # Start new item with the text after the number.
                    current.append(m.group(2).strip())
                elif current:
                    # Continuation of the current numbered item.
                    current.append(line)
        # Flush at section boundary so items don't bleed across sections.
        _flush()

    return exclusions


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_remedy_plan(extraction: dict[str, Any]) -> dict[str, Any]:
    """Parse an extraction dict into structured Remedy plan fields.

    Parameters
    ----------
    extraction : dict
        Raw output from ``extract_docx`` / the ingestion pipeline.

    Returns
    -------
    dict
        Structured fields. Missing data → ``None`` / ``[]``.
    """
    paragraphs: list[str] = extraction.get("paragraphs", [])
    tables: list[list[list[str]]] = extraction.get("tables", [])

    sections = detect_sections(paragraphs)

    plan_name = _extract_plan_name(tables)
    plan_code = _extract_plan_code(
        extraction.get("source_filename", ""), plan_name)

    return {
        "plan_name": _clean_scalar(plan_name),
        "plan_code": plan_code,
        "insurer_name": _clean_scalar(_extract_insurer_name(paragraphs)),
        "network_name": _clean_scalar(_extract_network_name(tables)),
        "area_of_coverage": _clean_scalar(_extract_area_of_coverage(tables)),
        "annual_limit": _clean_scalar(_extract_annual_limit(tables)),
        "direct_billing": _extract_direct_billing(paragraphs),
        "reimbursement_allowed": _extract_reimbursement_allowed(paragraphs),
        "referral_required": _extract_referral_required(paragraphs, tables),
        "maternity_cover": _clean_scalar(_extract_maternity_cover(tables)),
        "key_exclusions": _extract_exclusions(sections),
        "raw_section_map": sections,
    }
