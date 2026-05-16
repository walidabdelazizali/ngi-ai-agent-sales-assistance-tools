"""
legacy_modes.py - Centralized implementations for legacy formatter modes.

These formatters are kept for backward-compatible output modes but are
implemented under src/output to keep a single formatter authority.
"""

from __future__ import annotations

from typing import Optional

from src.output.shared_helpers import (
    _MISSING,
    _SAFE_REFUSAL,
    assert_approved,
    extract_core_fields,
    extract_data,
    safe_value,
)


def email_summary(agent_response: dict, recipient_name: Optional[str] = None) -> str:
    """
    Professional email-style plan summary using only approved deterministic fields.

    Returns a safe refusal string when ok=False or intent is unsupported.
    """
    try:
        assert_approved(agent_response, {"plan_core", "plan_summary", "plan_field", "plan_comparison"})
    except ValueError:
        return _SAFE_REFUSAL

    f = extract_core_fields(agent_response)
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
    "annual_limit": "annual_limit",
    "network": "network_name",
    "network_name": "network_name",
    "copay": "copay",
    "pharmacy": "pharmacy_cover",
    "pharmacy_cover_summary": "pharmacy_cover",
    "maternity": "maternity_cover",
    "maternity_cover": "maternity_cover",
    "dental": "dental_cover",
    "dental_cover_summary": "dental_cover",
}


def _normalize_benefit_key(benefit_key: Optional[str]) -> str:
    """Map a field name, label, or alias to a supported benefit key."""
    raw = (benefit_key or "").strip().lower().replace("-", " ")
    if not raw:
        return ""
    if raw in _BENEFIT_TEMPLATES:
        return raw

    alias_map = {
        "annual limit": "annual_limit",
        "annual_limit": "annual_limit",
        "network name": "network",
        "network": "network",
        "copay": "copay",
        "copayment": "copay",
        "pharmacy cover": "pharmacy",
        "pharmacy cover summary": "pharmacy",
        "pharmacy_cover_summary": "pharmacy",
        "maternity cover": "maternity",
        "maternity cover summary": "maternity",
        "maternity_cover": "maternity",
        "dental cover": "dental",
        "dental cover summary": "dental",
        "dental_cover_summary": "dental",
    }
    return alias_map.get(raw, raw)


def benefit_explanation(agent_response: dict, benefit_key: str) -> str:
    """
    Plain-language explanation for a single benefit field.

    Returns a safe refusal string when ok=False, intent is unsupported, the
    benefit key is invalid, or the fact is not present in the approved response.
    """
    try:
        assert_approved(agent_response, {"plan_core", "plan_summary", "plan_field", "plan_comparison"})
    except ValueError:
        return _SAFE_REFUSAL

    bkey = _normalize_benefit_key(benefit_key)
    if bkey not in _BENEFIT_TEMPLATES:
        return (
            f"The benefit '{benefit_key}' is not supported for explanation. "
            f"Supported keys: {', '.join(sorted(_BENEFIT_TEMPLATES))}."
        )

    f = extract_core_fields(agent_response)
    data_field = _BENEFIT_KEY_MAP[bkey]
    value = f.get(data_field, _MISSING)

    if value == _MISSING:
        raw_data = extract_data(agent_response)
        value = safe_value(raw_data.get("formatted") or raw_data.get("value"))

    if value == _MISSING:
        return f"The {bkey.replace('_', ' ')} information is not available in the current plan data."

    return _BENEFIT_TEMPLATES[bkey].format(value)
