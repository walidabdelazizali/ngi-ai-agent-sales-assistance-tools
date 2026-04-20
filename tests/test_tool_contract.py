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
    assert result["plan_name"] == "Remedy 04"
    assert result["plan_code"] == "HN-REMEDY-4"
    assert result["network_name"] == "hn_premier"
    assert result["annual_limit"] == "500,000"
    assert result["area_of_coverage"] == "UAE + GCC"
    assert result["direct_billing"] is True
    assert result["referral_required"] is True

# 2. test_get_plan_core_remedy05

def test_get_plan_core_remedy05():
    result = get_plan_core("Remedy 05")
    assert result["plan_name"] == "Remedy 05"
    assert result["plan_code"] == "HN-REMEDY-5"
    assert result["network_name"] == "hn_elite"
    assert result["annual_limit"] == "1,000,000"
    assert result["area_of_coverage"] == "Worldwide (excluding USA)"
    assert result["direct_billing"] is True
    assert result["referral_required"] is True

# 3. test_get_reimbursement_rules_remedy04

def test_get_reimbursement_rules_remedy04():
    result = get_reimbursement_rules("Remedy 04")
    assert result["reimbursement_allowed"] is True
    assert "emergency" in result["reimbursement_scope"].lower()
    assert "emergency" in result["outside_network_reimbursement"].lower()
    assert "gcc" in result["outside_uae_reimbursement"].lower()
    assert "incurred cost" in result["reimbursement_basis"].lower()
    assert "prior approval" in result["reimbursement_conditions"].lower()
    assert "invoice" in result["reimbursement_documents_required"].lower() or "medical report" in result["reimbursement_documents_required"].lower()

# 4. test_get_reimbursement_rules_remedy05

def test_get_reimbursement_rules_remedy05():
    result = get_reimbursement_rules("Remedy 05")
    assert result["reimbursement_allowed"] is True
    assert "emergency" in result["reimbursement_scope"].lower()
    assert "emergency" in result["outside_network_reimbursement"].lower()
    assert "worldwide" in result["outside_uae_reimbursement"].lower()
    assert "incurred cost" in result["reimbursement_basis"].lower()
    assert "prior approval" in result["reimbursement_conditions"].lower()
    assert "invoice" in result["reimbursement_documents_required"].lower() or "medical report" in result["reimbursement_documents_required"].lower()

# 5. test_get_plan_summary_remedy04

def test_get_plan_summary_remedy04():
    result = get_plan_summary("Remedy 04")
    assert result["plan_name"] == "Remedy 04"
    assert result["plan_code"] == "HN-REMEDY-4"
    assert isinstance(result["summary_text"], str)
    assert result["field_count"] > 0

# 6. test_get_plan_summary_remedy05

def test_get_plan_summary_remedy05():
    result = get_plan_summary("Remedy 05")
    assert result["plan_name"] == "Remedy 05"
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
    assert set(core.keys()) == {"plan_name", "plan_code", "network_name", "annual_limit", "area_of_coverage", "direct_billing", "referral_required"}
    rules = get_reimbursement_rules("Remedy 04")
    assert set(rules.keys()) == {"reimbursement_allowed", "reimbursement_scope", "outside_network_reimbursement", "outside_uae_reimbursement", "reimbursement_basis", "reimbursement_conditions", "reimbursement_documents_required"}
    summary = get_plan_summary("Remedy 04")
    assert set(summary.keys()) == {"plan_name", "plan_code", "summary_text", "field_count"}
