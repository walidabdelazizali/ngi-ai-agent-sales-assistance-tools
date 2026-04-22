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
    # If no supported plan or no supported intent, always return unsupported envelope
    if not plan_name or intent not in ("plan_core", "reimbursement_rules", "plan_summary"):
        if is_arabic:
            resp = {
                "ok": False,
                "intent": "unsupported",
                "plan_name": None,
                "tool_name": None,
                "data": None,
                "message": "عذراً، النظام يدعم فقط الريميدي 03 والريميدي 04 والريميدي 05 حالياً."
            }
        else:
            resp = {
                "ok": False,
                "intent": "unsupported",
                "plan_name": None,
                "tool_name": None,
                "data": None,
                "message": "No supported plan and/or intent found in query. Supported plans: Remedy 03, Remedy 04, Remedy 05. Supported intents: plan_core, reimbursement_rules, plan_summary."
            }
        resp["normalized"] = {
            "status": "not_found",
            "tool": None,
            "answer": None,
            "errors": [resp["message"]]
        }
        return resp
    if intent == "plan_core":
        try:
            data = get_plan_core(plan_name)
            msg = "تم عرض معلومات الخطة الأساسية." if is_arabic else "Plan core fields returned."
            resp = {
                "ok": True,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": "get_plan_core",
                "data": data,
                "message": msg
            }
            resp["normalized"] = {
                "status": "ok",
                "tool": "get_plan_core",
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
                "tool_name": "get_plan_core",
                "data": None,
                "message": msg
            }
            resp["normalized"] = {
                "status": "error",
                "tool": "get_plan_core",
                "answer": None,
                "errors": [msg]
            }
            return resp
    if intent == "reimbursement_rules":
        try:
            data = get_reimbursement_rules(plan_name)
            msg = "تم عرض قواعد التعويض." if is_arabic else "Reimbursement rules returned."
            resp = {
                "ok": True,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": "get_reimbursement_rules",
                "data": data,
                "message": msg
            }
            resp["normalized"] = {
                "status": "ok",
                "tool": "get_reimbursement_rules",
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
                "tool_name": "get_reimbursement_rules",
                "data": None,
                "message": msg
            }
            resp["normalized"] = {
                "status": "error",
                "tool": "get_reimbursement_rules",
                "answer": None,
                "errors": [msg]
            }
            return resp
    if intent == "plan_summary":
        try:
            data = get_plan_summary(plan_name)
            msg = "تم عرض ملخص الخطة." if is_arabic else "Plan summary returned."
            # Patch: Safe Arabic summary localization (labels and values)
            if is_arabic and data and data.get("summary_text"):
                ar_labels = {
                    "Plan Name": "اسم الخطة",
                    "Plan Code": "رمز الخطة",
                    "Network": "الشبكة",
                    "Annual Limit": "الحد السنوي",
                    "Area of Coverage": "نطاق التغطية",
                    "Direct Billing": "الدفع المباشر",
                    "Referral Required": "الإحالة مطلوبة",
                    "Maternity Cover": "تغطية الأمومة",
                    "Inpatient Cover": "تغطية المرضى الداخليين",
                    "Outpatient Cover": "تغطية العيادات الخارجية",
                    "Pharmacy Cover": "تغطية الصيدلية",
                    "Key Exclusions": "الاستثناءات الأساسية",
                }
                # Only replace full label lines, not substrings
                summary_lines = data["summary_text"].split("\n")
                localized_lines = []
                for line in summary_lines:
                    colon_idx = line.find(":")
                    if colon_idx > 0:
                        label = line[:colon_idx].strip()
                        value = line[colon_idx+1:].strip()
                        # Localize label if present
                        label_ar = ar_labels.get(label, label)
                        # Localize value if exact
                        if value == "Yes":
                            value_ar = "نعم"
                        elif value == "No":
                            value_ar = "لا"
                        elif value in ("Not available", "None", "null", "None listed"):
                            value_ar = "غير متوفر"
                        elif value == "لا يوجد":
                            value_ar = value
                        else:
                            value_ar = value
                        localized_lines.append(f"{label_ar}: {value_ar}")
                    else:
                        # For lines like "Key Exclusions: 3 listed"
                        for en, ar in ar_labels.items():
                            if line.startswith(en):
                                line = line.replace(en, ar, 1)
                        # Patch for "listed" count
                        if "listed" in line:
                            line = line.replace("listed", "عنصر/عناصر")
                        localized_lines.append(line)
                summary_text = "\n".join(localized_lines)
                data = dict(data)
                data["summary_text"] = summary_text
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
                "tool_name": "get_plan_summary",
                "data": None,
                "message": msg
            }
            resp["normalized"] = {
                "status": "error",
                "tool": "get_plan_summary",
                "answer": None,
                "errors": [msg]
            }
            return resp
