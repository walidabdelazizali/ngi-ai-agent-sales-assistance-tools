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
        # Try col 2 first (Remedy 02 layout), fallback to col 1 (Remedy 03).
        val = _cell(tbl, row_idx, 2)
        if val is None:
            val = _cell(tbl, row_idx, 1)
        return val
    return None


_RE_ITEM_START = re.compile(r"^\s*(\d+)\s*\.\s*(.+)$")

# ---------------------------------------------------------------------------
# Benefit summary patterns
# ---------------------------------------------------------------------------

_RE_INPATIENT_HEADER = re.compile(r"^IN-PATIENT", re.IGNORECASE)
_RE_OUTPATIENT_HEADER = re.compile(r"^OUT-PATIENT", re.IGNORECASE)
_RE_PHARMACY = re.compile(r"Prescribed\s+Drugs|Pharmacy", re.IGNORECASE)
_RE_DIAGNOSTICS = re.compile(
    r"Tests,?\s+diagnosis|Laboratory\s+tests|Radiology", re.IGNORECASE)
_RE_PHYSIO = re.compile(r"Physiotherapy", re.IGNORECASE)

# Rules patterns
_RE_PRE_EXISTING = re.compile(r"Pre-existing\s+conditions", re.IGNORECASE)
_RE_REIMBURSE_OUTSIDE_UAE = re.compile(
    r"Reimbursement\s+Outside\s+UAE", re.IGNORECASE)


def _extract_benefit_summary(tables: list[list[list[str]]],
                             header_pat: re.Pattern[str],
                             end_pat: Optional[re.Pattern[str]] = None,
                             ) -> Optional[str]:
    """Extract a summary from the benefits table section between headers."""
    tbl = _find_table_with_row(tables, header_pat)
    if tbl is None:
        return None
    start = _find_row(tbl, header_pat)
    if start is None:
        return None
    # Collect benefit rows until end pattern or end of table
    parts: list[str] = []
    for i in range(start + 1, len(tbl)):
        cell0 = _cell(tbl, i, 0) or ""
        if end_pat and end_pat.search(cell0):
            break
        cell1 = _cell(tbl, i, 1)
        if cell0 and cell1:
            label = cell0.split("\n")[0].strip()
            value = cell1.split("\n")[0].strip()
            parts.append(f"{label}: {value}")
        elif cell0:
            label = cell0.split("\n")[0].strip()
            parts.append(label)
    return "; ".join(parts) if parts else None


def _extract_inpatient_summary(tables: list[list[list[str]]]) -> Optional[str]:
    return _extract_benefit_summary(tables, _RE_INPATIENT_HEADER,
                                    end_pat=_RE_OUTPATIENT_HEADER)


def _extract_outpatient_summary(tables: list[list[list[str]]]) -> Optional[str]:
    return _extract_benefit_summary(tables, _RE_OUTPATIENT_HEADER)


def _extract_pharmacy_summary(tables: list[list[list[str]]]) -> Optional[str]:
    for tbl in tables:
        row_idx = _find_row(tbl, _RE_PHARMACY)
        if row_idx is not None:
            val = _cell(tbl, row_idx, 1)
            return val
    return None


def _extract_diagnostics_summary(tables: list[list[list[str]]]) -> Optional[str]:
    """Extract diagnostic-related benefit rows."""
    parts: list[str] = []
    for tbl in tables:
        for idx, row in enumerate(tbl):
            cell0 = (row[0] if row else "").strip()
            if re.search(r"Laboratory\s+tests", cell0, re.IGNORECASE):
                val = _cell(tbl, idx, 1)
                if val:
                    parts.append(f"Lab tests: {val.split(chr(10))[0].strip()}")
            elif re.search(r"Radiology", cell0, re.IGNORECASE):
                val = _cell(tbl, idx, 1)
                if val:
                    parts.append(
                        f"Radiology: {val.split(chr(10))[0].strip()}")
    return "; ".join(parts) if parts else None


def _extract_physiotherapy_summary(
        tables: list[list[list[str]]]) -> Optional[str]:
    for tbl in tables:
        row_idx = _find_row(tbl, _RE_PHYSIO)
        if row_idx is not None:
            val = _cell(tbl, row_idx, 1)
            return val
    return None


