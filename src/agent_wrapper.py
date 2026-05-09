PLAN_CORE_FIELDS = [
    "plan name", "plan_name", "plan code", "plan_code", "network", "network name", "network_name",
    "annual limit", "annual_limit", "area of coverage", "area", "area_of_coverage",
    "direct billing", "direct_billing", "cashless", "cash less",
    "referral required", "referral", "referral_required",
    "limit", "limt",
    "اسم الخطة", "رمز الخطة", "الشبكة", "شبكة", "الشبكه", "الحد السنوي",
    "التغطية", "تغطية", "ليمت", "الدفع المباشر", "الإحالة", "تحويل", "ريفرال", "كاشلس", "كاش ليس"
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
    # Classic 2 (plan_core only)
    "classic 2": "Classic 2",
    "classic2": "Classic 2",
    "classic-2": "Classic 2",
    "classic 02": "Classic 2",
    "hnclassic2": "Classic 2",
    "hn_classic_2": "Classic 2",
    "hn-classic-2": "Classic 2",
    "hn classic 2": "Classic 2",
    # Classic 2R
    "classic 2r": "Classic 2R",
    "classic2r": "Classic 2R",
    "classic-2r": "Classic 2R",
    "hn_classic_2r": "Classic 2R",
    "hn-classic-2r": "Classic 2R",
    "hn classic 2r": "Classic 2R",
    "كلاسيك 2r": "Classic 2R",
    # Classic 3
    "classic 3": "Classic 3",
    "classic3": "Classic 3",
    "classic-3": "Classic 3",
    "classic 03": "Classic 3",
    "hnclassic3": "Classic 3",
    "hn_classic_3": "Classic 3",
    "hn-classic-3": "Classic 3",
    "hn classic 3": "Classic 3",
    "كلاسيك 3": "Classic 3",
    "كلاسيك 03": "Classic 3",
    "كلاسيك3": "Classic 3",
}

import re

ARABIC_INDIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
EXT_ARABIC_INDIC_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

COMPARISON_ALIASES = [
    "compare",
    "قارن",
    "مقارنة",
    "الفرق بين",
    "ايه الفرق",
    "فرق",
]


def _normalize_query_text(text: str) -> str:
    normalized = (text or "").lower().translate(ARABIC_INDIC_DIGITS).translate(EXT_ARABIC_INDIC_DIGITS)
    # Minimal Arabic plan alias normalization for mixed routing.
    normalized = re.sub(r"\bريميدي\b", "remedy", normalized)
    normalized = re.sub(r"\bريمدي\b", "remedy", normalized)
    normalized = re.sub(r"\bكلاسيك\b", "classic", normalized)
    # Minimal separator normalization for comparison parsing.
    normalized = re.sub(r"\bversus\b", "vs", normalized)
    normalized = re.sub(r"\band\b", " and ", normalized)
    normalized = re.sub(r"\s+و\s+", " and ", normalized)
    return " ".join(normalized.split())


def _has_comparison_alias(text: str) -> bool:
    lowered = _normalize_query_text(text)
    return any(alias in lowered for alias in COMPARISON_ALIASES)


def _contains_alias(text: str, key: str) -> bool:
    pattern = r"(^|[\s\-_/?:.,؛،!؟()\[\]{}])" + re.escape(key) + r"($|[\s\-_/?:.,؛،!؟()\[\]{}])"
    return re.search(pattern, text) is not None

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
    text = _normalize_query_text(text)
    # English
    m = re.search(r"remedy ?0?(\d+)\s*(?:and|vs|بين)\s*remedy ?0?(\d+)", text)
    if m:
        p1, p2 = m.group(1), m.group(2)
        n1, n2 = f"Remedy 0{p1}" if len(p1)==1 else f"Remedy {p1}", f"Remedy 0{p2}" if len(p2)==1 else f"Remedy {p2}"
        if n1 in SUPPORTED_PLANS.values() and n2 in SUPPORTED_PLANS.values():
            return n1, n2
    # Generic extraction for mixed Arabic/English and Classic plans.
    has_separator = any(sep in text for sep in (" and ", " vs ", " بين "))
    all_plans = _extract_all_plan_names(text)
    if (has_separator or _has_comparison_alias(text)) and len(all_plans) >= 2:
        return all_plans[0], all_plans[1]
    return None

REIMBURSEMENT_FIELDS = [
    "reimbursement", "reimbursement allowed", "reimbursement scope", "outside network reimbursement",
    "outside uae reimbursement", "reimbursement basis", "reimbursement conditions",
    "reimbursement documents required", "documents required for reimbursement",
    "تعويض", "نطاق التعويض", "تعويض خارج الشبكة", "تعويض خارج الإمارات", "أساس التعويض", "شروط التعويض", "مستندات التعويض المطلوبة"
]

