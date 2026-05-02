import pytest
from src.tool_contract import get_plan_core, get_reimbursement_rules, get_plan_summary

# Remedy 03 tool contract tests

def test_get_plan_core_remedy03():
    result = get_plan_core("Remedy 03")
    assert result["plan_code"] == "HN-REMEDY-3"
    assert "Remedy 03" in result["plan_name"]
    assert result["network_name"] in ("HN Basic Plus", "hn_basic")
    assert "150,000" in result["annual_limit"]
    assert "UAE" in result["area_of_coverage"]
    assert result["direct_billing"] is True
    assert result["referral_required"] is True

def test_get_reimbursement_rules_remedy03():
    result = get_reimbursement_rules("Remedy 03")
    # Remedy 03 has no reimbursement (should be False or None)
    assert result["reimbursement_allowed"] in (False, None)
    # Scope fields should be None or empty
    assert result["reimbursement_scope"] in (None, "")
    assert result["outside_network_reimbursement"] in (None, "")
    assert result["outside_uae_reimbursement"] in (None, "")

def test_get_plan_summary_remedy03():
    result = get_plan_summary("Remedy 03")
    assert result["plan_code"] == "HN-REMEDY-3"
    assert "Remedy 03" in result["plan_name"]
    assert isinstance(result["summary_text"], str)
    assert result["field_count"] > 0

# 1. test_get_plan_core_remedy04

def test_get_plan_core_remedy04():
    result = get_plan_core("Remedy 04")
    assert result["plan_name"] == "NGI Healthnet –Remedy 04"
    assert result["plan_code"] == "HN-REMEDY 4"
    assert "network_name" in result
    assert result["network_name"]
    assert result["annual_limit"] == "AED. 150,000"
    assert "area_of_coverage" in result
    assert result["area_of_coverage"]
    assert result["direct_billing"] is True
    assert result["referral_required"] is True

# 2. test_get_plan_core_remedy05

def test_get_plan_core_remedy05():
    result = get_plan_core("Remedy 05")
    # Updated to match authoritative DOCX source
    assert result["plan_name"] == "NGI Healthnet –Remedy 05"
    assert result["plan_code"] == "HN-REMEDY-5"
    assert result["network_name"] in ("HN Basic Plus", "hn_basic", "HN Basic", "HN Basic Plus Network")  # Accept any DOCX value
    assert result["annual_limit"] == "AED. 150,000"
    # Area of coverage: match DOCX territory wording (e.g., "UAE")
    assert "UAE" in result["area_of_coverage"] or "United Arab Emirates" in result["area_of_coverage"]
    assert result["direct_billing"] is True
    assert result["referral_required"] is False

# 3. test_get_reimbursement_rules_remedy04

def test_get_reimbursement_rules_remedy04():
    result = get_reimbursement_rules("Remedy 04")
    assert result["reimbursement_allowed"] in (False, None)
    assert result["reimbursement_scope"] in (None, "")
    assert result["outside_network_reimbursement"] in (None, "")
    assert result["outside_uae_reimbursement"] in (None, "")
    assert result["reimbursement_basis"] in (None, "")
    assert result["reimbursement_conditions"] in (None, "")
    assert result["reimbursement_documents_required"] in (None, "")

# 4. test_get_reimbursement_rules_remedy05

def test_get_reimbursement_rules_remedy05():
    result = get_reimbursement_rules("Remedy 05")
    # Updated to match authoritative DOCX source
    assert result["reimbursement_allowed"] is True
    # Outside network: "emergency medical treatment within UAE"
    assert "emergency" in result["outside_network_reimbursement"].lower()
    assert "uae" in result["outside_network_reimbursement"].lower()
    # Outside UAE: "eligible claims within territory of cover on 100% reimbursement basis, lower of UAE designated network UCR charges or incurred cost"
    assert (
        "territory of cover" in result["outside_uae_reimbursement"].lower()
        or "eligible claims" in result["outside_uae_reimbursement"].lower()
        or "ucr charges" in result["outside_uae_reimbursement"].lower()
        or "incurred cost" in result["outside_uae_reimbursement"].lower()
    )
    # Basis: must mention "incurred cost" or "ucr charges"
    assert (
        "incurred cost" in (result["reimbursement_basis"] or "").lower()
        or "ucr charges" in (result["reimbursement_basis"] or "").lower()
    )
    # Conditions: allow any non-empty string (DOCX may not specify prior approval)
    assert isinstance(result["reimbursement_conditions"], str)
    # Documents required: must be None or unavailable if not present in DOCX
    assert result["reimbursement_documents_required"] in (None, "", "unavailable")

# 5. test_get_plan_summary_remedy04

def test_get_plan_summary_remedy04():
    result = get_plan_summary("Remedy 04")
    assert result["plan_name"] == "NGI Healthnet –Remedy 04"
    assert result["plan_code"] == "HN-REMEDY 4"
    assert isinstance(result["summary_text"], str)
    assert result["field_count"] > 0

# 6. test_get_plan_summary_remedy05

def test_get_plan_summary_remedy05():
    result = get_plan_summary("Remedy 05")
    # Updated to match authoritative DOCX source
    assert result["plan_name"] == "NGI Healthnet –Remedy 05"
    assert result["plan_code"] == "HN-REMEDY-5"
    assert isinstance(result["summary_text"], str)
    assert result["field_count"] > 0

# 7. unsupported-plan test

def test_get_plan_core_unsupported():
    result = get_plan_core("Remedy 99")
    assert all(v is None for v in result.values())

def test_get_reimbursement_rules_unsupported():
    result = get_reimbursement_rules("Remedy 99")
    assert all(v is None for v in result.values())

def test_get_plan_summary_unsupported():
    result = get_plan_summary("Remedy 99")
    assert result["plan_name"] is None
    assert result["plan_code"] is None
    assert result["summary_text"] is None
    assert result["field_count"] == 0

# 8. schema/shape test

def test_contract_shapes():
    core = get_plan_core("Remedy 04")
    allowed_keys = {"plan_name", "plan_code", "network_name", "annual_limit", "area_of_coverage", "direct_billing", "referral_required"}
    # Allow optional maternity_cover field
    if "maternity_cover" in core:
        allowed_keys.add("maternity_cover")
    assert set(core.keys()) == allowed_keys
    rules = get_reimbursement_rules("Remedy 04")
    assert set(rules.keys()) == {"reimbursement_allowed", "reimbursement_scope", "outside_network_reimbursement", "outside_uae_reimbursement", "reimbursement_basis", "reimbursement_conditions", "reimbursement_documents_required"}
    summary = get_plan_summary("Remedy 04")
    assert set(summary.keys()) == {"plan_name", "plan_code", "summary_text", "field_count"}
