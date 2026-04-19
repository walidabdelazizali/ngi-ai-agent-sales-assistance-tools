import json
import pytest
from pathlib import Path
from src.query.plan_query import load_plan

def test_remedy_04_reimbursement_fields():
    """Regression: Remedy 04 reimbursement fields must always be present and correct."""
    plan = load_plan("Remedy 04")
    assert plan["reimbursement_scope"] == "Reimbursement allowed for emergency treatment only, within UAE and GCC."
    assert plan["outside_network_reimbursement"] == "Emergency only, within UAE and GCC."
    assert plan["outside_uae_reimbursement"] == "Emergency only, within GCC (not worldwide)"
    assert plan["reimbursement_basis"] == "100% of incurred cost or UCR, whichever is lower, for eligible claims."
    assert plan["reimbursement_conditions"] == "Subject to prior approval for elective IP treatment outside UAE."
    assert plan["reimbursement_documents_required"] == "Original invoices and medical reports required."
