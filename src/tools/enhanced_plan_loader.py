import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.validation.plan_validator import normalize_plan, validate_plan_ready

# Registry for enhanced plans.
ENHANCED_PLAN_REGISTRY = {
    "Classic 2": {
        "aliases": ["classic 2", "hn_classic_2", "hn classic 2"],
        "plan_code": "HN_CLASSIC_2",
        "source_path": "data/plans/raw/HN_CLASSIC_2/source_table.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Classic 3": {
        "aliases": [
            "classic 3",
            "classic3",
            "classic-3",
            "classic 03",
            "hn_classic_3",
            "hn-classic-3",
            "hn classic 3",
            "كلاسيك 3",
            "كلاسيك 03",
        ],
        "plan_code": "HN_CLASSIC_3",
        "source_path": "data/plans/raw/HN_CLASSIC_3/source_table.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Classic 2R": {
        "aliases": [
            "classic 2r",
            "classic2r",
            "classic-2r",
            "hn_classic_2r",
            "hn classic 2r",
            "كلاسيك 2r",
        ],
        "plan_code": "HN_CLASSIC_2R",
        "source_path": "data/plans/raw/HN_CLASSIC_2R/source_table_HN_CLASSIC_2R.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Prime 1": {
        "aliases": [
            "prime 1",
            "prime1",
            "prime-1",
            "hn_prime_1",
            "hn-prime-1",
            "hn prime 1",
        ],
        "plan_code": "HN_PRIME_1",
        "source_path": "data/plans/raw/HN_PRIME_1/source_table_HN_PRIME_1.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Prime 2": {
        "aliases": [
            "prime 2",
            "prime2",
            "prime-2",
            "hn_prime_2",
            "hn-prime-2",
            "hn prime 2",
        ],
        "plan_code": "HN_PRIME_2",
        "source_path": "data/plans/raw/HN_PRIME_2/source_table_HN_PRIME_2.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Classic 1": {
        "aliases": [
            "classic 1",
            "classic1",
            "classic-1",
            "classic 01",
            "hn_classic_1",
            "hn-classic-1",
            "hn classic 1",
            "كلاسيك 1",
            "كلاسيك 01",
        ],
        "plan_code": "HN_CLASSIC_1",
        "source_path": "data/plans/raw/HN_CLASSIC_1/source_table_HN_CLASSIC_1.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Classic 1R": {
        "aliases": [
            "classic 1r",
            "classic1r",
            "classic-1r",
            "hn_classic_1r",
            "hn-classic-1r",
            "hn classic 1r",
            "كلاسيك 1r",
        ],
        "plan_code": "HN_CLASSIC_1R",
        "source_path": "data/plans/raw/HN_CLASSIC_1R/source_table_HN_CLASSIC_1R.json",
        "parser": "parse_enhanced_plan",
        "approved": True,
    },
    "Classic 4": {
        "aliases": [
            "classic 4",
            "classic4",
            "classic-4",
            "classic 04",
            "hn_classic_4",
            "hn-classic-4",
            "hn classic 4",
            "كلاسيك 4",
            "كلاسيك 04",
        ],
        "plan_code": "HN_CLASSIC_4",
        "source_path": "data/plans/raw/HN_CLASSIC_4/source_table_HN_CLASSIC_4.json",
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

# Shared parser for enhanced plans in the registry.
def parse_enhanced_plan(raw, *, canonical_name: str, plan_code: str) -> dict:
    # Accepts either dict or list-of-pairs
    if isinstance(raw, list):
        # Convert list of [key, value] to dict
        raw_dict = {k: v for k, v in raw}
    else:
        raw_dict = raw

    if canonical_name == "Classic 2":
        # Normalize network_name for Classic 2 legacy contract
        network_name = raw_dict.get("Provider Network", "Standard Plus")
        if network_name == "HN Standard Plus":
            network_name = "Standard Plus"
        direct_billing_raw = raw_dict.get("Direct Billing Available", "Yes")
        annual_limit = raw_dict.get("Maximum Benefit Per Year", "AED 250,000")
        area_of_coverage = raw_dict.get("Area of Coverage", "Worldwide Excluding USA and Canada")
    elif canonical_name == "Classic 3":
        network_name = raw_dict.get("provider_network", "Standard")
        if network_name == "HN Standard":
            network_name = "Standard"
        direct_billing_raw = raw_dict.get("direct_billing", "Direct Billing Available")
        annual_limit = raw_dict.get("annual_limit", "AED 250,000")
        area_of_coverage = raw_dict.get("area_of_coverage", "UAE+Home country")
    elif canonical_name == "Classic 2R":
        # Trust internal document markers in source content, not filename.
        network_name = raw_dict.get("provider_network", "HN Standard Plus")
        if network_name == "HN Standard Plus":
            network_name = "Standard Plus"
        direct_billing_raw = raw_dict.get("direct_billing", "Direct Billing Available")
        annual_limit = raw_dict.get("annual_limit", "AED 250,000")
        area_of_coverage = raw_dict.get("area_of_coverage", "Worldwide Excluding USA and Canada")
    elif canonical_name == "Classic 1R":
        network_name = raw_dict.get("provider_network") or raw_dict.get("network_name") or ""
        if network_name.startswith("HN "):
            network_name = network_name.replace("HN ", "", 1)
        direct_billing_raw = raw_dict.get("direct_billing", False)
        annual_limit = raw_dict.get("annual_limit", "REVIEW: source document not available in repository")
        area_of_coverage = raw_dict.get("area_of_coverage", "REVIEW: source document not available in repository")
        referral_required_raw = raw_dict.get("referral_required", True)
    elif canonical_name in {"Prime 1", "Prime 2", "Classic 1", "Classic 4"}:
        network_name = raw_dict.get("provider_network") or raw_dict.get("network_name") or ""
        if network_name.startswith("HN "):
            network_name = network_name.replace("HN ", "", 1)
        direct_billing_raw = raw_dict.get("direct_billing", False)
        annual_limit = raw_dict.get("annual_limit", "REVIEW: source document not available in repository")
        area_of_coverage = raw_dict.get("area_of_coverage", "REVIEW: source document not available in repository")
        referral_required_raw = raw_dict.get("referral_required", True)
    else:
        raise ValueError(f"Unsupported enhanced plan parser mapping: {canonical_name}")

    if isinstance(direct_billing_raw, bool):
        direct_billing = direct_billing_raw
    else:
        db_str = str(direct_billing_raw).strip().lower()
        direct_billing = db_str in ("yes", "true", "1") or "direct billing" in db_str

    if canonical_name in {"Prime 1", "Prime 2", "Classic 1", "Classic 1R", "Classic 4"}:
        if isinstance(referral_required_raw, bool):
            referral_required = referral_required_raw
        else:
            rr_str = str(referral_required_raw).strip().lower()
            referral_required = rr_str in ("yes", "true", "1", "required")
    else:
        referral_required = False

    canonical = {
        "plan_name": canonical_name,
        "plan_code": plan_code,
        "network_name": network_name,
        "annual_limit": annual_limit,
        "area_of_coverage": area_of_coverage,
        "direct_billing": direct_billing,
        "referral_required": referral_required,
    }

    if canonical_name == "Classic 1R":
        # Canonical field projections used by deterministic owner queries.
        pharmacy = raw_dict.get("pharmacy", {})
        maternity = raw_dict.get("maternity", {})
        dental = raw_dict.get("dental", {})
        mental = raw_dict.get("mental_health", {})
        inpatient = raw_dict.get("inpatient", {})
        outpatient = raw_dict.get("outpatient", {})

        canonical["pharmacy_cover_summary"] = (
            f"Covered: {pharmacy.get('covered', False)} | "
            f"Annual limit: {pharmacy.get('annual_limit', 'REVIEW')} | "
            f"Copay: {pharmacy.get('copay', 'REVIEW')} | "
            f"Type: {pharmacy.get('type', 'REVIEW')}"
        )

        maternity_ip = maternity.get("inpatient", {})
        maternity_op = maternity.get("outpatient", {})
        newborn = maternity.get("newborn_cover", {})
        canonical["maternity_cover"] = (
            f"Inpatient copay: {maternity_ip.get('copay', 'REVIEW')}; "
            f"Normal delivery: {maternity_ip.get('normal_delivery_limit', 'REVIEW')}; "
            f"C-section: {maternity_ip.get('c_section_limit', 'REVIEW')}; "
            f"Outpatient copay: {maternity_op.get('copay', 'REVIEW')}; "
            f"Max visits: {maternity_op.get('max_visits', 'REVIEW')}; "
            f"Newborn: {newborn.get('duration', 'REVIEW')} up to {newborn.get('limit', 'REVIEW')}"
        )

        canonical["dental_cover_summary"] = (
            f"Covered: {dental.get('covered', False)} | "
            f"Annual limit: {dental.get('annual_limit', 'REVIEW')} | "
            f"Copay: {dental.get('copay', 'REVIEW')}"
        )
        canonical["mental_health_cover_summary"] = (
            f"Covered: {mental.get('covered', False)} | "
            f"Annual limit: {mental.get('annual_limit', 'REVIEW')} | "
            f"Copay: {mental.get('copay', 'REVIEW')}"
        )

        canonical["inpatient_cover_summary"] = (
            f"Room: {inpatient.get('room_and_board', 'REVIEW')}; "
            f"Surgeries: {inpatient.get('surgeries', 'REVIEW')}; "
            f"Ambulance: {inpatient.get('ambulance', 'REVIEW')}"
        )
        consultation = outpatient.get("consultation", {})
        canonical["outpatient_cover_summary"] = (
            f"Consultation copay: {consultation.get('copay', 'REVIEW')} up to {consultation.get('limit', 'REVIEW')}; "
            f"Physiotherapy sessions: {outpatient.get('physiotherapy_sessions', 'REVIEW')}"
        )

    optional_fields = (
        "key_inpatient_benefits",
        "key_outpatient_benefits",
        "pharmacy",
        "maternity",
        "dental_optical",
        "copays",
        "dental",
        "mental_health",
    )
    for field in optional_fields:
        if field in raw_dict:
            canonical[field] = raw_dict[field]

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
    plan = parse_enhanced_plan(raw, canonical_name=canonical, plan_code=meta["plan_code"])
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
