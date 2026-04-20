"""
Deterministic agent-ready wrapper for the validated runtime.
Phase 1: intent classification, plan extraction, and tool-contract routing.
No AI, LLM, RAG, or fuzzy logic.
"""
from typing import Dict, Any, Optional
from src.tool_contract import get_plan_core, get_reimbursement_rules, get_plan_summary

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
    # Plan core
    for field in PLAN_CORE_FIELDS:
        if field in lowered:
            return "plan_core"
    # Reimbursement
    for field in REIMBURSEMENT_FIELDS:
        if field in lowered:
            return "reimbursement_rules"
    # Summary
    for pat in SUMMARY_PATTERNS:
        if pat in lowered:
            return "plan_summary"
    return None

def run_agent_wrapper(user_query: str) -> Dict[str, Any]:
    plan_name = _extract_plan_name(user_query)
    intent = _intent_from_query(user_query)
    # If no supported plan or no supported intent, always return unsupported envelope
    if not plan_name or intent not in ("plan_core", "reimbursement_rules", "plan_summary"):
        return {
            "ok": False,
            "intent": "unsupported",
            "plan_name": None,
            "tool_name": None,
            "data": None,
            "message": "No supported plan and/or intent found in query. Supported plans: Remedy 04, Remedy 05. Supported intents: plan_core, reimbursement_rules, plan_summary."
        }
    if intent == "plan_core":
        try:
            data = get_plan_core(plan_name)
            return {
                "ok": True,
                "intent": "plan_core",
                "plan_name": plan_name,
                "tool_name": "get_plan_core",
                "data": data,
                "message": "Plan core fields returned."
            }
        except Exception as e:
            return {
                "ok": False,
                "intent": "plan_core",
                "plan_name": plan_name,
                "tool_name": "get_plan_core",
                "data": None,
                "message": f"Error: {e}"
            }
    elif intent == "reimbursement_rules":
        try:
            data = get_reimbursement_rules(plan_name)
            return {
                "ok": True,
                "intent": "reimbursement_rules",
                "plan_name": plan_name,
                "tool_name": "get_reimbursement_rules",
                "data": data,
                "message": "Reimbursement rules returned."
            }
        except Exception as e:
            return {
                "ok": False,
                "intent": "reimbursement_rules",
                "plan_name": plan_name,
                "tool_name": "get_reimbursement_rules",
                "data": None,
                "message": f"Error: {e}"
            }
    elif intent == "plan_summary":
        try:
            data = get_plan_summary(plan_name)
            return {
                "ok": True,
                "intent": "plan_summary",
                "plan_name": plan_name,
                "tool_name": "get_plan_summary",
                "data": data,
                "message": "Plan summary returned."
            }
        except Exception as e:
            return {
                "ok": False,
                "intent": "plan_summary",
                "plan_name": plan_name,
                "tool_name": "get_plan_summary",
                "data": None,
                "message": f"Error: {e}"
            }
