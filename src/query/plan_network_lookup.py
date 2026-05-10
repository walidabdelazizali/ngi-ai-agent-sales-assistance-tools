import csv
from pathlib import Path
from typing import Optional, Dict

from src.tools.enhanced_plan_loader import load_enhanced_plan
from src.v2_plan_loader import load_clean_plan

MAPPING_CSV = Path(__file__).parent.parent.parent / "data/plans/plan_network_mapping.csv"

APPROVED_PLAN_CODES = {
    "Prime 1": "HN_PRIME_1",
    "Prime 2": "HN_PRIME_2",
    "Classic 1": "HN_CLASSIC_1",
    "Classic 1R": "HN_CLASSIC_1R",
    "Classic 4": "HN_CLASSIC_4",
    "Remedy 02": "HN-REMEDY-2",
    "Remedy 03": "HN-REMEDY-3",
    "Remedy 04": "HN-REMEDY-4",
    "Remedy 05": "HN-REMEDY-5",
    "Remedy 06": "HN-REMEDY-6",
    "Classic 2": "HN_CLASSIC_2",
    "Classic 2R": "HN_CLASSIC_2R",
    "Classic 3": "HN_CLASSIC_3",
}

APPROVED_PLAN_LOADERS = {
    "Prime 1": "enhanced",
    "Prime 2": "enhanced",
    "Classic 1": "enhanced",
    "Classic 1R": "enhanced",
    "Classic 4": "enhanced",
    "Remedy 02": "clean",
    "Remedy 03": "clean",
    "Remedy 04": "clean",
    "Remedy 05": "clean",
    "Remedy 06": "clean",
    "Classic 2": "enhanced",
    "Classic 2R": "enhanced",
    "Classic 3": "enhanced",
}

# Load mapping as a list of dicts
def load_plan_network_mapping(csv_path: Optional[Path] = None):
    path = csv_path or MAPPING_CSV
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def _normalize_plan_name(name: str) -> str:
    return name.strip().lower().replace(" ", "").replace("-", "").replace("_", "")


def _normalize_network_code(network_name: Optional[str]) -> Optional[str]:
    lowered = (network_name or "").strip().lower()
    if not lowered:
        return None
    if lowered in {
        "hn_basic_plus",
        "hn_basic",
        "hn_premier",
        "hn_elite",
        "hn_standard_plus",
        "hn_standard",
        "hn_advantage",
        "hn_advantage_plus",
    }:
        return lowered
    if "advantage plus" in lowered:
        return "hn_advantage_plus"
    if lowered == "advantage" or lowered.startswith("hn advantage") or "advantage network" in lowered:
        return "hn_advantage"
    if "basic plus" in lowered:
        return "hn_basic_plus"
    if "standard plus" in lowered:
        return "hn_standard_plus"
    if lowered == "standard" or lowered.startswith("hn standard") or "standard network" in lowered:
        return "hn_standard"
    if "premier" in lowered:
        return "hn_premier"
    if lowered == "basic" or lowered.startswith("hn basic"):
        return "hn_basic"
    if "elite" in lowered:
        return "hn_elite"
    return None


def _find_csv_row(plan_name_or_code: str, csv_path: Optional[Path] = None) -> Optional[Dict[str, str]]:
    norm = _normalize_plan_name(plan_name_or_code)
    for row in load_plan_network_mapping(csv_path):
        if _normalize_plan_name(row["plan_name"]) == norm or _normalize_plan_name(row["plan_code"]) == norm:
            return row
    return None


def _find_approved_plan(plan_name_or_code: str) -> Optional[str]:
    norm = _normalize_plan_name(plan_name_or_code)
    for canonical, plan_code in APPROVED_PLAN_CODES.items():
        if norm in {_normalize_plan_name(canonical), _normalize_plan_name(plan_code)}:
            return canonical
    return None


def _resolve_authoritative_plan_network(plan_name_or_code: str) -> Dict:
    canonical = _find_approved_plan(plan_name_or_code)
    if not canonical:
        return {"found": False}

    loader_kind = APPROVED_PLAN_LOADERS[canonical]
    if loader_kind == "clean":
        plan_data = load_clean_plan(canonical)
        source_network = plan_data.get("network") or plan_data.get("network_name") or plan_data.get("الشبكة")
    else:
        plan_data = load_enhanced_plan(canonical)
        source_network = plan_data.get("network_name") or plan_data.get("network") or plan_data.get("الشبكة")

    medical_network = _normalize_network_code(source_network)
    return {
        "plan_code": APPROVED_PLAN_CODES[canonical],
        "plan_name": canonical,
        "medical_network": medical_network,
        "found": bool(medical_network),
        "source_network": source_network,
        "source": "authoritative",
    }


def resolve_plan_network(plan_name_or_code: str, csv_path: Optional[Path] = None) -> Dict:
    authoritative = _resolve_authoritative_plan_network(plan_name_or_code)
    if authoritative.get("found"):
        csv_row = _find_csv_row(plan_name_or_code, csv_path)
        csv_network = _normalize_network_code(csv_row["medical_network"]) if csv_row else None
        authoritative["csv_mismatch"] = bool(csv_row and csv_network != authoritative["medical_network"])
        return authoritative

    row = _find_csv_row(plan_name_or_code, csv_path)
    if row:
        medical_network = _normalize_network_code(row["medical_network"])
        return {
            "plan_code": row["plan_code"],
            "plan_name": row["plan_name"],
            "medical_network": medical_network,
            "found": bool(medical_network),
            "source": "csv",
        }
    return {"found": False}


def get_medical_network_for_plan(plan_name_or_code: str, csv_path: Optional[Path] = None) -> Optional[str]:
    result = resolve_plan_network(plan_name_or_code, csv_path=csv_path)
    return result["medical_network"] if result.get("found") else None