# ---------------------------------------------------------------------------
# Rules extractors
# ---------------------------------------------------------------------------

def _extract_pre_existing_rule(tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_PRE_EXISTING)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_PRE_EXISTING)
    if row_idx is None:
        return None
    val = _cell(tbl, row_idx, 1)
    return val


def _extract_chronic_condition_rule(
        tables: list[list[list[str]]]) -> Optional[str]:
    """Chronic rule is often on the row after the pre-existing row."""
    tbl = _find_table_with_row(tables, _RE_PRE_EXISTING)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_PRE_EXISTING)
    if row_idx is None:
        return None
    # Check for a second pre-existing row (renewal rule)
    for i in range(row_idx + 1, len(tbl)):
        cell0 = _cell(tbl, i, 0) or ""
        if re.search(r"pre-existing", cell0, re.IGNORECASE):
            return _cell(tbl, i, 1)
    return None


def _extract_outside_network_rule(
        tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_REIMBURSE_OUTSIDE)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_REIMBURSE_OUTSIDE)
    if row_idx is None:
        return None
    return _cell(tbl, row_idx, 1)


def _extract_outside_uae_rule(
        tables: list[list[list[str]]]) -> Optional[str]:
    tbl = _find_table_with_row(tables, _RE_REIMBURSE_OUTSIDE_UAE)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_REIMBURSE_OUTSIDE_UAE)
    if row_idx is None:
        return None
    return _cell(tbl, row_idx, 1)


def _extract_approval_rule_summary(
        tables: list[list[list[str]]]) -> Optional[str]:
    """Collect pre-approval requirements found in benefit descriptions."""
    approvals: list[str] = []
    pat = re.compile(r"pre-?approval\s+is\s+required", re.IGNORECASE)
    for tbl in tables:
        for row in tbl:
            cell0 = (row[0] if row else "").strip()
            if pat.search(cell0):
                label = cell0.split("\n")[0].strip()
                if label not in approvals:
                    approvals.append(label)
    return "; ".join(approvals) if approvals else None


# ---------------------------------------------------------------------------
# Network prep field extractors (capture only — NOT provider intelligence)
# ---------------------------------------------------------------------------

def _extract_network_access_notes(
        tables: list[list[list[str]]]) -> Optional[str]:
    """Full provider network cell text — raw capture."""
    tbl = _find_table_with_row(tables, _RE_NETWORK)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_NETWORK)
    if row_idx is None:
        return None
    return _cell(tbl, row_idx, 1)


def _extract_clinic_only_flag(
        tables: list[list[list[str]]]) -> Optional[bool]:
    """Detect if OP access is restricted to clinics."""
    tbl = _find_table_with_row(tables, _RE_NETWORK)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_NETWORK)
    if row_idx is None:
        return None
    raw = _cell(tbl, row_idx, 1) or ""
    if re.search(r"OP\s+Restricted\s+to\s+Clinics", raw, re.IGNORECASE):
        return True
    return False


def _extract_hospital_access_notes(
        tables: list[list[list[str]]]) -> Optional[str]:
    """Extract direct hospital access mention from network cell."""
    tbl = _find_table_with_row(tables, _RE_NETWORK)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_NETWORK)
    if row_idx is None:
        return None
    raw = _cell(tbl, row_idx, 1) or ""
    m = re.search(r"direct\s+access\s+to\s+below\s+hospitals\s+for\s+OP\s+Services",
                  raw, re.IGNORECASE)
    return m.group(0) if m else None


def _extract_direct_access_hospitals_raw(
        tables: list[list[list[str]]]) -> list[str]:
    """Extract listed hospital names from the network cell."""
    tbl = _find_table_with_row(tables, _RE_NETWORK)
    if tbl is None:
        return []
    row_idx = _find_row(tbl, _RE_NETWORK)
    if row_idx is None:
        return []
    raw = _cell(tbl, row_idx, 1) or ""
    lines = raw.split("\n")
    # Skip first line (network description) and last line (referral note)
    hospitals: list[str] = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # Stop if we hit a referral/specialist note
        if re.search(r"Specialist\s+Subject\s+to|Referral", line, re.IGNORECASE):
            break
        hospitals.append(line)
    return hospitals


