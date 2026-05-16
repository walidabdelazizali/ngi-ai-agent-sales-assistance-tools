"""
shared_helpers.py — Reusable formatting utilities for all export modes.

Deterministic formatting rules for:
- Field ordering
- Label rendering
- Separator handling
- Empty field filtering
- Whitespace cleanup
- Safe text rendering
"""

from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# SENTINEL & SAFETY CONSTANTS
# ---------------------------------------------------------------------------

_MISSING = "Not specified in plan data."
_SAFE_REFUSAL = (
    "This information is not available or the query is not currently supported. "
    "Please contact an administrator or rephrase your request."
)

# Fields that must never leak into packaged output
_BLOCKED_FIELD_SUBSTRINGS = (
    "source_trace",
    "raw",
    "unapproved",
    "internal",
    "debug",
    "review",
)

# ---------------------------------------------------------------------------
# LANGUAGE LABELS — Centralized registry
# ---------------------------------------------------------------------------

ENGLISH_LABELS = {
    "plan_name": "Plan",
    "plan_code": "Plan Code",
    "network_name": "Network",
    "annual_limit": "Annual Limit",
    "area_of_coverage": "Coverage Area",
    "direct_billing": "Direct Billing",
    "referral_required": "Referral Required",
    "maternity_cover": "Maternity",
    "pharmacy_cover": "Pharmacy",
    "dental_cover": "Dental",
    "mental_health_cover": "Mental Health",
    "key_exclusions": "Key Exclusions",
    "reimbursement_allowed": "Reimbursement Allowed",
    "reimbursement_scope": "Reimbursement Scope",
    "outside_network_reimbursement": "Outside Network Reimbursement",
    "outside_uae_reimbursement": "Outside UAE Reimbursement",
    "reimbursement_basis": "Reimbursement Basis",
    "reimbursement_conditions": "Reimbursement Conditions",
    "reimbursement_documents_required": "Documents Required",
}

ARABIC_LABELS = {
    "plan_name": "اسم الخطة",
    "plan_code": "رمز الخطة",
    "network_name": "الشبكة",
    "annual_limit": "الحد السنوي",
    "area_of_coverage": "نطاق التغطية",
    "direct_billing": "الدفع المباشر",
    "referral_required": "الإحالة مطلوبة",
    "maternity_cover": "تغطية الأمومة",
    "pharmacy_cover": "تغطية الصيدلية",
    "dental_cover": "تغطية الأسنان",
    "mental_health_cover": "الصحة العقلية",
    "key_exclusions": "الاستثناءات الأساسية",
    "reimbursement_allowed": "التعويض متاح",
    "reimbursement_scope": "نطاق التعويض",
    "outside_network_reimbursement": "تعويض خارج الشبكة",
    "outside_uae_reimbursement": "تعويض خارج الإمارات",
    "reimbursement_basis": "أساس التعويض",
    "reimbursement_conditions": "شروط التعويض",
    "reimbursement_documents_required": "المستندات المطلوبة",
}

# ---------------------------------------------------------------------------
# FIELD ORDERING — Deterministic order for all formatters
# ---------------------------------------------------------------------------

# Standard field order for plan summaries (most to least important)
STANDARD_PLAN_FIELDS = [
    "plan_name",
    "plan_code",
    "network_name",
    "annual_limit",
    "area_of_coverage",
    "direct_billing",
    "referral_required",
    "maternity_cover",
    "pharmacy_cover",
    "dental_cover",
    "mental_health_cover",
    "key_exclusions",
]

# Reimbursement-specific fields
REIMBURSEMENT_FIELDS = [
    "reimbursement_allowed",
    "reimbursement_scope",
    "outside_network_reimbursement",
    "outside_uae_reimbursement",
    "reimbursement_basis",
    "reimbursement_conditions",
    "reimbursement_documents_required",
]

# Comparison-specific fields (order for comparison rows)
COMPARISON_FIELDS = [
    "annual_limit",
    "network_name",
    "area_of_coverage",
    "direct_billing",
    "referral_required",
    "maternity_cover",
    "pharmacy_cover",
    "dental_cover",
    "reimbursement_allowed",
]

# ---------------------------------------------------------------------------
# SAFE VALUE RENDERING
# ---------------------------------------------------------------------------


