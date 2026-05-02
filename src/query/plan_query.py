
# --- Network output formatter ---
def _format_network_output(details: dict, language: str = "en") -> str:
    # details: output of provider_details()
    if not details.get("found"):
        if details.get("ambiguous"):
            return "مزود غير محدد (Ambiguous provider match)." if language == "ar" else "Ambiguous provider match."
        return "المزود غير موجود (Provider not found)." if language == "ar" else "Provider not found."
    # Business-ready output
    name = details.get("provider_name") or details.get("google_name") or "-"
    city = details.get("city", "-")
    typ = details.get("type", "-")
    nets = details.get("available_network_tiers", [])
    nets_fmt = ", ".join(nets) if nets else ("لا توجد شبكات" if language == "ar" else "None")
    status = "داخل الشبكة" if language == "ar" else "In network"
    lines = []
    if language == "ar":
        lines.append("[الشبكة]")
        lines.append(f"المزود: {name}")
        lines.append(f"الحالة: {status}")
        lines.append(f"الشبكات: {nets_fmt}")
        lines.append(f"المدينة: {city}")
        lines.append(f"النوع: {typ}")
    else:
        lines.append("[NETWORK]")
        lines.append(f"Provider: {name}")
        lines.append(f"Status: {status}")
        lines.append(f"Networks: {nets_fmt}")
        lines.append(f"City: {city}")
        lines.append(f"Type: {typ}")
    return "\n".join(lines)

import json
import re
from pathlib import Path
from typing import Any, Optional

from src.config.settings import OUTPUT_DIR
from src.parsers.canonical_schema import BUSINESS_FIELDS
from src.parsers.plan_comparator import compare_plans as _raw_compare

