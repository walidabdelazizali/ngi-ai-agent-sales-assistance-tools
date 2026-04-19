
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any, Optional

from src.config.settings import OUTPUT_DIR
from src.parsers.canonical_schema import BUSINESS_FIELDS
from src.parsers.plan_comparator import compare_plans as _raw_compare
from src.parsers.remedy_parser import parse_remedy_plan

# ---------------------------------------------------------------------------
# Out-of-scope provider/network lookup intent detector (strict, conservative)
# ---------------------------------------------------------------------------
_PROVIDER_LOOKUP_PATTERNS = [
    # Arabic
    r"هل .*داخل الشبكة",  # e.g. هل Aster Qusais داخل الشبكة
    r"هل .*ضمن الشبكة",    # e.g. هل هذه المستشفى ضمن الشبكة
    r"هل يوجد direct billing.*عيادة",  # direct billing in clinic
    r"هل يوجد direct billing.*مستشفى", # direct billing in hospital
    r"هل يوجد direct billing.*مركز",   # direct billing in center
    r"direct billing في هذه العيادة",   # direct billing in this clinic
    r"direct billing في هذه المستشفى",  # direct billing in this hospital
    r"direct billing في هذا المركز",    # direct billing in this center
    # English
    r"is .+ in the network",            # Is Aster Qusais in the network?
    r"does this hospital offer direct billing", # Does this hospital offer direct billing?
    r"does this clinic offer direct billing",
    r"is this hospital in the network",
    r"is this clinic in the network",
    r"is this provider in the network",
    r"is this facility in the network",
]

_PROVIDER_LOOKUP_PAT = re.compile(
    "|".join(_PROVIDER_LOOKUP_PATTERNS),
    re.IGNORECASE,
)

# Deterministic owner-facing query layer for Remedy plans.
# 
# Provides four public functions:
# - get_plan_field   – retrieve a single field for a plan
# - compare_plans    – field-by-field comparison of two plans
# - summarize_plan   – short human-readable plan summary
# - answer_owner_query – route a plain-text question to the right handler
# 
# All answers are deterministic.  No AI, no fuzzy matching, no hallucination.


import json
import re
from pathlib import Path
from typing import Any, Optional

from src.config.settings import OUTPUT_DIR
from src.parsers.canonical_schema import BUSINESS_FIELDS
from src.parsers.plan_comparator import compare_plans as _raw_compare
from src.parsers.remedy_parser import parse_remedy_plan

# ---------------------------------------------------------------------------
# Plan registry — maps friendly aliases to JSON filenames
# ---------------------------------------------------------------------------

_PLAN_ALIASES: dict[str, str] = {
    "remedy 02": "HN-REMEDY-2.json",
    "remedy 2":  "HN-REMEDY-2.json",
    "remedy02":  "HN-REMEDY-2.json",
    "remedy2":   "HN-REMEDY-2.json",
    "hn-remedy-2": "HN-REMEDY-2.json",
    "remedy 03": "HN-REMEDY-3.json",
    "remedy 3":  "HN-REMEDY-3.json",
    "remedy03":  "HN-REMEDY-3.json",
    "remedy3":   "HN-REMEDY-3.json",
    "hn-remedy-3": "HN-REMEDY-3.json",
    # Arabic
    "ريميدي 2": "HN-REMEDY-2.json",
    "ريميدي 02": "HN-REMEDY-2.json",
    "ريميدي 3": "HN-REMEDY-3.json",
    "ريميدي 03": "HN-REMEDY-3.json",
}

# Fields exposed to the owner (subset of BUSINESS_FIELDS, excludes internal
# network-prep fields that are capture-only and not yet actionable).
OWNER_FIELDS: tuple[str, ...] = (
    "plan_name",
    "plan_code",
    "network_name",
    "annual_limit",
    "area_of_coverage",
    "direct_billing",
    "reimbursement_allowed",
    "referral_required",
    "maternity_cover",
    "inpatient_cover_summary",
    "outpatient_cover_summary",
    "pharmacy_cover_summary",
    "diagnostics_cover_summary",
    "physiotherapy_cover_summary",
    "pre_existing_condition_rule",
    "chronic_condition_rule",
    "outside_network_rule",
    "outside_uae_rule",
    "approval_rule_summary",
    "key_exclusions",
)

