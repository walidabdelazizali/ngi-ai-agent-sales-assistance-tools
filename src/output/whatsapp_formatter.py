"""
whatsapp_formatter.py — Compact single-screen WhatsApp-style plan summary.

Mobile-first readability with deterministic formatting.
"""

from typing import Any

from src.output.shared_helpers import (
    _MISSING,
    _SAFE_REFUSAL,
    ENGLISH_LABELS,
    STANDARD_PLAN_FIELDS,
    assert_approved,
    build_label_value_line,
    build_lines_from_fields,
    clean_aed,
    extract_core_fields,
    join_lines,
    safe_value,
    clean_utf8
)

def whatsapp_summary(agent_response: dict) -> str:
    """
    Compact single-screen WhatsApp-style plan summary.
    
    Features:
    - Mobile-first readability
    - Deterministic field ordering
    - No duplicate labels
    - Clean spacing
    - Copy-paste friendly
    
    Returns safe refusal if response not approved.
    """
    try:
        assert_approved(agent_response, {"plan_core", "plan_summary", "plan_field"})
    except ValueError:
        return _SAFE_REFUSAL
    
    f = extract_core_fields(agent_response)
    
    # Build lines in deterministic order, filtering _MISSING
    lines = []
    
    # Always include plan name first
    plan_name = f.get("plan_name", _MISSING)
    if plan_name and plan_name != _MISSING:
        lines.append(f"Plan: {plan_name}")
    
    # Add other fields in standard order, skipping _MISSING
    field_order = ["network_name", "annual_limit", "direct_billing", "referral_required", "area_of_coverage", "maternity_cover", "pharmacy_cover", "dental_cover"]
    
    for field_key in field_order:
        value = f.get(field_key, _MISSING)
        if value and value != _MISSING:
            label = ENGLISH_LABELS.get(field_key, field_key)
            # Special handling for AED currency
            if field_key == "annual_limit":
                value = clean_aed(value)
            lines.append(f"{label}: {value}")
    
    # Join with newlines, enforce no excess spacing
    output = join_lines(lines, separator="\n")
    
    # Clean UTF-8 artifacts before returning
    output = clean_utf8(output) if output else _SAFE_REFUSAL
    return output