SUMMARY_PATTERNS = [
    "summarize", "summary", "overview", "give me a summary", "plan summary", "tell me about", "ملخص", "اعطني ملخص", "أعطني ملخص", "عرض ملخص", "لخص", "ملخص لخطة", "summary لخطة", "ملخص plan", "اعطني summary", "اعطني ملخص لخطة", "ملخص Remedy", "ملخص ريميدي"
]

def _extract_plan_name(text: str) -> Optional[str]:
    lowered = _normalize_query_text(text)
    found = []
    for key in sorted(SUPPORTED_PLANS.keys(), key=len, reverse=True):
        canonical = SUPPORTED_PLANS[key]
        if _contains_alias(lowered, key):
            found.append(canonical)
    if found:
        return found[0]
    return None

def _extract_all_plan_names(text: str) -> list[str]:
    lowered = _normalize_query_text(text)
    found = []
    for key in sorted(SUPPORTED_PLANS.keys(), key=len, reverse=True):
        canonical = SUPPORTED_PLANS[key]
        if _contains_alias(lowered, key) and canonical not in found:
            found.append(canonical)
    return found

def _intent_from_query(text: str) -> Optional[str]:
    lowered = _normalize_query_text(text)
    plan_name = _extract_plan_name(lowered)
    # Special-case: route explicit "maternity limit" with plan to plan_core
    if "maternity limit" in lowered:
        if plan_name:
            return "plan_core"
    # Classic 3 coverage phrasing is common in broker usage.
    if plan_name == "Classic 3" and any(token in lowered for token in ("coverage", "covered")):
        return "plan_core"
    # Keep Classic 2 coverage handling narrow to avoid broad unsupported/data-gap capture.
    if plan_name == "Classic 2" and lowered.strip() in {
        "classic 2 coverage",
        "classic2 coverage",
        "classic-2 coverage",
        "classic 02 coverage",
        "hn_classic_2 coverage",
        "hn classic 2 coverage",
    }:
        return "plan_core"
    # Comparison/recommendation intent
    rec_patterns = ["better", "recommend", "which one", "offer to client", "should i offer", "which should i offer", "which plan"]
    if _extract_comparison_plans(lowered):
        for pat in rec_patterns:
            if pat in lowered:
                return "plan_comparison"
        return "plan_comparison"
    # If two supported plans are mentioned and a rec pattern is present, treat as comparison
    all_plans = _extract_all_plan_names(lowered)
    if len(all_plans) == 2:
        for pat in rec_patterns:
            if pat in lowered:
                return "plan_comparison"
    if _has_comparison_alias(lowered) and all_plans:
        return "plan_comparison"
    # Allow comparison intent when phrasing is explicit but one side is unsupported.
    if _has_comparison_alias(lowered) and ("remedy" in lowered or "classic" in lowered):
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
    # New: plan+city+type intent
    # e.g. "What hospitals are available in Sharjah for Remedy 6?"
    city_words = ["in ", "available in ", "located in ", "في "]
    # Add plural forms for robust detection
    type_words = [
        "hospital", "hospitals",
        "clinic", "clinics",
        "pharmacy", "pharmacies",
        "medical center", "medical centers",
        "laboratory", "laboratories",
        "lab", "labs",
        "diagnostic center", "diagnostic centers"
    ]
    # Standard pattern
    if any(t in lowered for t in type_words) and any(c in lowered for c in city_words) and plan_name:
        return "plan_network_city_type"
    # Alias patterns for existing supported queries (no output/logic change)
    # e.g. "Dubai providers Remedy 6", "Providers in Dubai Remedy 6", "Remedy 6 Dubai providers", etc.
    city_aliases = ["dubai", "abu dhabi", "sharjah"]
    plan_aliases = ["remedy 6", "remedy 06"]
    provider_aliases = ["providers", "labs", "diagnostic centers", "diagnostic", "lab"]
    for city in city_aliases:
        for plan in plan_aliases:
            for prov in provider_aliases:
                # "Dubai providers Remedy 6"
                if city in lowered and prov in lowered and plan in lowered:
                    return "plan_network_city_type"
                # "Providers in Dubai Remedy 6"
                if prov in lowered and city in lowered and plan in lowered:
                    return "plan_network_city_type"
                # "Remedy 6 Dubai providers"
                if plan in lowered and city in lowered and prov in lowered:
                    return "plan_network_city_type"
    return None