def safe_value(value: Any, fallback: str = _MISSING) -> str:
    """
    Return a safe string for `value`, or `fallback` if absent/unusable.
    
    Ensures:
    - No None values
    - No empty strings
    - No "not available" variants
    - No internal metadata leakage
    """
    if value is None:
        return fallback
    s = str(value).strip()
    if not s or s.lower() in {"none", "not available", "n/a", ""}:
        return fallback
    # Block internal metadata leakage
    sl = s.lower()
    if any(b in sl for b in _BLOCKED_FIELD_SUBSTRINGS):
        return fallback
    return s


def clean_utf8(text: str) -> str:
    """Remove mojibake (broken UTF-8 replacement characters)."""
    if not text:
        return text
    return text.replace("�", "").replace("  ", " ").strip()


def safe_boolean(value: Any) -> str:
    """Convert boolean-ish field to 'Yes' / 'No' / _MISSING."""
    if value is None:
        return _MISSING
    if isinstance(value, bool):
        return "Yes" if value else "No"
    s = str(value).strip().lower()
    if s in {"yes", "true", "1", "y"}:
        return "Yes"
    if s in {"no", "false", "0", "n"}:
        return "No"
    if s in {"none", "", "not available"}:
        return _MISSING
    return safe_value(value)


def detect_language(text: str) -> str:
    """
    Detect language by checking for Arabic Unicode ranges.
    
    Returns 'ar' if Arabic characters present, 'en' otherwise.
    """
    if not text:
        return "en"
    for c in text:
        # Arabic Unicode ranges
        if (
            "\u0600" <= c <= "\u06FF"  # Arabic
            or "\u0750" <= c <= "\u077F"  # Arabic Supplement
            or "\u08A0" <= c <= "\u08FF"  # Arabic Extended-A
            or "\uFB50" <= c <= "\uFDFF"  # Arabic Presentation Forms
            or "\uFE70" <= c <= "\uFEFF"  # Arabic Presentation Forms-B
        ):
            return "ar"
    return "en"


# ---------------------------------------------------------------------------
# FIELD EXTRACTION & NORMALIZATION
# ---------------------------------------------------------------------------


def extract_data(agent_response: dict) -> dict:
    """Pull the data payload from any approved agent response dict."""
    data = agent_response.get("data") or {}
    if not isinstance(data, dict):
        data = {}
    return data


def extract_core_fields(agent_response: dict) -> dict:
    """
    Return normalized core plan fields from an approved agent response.
    
    Extracts from both top-level and nested data payload.
    Returns safe/empty values for missing fields.
    """
    data = extract_data(agent_response)
    return {
        "plan_name": safe_value(data.get("plan_name") or agent_response.get("plan_name")),
        "plan_code": safe_value(data.get("plan_code")),
        "network_name": safe_value(data.get("network_name")),
        "annual_limit": safe_value(data.get("annual_limit")),
        "area_of_coverage": safe_value(data.get("area_of_coverage")),
        "direct_billing": safe_boolean(data.get("direct_billing")),
        "referral_required": safe_boolean(data.get("referral_required")),
        "maternity_cover": safe_value(data.get("maternity_cover")),
        "pharmacy_cover": safe_value(data.get("pharmacy_cover_summary") or data.get("pharmacy_cover")),
        "dental_cover": safe_value(data.get("dental_cover_summary") or data.get("dental_cover")),
        "mental_health_cover": safe_value(data.get("mental_health_cover_summary")),
        "key_exclusions": safe_value(data.get("key_exclusions")),
    }


def extract_reimbursement_fields(agent_response: dict) -> dict:
    """Extract reimbursement-specific fields."""
    data = extract_data(agent_response)
    return {
        "reimbursement_allowed": safe_boolean(data.get("reimbursement_allowed")),
        "reimbursement_scope": safe_value(data.get("reimbursement_scope")),
        "outside_network_reimbursement": safe_value(data.get("outside_network_reimbursement")),
        "outside_uae_reimbursement": safe_value(data.get("outside_uae_reimbursement")),
        "reimbursement_basis": safe_value(data.get("reimbursement_basis")),
        "reimbursement_conditions": safe_value(data.get("reimbursement_conditions")),
        "reimbursement_documents_required": safe_value(data.get("reimbursement_documents_required")),
    }


# ---------------------------------------------------------------------------
# LINE BUILDING HELPERS — No duplicate labels, consistent formatting
# ---------------------------------------------------------------------------


