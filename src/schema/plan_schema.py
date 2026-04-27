# Canonical normalized plan schema for insurance assistant

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
    "tests_passed": bool      # must be True
}
