"""
output_packaging.py — Controlled AI writing/presentation layer.

Formats already-approved deterministic plan outputs into business-friendly
client communication. No new facts are introduced. No inference. No LLM calls.

Supported output modes:
    whatsapp_summary   — compact, emoji-free, single-screen message
    email_summary      — structured, paragraph-style, professional tone
    benefit_explanation — per-benefit plain-language description

Safety constraints (enforced at every entry point):
    - Only fields present in the approved agent response data are rendered.
    - Fields that are None or "not available" are either omitted or replaced
      with the sentinel phrase "Not specified in plan data."
    - The text "REVIEW", "source_trace", "raw", "unapproved", "internal",
      "debug" must never appear in any packaged output.
    - No pricing invented, no benefits inferred.
    - If ok=False, all modes return a safe fallback refusal.
"""

from __future__ import annotations

from typing import Any, Optional

# ---------------------------------------------------------------------------
# Sentinel used when a field is absent or explicitly unavailable.
# Callers can check for this exact string to detect missing data.
# ---------------------------------------------------------------------------
_MISSING = "Not specified in plan data."

# Fields that must never be forwarded verbatim to packaged output.
_BLOCKED_FIELD_SUBSTRINGS = (
    "source_trace",
    "raw",
    "unapproved",
    "internal",
    "debug",
    "review",
)


def _safe(value: Any, fallback: str = _MISSING) -> str:
    """Return a safe string for `value`, or `fallback` if absent/unusable."""
    if value is None:
        return fallback
    s = str(value).strip()
    if not s or s.lower() in {"none", "not available", "n/a", ""}:
        return fallback
    # Block internal metadata leakage.
    sl = s.lower()
    if any(b in sl for b in _BLOCKED_FIELD_SUBSTRINGS):
        return fallback
    return s


def _yesno(value: Any) -> str:
    """Convert a boolean-ish field to 'Yes' / 'No' / _MISSING."""
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
    return _safe(value)


def _extract_data(agent_response: dict) -> dict:
    """Pull the data payload from any approved agent response dict."""
    data = agent_response.get("data") or {}
    if not isinstance(data, dict):
        data = {}
    return data


def _extract_core_fields(agent_response: dict) -> dict:
    """Return normalised core plan fields from an approved agent response."""
    data = _extract_data(agent_response)
    # plan_field responses nest facts inside data directly (label/value/formatted).
    # plan_core/summary responses expose fields at the top of data.
    return {
        "plan_name": _safe(data.get("plan_name") or agent_response.get("plan_name")),
        "plan_code": _safe(data.get("plan_code")),
        "network_name": _safe(data.get("network_name")),
        "annual_limit": _safe(data.get("annual_limit")),
        "area_of_coverage": _safe(data.get("area_of_coverage")),
        "direct_billing": _yesno(data.get("direct_billing")),
        "referral_required": _yesno(data.get("referral_required")),
        "maternity_cover": _safe(data.get("maternity_cover")),
        "pharmacy_cover": _safe(data.get("pharmacy_cover_summary")),
        "dental_cover": _safe(data.get("dental_cover_summary")),
        "mental_health_cover": _safe(data.get("mental_health_cover_summary")),
    }


# ---------------------------------------------------------------------------
# Safe refusal — used when ok=False or intent is unsupported.
# ---------------------------------------------------------------------------
_SAFE_REFUSAL = (
    "This information is not available or the query is not currently supported. "
    "Please contact an administrator or rephrase your request."
)


def _assert_approved(agent_response: dict) -> None:
    """Raise ValueError if the agent response is not approved for packaging."""
    if not agent_response.get("ok"):
        raise ValueError("not_approved")
    intent = agent_response.get("intent", "")
    allowed_intents = {
        "plan_core",
        "plan_summary",
        "plan_field",
        "plan_comparison",
    }
    if intent not in allowed_intents:
        raise ValueError(f"intent_not_packageable:{intent}")


# ---------------------------------------------------------------------------
# MODE 1 — whatsapp_summary
# ---------------------------------------------------------------------------