def _extract_direct_billing_notes(paragraphs: list[str]) -> Optional[str]:
    """Return paragraph text that mentions direct billing arrangements."""
    for para in paragraphs:
        if re.search(r"direct\s+billing", para, re.IGNORECASE):
            return para.strip()
    return None


def _extract_referral_behavior_notes(
        tables: list[list[list[str]]]) -> Optional[str]:
    """Capture referral behavior text from the network cell."""
    tbl = _find_table_with_row(tables, _RE_NETWORK)
    if tbl is None:
        return None
    row_idx = _find_row(tbl, _RE_NETWORK)
    if row_idx is None:
        return None
    raw = _cell(tbl, row_idx, 1) or ""
    for line in raw.split("\n"):
        if re.search(r"Specialist\s+Subject\s+to|Referral", line, re.IGNORECASE):
            return line.strip()
    return None


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

    # If no paragraphs/tables, treat as minimal stub and surface root fields
    if not paragraphs and not tables:
        return {
            "plan_name": extraction.get("plan_name"),
            "plan_code": extraction.get("plan_code"),
            "insurer_name": None,
            "network_name": extraction.get("medical_network") or extraction.get("network_name"),
            "area_of_coverage": extraction.get("area_of_coverage"),
            "annual_limit": extraction.get("annual_limit"),
            "direct_billing": extraction.get("direct_billing"),
            "reimbursement_allowed": extraction.get("reimbursement_allowed"),
            "reimbursement_scope": extraction.get("reimbursement_scope"),
            "outside_network_reimbursement": extraction.get("outside_network_reimbursement"),
            "outside_uae_reimbursement": extraction.get("outside_uae_reimbursement"),
            "reimbursement_basis": extraction.get("reimbursement_basis"),
            "reimbursement_conditions": extraction.get("reimbursement_conditions"),
            "reimbursement_documents_required": extraction.get("reimbursement_documents_required"),
            "referral_required": extraction.get("referral_required"),
            "maternity_cover": extraction.get("maternity_cover"),
            "inpatient_cover_summary": extraction.get("inpatient_cover_summary"),
            "outpatient_cover_summary": extraction.get("outpatient_cover_summary"),
            "pharmacy_cover_summary": extraction.get("pharmacy_cover_summary"),
            "diagnostics_cover_summary": extraction.get("diagnostics_cover_summary"),
            "physiotherapy_cover_summary": extraction.get("physiotherapy_cover_summary"),
            "pre_existing_condition_rule": extraction.get("pre_existing_condition_rule"),
            "chronic_condition_rule": extraction.get("chronic_condition_rule"),
            "outside_network_rule": extraction.get("outside_network_rule"),
            "outside_uae_rule": extraction.get("outside_uae_rule"),
            "approval_rule_summary": extraction.get("approval_rule_summary"),
            "key_exclusions": extraction.get("key_exclusions", []),
            "network_access_notes": extraction.get("network_access_notes"),
            "clinic_only_flag": extraction.get("clinic_only_flag"),
            "hospital_access_notes": extraction.get("hospital_access_notes"),
            "direct_access_hospitals_raw": extraction.get("direct_access_hospitals_raw", []),
            "direct_billing_notes": extraction.get("direct_billing_notes"),
            "referral_behavior_notes": extraction.get("referral_behavior_notes"),
            "raw_section_map": {},
        }

    sections = detect_sections(paragraphs)

    # --- Remedy 04 targeted extraction and debug ---
    plan_name = _extract_plan_name(tables)
    plan_code = _extract_plan_code(
        extraction.get("source_filename", ""), plan_name)
    # Remedy 04 detection: filename or plan name
    is_remedy04 = False
    remedy04_indicators = [
        extraction.get("source_filename", ""),
        extraction.get("filename", ""),
        extraction.get("file_path", ""),
        extraction.get("plan_code", ""),
        extraction.get("plan_name", ""),
    ]
    for val in remedy04_indicators:
        if val and ("remedy 4" in val.lower() or "remedy-4" in val.lower()):
            is_remedy04 = True
            break

    if is_remedy04:
        # Targeted extraction for Remedy 04
        # Plan name
        try:
            plan_name_dbg = None
            tbl = tables[0] if tables and len(tables) > 0 else None
            if tbl:
                for row in tbl:
                    if row and len(row) > 1 and ("plan" in row[0].lower()):
                        plan_name_dbg = row[1].strip()
                        break
            if plan_name_dbg:
                plan_name = plan_name_dbg
        except Exception as e:
            print("[Remedy04 DEBUG] plan_name extraction error:", e)
        # Annual limit
        try:
            annual_limit_dbg = None
            tbl = tables[0] if tables and len(tables) > 0 else None
            if tbl:
                for row in tbl:
                    if row and len(row) > 1 and ("maximum benefit" in row[0].lower()):
                        # Find first non-empty value in columns 1+ (Remedy 04 has 4 columns)
                        for col in range(1, min(5, len(row))):
                            v = row[col].strip()
                            if v:
                                annual_limit_dbg = v
                                break
                        if annual_limit_dbg:
                            break
            if annual_limit_dbg:
                parsed_annual_limit = annual_limit_dbg
            else:
                parsed_annual_limit = _clean_scalar(_extract_annual_limit(tables))
        except Exception as e:
            print("[Remedy04 DEBUG] annual_limit extraction error:", e)
            parsed_annual_limit = None
        # Area of coverage
        try:
            area_dbg = None
            tbl = tables[0] if tables and len(tables) > 0 else None
            if tbl:
                for row in tbl:
                    if row and len(row) > 1 and ("area of coverage" in row[0].lower()):
                        for col in range(1, min(5, len(row))):
                            v = row[col].strip()
                            if v:
                                area_dbg = v
                                break
                        if area_dbg:
                            break
            if area_dbg:
                parsed_area = area_dbg
            else:
                parsed_area = _clean_scalar(_extract_area_of_coverage(tables))
        except Exception as e:
            print("[Remedy04 DEBUG] area_of_coverage extraction error:", e)
            parsed_area = None
        # Network name
        try:
            network_dbg = None
            tbl = tables[0] if tables and len(tables) > 0 else None
            if tbl:
                for row in tbl:
                    if row and len(row) > 1 and ("provider network" in row[0].lower()):
                        for col in range(1, min(5, len(row))):
                            v = row[col].strip()
                            if v:
                                network_dbg = v
                                break
                        if network_dbg:
                            break
            if network_dbg:
                parsed_network = network_dbg
            else:
                parsed_network = _clean_scalar(_extract_network_name(tables))
        except Exception as e:
            print("[Remedy04 DEBUG] network_name extraction error:", e)
            parsed_network = None
        # Direct billing (from paragraphs)
        direct_billing_dbg = _extract_direct_billing(paragraphs)
        # Referral required (from paragraphs/tables)
        referral_dbg = _extract_referral_required(paragraphs, tables)
        # Debug print
        print(f"[Remedy04 DEBUG] plan_name={plan_name} annual_limit={parsed_annual_limit} area_of_coverage={parsed_area} network_name={parsed_network} direct_billing={direct_billing_dbg} referral_required={referral_dbg}")
        # Patch parsed dict for Remedy 04
        parsed = {}
        parsed["plan_name"] = _clean_scalar(plan_name)
        parsed["plan_code"] = plan_code
        parsed["insurer_name"] = _clean_scalar(_extract_insurer_name(paragraphs))
        parsed["network_name"] = _clean_scalar(parsed_network)
        parsed["area_of_coverage"] = _clean_scalar(parsed_area)
        parsed["annual_limit"] = parsed_annual_limit
        parsed["direct_billing"] = direct_billing_dbg
        parsed["reimbursement_allowed"] = extraction.get("reimbursement_allowed", _extract_reimbursement_allowed(paragraphs))
        parsed["reimbursement_scope"] = extraction.get("reimbursement_scope")
        parsed["outside_network_reimbursement"] = extraction.get("outside_network_reimbursement")
        parsed["outside_uae_reimbursement"] = extraction.get("outside_uae_reimbursement")
        parsed["reimbursement_basis"] = extraction.get("reimbursement_basis")
        parsed["reimbursement_conditions"] = extraction.get("reimbursement_conditions")
        parsed["reimbursement_documents_required"] = extraction.get("reimbursement_documents_required")
        parsed["referral_required"] = referral_dbg
        # Benefit summaries
        parsed["maternity_cover"] = _clean_scalar(_extract_maternity_cover(tables))
        parsed["inpatient_cover_summary"] = _clean_scalar(_extract_inpatient_summary(tables))
        parsed["outpatient_cover_summary"] = _clean_scalar(_extract_outpatient_summary(tables))
        parsed["pharmacy_cover_summary"] = _clean_scalar(_extract_pharmacy_summary(tables))
        parsed["diagnostics_cover_summary"] = _clean_scalar(_extract_diagnostics_summary(tables))
        parsed["physiotherapy_cover_summary"] = _clean_scalar(_extract_physiotherapy_summary(tables))
        # Rules
        parsed["pre_existing_condition_rule"] = _clean_scalar(_extract_pre_existing_rule(tables))
        parsed["chronic_condition_rule"] = _clean_scalar(_extract_chronic_condition_rule(tables))
        parsed["outside_network_rule"] = _clean_scalar(_extract_outside_network_rule(tables))
        parsed["outside_uae_rule"] = _clean_scalar(_extract_outside_uae_rule(tables))
        parsed["approval_rule_summary"] = _clean_scalar(_extract_approval_rule_summary(tables))
        # Exclusions
        parsed["key_exclusions"] = _extract_exclusions(sections)
        # Network prep fields (capture only)
        parsed["network_access_notes"] = _clean_scalar(_extract_network_access_notes(tables))
        parsed["clinic_only_flag"] = _extract_clinic_only_flag(tables)
        parsed["hospital_access_notes"] = _clean_scalar(_extract_hospital_access_notes(tables))
        parsed["direct_access_hospitals_raw"] = _extract_direct_access_hospitals_raw(tables)
        parsed["direct_billing_notes"] = _clean_scalar(_extract_direct_billing_notes(paragraphs))
        parsed["referral_behavior_notes"] = _clean_scalar(_extract_referral_behavior_notes(tables))
        # Internal
        parsed["raw_section_map"] = sections
        # Always override with any field present in extraction dict (for passthrough fields like reimbursement_*)
        from src.parsers.canonical_schema import CANONICAL_FIELDS
        for field in CANONICAL_FIELDS:
            if field in extraction:
                parsed[field] = extraction[field]
        for field in CANONICAL_FIELDS:
            if field not in parsed:
                parsed[field] = None
        return parsed

    # Always pass through all fields in CANONICAL_FIELDS from extraction dict if present
    from src.parsers.canonical_schema import CANONICAL_FIELDS
    parsed = {}
    # Use the existing extraction logic for known fields, but always override with extraction dict if present
    # Identity
    parsed["plan_name"] = _clean_scalar(plan_name)
    parsed["plan_code"] = plan_code
    parsed["insurer_name"] = _clean_scalar(_extract_insurer_name(paragraphs))
    parsed["network_name"] = _clean_scalar(_extract_network_name(tables))
    # Coverage core
    parsed["area_of_coverage"] = _clean_scalar(_extract_area_of_coverage(tables))

    # Remedy 06: annual_limit is in tables[0][1][1], reimbursement_allowed is False if 'No reimbursement is allowed' in paragraphs

    # --- Robust Remedy 06 detection across all filename/path variants ---
    remedy06_indicators = [
        extraction.get("source_filename", ""),
        extraction.get("filename", ""),
        extraction.get("file_path", ""),
        extraction.get("plan_code", ""),
        extraction.get("plan_name", ""),
    ]
    is_remedy06 = False
    for val in remedy06_indicators:
        if val and ("remedy 6" in val.lower() or "remedy-6" in val.lower()):
            is_remedy06 = True
            break

    if is_remedy06:
        # Robust annual_limit extraction: search all tables/rows for label containing 'Maximum Benefit'
        annual_limit_val = None
        for tbl in tables:
            for row in tbl:
                if row and len(row) > 1 and "maximum benefit" in row[0].lower():
                    for col in range(1, min(4, len(row))):
                        v = row[col].strip()
                        if v:
                            annual_limit_val = v
                            break
                    if annual_limit_val:
                        break
            if annual_limit_val:
                break
        parsed["annual_limit"] = annual_limit_val if annual_limit_val else _clean_scalar(_extract_annual_limit(tables))

        # Robust reimbursement detection: scan all paragraphs for denial phrase
        reimbursement_allowed = None
        for para in paragraphs:
            if "no reimbursement is allowed under this plan" in para.lower():
                reimbursement_allowed = False
                break
        parsed["reimbursement_allowed"] = reimbursement_allowed
    else:
        parsed["annual_limit"] = _clean_scalar(_extract_annual_limit(tables))
        parsed["reimbursement_allowed"] = extraction.get("reimbursement_allowed", _extract_reimbursement_allowed(paragraphs))

    parsed["direct_billing"] = _extract_direct_billing(paragraphs)
    # Explicit passthrough for reimbursement fields (fixes Remedy 04 drop)
    parsed["reimbursement_scope"] = extraction.get("reimbursement_scope")
    parsed["outside_network_reimbursement"] = extraction.get("outside_network_reimbursement")
    parsed["outside_uae_reimbursement"] = extraction.get("outside_uae_reimbursement")
    parsed["reimbursement_basis"] = extraction.get("reimbursement_basis")
    parsed["reimbursement_conditions"] = extraction.get("reimbursement_conditions")
    parsed["reimbursement_documents_required"] = extraction.get("reimbursement_documents_required")
    parsed["referral_required"] = _extract_referral_required(paragraphs, tables)
    # Benefit summaries
    parsed["maternity_cover"] = _clean_scalar(_extract_maternity_cover(tables))
    parsed["inpatient_cover_summary"] = _clean_scalar(_extract_inpatient_summary(tables))
    parsed["outpatient_cover_summary"] = _clean_scalar(_extract_outpatient_summary(tables))
    parsed["pharmacy_cover_summary"] = _clean_scalar(_extract_pharmacy_summary(tables))
    parsed["diagnostics_cover_summary"] = _clean_scalar(_extract_diagnostics_summary(tables))
    parsed["physiotherapy_cover_summary"] = _clean_scalar(_extract_physiotherapy_summary(tables))
    # Rules
    parsed["pre_existing_condition_rule"] = _clean_scalar(_extract_pre_existing_rule(tables))
    parsed["chronic_condition_rule"] = _clean_scalar(_extract_chronic_condition_rule(tables))
    parsed["outside_network_rule"] = _clean_scalar(_extract_outside_network_rule(tables))
    parsed["outside_uae_rule"] = _clean_scalar(_extract_outside_uae_rule(tables))
    parsed["approval_rule_summary"] = _clean_scalar(_extract_approval_rule_summary(tables))
    # Exclusions
    parsed["key_exclusions"] = _extract_exclusions(sections)
    # Network prep fields (capture only)
    parsed["network_access_notes"] = _clean_scalar(_extract_network_access_notes(tables))
    parsed["clinic_only_flag"] = _extract_clinic_only_flag(tables)
    parsed["hospital_access_notes"] = _clean_scalar(_extract_hospital_access_notes(tables))
    parsed["direct_access_hospitals_raw"] = _extract_direct_access_hospitals_raw(tables)
    parsed["direct_billing_notes"] = _clean_scalar(_extract_direct_billing_notes(paragraphs))
    parsed["referral_behavior_notes"] = _clean_scalar(_extract_referral_behavior_notes(tables))
    # Internal
    parsed["raw_section_map"] = sections

    # Always override with any field present in extraction dict (for passthrough fields like reimbursement_*)
    for field in CANONICAL_FIELDS:
        if field in extraction:
            parsed[field] = extraction[field]

    # Ensure all CANONICAL_FIELDS are present in the parsed dict (None if missing)
    for field in CANONICAL_FIELDS:
        if field not in parsed:
            parsed[field] = None

    return parsed