def build_label_value_line(
    label: str,
    value: str,
    field_key: Optional[str] = None,
    language: str = "en",
) -> Optional[str]:
    """
    Build a single "Label: Value" line, safely handling missing values.
    
    Returns None if value is _MISSING (caller should filter).
    """
    if value == _MISSING or not value:
        return None
    # Use mapped label if field_key provided, otherwise use label as-is
    display_label = label
    return f"{display_label}: {value}"


def build_lines_from_fields(
    fields: Dict[str, str],
    field_keys: List[str],
    labels: Dict[str, str],
    language: str = "en",
) -> List[str]:
    """
    Build list of "Label: Value" lines in deterministic order.
    
    Only includes fields where value != _MISSING.
    No duplicate labels (one per field).
    """
    lines = []
    for key in field_keys:
        value = fields.get(key, _MISSING)
        if value == _MISSING or not value:
            continue
        label = labels.get(key, key)
        line = build_label_value_line(label, value, key, language)
        if line:
            lines.append(line)
    return lines


# ---------------------------------------------------------------------------
# LINE JOINING WITH SPACING RULES
# ---------------------------------------------------------------------------


def join_lines(lines: List[str], separator: str = "\n", max_blank_lines: int = 1) -> str:
    """
    Join lines with separator, enforcing spacing rules.
    
    Rules:
    - No repeated blank lines (max 1 in sequence)
    - No trailing separators
    - Strip leading/trailing whitespace
    """
    if not lines:
        return ""
    # Join with separator
    result = separator.join(lines)
    # Remove trailing separators
    result = result.rstrip(separator)
    return result


def join_sections(sections: List[str], separator: str = "\n\n") -> str:
    """Join major sections with double spacing, enforcing no excess blanks."""
    if not sections:
        return ""
    # Filter empty sections
    non_empty = [s for s in sections if s and s.strip()]
    return separator.join(non_empty)


# ---------------------------------------------------------------------------
# APPROVAL VALIDATION
# ---------------------------------------------------------------------------


def assert_approved(agent_response: dict, allowed_intents: set) -> None:
    """
    Raise ValueError if the agent response is not approved for formatting.
    
    Checks:
    - ok=True
    - intent in allowed_intents
    """
    if not agent_response.get("ok"):
        raise ValueError("not_approved")
    intent = agent_response.get("intent", "")
    if intent not in allowed_intents:
        raise ValueError(f"intent_not_packageable:{intent}")


# ---------------------------------------------------------------------------
# AED HANDLING — Remove duplicate currency markers
# ---------------------------------------------------------------------------


def clean_aed(value: str) -> str:
    """Remove duplicate AED markers that sometimes appear in output."""
    if not value:
        return value
    # Remove various duplicate AED patterns
    value = value.replace("AED AED.", "AED.")
    value = value.replace("AED AED", "AED")
    value = value.replace("AED. AED.", "AED.")
    # Remove leading "AED. " if followed by number (already contains AED)
    if value.startswith("AED. ") and value.count("AED") > 1:
        value = value[6:].strip()
    return value


# ---------------------------------------------------------------------------
# COMPARISON-SPECIFIC HELPERS
# ---------------------------------------------------------------------------


def build_comparison_line(label: str, plan1_val: str, plan2_val: str, language: str = "en") -> Optional[str]:
    """
    Build a comparison line: "Label: Plan1Val | Plan2Val"
    
    Returns None if both values are _MISSING.
    """
    if (plan1_val == _MISSING or not plan1_val) and (plan2_val == _MISSING or not plan2_val):
        return None
    v1 = plan1_val if plan1_val and plan1_val != _MISSING else "—"
    v2 = plan2_val if plan2_val and plan2_val != _MISSING else "—"
    return f"{label}: {v1} | {v2}"


# ---------------------------------------------------------------------------
# VALIDATION UTILITIES
# ---------------------------------------------------------------------------


def no_duplicate_labels(lines: List[str]) -> bool:
    """Check that no label appears twice in output (sanity check)."""
    labels_seen = set()
    for line in lines:
        if ":" in line:
            label = line.split(":", 1)[0].strip()
            if label in labels_seen:
                return False
            labels_seen.add(label)
    return True


def no_empty_lines(text: str) -> bool:
    """Check that text doesn't have repeated blank lines."""
    return "\n\n\n" not in text


def no_trailing_separators(text: str) -> bool:
    """Check that text doesn't end with separator."""
    return not (text.rstrip().endswith("\n") or text.rstrip().endswith("|"))
