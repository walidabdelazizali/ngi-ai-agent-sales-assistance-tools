# Canonical normalized plan schema for insurance assistant


# Baseline required fields for plan readiness (do not change for sales core extension)
REQUIRED_FIELDS = [
    "plan_name",
    "plan_code",
    "network_name",
    "annual_limit",
    "area_of_coverage",
    "direct_billing",
    "referral_required",
    "approval_status",
    "source_trace",
    "tests_passed"
]

# Phase 1: Sales Core Fields (do not add to REQUIRED_FIELDS)
SALES_CORE_FIELDS = [
    "consultation_copay",
    "lab_copay",
    "radiology_copay",
    "physiotherapy_sessions",
    "physiotherapy_copay",
    "pharmacy_limit",
    "pharmacy_copay",
    "maternity_waiting_period",
    "maternity_normal_limit",
    "maternity_csection_limit",
    "maternity_copay",
]

# All fields that must be present for a plan to be considered ready for customer-facing answers
CANONICAL_PLAN_SCHEMA = {
    "plan_name": str,
    "plan_code": str,
    "network_name": str,
    "annual_limit": str,
    "area_of_coverage": str,
    "direct_billing": bool,
    "referral_required": bool,
    "approval_status": str,  # must be 'approved'
    "source_trace": dict,     # must be present and non-empty for all key fields
    "tests_passed": bool,     # must be True
    # Sales core fields (optional, may be None)
    "consultation_copay": (str, type(None)),
    "lab_copay": (str, type(None)),
    "radiology_copay": (str, type(None)),
    "physiotherapy_sessions": (str, int, type(None)),
    "physiotherapy_copay": (str, type(None)),
    "pharmacy_limit": (str, type(None)),
    "pharmacy_copay": (str, type(None)),
    "maternity_waiting_period": (str, type(None)),
    "maternity_normal_limit": (str, type(None)),
    "maternity_csection_limit": (str, type(None)),
    "maternity_copay": (str, type(None)),
}

# Helper for sales core field validation
def validate_sales_core_field(plan: dict, field_name: str) -> bool:
    """
    Returns True if:
      - plan is approved
      - field has a value (not None)
      - source_trace exists for that field and is not empty
    """
    if not plan or plan.get("approval_status", "").lower() != "approved":
        return False
    if field_name not in SALES_CORE_FIELDS:
        return False
    if plan.get(field_name) in (None, ""):
        return False
    st = plan.get("source_trace", {})
    if not isinstance(st, dict) or not st.get(field_name):
        return False
    return True
