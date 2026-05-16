"""
compact_formatter.py — Single-line or highly condensed plan summary.

For scenarios where minimal space is critical.
"""

from typing import Any

from src.output.shared_helpers import (
    _MISSING,
    _SAFE_REFUSAL,
    ENGLISH_LABELS,
    assert_approved,
    clean_aed,
    clean_utf8,
    extract_core_fields,
    safe_value,
)


def compact_summary(agent_response: dict) -> str:
    """
    Single-line or condensed plan summary.
    
    Format: Plan Name | Network | Annual Limit | Direct Billing
    
    Features:
    - Minimal whitespace
    - Single separator (|) with no duplication
    - No duplicate labels
    - No trailing separators
    - Copy-paste friendly
    """
    try:
        assert_approved(agent_response, {"plan_core", "plan_summary", "plan_field"})
    except ValueError:
        return _SAFE_REFUSAL
    
    f = extract_core_fields(agent_response)
    
    # Build compact parts in order, skipping _MISSING
    parts = []
    
    # Plan name (always required)
    plan_name = f.get("plan_name", _MISSING)
    if plan_name and plan_name != _MISSING:
        parts.append(plan_name)
    
    # Add select fields for compact output
    for field_key in ["network_name", "annual_limit", "direct_billing"]:
        value = f.get(field_key, _MISSING)
        if value and value != _MISSING:
            # Special handling for AED
            if field_key == "annual_limit":
                value = clean_aed(value)
            parts.append(value)
    
    if not parts:
        return _SAFE_REFUSAL
    
    # Join with separator, ensure no duplication
    output = " | ".join(parts)
    
    # Remove any trailing separator
    output = output.rstrip(" |").strip()
    
    # Clean UTF-8 artifacts
    output = clean_utf8(output)
    return output
