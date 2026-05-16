"""
Constrained Planner: Deterministic intent/plan classifier for agent system.
"""
from typing import Dict, Any, Optional, Union
from src.agent_adapter import handle_user_query
from src.agent_wrapper import _build_unsupported_response

SUPPORTED_PLANS = {
    "remedy 04": "Remedy 04",
    "remedy 4": "Remedy 04",
    "hn-remedy-4": "Remedy 04",
    "ريميدي 4": "Remedy 04",
    "ريميدي 04": "Remedy 04",
    "remedy 05": "Remedy 05",
    "remedy 5": "Remedy 05",
    "hn-remedy-5": "Remedy 05",
    "ريميدي 5": "Remedy 05",
    "ريميدي 05": "Remedy 05",
    # Prime Plan-2 support
    "prime 2": "Prime 2",
    "prime2": "Prime 2",
    "prime-2": "Prime 2",
    "hn_prime_2": "Prime 2",
    "hn-prime-2": "Prime 2",
    "hn prime 2": "Prime 2",
}

PLAN_CORE_FIELDS = [
    "plan name", "plan_name", "plan code", "plan_code", "network", "network name", "network_name",
    "annual limit", "annual_limit", "area of coverage", "area", "area_of_coverage",
    "direct billing", "direct_billing", "referral required", "referral", "referral_required",
    "اسم الخطة", "رمز الخطة", "الشبكة", "الحد السنوي", "التغطية", "الدفع المباشر", "الإحالة"
]

REIMBURSEMENT_FIELDS = [
    "reimbursement", "reimbursement allowed", "reimbursement scope", "outside network reimbursement",
    "outside uae reimbursement", "reimbursement basis", "reimbursement conditions",
    "reimbursement documents required", "documents required for reimbursement",
    "تعويض", "نطاق التعويض", "تعويض خارج الشبكة", "تعويض خارج الإمارات", "أساس التعويض", "شروط التعويض", "مستندات التعويض المطلوبة"
]

SUMMARY_PATTERNS = [
    "summary", "overview", "give me a summary", "plan summary", "tell me about", "ملخص", "اعطني ملخص", "أعطني ملخص", "عرض ملخص"
]

def _extract_plan_name(text: str) -> Optional[str]:
    lowered = text.lower()
    for key, canonical in SUPPORTED_PLANS.items():
        if key in lowered:
            return canonical
    return None

def _intent_from_query(text: str) -> Optional[str]:
    lowered = text.lower()
    for field in PLAN_CORE_FIELDS:
        if field in lowered:
            return "plan_core"
    for field in REIMBURSEMENT_FIELDS:
        if field in lowered:
            return "reimbursement_rules"
    for pat in SUMMARY_PATTERNS:
        if pat in lowered:
            return "plan_summary"
    return None

def plan_user_query(user_query: str) -> Dict[str, Any]:
    plan_name = _extract_plan_name(user_query)
    intent = _intent_from_query(user_query)
    normalized_query = user_query.strip()
    if not plan_name or intent not in ("plan_core", "reimbursement_rules", "plan_summary"):
        return {
            "ok": False,
            "intent": "unsupported",
            "plan_name": None,
            "reason": "No supported plan and/or intent found in query.",
            "normalized_query": normalized_query
        }
    return {
        "ok": True,
        "intent": intent,
        "plan_name": plan_name,
        "reason": "Supported plan and intent.",
        "normalized_query": normalized_query
    }

def execute_planned_query(user_query: str, output_mode: str = "dict") -> Union[Dict[str, Any], str]:
    plan = plan_user_query(user_query)
    if not plan["ok"]:
        # Return a safe unsupported envelope in the requested output mode
        if output_mode == "dict":
            return _build_unsupported_response(
                message=plan["reason"] + " Supported plans: Remedy 04, Remedy 05, Prime 2. Supported intents: plan_core, reimbursement_rules, plan_summary."
            )
        elif output_mode == "text":
            return f"Intent: unsupported\nMessage: {plan['reason']} Supported plans: Remedy 04, Remedy 05, Prime 2. Supported intents: plan_core, reimbursement_rules, plan_summary."
        else:
            return _build_unsupported_response(
                message=f"Invalid output_mode: {output_mode}. Supported: 'dict', 'text'."
            )
    # Supported: delegate to adapter
    return handle_user_query(user_query, output_mode)