# Friendly display labels for owner output
_FIELD_LABELS: dict[str, str] = {
    "plan_name": "Plan Name",
    "plan_code": "Plan Code",
    "insurer_name": "Insurer",
    "network_name": "Network",
    "annual_limit": "Annual Limit",
    "area_of_coverage": "Area of Coverage",
    "direct_billing": "Direct Billing",
    "reimbursement_allowed": "Reimbursement Allowed",
    "referral_required": "Referral Required",
    "maternity_cover": "Maternity Cover",
    "inpatient_cover_summary": "Inpatient Cover",
    "outpatient_cover_summary": "Outpatient Cover",
    "pharmacy_cover_summary": "Pharmacy Cover",
    "diagnostics_cover_summary": "Diagnostics Cover",
    "physiotherapy_cover_summary": "Physiotherapy Cover",
    "pre_existing_condition_rule": "Pre-existing Condition Rule",
    "chronic_condition_rule": "Chronic Condition Rule",
    "outside_network_rule": "Outside Network Rule",
    "outside_uae_rule": "Outside UAE Rule",
    "approval_rule_summary": "Approval Rule",
    "key_exclusions": "Key Exclusions",
}

# Short aliases the owner might use in a query → canonical field name
_FIELD_ALIASES: dict[str, str] = {
        # Add direct Arabic aliases for test cases
        "ما هي الاستثناءات الأساسية": "key_exclusions",
        "ما هي الشروط": "approval_rule_summary",
    "annual limit": "annual_limit",
    "limit": "annual_limit",
    "network": "network_name",
    "network name": "network_name",
    "area": "area_of_coverage",
    "area of coverage": "area_of_coverage",
    "coverage area": "area_of_coverage",
    "direct billing": "direct_billing",
    "billing": "direct_billing",
    "reimbursement": "reimbursement_allowed",
    "referral": "referral_required",
    "maternity": "maternity_cover",
    "maternity cover": "maternity_cover",
    "inpatient": "inpatient_cover_summary",
    "inpatient cover": "inpatient_cover_summary",
    "outpatient": "outpatient_cover_summary",
    "outpatient cover": "outpatient_cover_summary",
    "pharmacy": "pharmacy_cover_summary",
    "pharmacy cover": "pharmacy_cover_summary",
    "drugs": "pharmacy_cover_summary",
    "diagnostics": "diagnostics_cover_summary",
    "diagnostics cover": "diagnostics_cover_summary",
    "lab": "diagnostics_cover_summary",
    "radiology": "diagnostics_cover_summary",
    "physiotherapy": "physiotherapy_cover_summary",
    "physio": "physiotherapy_cover_summary",
    "pre-existing": "pre_existing_condition_rule",
    "pre existing": "pre_existing_condition_rule",
    "pre_existing": "pre_existing_condition_rule",
    "chronic": "chronic_condition_rule",
    "chronic condition": "chronic_condition_rule",
    "outside network": "outside_network_rule",
    "outside uae": "outside_uae_rule",
    "approval": "approval_rule_summary",
    "exclusions": "key_exclusions",
    "key exclusions": "key_exclusions",
    "plan name": "plan_name",
    "plan code": "plan_code",
    "name": "plan_name",
    "code": "plan_code",
    # Arabic aliases (must match test cases and common queries)
    "ما هو الحد السنوي": "annual_limit",
    "الحد السنوي": "annual_limit",
    "اظهر الحمل": "maternity_cover",
    "الحمل": "maternity_cover",
    "ما هي الاستثناءات الأساسية": "key_exclusions",
    "الاستثناءات الأساسية": "key_exclusions",
    "ما هي الشروط": "approval_rule_summary",
    "الشروط": "approval_rule_summary",
    "اظهر الأدوية": "pharmacy_cover_summary",
    "الأدوية": "pharmacy_cover_summary",
    "اظهر الشبكة": "network_name",
    "الشبكة": "network_name",
    "اظهر التغطية": "area_of_coverage",
    "التغطية": "area_of_coverage",
    "اظهر العلاج الطبيعي": "physiotherapy_cover_summary",
    "العلاج الطبيعي": "physiotherapy_cover_summary",
    "اظهر التحاليل": "diagnostics_cover_summary",
    "التحاليل": "diagnostics_cover_summary",
    "اظهر الموافقات": "approval_rule_summary",
    "الموافقات": "approval_rule_summary",
    "اظهر الإحالة": "referral_required",
    "الإحالة": "referral_required",
    "اظهر الحالات السابقة": "pre_existing_condition_rule",
    "الحالات السابقة": "pre_existing_condition_rule",
    "اظهر خارج الشبكة": "outside_network_rule",
    "خارج الشبكة": "outside_network_rule",
    "اظهر خارج الإمارات": "outside_uae_rule",
    "خارج الإمارات": "outside_uae_rule",
    "اظهر ملخص": "summary",
    "ملخص": "summary",
}

