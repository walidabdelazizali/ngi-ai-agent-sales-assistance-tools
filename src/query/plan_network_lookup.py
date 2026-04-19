import csv
from pathlib import Path
from typing import Optional, Dict

MAPPING_CSV = Path(__file__).parent.parent.parent / "data/plans/plan_network_mapping.csv"

# Load mapping as a list of dicts
def load_plan_network_mapping(csv_path: Optional[Path] = None):
    path = csv_path or MAPPING_CSV
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]

def _normalize_plan_name(name: str) -> str:
    return name.strip().lower().replace(" ", "").replace("-", "").replace("_", "")

def resolve_plan_network(plan_name_or_code: str) -> Dict:
    mapping = load_plan_network_mapping()
    norm = _normalize_plan_name(plan_name_or_code)
    for row in mapping:
        if _normalize_plan_name(row["plan_name"]) == norm or _normalize_plan_name(row["plan_code"]) == norm:
            return {
                "plan_code": row["plan_code"],
                "plan_name": row["plan_name"],
                "medical_network": row["medical_network"],
                "found": bool(row["medical_network"]),
            }
    return {"found": False}

def get_medical_network_for_plan(plan_name_or_code: str) -> Optional[str]:
    result = resolve_plan_network(plan_name_or_code)
    return result["medical_network"] if result.get("found") else None
