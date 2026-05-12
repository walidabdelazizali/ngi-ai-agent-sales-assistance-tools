from typing import Any, Dict

from src.tools.enhanced_plan_loader import load_enhanced_plan, resolve_enhanced_plan_name


BLOCKED_MESSAGE = "Comparison is not available because one or more approved comparison fields are missing."

REQUIRED_COMPARISON_FIELDS = (
    "plan_name",
    "plan_code",
    "network_name",
    "annual_limit",
    "area_of_coverage",
    "direct_billing",
    "referral_required",
    "approval_status",
    "source_trace",
)

PHASE1_SUPPORTED_PAIR = frozenset({"Classic 1", "Prime 1"})


def _has_required_fields(plan: Dict[str, Any]) -> bool:
    for field in REQUIRED_COMPARISON_FIELDS:
        value = plan.get(field)
        if value in (None, ""):
            return False
        if field == "source_trace" and (not isinstance(value, dict) or not value):
            return False
    return True


def compare_enhanced_plans(plan_a: str, plan_b: str) -> Dict[str, Any]:
    resolved_a = resolve_enhanced_plan_name(plan_a) or plan_a
    resolved_b = resolve_enhanced_plan_name(plan_b) or plan_b

    if frozenset({resolved_a, resolved_b}) != PHASE1_SUPPORTED_PAIR:
        return {"ok": False, "message": BLOCKED_MESSAGE}

    try:
        left = load_enhanced_plan(resolved_a)
        right = load_enhanced_plan(resolved_b)
    except Exception:
        return {"ok": False, "message": BLOCKED_MESSAGE}

    if left.get("approval_status") != "approved" or right.get("approval_status") != "approved":
        return {"ok": False, "message": BLOCKED_MESSAGE}

    if not _has_required_fields(left) or not _has_required_fields(right):
        return {"ok": False, "message": BLOCKED_MESSAGE}

    lines = [
        "[ENHANCED COMPARISON]",
        f"Plan A: {left['plan_name']} ({left['plan_code']})",
        f"Plan B: {right['plan_name']} ({right['plan_code']})",
        f"Network: {left['plan_name']}: {left['network_name']} | {right['plan_name']}: {right['network_name']}",
        f"Annual Limit: {left['plan_name']}: {left['annual_limit']} | {right['plan_name']}: {right['annual_limit']}",
        f"Area of Coverage: {left['plan_name']}: {left['area_of_coverage']} | {right['plan_name']}: {right['area_of_coverage']}",
        f"Direct Billing: {left['plan_name']}: {'Yes' if left['direct_billing'] else 'No'} | {right['plan_name']}: {'Yes' if right['direct_billing'] else 'No'}",
        f"Referral Required: {left['plan_name']}: {'Yes' if left['referral_required'] else 'No'} | {right['plan_name']}: {'Yes' if right['referral_required'] else 'No'}",
        f"Approval Status: {left['approval_status']} | {right['approval_status']}",
        "Source Trace: present | present",
    ]

    return {
        "ok": True,
        "message": "\n".join(lines),
        "plan_a": left["plan_name"],
        "plan_b": right["plan_name"],
    }
