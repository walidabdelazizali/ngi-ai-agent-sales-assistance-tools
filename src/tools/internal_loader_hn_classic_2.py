"""
Internal loader for HN_CLASSIC_2 from source_table.json
"""
import json
import os
from src.parsers.enhanced_plan_parser import parse_enhanced_plan
from src.validation.plan_validator import normalize_plan, validate_plan_ready
from src.schema.plan_schema import REQUIRED_FIELDS

HN_CLASSIC_2_SOURCE = "data/plans/raw/HN_CLASSIC_2/source_table.json"


def load_internal_hn_classic_2() -> dict:
    # Delegate to generic enhanced loader for Classic 2
    from src.tools.enhanced_plan_loader import load_enhanced_plan
    plan = load_enhanced_plan("Classic 2")
    # Patch source_trace to use forward slashes (legacy contract)
    if "source_trace" in plan:
        plan["source_trace"] = {k: v.replace("\\", "/") for k, v in plan["source_trace"].items()}
    return plan
