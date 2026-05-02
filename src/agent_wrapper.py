PLAN_CORE_FIELDS = [
    "plan name", "plan_name", "plan code", "plan_code", "network", "network name", "network_name",
    "annual limit", "annual_limit", "area of coverage", "area", "area_of_coverage",
    "direct billing", "direct_billing", "referral required", "referral", "referral_required",
    "اسم الخطة", "رمز الخطة", "الشبكة", "الحد السنوي", "التغطية", "الدفع المباشر", "الإحالة"
]
"""
Deterministic agent-ready wrapper for the validated runtime.
Phase 1: intent classification, plan extraction, and tool-contract routing.
No AI, LLM, RAG, or fuzzy logic.
"""
from typing import Dict, Any, Optional
from src.tool_contract import get_plan_core, get_reimbursement_rules, get_plan_summary

SUPPORTED_PLANS = {
    # Remedy 02
    "remedy 02": "Remedy 02",
    "remedy 2": "Remedy 02",
    "hn-remedy-2": "Remedy 02",
    "ريميدي 2": "Remedy 02",
    "ريميدي 02": "Remedy 02",
    # Remedy 03
    "remedy 03": "Remedy 03",
    "remedy 3": "Remedy 03",
    "hn-remedy-3": "Remedy 03",
    "ريميدي 3": "Remedy 03",
    "ريميدي 03": "Remedy 03",
    # Remedy 04
    "remedy 04": "Remedy 04",
    "remedy 4": "Remedy 04",
    "hn-remedy-4": "Remedy 04",
    "ريميدي 4": "Remedy 04",
    "ريميدي 04": "Remedy 04",
    # Remedy 05
    "remedy 05": "Remedy 05",
    "remedy 5": "Remedy 05",
    "hn-remedy-5": "Remedy 05",
    "ريميدي 5": "Remedy 05",
    "ريميدي 05": "Remedy 05",
    # Remedy 06
    "remedy 06": "Remedy 06",
    "remedy 6": "Remedy 06",
    "hn-remedy-6": "Remedy 06",
    "ريميدي 6": "Remedy 06",
    "ريميدي 06": "Remedy 06",
}

import re

PLAN_COMPARISON_PATTERNS = [
    r"compare (remedy|ريميدي) ?0?2 and (remedy|ريميدي) ?0?3",
    r"compare (remedy|ريميدي) ?0?2 and (remedy|ريميدي) ?0?4",
    r"compare (remedy|ريميدي) ?0?3 and (remedy|ريميدي) ?0?4",
    r"ما الفرق بين ريميدي 02 و ريميدي 04",
    r"ما الفرق بين ريميدي 02 و ريميدي 03",
    r"ما الفرق بين ريميدي 03 و ريميدي 04",
    r"قارن ريميدي 02 و ريميدي 04",
    r"قارن ريميدي 02 و ريميدي 03",
    r"قارن ريميدي 03 و ريميدي 04",
    r"compare remedy [0-9]+ and remedy [0-9]+",
    r"ما الفرق بين ريميدي [0-9]+ و ريميدي [0-9]+",
    r"قارن ريميدي [0-9]+ و ريميدي [0-9]+",
]

def _extract_comparison_plans(text: str) -> Optional[tuple[str, str]]:
    # Extract two plan names from the query (English or Arabic)
    # Accepts: compare Remedy 02 and Remedy 04, ما الفرق بين ريميدي 02 و ريميدي 04
    # Returns canonical names if both are supported
    text = text.lower()
    # English
    m = re.search(r"remedy ?0?(\d+) and remedy ?0?(\d+)", text)
    if m:
        p1, p2 = m.group(1), m.group(2)
        n1, n2 = f"Remedy 0{p1}" if len(p1)==1 else f"Remedy {p1}", f"Remedy 0{p2}" if len(p2)==1 else f"Remedy {p2}"
        if n1 in SUPPORTED_PLANS.values() and n2 in SUPPORTED_PLANS.values():
            return n1, n2
    # Arabic
    m = re.search(r"ريميدي ?0?(\d+) و ريميدي ?0?(\d+)", text)
    if m:
        p1, p2 = m.group(1), m.group(2)
        n1, n2 = f"Remedy 0{p1}" if len(p1)==1 else f"Remedy {p1}", f"Remedy 0{p2}" if len(p2)==1 else f"Remedy {p2}"
        if n1 in SUPPORTED_PLANS.values() and n2 in SUPPORTED_PLANS.values():
            return n1, n2
    return None

REIMBURSEMENT_FIELDS = [
    "reimbursement", "reimbursement allowed", "reimbursement scope", "outside network reimbursement",
    "outside uae reimbursement", "reimbursement basis", "reimbursement conditions",
    "reimbursement documents required", "documents required for reimbursement",
    "تعويض", "نطاق التعويض", "تعويض خارج الشبكة", "تعويض خارج الإمارات", "أساس التعويض", "شروط التعويض", "مستندات التعويض المطلوبة"
]

