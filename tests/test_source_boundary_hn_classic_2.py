import os
import json
from src.parsers.enhanced_plan_parser import parse_enhanced_plan

def test_source_file_exists():
    path = os.path.join(
        "data", "plans", "raw", "HN_CLASSIC_2", "source_table.json"
    )
    assert os.path.exists(path), f"Source file missing: {path}"

def test_parse_source_table_fields():
    path = os.path.join(
        "data", "plans", "raw", "HN_CLASSIC_2", "source_table.json"
    )
    with open(path, encoding="utf-8") as f:
        table = json.load(f)
    result = parse_enhanced_plan(table)
    required = [
        "plan_name",
        "plan_code",
        "network_name",
        "annual_limit",
        "area_of_coverage",
        "direct_billing",
        "referral_required",
    ]
    for field in required:
        assert field in result, f"Missing field: {field}"
        assert result[field] is not None, f"Field {field} is None"
