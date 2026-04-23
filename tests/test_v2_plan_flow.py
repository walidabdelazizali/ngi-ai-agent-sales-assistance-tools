import pytest
from src.v2_plan_loader import load_clean_plan
from src.v2_plan_normalizer import normalize_clean_plan

def test_loader_source_lock():
    # Only DOCX files are allowed, no legacy fallback
    for plan in ["Remedy 02", "Remedy 03", "Remedy 04", "Remedy 05", "Remedy 06"]:
        raw = load_clean_plan(plan)
        assert raw["plan_name"] == plan
        # Must be under input_docs and end with .docx
        assert raw["source_path"].startswith("input_docs/")
        assert raw["source_path"].endswith(".docx")
        assert isinstance(raw["paragraphs"], list)
        assert isinstance(raw["tables"], list)
        assert isinstance(raw["raw_text"], str)
def test_loader_fails_if_missing():
    # Loader must fail if file is missing or not under input_docs
    from src.v2_plan_loader import PLAN_DOCX_MAP
    # Temporarily patch mapping to a non-existent file
    bad_map = PLAN_DOCX_MAP.copy()
    bad_map["Remedy 02"] = "input_docs/DOES_NOT_EXIST.docx"
    import importlib
    import sys
    # Patch PLAN_DOCX_MAP in module
    import src.v2_plan_loader as loader_mod
    orig_map = loader_mod.PLAN_DOCX_MAP.copy()
    loader_mod.PLAN_DOCX_MAP = bad_map
    try:
        with pytest.raises(ValueError) as e:
            loader_mod.load_clean_plan("Remedy 02")
        assert "input_docs/DOES_NOT_EXIST.docx" in str(e.value)
    finally:
        loader_mod.PLAN_DOCX_MAP = orig_map
def test_loader_rejects_non_input_docs():
    # Loader must not resolve from any other directory
    from src.v2_plan_loader import PLAN_DOCX_MAP
    bad_map = PLAN_DOCX_MAP.copy()
    bad_map["Remedy 03"] = "data/HN-REMEDY-3.docx"
    import src.v2_plan_loader as loader_mod
    orig_map = loader_mod.PLAN_DOCX_MAP.copy()
    loader_mod.PLAN_DOCX_MAP = bad_map
    try:
        with pytest.raises(ValueError) as e:
            loader_mod.load_clean_plan("Remedy 03")
        assert "input_docs/" in str(e.value) or "must be under input_docs" in str(e.value)
    finally:
        loader_mod.PLAN_DOCX_MAP = orig_map

def test_normalizer_no_legacy():
    # Normalizer must not depend on legacy files or fallback
    raw = {
        "plan_name": "Remedy 02",
        "source_path": "input_docs/HN-REMEDY-2.docx",
        "paragraphs": ["Annual Limit: AED. 150,000", "Referral required for specialist"],
        "tables": [[["Pharmacy", "AED 3,000 per year, 30% cost share"]]],
        "raw_text": "Annual Limit: AED. 150,000\nReferral required for specialist\nPharmacy\tAED 3,000 per year, 30% cost share"
    }
    norm = normalize_clean_plan(raw)
    assert norm["plan_name"] == "Remedy 02"
    assert norm["annual_limit"] == "AED. 150,000"
    assert norm["specialist_access_model"] == "referral"
    assert "3,000" in (norm["pharmacy_limit_and_cost_share"] or "")
    assert "30%" in (norm["pharmacy_limit_and_cost_share"] or "")

def test_expected_values_remedy_02_04_05():
    # These tests require actual DOCX content to pass
    plans = ["Remedy 02", "Remedy 04", "Remedy 05"]
    expected = {
        "Remedy 02": {"annual_limit": "AED. 150,000", "specialist_access_model": "referral", "pharmacy": ["3,000", "30%"]},
        "Remedy 04": {"annual_limit": "AED. 150,000", "specialist_access_model": "referral", "pharmacy": ["7,500", "20%"], "lab": "Nil", "radiology": "Nil"},
        "Remedy 05": {"annual_limit": "AED. 150,000", "specialist_access_model": "direct", "pharmacy": ["7,500", "20%"]},
    }
    for plan in plans:
        raw = load_clean_plan(plan)
        norm = normalize_clean_plan(raw)
        exp = expected[plan]
        assert norm["annual_limit"] == exp["annual_limit"], f"{plan} annual_limit: {norm['annual_limit']} != {exp['annual_limit']}"
        assert norm["specialist_access_model"] == exp["specialist_access_model"], f"{plan} specialist_access_model: {norm['specialist_access_model']} != {exp['specialist_access_model']}"
        for anchor in exp.get("pharmacy", []):
            assert anchor in (norm["pharmacy_limit_and_cost_share"] or ""), f"{plan} pharmacy_limit_and_cost_share missing {anchor}: {norm['pharmacy_limit_and_cost_share']}"
        if "lab" in exp:
            assert norm["laboratory_cost_share"] == exp["lab"], f"{plan} laboratory_cost_share: {norm['laboratory_cost_share']} != {exp['lab']}"
        if "radiology" in exp:
            assert norm["radiology_cost_share"] == exp["radiology"], f"{plan} radiology_cost_share: {norm['radiology_cost_share']} != {exp['radiology']}"