def run_agent_wrapper(user_query: str) -> Dict[str, Any]:
    plan_name = _extract_plan_name(user_query)
    intent = _intent_from_query(user_query)
    is_arabic = any(c in user_query for c in '\u0627\u0623\u0625\u0622\u0628\u062a\u062b\u062c\u062d\u062e\u062d\u0632\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u064a\u0621\u0649\u0629')

    # New: plan_network_city_type intent
    if intent == "plan_network_city_type":
        # Extract city and provider type
        import re
        # Extract provider type (first match, map plural to singular for lookup)
        type_map = {
            "hospitals": "hospital",
            "hospital": "hospital",
            "clinics": "clinic",
            "clinic": "clinic",
            "pharmacies": "pharmacy",
            "pharmacy": "pharmacy",
            "medical centers": "medical center",
            "medical center": "medical center",
            "laboratories": "laboratory",
            "laboratory": "laboratory",
            "labs": "lab",
            "lab": "lab",
            "diagnostic centers": "diagnostic center",
            "diagnostic center": "diagnostic center"
        }
        provider_type = None
        lowered_query = user_query.lower()
        for t in type_map:
            if t in lowered_query:
                provider_type = type_map[t]
                break
        # Extract city (word after 'in' or 'available in' or 'في')
        city = None
        m = re.search(r"in ([A-Za-z\u0621-\u064A ]+)", user_query, re.IGNORECASE)
        if m:
            city = m.group(1).strip().split()[0]
        else:
            m = re.search(r"available in ([A-Za-z\u0621-\u064A ]+)", user_query, re.IGNORECASE)
            if m:
                city = m.group(1).strip().split()[0]
            else:
                m = re.search(r"في ([A-Za-z\u0621-\u064A ]+)", user_query, re.IGNORECASE)
                if m:
                    city = m.group(1).strip().split()[0]
        # Get plan network
        from src.v2_plan_loader import load_clean_plan
        try:
            plan_data = load_clean_plan(plan_name)
            network_name = None
            for k in ["network", "network_name", "الشبكة"]:
                if k in plan_data and plan_data[k]:
                    network_name = plan_data[k]
                    break
            if not network_name:
                msg = "Network not defined for this plan"
                return {
                    "ok": False,
                    "intent": intent,
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
            # Only support HN Basic Plus for now (minimal patch)
            if "basic plus" not in network_name.lower():
                msg = f"Network '{network_name}' not supported for provider listing"
                return {
                    "ok": False,
                    "intent": intent,
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
            from src.query.network_lookup import get_network_lookup
            lookup = get_network_lookup()
            result = lookup.list_basic_plus_providers(city=city, provider_type=provider_type)
            # Output hardening: Remove [NETWORK] and standardize heading for supported cities/categories
            if intent == "plan_network_city_type" and plan_name in ("Remedy 06", "Remedy 6") and city and provider_type:
                lines = result.splitlines()
                # Remove [NETWORK] if present
                if lines and lines[0].strip().startswith("[NETWORK]"):
                    lines = lines[1:]
                # Standardize heading for Sharjah hospitals
                if city.lower() == "sharjah" and provider_type == "hospital":
                    heading = f"Sharjah hospitals (HN Basic Plus) for Remedy 6:"
                    improved = [heading] + lines[1:] if len(lines) > 1 else [heading]
                    result = "\n".join(improved)
                # Standardize heading for Dubai/Abu Dhabi diagnostic providers (already clean, but ensure no [NETWORK])
                elif city.lower() in ("dubai", "abu", "abu dhabi") and provider_type in ("lab", "diagnostic center"):
                    city_heading = "Abu Dhabi" if city.lower().startswith("abu") else city.title()
                    heading = f"{city_heading} diagnostic providers (HN Basic Plus) for Remedy 6:"
                    improved = [heading] + lines[1:] if len(lines) > 1 else [heading]
                    result = "\n".join(improved)
            return {
                "ok": True,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": "list_basic_plus_providers",
                "data": None,
                "message": result,
                "normalized": {
                    "status": "ok",
                    "tool": "list_basic_plus_providers",
                    "answer": result,
                    "errors": []
                }
            }
        except Exception as e:
            msg = f"Error: {e}"
            return {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "error",
                    "tool": None,
                    "answer": None,
                    "errors": [msg]
                }
            }
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
        # Fallback: if not found, try all plan names in query
        if not plans:
            all_plans = _extract_all_plan_names(user_query)
            if len(all_plans) == 2:
                plans = (all_plans[0], all_plans[1])
        if not plans:
            msg = "Comparison is not supported or not available for one or both plans. Please specify two supported plans to compare." if not is_arabic else "يرجى تحديد خطتين مدعومتين للمقارنة."
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
        def _comparison_not_available():
            msg = (
                "Sorry, comparison is not supported or not available for one or both plans."
                if not is_arabic else
                "ط¹ط°ط±ط§ظ‹طŒ ط§ظ„ظ…ظ‚ط§ط±ظ†ط© ط؛ظٹط± ظ…ط¯ط¹ظˆظ…ط© ط£ظˆ ط؛ظٹط± ظ…طھط§ط­ط© ظ„ط®ط·ط© ط£ظˆ ط£ظƒط«ط±."
            )
            return {
                "ok": False,
                "intent": "plan_comparison",
                "plan_name": f"{plan1} vs {plan2}",
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
        try:
            from src.tools.enhanced_plan_loader import is_enhanced_plan
            from src.query.plan_query import load_plan
            from src.validation.plan_validator import normalize_plan, validate_plan_ready
            allow_enhanced_pair = {plan1, plan2} == {"Classic 2", "Classic 3"}
            if (is_enhanced_plan(plan1) or is_enhanced_plan(plan2)) and not allow_enhanced_pair:
                return _comparison_not_available()
            for candidate in (plan1, plan2):
                norm_candidate = normalize_plan(load_plan(candidate))
                ok_candidate, _ = validate_plan_ready(norm_candidate)
                if not ok_candidate:
                    return _comparison_not_available()
        except Exception:
            return _comparison_not_available()
        try:
            from src.query.plan_query import compare_plans
            cmp = compare_plans(plan1, plan2)
        except Exception as ex:
            # Block unsupported/unknown plans and return safe message
            msg = (
                "Sorry, comparison is not supported or not available for one or both plans."
                if not is_arabic else
                "عذراً، المقارنة غير مدعومة أو غير متاحة لخطة أو أكثر."
            )
            return {
                "ok": False,
                "intent": "plan_comparison",
                "plan_name": f"{plan1} vs {plan2}",
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
        # Only show key fields (no internal fields)
        key_fields = [
            ("annual_limit", "Annual Limit", "الحد السنوي"),
            ("pharmacy_cover_summary", "Pharmacy", "الصيدلة"),
            ("diagnostics_cover_summary", "Diagnostics", "التشخيص"),
            ("physiotherapy_cover_summary", "Physiotherapy", "العلاج الطبيعي"),
            ("direct_billing", "Direct Billing", "الدفع المباشر"),
            ("reimbursement_allowed", "Reimbursement Allowed", "التعويض"),
            ("referral_required", "Referral Required", "الإحالة"),
            ("area_of_coverage", "Area of Coverage", "نطاق التغطية"),
            ("network_name", "Network", "الشبكة"),
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
                v1 = v2 = None
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
        # Sales-friendly recommendation section (unchanged, but do not leak internal fields)
        def get_sales_recommendation():
            reasons_b = []
            reasons_a = []
            # Pharmacy
            pharm_a = cmp['differing'].get('pharmacy_cover_summary', {}).get('plan_a')
            pharm_b = cmp['differing'].get('pharmacy_cover_summary', {}).get('plan_b')
            if pharm_a and pharm_b:
                import re
                lim_a = re.search(r"AED[\s.]*([\d,]+)", pharm_a)
                lim_b = re.search(r"AED[\s.]*([\d,]+)", pharm_b)
                if lim_a and lim_b:
                    val_a = int(lim_a.group(1).replace(",", ""))
                    val_b = int(lim_b.group(1).replace(",", ""))
                    if val_b > val_a:
                        reasons_b.append(f"Higher pharmacy limit (AED {val_b:,} vs {val_a:,})")
                    elif val_a > val_b:
                        reasons_a.append(f"Higher pharmacy limit (AED {val_a:,} vs {val_b:,})")
            # Physio
            physio_a = cmp['differing'].get('physiotherapy_cover_summary', {}).get('plan_a')
            physio_b = cmp['differing'].get('physiotherapy_cover_summary', {}).get('plan_b')
            import re
            def physio_sessions(val):
                if not val:
                    return 0
                m = re.search(r"(\d{1,3})\s*(sessions|جلسة)", val)
                return int(m.group(1)) if m else 0
            s_a = physio_sessions(physio_a)
            s_b = physio_sessions(physio_b)
            if s_b > s_a:
                reasons_b.append(f"Better physiotherapy coverage ({s_b} sessions vs {s_a})")
            elif s_a > s_b:
                reasons_a.append(f"Better physiotherapy coverage ({s_a} sessions vs {s_b})")
            # Diagnostics (just mention if different)
            diag_a = cmp['differing'].get('diagnostics_cover_summary', {}).get('plan_a')
            diag_b = cmp['differing'].get('diagnostics_cover_summary', {}).get('plan_b')
            if diag_a and diag_b and diag_a != diag_b:
                reasons_b.append("Stronger diagnostics benefits")
            # Referral
            ref_a = cmp['differing'].get('referral_required', {}).get('plan_a')
            ref_b = cmp['differing'].get('referral_required', {}).get('plan_b')
            if ref_b is False and ref_a is not False:
                reasons_b.append("No referral required")
            if ref_a is False and ref_b is not False:
                reasons_a.append("No referral required")
            # Reimbursement
            reimb_a = cmp['differing'].get('reimbursement_allowed', {}).get('plan_a')
            reimb_b = cmp['differing'].get('reimbursement_allowed', {}).get('plan_b')
            if reimb_a and not reimb_b:
                reasons_a.append("Reimbursement flexibility is important")
            if reimb_b and not reimb_a:
                reasons_b.append("Reimbursement flexibility is important")
            # Compose recommendation
            rec_lines = ["Recommendation:"]
            if reasons_b:
                rec_lines.append(f"{plan2} is generally better if your client is looking for stronger outpatient benefits:")
                for r in reasons_b:
                    rec_lines.append(f"- {r}")
            if reasons_a:
                if reasons_b:
                    rec_lines.append("")
                rec_lines.append(f"{plan1} may be preferred if:")
                for r in reasons_a:
                    rec_lines.append(f"- {r}")
            if not reasons_a and not reasons_b:
                rec_lines.append("Both plans are very similar in their key benefits.")
            return "\n".join(rec_lines)
        # Old similarity/difference logic for fallback
        def score(plan):
            score = 0
            for field in ["pharmacy_cover_summary", "diagnostics_cover_summary", "physiotherapy_cover_summary"]:
                val = cmp['differing'].get(field, {}).get('plan_a' if plan == plan1 else 'plan_b')
                if val and isinstance(val, str) and ("unlimited" in val.lower() or "covered" in val.lower() or "yes" in val.lower()):
                    score += 2
                elif val:
                    score += 1
            direct = cmp['differing'].get("referral_required", {}).get('plan_a' if plan == plan1 else 'plan_b')
            if direct is False:
                score += 2
            return score
        s1 = score(plan1)
        s2 = score(plan2)
        if s1 == s2:
            diffs = []
            for field, label_en, _ in key_fields:
                v1 = cmp['differing'].get(field, {}).get('plan_a')
                v2 = cmp['differing'].get(field, {}).get('plan_b')
                if v1 != v2 and v1 is not None and v2 is not None:
                    diffs.append(f"{label_en}: {plan1}={v1}, {plan2}={v2}")
            if diffs:
                lines.append("")
                lines.append(f"Both plans are similar overall, but differ in: {', '.join(diffs)}.")
            else:
                lines.append("")
                lines.append("Both plans are very similar in their key benefits.")
        lines.append("")
        lines.append(get_sales_recommendation())
        # Filter out internal fields from message (no approval_status, tests_passed, source_trace, raw dicts)
        msg = "\n".join(lines)
        forbidden = ["approval_status", "tests_passed", "source_trace", "status", "tool", "answer", "errors", "{", "}"]
        for key in forbidden:
            if key in msg:
                msg = msg.replace(key, "")
        return {
            "ok": True,
            "intent": "plan_comparison",
            "plan_name": f"{plan1} vs {plan2}",
            "tool_name": "compare_plans",
            "data": None,  # Do not expose raw cmp
            "message": msg,
            "normalized": {
                "status": "ok",
                "tool": "compare_plans",
                "answer": None,
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
    import re
    def _strip_internal_metadata(d):
        if isinstance(d, dict):
            d = dict(d)
            d.pop("approval_status", None)
            d.pop("tests_passed", None)
            d.pop("source_trace", None)
        return d
    if intent in ("plan_core", "reimbursement_rules", "plan_summary"):
        try:
            # Classic 2: use authoritative enhanced loader for readiness and data
            if plan_name == "Classic 2":
                from src.tools.internal_loader_hn_classic_2 import load_internal_hn_classic_2
                full_plan = load_internal_hn_classic_2()
            else:
                from src.query.plan_query import load_plan
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