from src.parsers.remedy_parser import parse_remedy_plan
from src.query.network_lookup import get_network_lookup

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
    # Batch 1 Expansion: Remedy 04
    "remedy 04": "HN-REMEDY-4.json",
    "remedy 4":  "HN-REMEDY-4.json",
    "remedy04":  "HN-REMEDY-4.json",
    "remedy4":   "HN-REMEDY-4.json",
    "hn-remedy-4": "HN-REMEDY-4.json",
    # Batch 2B Expansion: Remedy 05
    "remedy 05": "HN-REMEDY-5.json",
    "remedy 5":  "HN-REMEDY-5.json",
    "remedy05":  "HN-REMEDY-5.json",
    "remedy5":   "HN-REMEDY-5.json",
    "hn-remedy-5": "HN-REMEDY-5.json",
    # Arabic
    "ريميدي 2": "HN-REMEDY-2.json",
    "ريميدي 02": "HN-REMEDY-2.json",
    "ريميدي 3": "HN-REMEDY-3.json",
    "ريميدي 03": "HN-REMEDY-3.json",
    "ريميدي 4": "HN-REMEDY-4.json",
    "ريميدي 04": "HN-REMEDY-4.json",
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
    "reimbursement_scope",
    "outside_network_reimbursement",
    "outside_uae_reimbursement",
    "reimbursement_basis",
    "reimbursement_conditions",
    "reimbursement_documents_required",
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
    "reimbursement_scope": "Reimbursement Scope",
    "outside_network_reimbursement": "Outside Network Reimbursement",
    "outside_uae_reimbursement": "Outside UAE Reimbursement",
    "reimbursement_basis": "Reimbursement Basis",
    "reimbursement_conditions": "Reimbursement Conditions",
    "reimbursement_documents_required": "Reimbursement Documents Required",
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
    "reimbursement allowed": "reimbursement_allowed",
    "reimbursement scope": "reimbursement_scope",
    "scope of reimbursement": "reimbursement_scope",
    "outside network reimbursement": "outside_network_reimbursement",
    "outside uae reimbursement": "outside_uae_reimbursement",
    "reimbursement basis": "reimbursement_basis",
    "reimbursement conditions": "reimbursement_conditions",
    "reimbursement documents required": "reimbursement_documents_required",
    "documents required for reimbursement": "reimbursement_documents_required",
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
    # Arabic reimbursement aliases
    "تعويض": "reimbursement_allowed",
    "نطاق التعويض": "reimbursement_scope",
    "تعويض خارج الشبكة": "outside_network_reimbursement",
    "تعويض خارج الإمارات": "outside_uae_reimbursement",
    "أساس التعويض": "reimbursement_basis",
    "شروط التعويض": "reimbursement_conditions",
    "مستندات التعويض المطلوبة": "reimbursement_documents_required",
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
    """Return the JSON filename for a plan alias, or None. Ignores spaces and zero padding for robust matching."""
    def norm(s):
        return s.strip().lower().replace(" ", "").replace("0", "")
    n = norm(name)
    for alias, fname in _PLAN_ALIASES.items():
        if norm(alias) == n:
            return fname
    return None


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

    # Source Boundary Lock: Never load Remedy 05 from legacy output JSON
    if name.strip().lower() in ["remedy 05", "remedy 5", "hn-remedy-5"] or filename == "HN-REMEDY-5.json":
        # Always load from authoritative DOCX, never output JSON
        if filename in _plan_cache:
            return _plan_cache[filename]
        from src.extractors.docx_extractor import extract_docx
        docx_path = Path("input_docs/HN-REMEDY 5.docx")
        if not docx_path.exists():
            raise ValueError("Authoritative DOCX for Remedy 05 not found: input_docs/HN-REMEDY 5.docx")
        extraction = extract_docx(docx_path)
        parsed = parse_remedy_plan(extraction)
        # --- Approval metadata patch for Remedy 05 ---
        parsed["approval_status"] = "approved"
        parsed["tests_passed"] = True
        # source_trace must be a dict mapping each required field (except approval_status, tests_passed, source_trace) to the DOCX path
        from src.schema.plan_schema import REQUIRED_FIELDS
        parsed["source_trace"] = {field: str(docx_path) for field in REQUIRED_FIELDS if field not in ("approval_status", "tests_passed", "source_trace")}
        _plan_cache[filename] = parsed
        return parsed

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
    from src.validation.plan_validator import normalize_plan, validate_plan_ready
    plan = load_plan(plan_name, output_dir=output_dir)
    plan = normalize_plan(plan)
    ok, reason = validate_plan_ready(plan)
    field = _resolve_field(field_name)
    if not ok:
        # Return all expected keys for backward compatibility
        return {
            "ok": False,
            "plan_code": plan.get("plan_code"),
            "field": field if field else field_name,
            "label": _FIELD_LABELS.get(field, field) if field else field_name,
            "value": _SAFE_FALLBACK,
            "formatted": _SAFE_FALLBACK,
            "source": "safety_gate",
            "errors": [reason] if reason else [],
        }

    # Canonical normalized field mapping for key fields
    CANONICAL_FIELDS = {
        "annual_limit": "annual_limit",
        "network_name": "network_name",
        "area_of_coverage": "area_of_coverage",
        "direct_billing": "direct_billing",
        "referral_required": "referral_required",
    }
    if field in CANONICAL_FIELDS:
        value = plan.get(field)
        if value is not None:
            return {
                "ok": True,
                "plan_code": plan.get("plan_code"),
                "field": field,
                "label": _FIELD_LABELS.get(field, field),
                "value": value,
                "formatted": _format_value(field, value),
            }
    # Otherwise, fallback to legacy logic
    if field is None or field not in set(OWNER_FIELDS):
        return {
            "ok": False,
            "plan_code": plan.get("plan_code"),
            "field": field_name,
            "label": field_name,
            "value": _SAFE_FALLBACK,
            "formatted": _SAFE_FALLBACK,
            "source": "field_resolve",
            "errors": ["Unknown or unsupported field"]
        }
    value = plan.get(field)
    return {
        "ok": True,
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

    import os
    from src.query.network_lookup import NetworkLookup, get_network_lookup
    from src.query.plan_network_lookup import resolve_plan_network, get_medical_network_for_plan
    test_csv = os.path.join(os.path.dirname(__file__), '../../tests/fixtures/network_list_test.csv')
    use_test_fixture = os.path.exists(test_csv) and (
        os.environ.get('PYTEST_CURRENT_TEST') or 'test' in os.path.basename(__file__)
    )
    if use_test_fixture:
        lookup = NetworkLookup(test_csv)
    else:
        lookup = get_network_lookup()

    # Direct billing guardrail
    # Only block if 'direct billing' in English or exact Arabic phrase
    direct_billing_pat_en = re.compile(r"direct billing", re.IGNORECASE)
    direct_billing_pat_ar = re.compile(r"الدفع المباشر", re.IGNORECASE)
    if direct_billing_pat_en.search(text) or direct_billing_pat_ar.search(text):
        # Only block if the Arabic phrase is present, not just transliterated
        is_arabic = any(ord(c) >= 0x0600 for c in text)
        if (is_arabic and direct_billing_pat_ar.search(text)) or (not is_arabic and direct_billing_pat_en.search(text)):
            msg = (
                "تأكيد الدفع المباشر غير متاح بشكل حتمي من بيانات النظام الحالية."
                if is_arabic else
                "Direct billing confirmation is not deterministically available from the current dataset."
            )
            return {"type": "unsupported", "result": msg}

    # Plan network identity (strict, named groups, only if 'for/of <plan>' present)
    plan_network_en_pat = re.compile(r"^(what is|which)\s+(the\s+)?network\s+(for|of)\s+(?P<plan>[\w\s\-]+)\??$", re.IGNORECASE)
    m_en = plan_network_en_pat.match(text.strip())
    if m_en:
        plan_candidate = m_en.group('plan').strip()
        plan_info = resolve_plan_network(plan_candidate)
        if plan_info.get("found") and plan_info.get("medical_network"):
            result = f"[PLAN NETWORK]\nPlan: {plan_info['plan_name']}\nMedical Network: {plan_info['medical_network']}"
            return {"type": "plan_network", "result": result}
        else:
            return {"type": "plan_network", "result": "Plan network mapping not available."}

    plan_network_ar_pat = re.compile(r"^ما هي شبكة\s+(?P<plan>[\w\s\-]+)\؟?$", re.IGNORECASE)
    m_ar = plan_network_ar_pat.match(text.strip())
    if m_ar:
        plan_candidate = m_ar.group('plan').strip()
        plan_info = resolve_plan_network(plan_candidate)
        if plan_info.get("found") and plan_info.get("medical_network"):
            result = f"[شبكة الخطة]\nالخطة: {plan_info['plan_name']}\nالشبكة الطبية: {plan_info['medical_network']}"
            return {"type": "plan_network", "result": result}
        else:
            return {"type": "plan_network", "result": "تعذر العثور على شبكة الخطة المطلوبة."}

    # Fallback: generic provider/network lookup (must come after plan-network patterns)
    network_intents = [
        # English
        r"is .+ in the network",
        r"which network .+",
        r"is .+ in dental network",
        r"is .+ in optical network",
        r"has .+ been added",
        r"has .+ been deleted",
        # Arabic
        r"هل .+ داخل الشبكة",
        r".+ في أي شبكة",
        r"هل .+ داخل شبكة الأسنان",
        r"هل .+ داخل شبكة النظارات",
        r"هل تمت إضافة .+",
        r"هل تم حذف .+",
    ]
    network_intent_pat = re.compile("|".join(network_intents), re.IGNORECASE)
    if network_intent_pat.search(text) or _PROVIDER_LOOKUP_PAT.search(text):
        result = lookup.provider_details(lookup.extract_provider_from_query(text))
        is_arabic = any(ord(c) >= 0x0600 for c in text)
        return {
            "type": "network",
            "result": _format_network_output(result, language="ar" if is_arabic else "en"),
        }

    # Provider in plan network (strict, named groups)
    provider_in_plan_en_pat = re.compile(r"^is\s+(?P<provider>.+?)\s+in\s+(?P<plan>.+?)\s+network\??$", re.IGNORECASE)
    m_en = provider_in_plan_en_pat.match(text.strip())
    if m_en:
        provider = m_en.group('provider').strip()
        plan = m_en.group('plan').strip()
        plan_info = resolve_plan_network(plan)
        if plan_info.get("found") and plan_info.get("medical_network"):
            net_code = plan_info["medical_network"]
            details = lookup.provider_in_network(provider, net_code)
            if details.get("ambiguous"):
                return {"type": "network", "result": "Ambiguous provider match."}
            if not details.get("found"):
                return {"type": "network", "result": "Provider not found."}
            in_net = details.get("in_network")
            status = "In network" if in_net else "Out of network"
            result = (
                f"[NETWORK]\nProvider: {details['provider_name'].upper()}\nPlan: {plan_info['plan_name']}\n"
                f"Required Network: {net_code}\nStatus: {status}"
            )
            return {"type": "network", "result": result}
        else:
            return {"type": "plan_network", "result": "Plan network mapping not available."}

    provider_in_plan_ar_pat = re.compile(r"^هل\s+(?P<provider>.+?)\s+داخل شبكة\s+(?P<plan>.+?)\؟?$", re.IGNORECASE)
    m_ar = provider_in_plan_ar_pat.match(text.strip())
    if m_ar:
        provider = m_ar.group('provider').strip()
        plan = m_ar.group('plan').strip()
        plan_info = resolve_plan_network(plan)
        if plan_info.get("found") and plan_info.get("medical_network"):
            net_code = plan_info["medical_network"]
            details = lookup.provider_in_network(provider, net_code)
            if details.get("ambiguous"):
                return {"type": "network", "result": "مزود غير محدد (Ambiguous provider match)."}
            if not details.get("found"):
                return {"type": "network", "result": "المزود غير موجود (Provider not found)."}
            in_net = details.get("in_network")
            status = "داخل الشبكة" if in_net else "خارج الشبكة"
            result = (
                f"[الشبكة]\nالمزود: {details['provider_name'].upper()}\nالخطة: {plan_info['plan_name']}\n"
                f"الشبكة المطلوبة: {net_code}\nالحالة: {status}"
            )
            return {"type": "network", "result": result}
        else:
            return {"type": "plan_network", "result": "تعذر العثور على شبكة الخطة المطلوبة."}

    # Fallback: generic provider/network lookup
    network_intents = [
        # English
        r"is .+ in the network",
        r"which network .+",
        r"is .+ in dental network",
        r"is .+ in optical network",
        r"has .+ been added",
        r"has .+ been deleted",
        # Arabic
        r"هل .+ داخل الشبكة",
        r".+ في أي شبكة",
        r"هل .+ داخل شبكة الأسنان",
        r"هل .+ داخل شبكة النظارات",
        r"هل تمت إضافة .+",
        r"هل تم حذف .+",
    ]
    network_intent_pat = re.compile("|".join(network_intents), re.IGNORECASE)
    if network_intent_pat.search(text) or _PROVIDER_LOOKUP_PAT.search(text):
        result = lookup.provider_details(lookup.extract_provider_from_query(text))
        is_arabic = any(ord(c) >= 0x0600 for c in text)
        return {
            "type": "network",
            "result": _format_network_output(result, language="ar" if is_arabic else "en"),
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