_SAFE_FALLBACK = "No deterministic answer is available for that query yet."

# Deterministic missing-plan messages
_MISSING_PLAN_MSG_EN = "Please specify the plan: Remedy 02 or Remedy 03."
_MISSING_PLAN_MSG_AR = "يرجى تحديد الخطة: Remedy 02 أو Remedy 03."

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_plan_cache: dict[str, dict[str, Any]] = {}


def _resolve_plan_key(name: str) -> Optional[str]:
    """Return the JSON filename for a plan alias, or None."""
    return _PLAN_ALIASES.get(name.strip().lower())


def _resolve_field(text: str) -> Optional[str]:
    """Return the canonical field name for owner-friendly text, or None."""
    key = text.strip().lower().replace("_", " ")
    if key in _FIELD_ALIASES:
        return _FIELD_ALIASES[key]
    # Try matching the canonical field name directly
    canon = text.strip().lower().replace(" ", "_")
    if canon in set(OWNER_FIELDS):
        return canon
    return None


def _format_value(field: str, value: Any) -> str:
    """Format a field value for owner-readable display."""
    if value is None:
        return "Not available"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        if not value:
            return "None listed"
        return "\n".join(f"  - {item}" for item in value)
    return str(value)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_plan(name: str, *, output_dir: Optional[Path] = None) -> dict[str, Any]:
    """Load and parse a plan by friendly name.  Returns the parsed dict.

    Raises ``ValueError`` if the plan name is not recognized or the file
    is missing.
    """
    filename = _resolve_plan_key(name)
    if filename is None:
        raise ValueError(
            f"Unknown plan: {name!r}. "
            f"Known plans: {', '.join(sorted(set(_PLAN_ALIASES.values())))}"
        )

    if filename in _plan_cache:
        return _plan_cache[filename]

    base = output_dir or OUTPUT_DIR
    path = base / filename
    if not path.exists():
        raise ValueError(f"Plan file not found: {path}")

    extraction = json.loads(path.read_text(encoding="utf-8"))
    parsed = parse_remedy_plan(extraction)
    _plan_cache[filename] = parsed
    return parsed


def available_plans() -> list[str]:
    """Return sorted list of unique plan filenames."""
    return sorted(set(_PLAN_ALIASES.values()))
# Friendly display labels for owner output


def clear_cache() -> None:
    """Clear the internal plan cache (useful in tests)."""
    _plan_cache.clear()