SUMMARY_PATTERNS = [
    "summary", "overview", "give me a summary", "plan summary", "tell me about", "ملخص", "اعطني ملخص", "أعطني ملخص", "عرض ملخص", "لخص", "ملخص لخطة", "summary لخطة", "ملخص plan", "اعطني summary", "اعطني ملخص لخطة", "ملخص Remedy", "ملخص ريميدي"
]

def _extract_plan_name(text: str) -> Optional[str]:
    lowered = text.lower()
    for key, canonical in SUPPORTED_PLANS.items():
        if key in lowered:
            return canonical
    return None

def _intent_from_query(text: str) -> Optional[str]:
    lowered = text.lower()
    # Special-case: route explicit "maternity limit" with plan to plan_core
    if "maternity limit" in lowered:
        if _extract_plan_name(lowered):
            return "plan_core"
    # Comparison intent
    if _extract_comparison_plans(lowered):
        return "plan_comparison"
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
    is_arabic = any(c in user_query for c in 'اأإآبتثجحخدذرزسشصضطظعغفقكلمنهويءىة')
    # Patch: Robust summary routing for mixed Arabic/English phrasing
    # If summary pattern is present and plan_name is present, force plan_summary intent
    if not intent and plan_name:
        for pat in SUMMARY_PATTERNS:
            if pat in user_query.lower():
                intent = "plan_summary"
                break
    # Comparison intent
    if intent == "plan_comparison":
        plans = _extract_comparison_plans(user_query)
        if not plans:
            msg = "Please specify two supported plans to compare." if not is_arabic else "يرجى تحديد خطتين للمقارنة."
            return {
                "ok": False,
                "intent": "plan_comparison",
                "plan_name": None,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg]
                }
            }
        plan1, plan2 = plans
        from src.query.plan_query import compare_plans
        cmp = compare_plans(plan1, plan2)
        # Only show key fields
        key_fields = [
            ("annual_limit", "Annual Limit", "الحد السنوي"),
            ("network_name", "Network", "الشبكة"),
            ("area_of_coverage", "Area of Coverage", "نطاق التغطية"),
            ("direct_billing", "Direct Billing", "الدفع المباشر"),
            ("reimbursement_allowed", "Reimbursement Allowed", "التعويض")
        ]
        lines = []
        if is_arabic:
            lines.append(f"مقارنة بين {plan1} و {plan2}:")
        else:
            lines.append(f"Comparison between {plan1} and {plan2}:")
        for field, label_en, label_ar in key_fields:
            v1 = cmp['differing'].get(field, {}).get('plan_a') if field in cmp['differing'] else None
            v2 = cmp['differing'].get(field, {}).get('plan_b') if field in cmp['differing'] else None
            if v1 is None and v2 is None:
                v1 = v2 = cmp['matched'][0]['value'] if cmp['matched'] and cmp['matched'][0]['field'] == field else None
            if v1 is None and v2 is None:
                # Try matched
                for m in cmp['matched']:
                    if m['field'] == field:
                        v1 = v2 = m['value']
                        break
            if is_arabic:
                label = label_ar
            else:
                label = label_en
            if v1 is not None or v2 is not None:
                lines.append(f"{label}: {plan1}: {v1 if v1 is not None else '-'} | {plan2}: {v2 if v2 is not None else '-'}")
        msg = "\n".join(lines)
        return {
            "ok": True,
            "intent": "plan_comparison",
            "plan_name": f"{plan1} vs {plan2}",
            "tool_name": "compare_plans",
            "data": cmp,
            "message": msg,
            "normalized": {
                "status": "ok",
                "tool": "compare_plans",
                "answer": cmp,
                "errors": []
            }
        }
    # If no supported plan or no supported intent, always return unsupported-query message
    if not plan_name or intent not in ("plan_core", "reimbursement_rules", "plan_summary"):
        msg = (
            "Sorry, this query is not supported or not available. Please specify a supported plan or question."
            if not is_arabic else
            "عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم."
        )
        resp = {
            "ok": False,
            "intent": "unsupported",
            "plan_name": plan_name,
            "tool_name": None,
            "data": None,
            "message": msg,
            "normalized": {
                "status": "not_found",
                "tool": None,
                "answer": None,
                "errors": [msg]
            }
        }
        return resp
    from src.validation.plan_validator import normalize_plan, validate_plan_ready
    from src.query.plan_query import load_plan
    def _strip_internal_metadata(d):
        if isinstance(d, dict):
            d = dict(d)
            d.pop("approval_status", None)
            d.pop("tests_passed", None)
            d.pop("source_trace", None)
        return d
    if intent in ("plan_core", "reimbursement_rules", "plan_summary"):
        try:
            # Always validate readiness using the full plan, not the tool output
            full_plan = load_plan(plan_name)
            norm_plan = normalize_plan(full_plan)
            ok, reason = validate_plan_ready(norm_plan)
            if not ok:
                msg = (
                    "هذه الخطة غير متاحة حالياً للإجابة على العملاء."
                    if is_arabic else
                    "Sorry, this plan is not available for customer-facing answers."
                )
                resp = {
                    "ok": False,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": f"get_{intent}",
                    "data": None,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "not_ready",
                    "tool": f"get_{intent}",
                    "answer": None,
                    "errors": [reason]
                }
                return resp
            # If ready, return tool output as before
            if intent == "plan_core":
                data = get_plan_core(plan_name)
                plan = normalize_plan(data)
                plan = _strip_internal_metadata(plan)
                # Special-case: if query is for maternity limit and plan is Remedy 02, extract AED value from maternity_cover
                if "maternity limit" in user_query.lower() and plan_name == "Remedy 02":
                    maternity_cover = plan.get("maternity_cover")
                    aed_match = None
                    if maternity_cover:
                        m = re.search(r"AED[ .]*([0-9,]+)", maternity_cover)
                        if m:
                            aed_match = f"AED {m.group(1)}"
                    msg = f"Maternity limit: {aed_match if aed_match else 'Not available'}"
                    resp = {
                        "ok": True,
                        "intent": intent,
                        "plan_name": plan_name,
                        "tool_name": "get_plan_core",
                        "data": plan,
                        "message": msg
                    }
                    resp["normalized"] = {
                        "status": "ok",
                        "tool": "get_plan_core",
                        "answer": plan,
                        "errors": []
                    }
                    return resp
                # Default plan_core output
                lines = []
                lines.append(f"Plan: {plan.get('plan_name')}")
                lines.append(f"Code: {plan.get('plan_code')}")
                lines.append(f"الشبكة: {plan.get('network_name')}")
                lines.append(f"Annual limit: {plan.get('annual_limit')}")
                lines.append(f"Area: {plan.get('area_of_coverage')}")
                lines.append(f"Direct billing: {'Yes' if plan.get('direct_billing') else 'No' if plan.get('direct_billing') is not None else 'Not available'}")
                lines.append(f"Referral required: {'Yes' if plan.get('referral_required') else 'No' if plan.get('referral_required') is not None else 'Not available'}")
                msg = "\n".join(lines)
                resp = {
                    "ok": True,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": "get_plan_core",
                    "data": plan,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "ok",
                    "tool": "get_plan_core",
                    "answer": plan,
                    "errors": []
                }
                return resp
            elif intent == "reimbursement_rules":
                data = get_reimbursement_rules(plan_name)
                plan = normalize_plan(data)
                plan = _strip_internal_metadata(plan)
                lines = []
                lines.append(f"Reimbursement allowed: {'Yes' if plan.get('reimbursement_allowed') else 'No' if plan.get('reimbursement_allowed') is not None else 'Not available' }.")
                if plan.get('reimbursement_scope'):
                    lines.append(f"Scope: {plan['reimbursement_scope']}.")
                if plan.get('outside_network_reimbursement'):
                    lines.append(f"Outside network reimbursement: {plan['outside_network_reimbursement']}.")
                if plan.get('outside_uae_reimbursement'):
                    lines.append(f"Outside UAE reimbursement: {plan['outside_uae_reimbursement']}.")
                if plan.get('reimbursement_basis'):
                    lines.append(f"Basis: {plan['reimbursement_basis']}.")
                if plan.get('reimbursement_conditions'):
                    lines.append(f"Conditions: {plan['reimbursement_conditions']}.")
                if plan.get('reimbursement_documents_required'):
                    lines.append(f"Documents required: {plan['reimbursement_documents_required']}.")
                msg = "\n".join(lines)
                resp = {
                    "ok": True,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": "get_reimbursement_rules",
                    "data": plan,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "ok",
                    "tool": "get_reimbursement_rules",
                    "answer": plan,
                    "errors": []
                }
                return resp
            elif intent == "plan_summary":
                data = get_plan_summary(plan_name)
                # Do not validate summary output, just return if plan is ready
                data = _strip_internal_metadata(data)
                summary_text = data.get("summary_text")
                if summary_text and isinstance(summary_text, str) and summary_text.strip() and summary_text.strip().lower() not in ["none", "not available", "plan summary returned."]:
                    msg = summary_text.strip()
                else:
                    lines = []
                    lines.append(f"Plan: {data.get('plan_name')}")
                    lines.append(f"Code: {data.get('plan_code')}")
                    msg = "\n".join(lines)
                resp = {
                    "ok": True,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": "get_plan_summary",
                    "data": data,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "ok",
                    "tool": "get_plan_summary",
                    "answer": data,
                    "errors": []
                }
                return resp
        except Exception as e:
            msg = f"حدث خطأ: {e}" if is_arabic else f"Error: {e}"
            resp = {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": f"get_{intent}",
                "data": None,
                "message": msg
            }
            resp["normalized"] = {
                "status": "error",
                "tool": f"get_{intent}",
                "answer": None,
                "errors": [msg]
            }
            return resp
