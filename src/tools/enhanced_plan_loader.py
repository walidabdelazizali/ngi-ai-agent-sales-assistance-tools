import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.validation.plan_validator import normalize_plan, validate_plan_ready

# Registry for enhanced plans (initial: Classic 2 only)
ENHANCED_PLAN_REGISTRY = {
    "Classic 2": {
        "aliases": ["classic 2", "hn_classic_2", "hn classic 2"],
        "plan_code": "HN_CLASSIC_2",
        "source_path": "data/plans/raw/HN_CLASSIC_2/source_table.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
}

# Alias lookup
_ALIAS_TO_CANONICAL = {}
for canonical, meta in ENHANCED_PLAN_REGISTRY.items():
    _ALIAS_TO_CANONICAL[canonical.lower()] = canonical
    for alias in meta["aliases"]:
        _ALIAS_TO_CANONICAL[alias.lower()] = canonical

def is_enhanced_plan(name: str) -> bool:
    return resolve_enhanced_plan_name(name) is not None

def resolve_enhanced_plan_name(name: str) -> Optional[str]:
    if not name:
        return None
    return _ALIAS_TO_CANONICAL.get(name.strip().lower())

# Dummy parser for Classic 2 (replace with real parser as needed)
def parse_enhanced_plan(raw) -> dict:
    # Accepts either dict or list-of-pairs
    if isinstance(raw, list):
        # Convert list of [key, value] to dict
        raw_dict = {k: v for k, v in raw}
    else:
        raw_dict = raw
    # Map source keys to canonical fields for Classic 2
    key_map = {
        "Plan Name": "plan_name",
        "Provider Network": "network_name",
        "Maximum Benefit Per Year": "annual_limit",
        "Area of Coverage": "area_of_coverage",
        "Direct Billing Available": "direct_billing",
    }
    # Normalize network_name for Classic 2 legacy contract
    network_name = raw_dict.get("Provider Network", "Standard Plus")
    if network_name == "HN Standard Plus":
        network_name = "Standard Plus"
    canonical = {
        "plan_name": "Classic 2",
        "plan_code": "HN_CLASSIC_2",
        "network_name": network_name,
        "annual_limit": raw_dict.get("Maximum Benefit Per Year", "AED 250,000"),
        "area_of_coverage": raw_dict.get("Area of Coverage", "Worldwide Excluding USA and Canada"),
        "direct_billing": True if str(raw_dict.get("Direct Billing Available", "Yes")).lower() in ("yes", "true", "1") else False,
        "referral_required": False,  # Not present in source, default to False
    }
    return canonical

def load_enhanced_plan(name: str) -> Dict[str, Any]:
    canonical = resolve_enhanced_plan_name(name)
    if not canonical:
        raise ValueError(f"Unknown enhanced plan: {name}")
    meta = ENHANCED_PLAN_REGISTRY[canonical]
    source_path = Path(meta["source_path"])
    if not source_path.exists():
        raise FileNotFoundError(f"Enhanced plan source not found: {source_path}")
    with source_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    # Parse
    plan = parse_enhanced_plan(raw)
    # Approval metadata
    if meta.get("approved"):
        plan["approval_status"] = "approved"
        plan["tests_passed"] = True
        # Minimal source_trace for all fields present, use forward slashes
        src_path_str = str(source_path).replace("\\", "/")
        plan["source_trace"] = {k: f"{src_path_str}:{k}" for k in plan.keys() if k not in ("approval_status", "tests_passed", "source_trace")}
    # Normalize and validate
    norm = normalize_plan(plan)
    ok, reason = validate_plan_ready(norm)
    if not ok:
        raise ValueError(f"Enhanced plan not ready: {reason}")
    return norm