def get_plan_field(plan_name: str, field_name: str,
                   *, output_dir: Optional[Path] = None) -> dict[str, Any]:
    """Retrieve a single field from a plan.

    Returns a dict with keys: plan_code, field, label, value, formatted.
    """
    plan = load_plan(plan_name, output_dir=output_dir)
    field = _resolve_field(field_name)
    if field is None or field not in set(OWNER_FIELDS):
        return {
            "plan_code": plan.get("plan_code"),
            "field": field_name,
            "label": field_name,
            "value": None,
            "formatted": _SAFE_FALLBACK,
        }
    value = plan.get(field)
    return {
        "plan_code": plan.get("plan_code"),
        "field": field,
        "label": _FIELD_LABELS.get(field, field),
        "value": value,
        "formatted": _format_value(field, value),
    }


def compare_plans(plan_a_name: str, plan_b_name: str,
                  *, field_name: Optional[str] = None,
                  differences_only: bool = False,
                  output_dir: Optional[Path] = None) -> dict[str, Any]:
    """Compare two plans, optionally filtered to a specific field.

    Returns a dict with: plan_a_code, plan_b_code, and either a full
    comparison or a single-field comparison.
    """
    plan_a = load_plan(plan_a_name, output_dir=output_dir)
    plan_b = load_plan(plan_b_name, output_dir=output_dir)

    # Single-field comparison
    if field_name is not None:
        field = _resolve_field(field_name)
        if field is None or field not in set(OWNER_FIELDS):
            return {
                "plan_a_code": plan_a.get("plan_code"),
                "plan_b_code": plan_b.get("plan_code"),
                "field": field_name,
                "error": _SAFE_FALLBACK,
            }
        val_a = plan_a.get(field)
        val_b = plan_b.get(field)
        return {
            "plan_a_code": plan_a.get("plan_code"),
            "plan_b_code": plan_b.get("plan_code"),
            "field": field,
            "label": _FIELD_LABELS.get(field, field),
            "plan_a_value": val_a,
            "plan_b_value": val_b,
            "match": val_a == val_b,
            "plan_a_formatted": _format_value(field, val_a),
            "plan_b_formatted": _format_value(field, val_b),
        }

    # Full comparison using existing comparator
    raw = _raw_compare(plan_a, plan_b)

    if differences_only:
        return {
            "plan_a_code": raw["plan_a_code"],
            "plan_b_code": raw["plan_b_code"],
            "differences_only": True,
            "differing": {
                f: {
                    "label": _FIELD_LABELS.get(f, f),
                    "plan_a": _format_value(f, d["plan_a"]),
                    "plan_b": _format_value(f, d["plan_b"]),
                }
                for f, d in raw["differing"].items()
                if f in set(OWNER_FIELDS)
            },
        }

    # Full comparison — include matched + differing (owner fields only)
    owner_set = set(OWNER_FIELDS)
    return {
        "plan_a_code": raw["plan_a_code"],
        "plan_b_code": raw["plan_b_code"],
        "matched": [
            {"field": f, "label": _FIELD_LABELS.get(f, f),
             "value": _format_value(f, plan_a.get(f))}
            for f in raw["matched"] if f in owner_set
        ],
        "differing": {
            f: {
                "label": _FIELD_LABELS.get(f, f),
                "plan_a": _format_value(f, d["plan_a"]),
                "plan_b": _format_value(f, d["plan_b"]),
            }
            for f, d in raw["differing"].items()
            if f in owner_set
        },
    }


def summarize_plan(plan_name: str,
                   *, output_dir: Optional[Path] = None) -> dict[str, Any]:
    """Return a short owner-friendly summary of a plan."""
    plan = load_plan(plan_name, output_dir=output_dir)

    summary_fields = (
        "plan_name", "plan_code", "network_name", "annual_limit",
        "area_of_coverage", "direct_billing", "referral_required",
        "maternity_cover", "inpatient_cover_summary",
        "outpatient_cover_summary", "pharmacy_cover_summary",
    )
    lines: list[str] = []
    for f in summary_fields:
        label = _FIELD_LABELS.get(f, f)
        val = _format_value(f, plan.get(f))
        lines.append(f"{label}: {val}")

    excl_count = len(plan.get("key_exclusions", []))
    lines.append(f"Key Exclusions: {excl_count} listed")

    return {
        "plan_code": plan.get("plan_code"),
        "summary_text": "\n".join(lines),
        "field_count": len(summary_fields) + 1,
    }


