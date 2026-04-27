import json
import pytest
from pathlib import Path
from src.query.plan_query import load_plan

def test_remedy_04_reimbursement_fields():
    """Regression: Remedy 04 reimbursement fields must always be present and correct."""
    plan = load_plan("Remedy 04")
    # For blocked plans, all reimbursement fields must be unavailable/None
    assert plan["reimbursement_scope"] is None
    assert plan["outside_network_reimbursement"] is None
    assert plan["outside_uae_reimbursement"] is None
    assert plan["reimbursement_basis"] is None
    assert plan["reimbursement_conditions"] is None
    assert plan["reimbursement_documents_required"] is None
