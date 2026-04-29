"""Deterministic tool contract layer for agent/tool-calling use.

Provides stable, structured functions for plan core, reimbursement rules, and summary.
"""
from typing import Optional, Dict, Any
from src.query.plan_query import load_plan, summarize_plan
from src.parsers.canonical_schema import CANONICAL_FIELDS

# --- Tool contract functions ---

def get_plan_core(plan_name: str) -> Dict[str, Any]:
    try:
        plan = load_plan(plan_name)
    except Exception:
        return {
            "plan_name": None,
            "plan_code": None,
            "network_name": None,
            "annual_limit": None,
            "area_of_coverage": None,
            "direct_billing": None,
            "referral_required": None,
        }
    return {
        "plan_name": plan.get("plan_name"),
        "plan_code": plan.get("plan_code"),
        "network_name": plan.get("network_name"),
        "annual_limit": plan.get("annual_limit"),
        "area_of_coverage": plan.get("area_of_coverage"),
        "direct_billing": plan.get("direct_billing"),
        "referral_required": plan.get("referral_required"),
        "maternity_cover": plan.get("maternity_cover"),
    }

def get_reimbursement_rules(plan_name: str) -> Dict[str, Any]:
    try:
        plan = load_plan(plan_name)
    except Exception:
        return {
            "reimbursement_allowed": None,
            "reimbursement_scope": None,
            "outside_network_reimbursement": None,
            "outside_uae_reimbursement": None,
            "reimbursement_basis": None,
            "reimbursement_conditions": None,
            "reimbursement_documents_required": None,
        }
    # Deterministic logic for reimbursement_allowed
    allowed = plan.get("reimbursement_allowed")
    # If not present, infer as True if any reimbursement field is non-empty
    if allowed is None:
        allowed = any(
            bool(plan.get(f)) for f in [
                "reimbursement_scope",
                "outside_network_reimbursement",
                "outside_uae_reimbursement",
                "reimbursement_basis",
                "reimbursement_conditions",
                "reimbursement_documents_required",
            ]
        ) or None
    return {
        "reimbursement_allowed": allowed,
        "reimbursement_scope": plan.get("reimbursement_scope"),
        "outside_network_reimbursement": plan.get("outside_network_reimbursement"),
        "outside_uae_reimbursement": plan.get("outside_uae_reimbursement"),
        "reimbursement_basis": plan.get("reimbursement_basis"),
        "reimbursement_conditions": plan.get("reimbursement_conditions"),
        "reimbursement_documents_required": plan.get("reimbursement_documents_required"),
    }

def get_plan_summary(plan_name: str) -> Dict[str, Any]:
    try:
        summary = summarize_plan(plan_name)
    except Exception:
        return {
            "plan_name": None,
            "plan_code": None,
            "summary_text": None,
            "field_count": 0,
        }
    # Patch: If plan_name is None in summary, try to get it from loaded plan (passthrough case)
    plan_name_val = summary.get("plan_name")
    if plan_name_val is None:
        try:
            from src.query.plan_query import load_plan
            plan = load_plan(plan_name)
            plan_name_val = plan.get("plan_name")
        except Exception:
            plan_name_val = None
    plan_code_val = summary.get("plan_code")
    if plan_code_val is None:
        try:
            from src.query.plan_query import load_plan
            plan = load_plan(plan_name)
            plan_code_val = plan.get("plan_code")
        except Exception:
            plan_code_val = None
    used_fields = [
        plan_name_val,
        plan_code_val,
        summary.get("network_name"),
        summary.get("annual_limit"),
        summary.get("area_of_coverage"),
        summary.get("direct_billing"),
        summary.get("referral_required"),
    ]
    field_count = sum(1 for v in used_fields if v not in (None, "", []))
    return {
        "plan_name": plan_name_val,
        "plan_code": plan_code_val,
        "summary_text": summary.get("summary_text"),
        "field_count": field_count,
    }