# ---------------------------------------------------------------------------
# Natural-language intent mapper (deterministic, no AI)
# ---------------------------------------------------------------------------

# Patterns matched in order — first match wins
_COMPARE_PAT = re.compile(
    r"compare\b|difference|differ|vs\.?\b|versus|قارن|مقارنة|الفرق|ما الفرق",
    re.IGNORECASE,
)
_SUMMARY_PAT = re.compile(r"summar|overview|ملخص|اعطني ملخص|أعطني ملخص|عرض ملخص", re.IGNORECASE)
_PLAN_PAT = re.compile(
    r"remedy\s*0?[23]|hn-remedy-[23]",
    re.IGNORECASE,
)
_DIFF_ONLY_PAT = re.compile(
    r"difference|differ|only diff",
    re.IGNORECASE,
)


def _extract_plans(text: str) -> list[str]:
    """Extract plan references from free text."""
    return [m.group(0) for m in _PLAN_PAT.finditer(text)]


def _extract_field(text: str) -> Optional[str]:
    """Try to identify a field reference in the query text."""
    lower = text.lower()
    # Try longest alias first so "outside network" beats "network"
    for alias in sorted(_FIELD_ALIASES, key=len, reverse=True):
        if alias in lower:
            return _FIELD_ALIASES[alias]
    return None


def answer_owner_query(text: str,
                       *, output_dir: Optional[Path] = None) -> dict[str, Any]:
    """Route a plain-text owner question to the right handler."""
    # Out-of-scope provider/network lookup intent (strict precedence)
    if _PROVIDER_LOOKUP_PAT.search(text):
        return {
            "type": "unsupported",
            "message": _SAFE_FALLBACK,
        }
    plans = _extract_plans(text)
    field = _extract_field(text)
    is_compare = bool(_COMPARE_PAT.search(text))
    is_summary = bool(_SUMMARY_PAT.search(text))
    diff_only = bool(_DIFF_ONLY_PAT.search(text))

    # Compare intent (needs exactly 2 plans, or defaults to R02 vs R03)
    if is_compare:
        a = plans[0] if len(plans) >= 1 else "Remedy 02"
        b = plans[1] if len(plans) >= 2 else (
            "Remedy 03" if "02" in a or "2" in a else "Remedy 02"
        )
        return {
            "type": "compare",
            "result": compare_plans(
                a, b,
                field_name=field if field else None,
                differences_only=diff_only and field is None,
                output_dir=output_dir,
            ),
        }

    # Summary intent
    if is_summary and plans:
        return {
            "type": "summary",
            "result": summarize_plan(plans[0], output_dir=output_dir),
        }

    # Single-field intent
    if field:
        if plans:
            return {
                "type": "field",
                "result": get_plan_field(plans[0], field, output_dir=output_dir),
            }
        # Only return missing-plan message if the query is a supported field query (not provider/network intent)
        # Heuristic: if the field is in OWNER_FIELDS, it's a supported field query
        if field in OWNER_FIELDS:
            is_arabic = any(ord(c) >= 0x0600 for c in text)
            return {
                "type": "unsupported",
                "message": _MISSING_PLAN_MSG_AR if is_arabic else _MISSING_PLAN_MSG_EN,
            }
        # Otherwise, treat as unsupported (e.g., provider/network lookup)
        return {
            "type": "unsupported",
            "message": _SAFE_FALLBACK,
        }

    # Plan mentioned but no specific field or compare → summary
    if plans and not field and not is_compare:
        return {
            "type": "summary",
            "result": summarize_plan(plans[0], output_dir=output_dir),
        }

    # Unsupported
    return {
        "type": "unsupported",
        "message": _SAFE_FALLBACK,
    }
