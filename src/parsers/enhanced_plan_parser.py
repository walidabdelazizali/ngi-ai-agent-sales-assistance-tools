"""
Enhanced Plan Parser for HN_CLASSIC_2 (Classic 2)
Extracts only required canonical fields from structured table input.
Not integrated with plan_query or output pipeline yet.
"""
from typing import Dict, Any, List

REQUIRED_FIELDS = [
    "plan_name",
    "plan_code",
    "network_name",
    "annual_limit",
    "area_of_coverage",
    "direct_billing",
    "referral_required",
]

def parse_enhanced_plan(table: List[List[str]]) -> Dict[str, Any]:
    """
    Parse a structured table (list of rows) for HN_CLASSIC_2 and extract required fields.
    Expects table as list of [row_label, value] pairs or similar.
    """
    result = {
        "plan_name": None,
        "plan_code": "HN_CLASSIC_2",
        "network_name": None,
        "annual_limit": None,
        "area_of_coverage": None,
        "direct_billing": None,
        "referral_required": False,  # Master mapping: Direct
    }
    for row in table:
        if len(row) < 2:
            continue
        label, value = row[0].strip().lower(), row[1].strip()
        if "plan name" in label:
            # Normalize to canonical name
            result["plan_name"] = "Classic 2"
        elif "provider network" in label:
            # Normalize network name
            if "standard plus" in value.lower():
                result["network_name"] = "Standard Plus"
            else:
                result["network_name"] = value
        elif "maximum benefit per year" in label or "annual limit" in label:
            result["annual_limit"] = value
        elif "area of coverage" in label:
            result["area_of_coverage"] = value
        elif "direct billing available" in label or ("claims settlement" in label and "direct billing" in value.lower()):
            result["direct_billing"] = True
    # If direct_billing not found, set to False
    if result["direct_billing"] is None:
        result["direct_billing"] = False
    return result
