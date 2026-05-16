"""
arabic_formatter.py — Arabic-language plan and comparison summaries.

Deterministic Arabic formatting with centralized labels.
"""

from typing import Any, Optional
import re

from src.output.shared_helpers import (
    _MISSING,
    _SAFE_REFUSAL,
    ARABIC_LABELS,
    COMPARISON_FIELDS,
    REIMBURSEMENT_FIELDS,
    STANDARD_PLAN_FIELDS,
    assert_approved,
    clean_aed,
    clean_utf8,
    extract_core_fields,
    extract_reimbursement_fields,
    join_lines,
    safe_value,
)


def arabic_plan_summary(agent_response: dict) -> str:
    """
    Arabic-language plan summary with deterministic field ordering.
    
    Features:
    - Centralized Arabic labels
    - Standard field ordering
    - No duplicate labels
    - Mobile-friendly spacing
    """
    try:
        assert_approved(agent_response, {"plan_core", "plan_summary", "plan_field"})
    except ValueError:
        return _SAFE_REFUSAL
    
    f = extract_core_fields(agent_response)
    
    lines = []
    
    # Build in standard plan field order
    for field_key in STANDARD_PLAN_FIELDS:
        value = f.get(field_key, _MISSING)
        if value and value != _MISSING:
            label = ARABIC_LABELS.get(field_key, field_key)
            # Special handling for AED
            if field_key == "annual_limit":
                value = clean_aed(value)
            lines.append(f"{label}: {value}")
    
    output = join_lines(lines, separator="\n")
    return output if output else _SAFE_REFUSAL


def arabic_reimbursement_summary(agent_response: dict) -> str:
    """Arabic reimbursement rules summary."""
    try:
        assert_approved(agent_response, {"reimbursement_rules"})
    except ValueError:
        return _SAFE_REFUSAL
    
    f = extract_reimbursement_fields(agent_response)
    
    lines = []
    
    for field_key in REIMBURSEMENT_FIELDS:
        value = f.get(field_key, _MISSING)
        if value and value != _MISSING:
            label = ARABIC_LABELS.get(field_key, field_key)
            lines.append(f"{label}: {value}")
    
    output = join_lines(lines, separator="\n")
    return output if output else _SAFE_REFUSAL


def arabic_comparison_summary(comparison_message: str, plan1_name: str, plan2_name: str) -> str:
    """
    Parse English comparison message and render in Arabic.
    
    Converts field labels and Yes/No values to Arabic equivalents.
    """
    if not comparison_message or not plan1_name or not plan2_name:
        return _SAFE_REFUSAL
    
    lines = comparison_message.splitlines()
    if not lines:
        return _SAFE_REFUSAL
    
    # Field label mapping for comparison output
    ar_field_map = {
        "Annual Limit": "الحد السنوي",
        "Network": "الشبكة",
        "Area of Coverage": "نطاق التغطية",
        "Direct Billing": "الدفع المباشر",
        "Referral Required": "الإحالة مطلوبة",
        "Reimbursement Allowed": "التعويض متاح",
        "Coverage Area": "نطاق التغطية",
    }
    
    ar_yesno = {"Yes": "نعم", "No": "لا"}
    
    # Parse header and build Arabic comparison header
    header = lines[0]
    m = re.match(r"Comparison between (.+) and (.+):", header)
    
    if not m:
        return _SAFE_REFUSAL
    
    # Use provided plan names (cleaned)
    p1_clean = clean_utf8(plan1_name)
    p2_clean = clean_utf8(plan2_name)
    
    out = [f"مقارنة بين {p1_clean} و {p2_clean}:"]
    
    # Parse and translate comparison rows
    for line in lines[1:]:
        if not line.strip():
            continue
        
        if ":" in line and "|" in line:
            # Split on first colon to get label
            label, rest = line.split(":", 1)
            label = label.strip()
            
            # Map to Arabic label if available
            ar_label = ar_field_map.get(label, label)
            
            # Split values on pipe
            vals = rest.split("|")
            if len(vals) == 2:
                v1 = vals[0].split(":", 1)[-1].strip()
                v2 = vals[1].split(":", 1)[-1].strip()
                
                # Clean UTF-8 artifacts
                v1 = clean_utf8(v1)
                v2 = clean_utf8(v2)
                
                # Translate Yes/No
                if label in ["Direct Billing", "Referral Required", "Reimbursement Allowed"]:
                    v1 = ar_yesno.get(v1, v1)
                    v2 = ar_yesno.get(v2, v2)
                
                # Clean AED
                v1 = clean_aed(v1)
                v2 = clean_aed(v2)
                
                out.append(f"{ar_label}: {p1_clean}: {v1} | {p2_clean}: {v2}")
        else:
            # Non-comparison line, just add it
            out.append(clean_utf8(line))
    
    result = join_lines(out, separator="\n")
    return result if result and len(out) > 1 else _SAFE_REFUSAL