def whatsapp_summary(agent_response: dict) -> str:
    """
    Compact single-screen WhatsApp-style plan summary.

    Includes only fields that are present in the approved agent response.
    Returns a safe refusal string when ok=False or intent is unsupported.
    """
    try:
        _assert_approved(agent_response)
    except ValueError:
        return _SAFE_REFUSAL

    f = _extract_core_fields(agent_response)
    plan = f["plan_name"]
    lines: list[str] = []
    lines.append(f"Plan: {plan}")

    if f["network_name"] != _MISSING:
        lines.append(f"Network: {f['network_name']}")
    if f["annual_limit"] != _MISSING:
        lines.append(f"Annual Limit: {f['annual_limit']}")
    if f["direct_billing"] != _MISSING:
        lines.append(f"Direct Billing: {f['direct_billing']}")
    if f["referral_required"] != _MISSING:
        lines.append(f"Referral Required: {f['referral_required']}")
    if f["area_of_coverage"] != _MISSING:
        lines.append(f"Coverage Area: {f['area_of_coverage']}")
    if f["maternity_cover"] != _MISSING:
        lines.append(f"Maternity: {f['maternity_cover']}")
    if f["pharmacy_cover"] != _MISSING:
        lines.append(f"Pharmacy: {f['pharmacy_cover']}")
    if f["dental_cover"] != _MISSING:
        lines.append(f"Dental: {f['dental_cover']}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MODE 2 — email_summary
# ---------------------------------------------------------------------------

def email_summary(agent_response: dict, recipient_name: Optional[str] = None) -> str:
    """
    Professional email-style plan summary using only approved deterministic fields.

    `recipient_name` is an optional display-only label, not used for any fact lookup.
    Returns a safe refusal string when ok=False or intent is unsupported.
    """
    try:
        _assert_approved(agent_response)
    except ValueError:
        return _SAFE_REFUSAL

    f = _extract_core_fields(agent_response)
    plan = f["plan_name"]

    greeting = f"Dear {recipient_name}," if recipient_name else "Dear Valued Client,"
    intro = (
        f"Please find below the key details for the {plan} insurance plan "
        "as confirmed in our plan data."
    )

    sections: list[str] = []
    if f["annual_limit"] != _MISSING:
        sections.append(f"  Annual Limit: {f['annual_limit']}")
    if f["network_name"] != _MISSING:
        sections.append(f"  Provider Network: {f['network_name']}")
    if f["area_of_coverage"] != _MISSING:
        sections.append(f"  Coverage Area: {f['area_of_coverage']}")
    if f["direct_billing"] != _MISSING:
        sections.append(f"  Direct Billing (Cashless): {f['direct_billing']}")
    if f["referral_required"] != _MISSING:
        sections.append(f"  Referral Required: {f['referral_required']}")
    if f["maternity_cover"] != _MISSING:
        sections.append(f"  Maternity Benefit: {f['maternity_cover']}")
    if f["pharmacy_cover"] != _MISSING:
        sections.append(f"  Pharmacy Benefit: {f['pharmacy_cover']}")
    if f["dental_cover"] != _MISSING:
        sections.append(f"  Dental Benefit: {f['dental_cover']}")

    if not sections:
        body = "  Detailed field data is not yet available for this plan."
    else:
        body = "\n".join(sections)

    closing = (
        "Please note that the above information is based on the approved plan data. "
        "All final terms are subject to the official policy document."
    )
    footer = "Regards,\nNGI Health Insurance Team"

    return "\n\n".join([greeting, intro, body, closing, footer])


# ---------------------------------------------------------------------------
# MODE 3 — benefit_explanation
# ---------------------------------------------------------------------------

# Approved benefit keys and their plain-language templates.
# Only fields that already exist in deterministic output are referenced.
# Template strings use Python .format() with a single positional slot.
_BENEFIT_TEMPLATES: dict[str, str] = {
    "annual_limit": (
        "Under this plan, the total amount the insurer will pay for covered medical "
        "expenses in a policy year is {0}."
    ),
    "network": (
        "This plan operates on the {0} provider network. "
        "Members can access direct billing at providers within this network."
    ),
    "copay": (
        "A copayment (copay) is the portion of each eligible medical bill that the "
        "member pays directly at the point of service. "
        "The copay applicable under this plan is: {0}."
    ),
    "pharmacy": (
        "The pharmacy benefit under this plan covers prescription medications as follows: {0}."
    ),
    "maternity": (
        "The maternity benefit under this plan covers eligible pregnancy and delivery "
        "expenses as follows: {0}."
    ),
    "dental": (
        "The dental benefit under this plan covers eligible dental treatment as follows: {0}."
    ),
}

_BENEFIT_KEY_MAP: dict[str, str] = {
    # canonical key → data field
    "annual_limit": "annual_limit",
    "network": "network_name",
    "copay": "copay",          # may be absent; safe fallback applies
    "pharmacy": "pharmacy_cover",
    "maternity": "maternity_cover",
    "dental": "dental_cover",
}


def benefit_explanation(agent_response: dict, benefit_key: str) -> str:
    """
    Plain-language explanation for a single benefit field.

    `benefit_key` must be one of: annual_limit, network, copay, pharmacy, maternity, dental.
    Returns a safe refusal string when ok=False, intent is unsupported, the benefit key is
    invalid, or the fact is not present in the approved agent response.
    """
    try:
        _assert_approved(agent_response)
    except ValueError:
        return _SAFE_REFUSAL

    bkey = (benefit_key or "").strip().lower()
    if bkey not in _BENEFIT_TEMPLATES:
        return (
            f"The benefit '{benefit_key}' is not supported for explanation. "
            f"Supported keys: {', '.join(sorted(_BENEFIT_TEMPLATES))}."
        )

    f = _extract_core_fields(agent_response)

    # For plan_field responses, the fact may also be in data["formatted"] or data["value"].
    # Try the core field map first, then fall back to data payload directly.
    data_field = _BENEFIT_KEY_MAP[bkey]
    value = f.get(data_field, _MISSING)

    if value == _MISSING:
        # Secondary fallback: check data["formatted"] or data["value"] for plan_field responses.
        raw_data = _extract_data(agent_response)
        value = _safe(raw_data.get("formatted") or raw_data.get("value"))

    if value == _MISSING:
        return (
            f"The {bkey.replace('_', ' ')} information is not available in the current plan data."
        )

    template = _BENEFIT_TEMPLATES[bkey]
    return template.format(value)


# ---------------------------------------------------------------------------
# Convenience dispatcher — call any mode by name.
# ---------------------------------------------------------------------------

SUPPORTED_MODES = frozenset({"whatsapp_summary", "email_summary", "benefit_explanation"})


def format_output(
    agent_response: dict,
    mode: str,
    *,
    recipient_name: Optional[str] = None,
    benefit_key: Optional[str] = None,
) -> str:
    """
    Single entry point for the output packaging layer.

    Parameters
    ----------
    agent_response : dict
        The dict returned by `run_agent_wrapper()` (or equivalent approved source).
    mode : str
        One of: 'whatsapp_summary', 'email_summary', 'benefit_explanation'.
    recipient_name : str | None
        Optional name used only for the email greeting.
    benefit_key : str | None
        Required when mode='benefit_explanation'.

    Returns
    -------
    str
        Formatted output string. Never raises; returns safe refusal on all error paths.
    """
    m = (mode or "").strip().lower()
    if m not in SUPPORTED_MODES:
        return (
            f"Output mode '{mode}' is not supported. "
            f"Supported modes: {', '.join(sorted(SUPPORTED_MODES))}."
        )

    try:
        if m == "whatsapp_summary":
            return whatsapp_summary(agent_response)
        if m == "email_summary":
            return email_summary(agent_response, recipient_name=recipient_name)
        if m == "benefit_explanation":
            return benefit_explanation(agent_response, benefit_key or "")
    except Exception:
        return _SAFE_REFUSAL

    return _SAFE_REFUSAL
