# --- Lead qualification helpers ---
import re
def _has_lead_qualification_intent(text: str, lang: str) -> bool:
    t = text.strip().lower()
    if lang == "ar":
        # Arabic triggers: employee count, renewal, budget, company+insurance, preferred network/location, explicit pricing, or just a company
        if re.search(r"[0-9]+\s*(موظف|موظفين)", t):
            return True
        if re.search(r"تجديد|انتهاء|الشهر الجاي", t):
            return True
        if re.search(r"ميزانية|السعر|الأسعار", t):
            return True
        if re.search(r"شركة.*تأمين طبي", t):
            return True
        if re.search(r"(عيادات|مستشفيات).*(الشارقة|دبي|عجمان|ابوظبي|أبوظبي)", t):
            return True
        if re.search(r"عايز أعرف الأسعار", t):
            return True
        if re.fullmatch(r".*شركة.*", t):
            return True
        return False
    else:
        # English triggers: employees+number, renewal/expiry, budget/price, company+medical insurance, current policy, preferred hospitals/clinics+city, or just a company
        if re.search(r"[0-9]+\s*employees", t):
            return True
        if re.search(r"renewal|expiry|expiring|expire|next month|this month", t):
            return True
        if re.search(r"budget|price|low budget|tight budget|cost", t):
            return True
        if re.search(r"company.*medical insurance", t):
            return True
        if re.search(r"current policy", t):
            return True
        if re.search(r"(hospitals|clinics).*(sharjah|dubai|ajman|abu dhabi)", t):
            return True
        if re.fullmatch(r".*company.*", t):
            return True
        return False

def _build_lead_qualification_answer(text: str, lang: str) -> str:
    qual = detect_lead_qualification(text, lang)
    def extract_company_size(text):
        m = re.search(r"([0-9]+)\s*(موظف|موظفين|موظفة|lives|employees|employee)", text, re.IGNORECASE)
        return m.group(1) if m else None
    def extract_renewal_timing(text):
        # Match 'renewal is next month', 'renewal next month', 'renewal is soon', etc.
        m = re.search(r"renewal( is|\s*)?( next month| this month| soon)?", text, re.IGNORECASE)
        if m and m.group(0):
            # Prefer to return 'next month', 'this month', 'soon' if present
            if 'next month' in m.group(0):
                return 'next month'
            if 'this month' in m.group(0):
                return 'this month'
            if 'soon' in m.group(0):
                return 'soon'
            return m.group(0)
        # Arabic and other fallback
        m = re.search(r"(التجديد\s*[^-\s]+|ينتهي\s*[^-\s]+|ينتهى\s*[^-\s]+|الشهر الجاي|قريب)", text, re.IGNORECASE)
        return m.group(0) if m else None
    def extract_budget_status(text):
        m = re.search(r"(ميزانية|budget|low budget|قليلة|محدودة|tight budget|cost|سعر|سعرها|سعره|سعرهم)", text, re.IGNORECASE)
        return m.group(0) if m else None
    def extract_preferred_network(text):
        m = re.search(r"((عيادات|مستشفيات|مستشفى|hospital|clinic|clinics|network|شبكة|pharmacy|صيدلية|labs|مختبر|مفضل|مفضلة)(\s*(في|in)\s*[^-\s]+)?)", text, re.IGNORECASE)
        return m.group(0) if m else None
    def extract_current_policy(text):
        m = re.search(r"(شركة ثانية|عرض|وثيقة|policy|current insurer|another quote|quote|proposal|insurance company|شركة تأمين|وثيقة حالية)", text, re.IGNORECASE)
        return m.group(0) if m else None
    def extract_decision_maker(text):
        m = re.search(r"(decision maker|مدير|المدير|مسافر|traveling|not available|غير متوفر|غير موجود|مشغول)", text, re.IGNORECASE)
        return m.group(0) if m else None
    company_size = extract_company_size(text)
    renewal_timing = extract_renewal_timing(text)
    budget_status = extract_budget_status(text)
    preferred_network = extract_preferred_network(text)
    current_policy = extract_current_policy(text)
    decision_maker = extract_decision_maker(text)
    next_required_documents = []
    for act in qual['next_actions']:
        if lang == "ar":
            if any(x in act for x in ["census", "الرخصة التجارية", "وثيقة"]):
                next_required_documents.append(act)
        else:
            if any(x in act for x in ["census", "trade license", "policy"]):
                next_required_documents.append(act)
    def show(val, ar=False):
        if not val:
            return "غير محدد" if ar else "unknown"
        return val
    if lang == "ar":
        lines = ["تقييم الفرصة:"]
        status_map = {"strong": "قوية", "medium": "متوسطة", "weak": "ضعيفة"}
        lines.append(f"- الحالة: {status_map.get(qual['status'], qual['status'])}")
        lines.append(f"- السبب: {'، '.join(qual['reasons'])}")
        lines.append("")
        lines.append("حقول التقاط العميل:")
        lines.append(f"- عدد الموظفين: {show(company_size, True)}")
        lines.append(f"- توقيت التجديد: {show(renewal_timing, True)}")
        lines.append(f"- حالة الميزانية: {show(budget_status, True)}")
        lines.append(f"- الشبكة أو المستشفيات المفضلة: {show(preferred_network, True)}")
        lines.append(f"- توفر وثيقة حالية: {show(current_policy, True)}")
        lines.append(f"- حالة متخذ القرار: {show(decision_maker, True)}")
        lines.append(f"- المستندات المطلوبة التالية: {', '.join(next_required_documents) if next_required_documents else 'غير محدد'}")
        lines.append("")
        lines.append("الخطوة التالية:")
        for act in qual['next_actions']:
            lines.append(f"- {act}")
        return "\n".join(lines)
    else:
        lines = ["Lead Qualification:"]
        status_map = {"strong": "Strong", "medium": "Medium", "weak": "Weak"}
        lines.append(f"- Status: {status_map.get(qual['status'], qual['status']).capitalize()}")
        lines.append(f"- Reason: {', '.join(qual['reasons'])}")
        lines.append("")
        lines.append("Lead Capture Fields:")
        lines.append(f"- company_size: {show(company_size)}")
        lines.append(f"- renewal_timing: {show(renewal_timing)}")
        lines.append(f"- budget_status: {show(budget_status)}")
        lines.append(f"- preferred_network_or_hospitals: {show(preferred_network)}")
        lines.append(f"- current_policy_available: {show(current_policy)}")
        lines.append(f"- decision_maker_status: {show(decision_maker)}")
        lines.append(f"- next_required_documents: {', '.join(next_required_documents) if next_required_documents else 'unknown'}")
        lines.append("")
        lines.append("Recommended next action:")
        for act in qual['next_actions']:
            lines.append(f"- {act}")
        return "\n".join(lines)
def detect_lead_qualification(text: str, lang: str = "en") -> dict:
    import re
    t = text.strip().lower()
    # --- Signal detection ---
    signals = {
        "employee_count": False,
        "renewal": False,
        "budget": False,
        "network_pref": False,
        "current_policy": False,
        "urgency": False,
        "decision_maker": False,
        "location": False,
    }
    # Employee count
    if re.search(r"([0-9]+)\s*(موظف|موظفين|موظفة|lives|employees|employee)", t):
        signals["employee_count"] = True
    # Renewal/expiry
    if re.search(r"(تجديد|التجديد|renewal|expiry|expiring|expire|ينتهي|ينتهى|الشهر الجاي|next month|this month|soon|قريب)", t):
        signals["renewal"] = True
    # Budget
    if re.search(r"(ميزانية|budget|low budget|قليلة|محدودة|tight budget|cost|سعر|سعرها|سعره|سعرهم)", t):
        signals["budget"] = True
    # Network/hospital/clinic preference
    if re.search(r"(مستشفى|مستشفيات|عيادة|عيادات|hospital|clinic|clinics|preferred|network|شبكة|pharmacy|صيدلية|labs|مختبر|مفضل|مفضلة|في الشارقة|in sharjah|in dubai|in abu dhabi|في دبي|في أبوظبي|في عجمان|in ajman)", t):
        signals["network_pref"] = True
        signals["location"] = True
    # Current policy/quote/insurer
    if re.search(r"(شركة ثانية|عرض|وثيقة|policy|current insurer|another quote|quote|proposal|insurance company|شركة تأمين|وثيقة حالية)", t):
        signals["current_policy"] = True
    # Urgency
    if re.search(r"(مستعجل|بسرعة|urgency|urgent|asap|soon|قريب|محتاج أخلص بسرعة|محتاج بسرعة|مستعجل|مستعجلة)", t):
        signals["urgency"] = True
    # Decision maker
    if re.search(r"(decision maker|مدير|المدير|مسافر|traveling|not available|غير متوفر|غير موجود|مشغول)", t):
        signals["decision_maker"] = True
    # Location (already covered in network_pref)

    # --- Scoring ---
    if signals["employee_count"] and (signals["renewal"] or signals["urgency"] or signals["network_pref"] or signals["budget"] or signals["current_policy"]):
        status = "strong"
    elif any([signals["employee_count"], signals["renewal"], signals["budget"], signals["network_pref"], signals["current_policy"]]):
        status = "medium"
    else:
        status = "weak"

    # --- Reason ---
    reasons = []
    if signals["employee_count"]:
        reasons.append("employee count known" if lang == "en" else "عدد الموظفين واضح")
    else:
        reasons.append("employee count unknown" if lang == "en" else "عدد الموظفين غير محدد")
    if signals["renewal"]:
        reasons.append("renewal/expiry known" if lang == "en" else "تجديد أو انتهاء واضح")
    if signals["budget"]:
        reasons.append("budget known" if lang == "en" else "الميزانية واضحة")
    if signals["network_pref"]:
        reasons.append("network/hospital preference known" if lang == "en" else "تم تحديد شبكة/موقع مفضل")
    if signals["current_policy"]:
        reasons.append("current policy/quote known" if lang == "en" else "يوجد عرض أو وثيقة حالية")
    if signals["urgency"]:
        reasons.append("urgency/fast timeline" if lang == "en" else "يوجد استعجال أو حاجة قريبة")
    if signals["decision_maker"]:
        reasons.append("decision maker status mentioned" if lang == "en" else "تم ذكر حالة متخذ القرار")

    # --- Next action ---
    next_actions = []
    if not signals["employee_count"]:
        next_actions.append("ask for census" if lang == "en" else "أرسل census sheet")
    if not signals["current_policy"]:
        next_actions.append("ask for current policy" if lang == "en" else "أرسل آخر وثيقة إن وجدت")
    if not signals["budget"]:
        next_actions.append("ask for budget" if lang == "en" else "حدد الميزانية المطلوبة")
    if not signals["network_pref"]:
        next_actions.append("ask for preferred hospitals" if lang == "en" else "حدد المستشفيات أو الشبكة المطلوبة")
    next_actions.append("ask for trade license" if lang == "en" else "أرسل الرخصة التجارية")
    next_actions.append("schedule short meeting" if lang == "en" else "حدد موعد مكالمة قصيرة")
    if status == "strong":
        next_actions.append("prepare quotation" if lang == "en" else "جهز عرض سعر")

    return {
        "status": status,
        "reasons": reasons,
        "next_actions": next_actions,
    }
"""
Business-facing deterministic answer shaping for Remedy plans.
- Executive summaries
- Business-friendly comparisons
- Bilingual (English/Arabic) output
- No AI, no inference, no hallucination
- All outputs traceable to structured fields
"""

from src.query.plan_query import (
    answer_owner_query,
    compare_plans,
    get_plan_field,
    summarize_plan,
    _PLAN_ALIASES,
    OWNER_FIELDS,
)

from src.parsers.canonical_schema import BUSINESS_FIELDS

# --- Business answer shaping helpers ---

def explain_plan_for_business(plan_name: str, language: str = "en") -> str:
    """
    Short business summary for a plan (executive/client-facing).
    """
    try:
        summary = summarize_plan(plan_name)
    except Exception:
        return _fallback(language)
    plan_code = summary.get("plan_code")
    lines = []
    if language == "ar":
        lines.append(f"ملخص تنفيذي لخطة {plan_name} ({plan_code}):")
    else:
        lines.append(f"Executive summary for {plan_name} ({plan_code}):")
    for line in summary["summary_text"].split("\n"):
        if language == "ar":
            # Simple deterministic mapping for demo; real translation would be more thorough
            line = (
                line.replace("Annual Limit", "الحد السنوي")
                    .replace("Pharmacy", "الصيدلية")
                    .replace("Maternity", "الحمل")
                    .replace("Network", "الشبكة")
                    .replace("Key Exclusions", "الاستثناءات الأساسية")
            )
        lines.append(line)
    if language == "ar":
        lines.append("هذا الملخص مخصص للعرض التنفيذي أو للعميل. لا يوجد استنتاجات إضافية.")
    else:
        lines.append("This summary is for executive or client-facing use. No additional inference.")
    return "\n".join(lines)

def explain_plan_comparison(plan_a: str, plan_b: str, language: str = "en", mode: str = "executive") -> str:
    """
    Short executive summary of differences between two plans.
    """
    try:
        comp = compare_plans(plan_a, plan_b)
    except Exception:
        return _fallback(language)
    diffs = comp.get("differing", {})
    plan_a_code = comp.get("plan_a_code", plan_a)
    plan_b_code = comp.get("plan_b_code", plan_b)
    lines = []
    if language == "ar":
        lines.append(f"مقارنة تنفيذية بين {plan_a} و {plan_b}:")
    else:
        lines.append(f"Executive comparison: {plan_a} vs {plan_b}")
    if not diffs:
        if language == "ar":
            lines.append("لا يوجد فرق جوهري بين الخطتين. جميع المزايا متساوية أو متشابهة.")
        else:
            lines.append("No material difference found. All key benefits are equal or similar.")
        return "\n".join(lines)
    # Show most material differences first (annual_limit, pharmacy, maternity, outpatient, diagnostics, physiotherapy)
    priority = [
        "annual_limit", "pharmacy_cover_summary", "maternity_cover", "outpatient_cover_summary",
        "diagnostics_cover_summary", "physiotherapy_cover_summary"
    ]
    shown = set()
    for field in priority:
        if field in diffs:
            _append_diff(lines, field, diffs[field], plan_a, plan_b, language)
            shown.add(field)
    # Show other differences
    for field, diff in diffs.items():
        if field in shown:
            continue
        _append_diff(lines, field, diff, plan_a, plan_b, language)
    if language == "ar":
        lines.append("تمت المقارنة بناءً على البيانات المتوفرة فقط. لا يوجد استنتاجات إضافية.")
    else:
        lines.append("Comparison is strictly based on available data. No additional inference.")
    return "\n".join(lines)

import re
def _parse_max_and_copay(text):
    """Extract numeric max and copay from a benefit summary string."""
    max_match = re.search(r"max(?:imum)?\s*(AED\.?|د\.إ\.?|)\s*([\d,]+)", text, re.IGNORECASE)
    copay_match = re.search(r"(\d{1,2})%\s*(co-?pay|payable|تحمل|نسبة)", text, re.IGNORECASE)
    max_val = int(max_match.group(2).replace(",", "")) if max_match else None
    copay_val = int(copay_match.group(1)) if copay_match else None
    return max_val, copay_val

def _append_diff(lines, field, diff, plan_a, plan_b, language):
    label = field.replace("_", " ").capitalize()
    a_val = diff["plan_a"]
    b_val = diff["plan_b"]
    # Annual limit (numeric, higher is better)
    if field == "annual_limit":
        try:
            a_num = int(str(a_val).replace(",", "").replace("AED.", "").replace("د.إ.", "").strip())
            b_num = int(str(b_val).replace(",", "").replace("AED.", "").replace("د.إ.", "").strip())
            if a_num > b_num:
                if language == "ar":
                    lines.append(f"{plan_a} أقوى في الحد السنوي ({a_num} مقابل {b_num})")
                else:
                    lines.append(f"{plan_a} has a higher annual limit ({a_num} vs {b_num}) and is stronger for annual limit.")
            elif b_num > a_num:
                if language == "ar":
                    lines.append(f"{plan_b} أقوى في الحد السنوي ({b_num} مقابل {a_num})")
                else:
                    lines.append(f"{plan_b} has a higher annual limit ({b_num} vs {a_num}) and is stronger for annual limit.")
            else:
                if language == "ar":
                    lines.append(f"الحد السنوي متساوي ({a_num})")
                else:
                    lines.append(f"Annual limit is equal ({a_num})")
            return
        except Exception:
            pass
    # Pharmacy/maternity/diagnostics/physiotherapy/outpatient: parse max and copay
    benefit_fields = {
        "pharmacy_cover_summary": ("pharmacy", "الأدوية"),
        "maternity_cover": ("maternity", "الحمل"),
        "diagnostics_cover_summary": ("diagnostics", "التحاليل"),
        "physiotherapy_cover_summary": ("physiotherapy", "العلاج الطبيعي"),
        "outpatient_cover_summary": ("outpatient", "العلاج الخارجي"),
    }
    if field in benefit_fields:
        a_max, a_copay = _parse_max_and_copay(str(a_val))
        b_max, b_copay = _parse_max_and_copay(str(b_val))
        field_en, field_ar = benefit_fields[field]
        # Both max and copay present
        if a_max and b_max and a_copay is not None and b_copay is not None:
            if a_max > b_max and a_copay <= b_copay:
                if language == "ar":
                    lines.append(f"{plan_a} أقوى في {field_ar} (حد أعلى {a_max} ونسبة تحمل {a_copay}%)")
                else:
                    lines.append(f"{plan_a} is stronger for {field_en} (higher max {a_max}, copay {a_copay}%)")
                return
            elif b_max > a_max and b_copay <= a_copay:
                if language == "ar":
                    lines.append(f"{plan_b} أقوى في {field_ar} (حد أعلى {b_max} ونسبة تحمل {b_copay}%)")
                else:
                    lines.append(f"{plan_b} is stronger for {field_en} (higher max {b_max}, copay {b_copay}%)")
                return
            elif (a_max > b_max and a_copay > b_copay) or (b_max > a_max and b_copay > a_copay):
                if language == "ar":
                    lines.append(f"اختلاف مختلط في {field_ar} (حد أعلى ونسبة تحمل متعاكسان)")
                else:
                    lines.append(f"Mixed difference for {field_en} (higher max but higher copay)")
                return
            elif a_max == b_max and a_copay == b_copay:
                if language == "ar":
                    lines.append(f"{field_ar} متساوي (حد أعلى {a_max} ونسبة تحمل {a_copay}%)")
                else:
                    lines.append(f"{field_en.capitalize()} is equal (max {a_max}, copay {a_copay}%)")
                return
        # Only max present
        elif a_max and b_max:
            if a_max > b_max:
                if language == "ar":
                    lines.append(f"{plan_a} أقوى في {field_ar} (حد أعلى {a_max})")
                else:
                    lines.append(f"{plan_a} is stronger for {field_en} (higher max {a_max})")
                return
            elif b_max > a_max:
                if language == "ar":
                    lines.append(f"{plan_b} أقوى في {field_ar} (حد أعلى {b_max})")
                else:
                    lines.append(f"{plan_b} is stronger for {field_en} (higher max {b_max})")
                return
            else:
                if language == "ar":
                    lines.append(f"{field_ar} متساوي (حد أعلى {a_max})")
                else:
                    lines.append(f"{field_en.capitalize()} is equal (max {a_max})")
                return
        # Only copay present
        elif a_copay is not None and b_copay is not None:
            if a_copay < b_copay:
                if language == "ar":
                    lines.append(f"{plan_a} نسبة تحمل أقل في {field_ar} ({a_copay}% مقابل {b_copay}%)")
                else:
                    lines.append(f"{plan_a} has lower copay for {field_en} ({a_copay}% vs {b_copay}%)")
                return
            elif b_copay < a_copay:
                if language == "ar":
                    lines.append(f"{plan_b} نسبة تحمل أقل في {field_ar} ({b_copay}% مقابل {a_copay}%)")
                else:
                    lines.append(f"{plan_b} has lower copay for {field_en} ({b_copay}% vs {a_copay}%)")
                return
            else:
                if language == "ar":
                    lines.append(f"{field_ar} متساوي (نسبة تحمل {a_copay}%)")
                else:
                    lines.append(f"{field_en.capitalize()} is equal (copay {a_copay}%)")
                return
    # Fallback: just show the difference
    if language == "ar":
        lines.append(f"{label}: {plan_a}: {a_val} | {plan_b}: {b_val}")
    else:
        lines.append(f"{label}: {plan_a}: {a_val} | {plan_b}: {b_val}")

def answer_business_query(text: str) -> str:
    # --- CLOSING INTENT DETECTION ---
    import re
    t = text.strip().lower()

    # --- ROUTING PRIORITY ---
    # 1. Multi-intent (plan + network)
    plan_pat = r"(remedy\s*0?[23456]|ريميدي\s*0?[23456])"
    plan_intent = re.search(plan_pat, t) and ("مميزات" in t or "benefits" in t or "summary" in t or "ملخص" in t)
    network_intent = (
        re.search(r"(clinics|hospitals|labs|pharmacies|عيادات|مستشفيات|تحاليل|صيدليات)", t)
        and re.search(r"(sharjah|dubai|ajman|abu dhabi|الشارقة|دبي|عجمان|ابوظبي|أبوظبي)", t)
    )
    # 2. Plan-only intent
    # 3. Explicit closing/decision intent
    closing_patterns_en = [
        r"should i choose", r"which plan do you recommend", r"recommend.*plan", r"is this plan suitable", r"is remedy [0-9]+ suitable", r"suitable for.*company", r"best plan for low budget", r"which plan is better", r"finalize.*plan", r"decision", r"next step", r"practical option", r"upgrade plan", r"choose remedy"
    ]
    closing_patterns_ar = [
        r"هل الخطة مناسبة", r"أنصحني بأي خطة", r"أي خطة أفضل", r"عايز أقفل على خطة", r"هل remedy [0-9]+ كويسة", r"هل remedy [0-9]+ مناسبة", r"ايه احسن خطة لو الميزانية قليلة", r"هل أختار remedy [0-9]+", r"اختيار خطة", r"الخطوة التالية", r"قرار", r"انهاء.*خطة"
    ]
    closing_patterns = closing_patterns_en + closing_patterns_ar
    is_closing = any(re.search(pat, t) for pat in closing_patterns)

    # 4. Lead qualification: only match if explicit pricing query in Arabic or concrete multi-signal English query (not explicit closing)
    business_intent_patterns = [
        r"تأمين طبي", r"insurance", r"policy", r"شركة", r"company", r"موظف", r"employees", r"renewal", r"budget", r"network", r"مستشفى", r"عيادة", r"عرض", r"وثيقة", r"decision maker", r"مدير"
    ]
    is_lead_qualification = any(re.search(pat, t) for pat in business_intent_patterns)
    is_arabic = any(ord(c) >= 0x0600 for c in text)
    # Arabic: only trigger lead qualification for explicit pricing queries
    is_arabic_pricing = re.search(r"أسعار", t)
    # English: only trigger lead qualification if at least two concrete lead signals (employees + renewal/budget/current policy, or renewal + budget/current policy)
    english_signals = [bool(re.search(r"employees", t)), bool(re.search(r"renewal", t)), bool(re.search(r"budget", t)), bool(re.search(r"current policy", t))]
    english_lead_combo = sum(english_signals) >= 2

    lang = "ar" if any(ord(c) >= 0x0600 for c in text) else "en"
    # If all lead qualification fields are present in English, always use lead qualification output
    if lang == "en":
        # Check for all fields: employees, renewal, budget, preferred network, current policy, decision maker
        all_fields = [
            re.search(r"[0-9]+\s*employees", t),
            re.search(r"renewal|expiry|expiring|expire|next month|this month", t),
            re.search(r"budget|price|low budget|tight budget|cost", t),
            re.search(r"(hospitals|clinics|network|preferred hospitals|broad network)", t),
            re.search(r"current policy|current policy available|insurance company|another quote|proposal", t),
            re.search(r"decision maker|present", t),
        ]
        if all(all_fields):
            return _build_lead_qualification_answer(text, lang)
    if plan_intent and network_intent:
        pass
    elif not is_closing and _has_lead_qualification_intent(text, lang):
        return _build_lead_qualification_answer(text, lang)
    # ...existing code for other branches...
    # (fall through to existing multi-intent/plan/closing/other logic below)
    closing_patterns_en = [
        r"is this plan suitable", r"is remedy [0-9]+ suitable", r"suitable for.*company", r"which plan do you recommend", r"best plan for low budget", r"i have [0-9]+ employees", r"should i choose remedy [0-9]+", r"low budget", r"suitable for my company", r"close on a plan", r"practical option", r"upgrade plan", r"choose remedy", r"which plan is better", r"recommend.*plan", r"next step", r"decision", r"finalize.*plan"
    ]
    closing_patterns_ar = [
        r"هل الخطة مناسبة", r"أنصحني بأي خطة", r"أي خطة أفضل", r"ميزانيتي قليلة", r"عندي [0-9]+ موظف", r"عايز أقفل على خطة", r"هل remedy [0-9]+ كويسة", r"هل remedy [0-9]+ مناسبة", r"ايه احسن خطة لو الميزانية قليلة", r"هل أختار remedy [0-9]+", r"اختيار خطة", r"الخطوة التالية", r"قرار", r"انهاء.*خطة"
    ]
    # Detect language
    lang = "ar" if any(ord(c) >= 0x0600 for c in text) else "en"
    closing_match = False
    if lang == "ar":
        for pat in closing_patterns_ar:
            if re.search(pat, t):
                closing_match = True
                break
    else:
        for pat in closing_patterns_en:
            if re.search(pat, t):
                closing_match = True
                break

    # --- CLOSING RESPONSE ---
    if closing_match:
        # Extract plan(s) and employee count if present
        plan_pat = r"remedy\s*0?[23456]|ريميدي\s*0?[23456]"
        plan_matches = re.findall(plan_pat, t)
        # Normalize plan names
        plan_map = {
            "remedy 02": "Remedy 02", "remedy 2": "Remedy 02", "ريميدي 02": "Remedy 02", "ريميدي 2": "Remedy 02",
            "remedy 03": "Remedy 03", "remedy 3": "Remedy 03", "ريميدي 03": "Remedy 03", "ريميدي 3": "Remedy 03",
            "remedy 04": "Remedy 04", "remedy 4": "Remedy 04", "ريميدي 04": "Remedy 04", "ريميدي 4": "Remedy 04",
            "remedy 05": "Remedy 05", "remedy 5": "Remedy 05", "ريميدي 05": "Remedy 05", "ريميدي 5": "Remedy 05",
            "remedy 06": "Remedy 06", "remedy 6": "Remedy 06", "ريميدي 06": "Remedy 06", "ريميدي 6": "Remedy 06",
        }
        plans = [plan_map.get(p.replace(" ", "").replace("ريميدي", "Remedy ").replace("remedy", "Remedy ").replace("0", "").strip().lower(), p) for p in plan_matches]
        plans = [p for p in plans if p]
        # Try to get facts for the first plan
        plan_facts = None
        plan_name = plans[0] if plans else None
        if plan_name:
            try:
                summary = summarize_plan(plan_name)
                plan_facts = summary
            except Exception:
                plan_facts = None
        # Extract employee count if present
        emp_count = None
        emp_match = re.search(r"([0-9]+)\s*(موظف|employees)", t)
        if emp_match:
            emp_count = emp_match.group(1)
        # Compose safe, conservative closing
        if lang == "ar":
            lines = []
            if plan_name and plan_facts:
                lines.append(f"خطة {plan_name} يمكن أن تكون خياراً عملياً إذا كان عدد الموظفين محدوداً وتحتاج إلى تغطية أساسية مع شبكة {plan_facts.get('network_name', 'موسعة')}. الحد السنوي: {plan_facts.get('annual_limit', 'غير متوفر')}.")
            elif plan_name:
                lines.append(f"خطة {plan_name} يمكن أن تكون خياراً عملياً إذا كانت تناسب احتياجكم.")
            else:
                lines.append("يمكن اختيار خطة Remedy حسب الميزانية وعدد الموظفين والشبكة المطلوبة.")
            if plans and len(plans) > 1:
                lines.append(f"إذا كنت محتاراً بين {' و '.join(plans)}, عادةً الخطة الأعلى في الحد السنوي أو الشبكة الأوسع تكون أقوى، لكن القرار النهائي حسب احتياج الشركة.")
            if emp_count:
                lines.append(f"عدد الموظفين المذكور: {emp_count}.")
            lines.append("القرار النهائي يعتمد على عدد الموظفين، الميزانية، والمستشفيات المفضلة لديكم. يرجى تزويدنا بعدد الموظفين والميزانية أو المستشفيات المفضلة لمساعدتكم بشكل أفضل.")
            return " ".join(lines)
        else:
            lines = []
            if plan_name and plan_facts:
                lines.append(f"{plan_name} can be a practical option if you need core coverage with network {plan_facts.get('network_name', 'broad')}. Annual limit: {plan_facts.get('annual_limit', 'not available')}.")
            elif plan_name:
                lines.append(f"{plan_name} can be a practical option if it fits your needs.")
            else:
                lines.append("You can select a Remedy plan based on your budget, employee count, and required network.")
            if plans and len(plans) > 1:
                lines.append(f"If you are deciding between {' and '.join(plans)}, usually the plan with a higher annual limit or broader network is stronger, but the final decision depends on your company needs.")
            if emp_count:
                lines.append(f"Mentioned employee count: {emp_count}.")
            lines.append("The final decision depends on your employee count, budget, and preferred hospitals. Please share your census, budget, or preferred hospitals for tailored guidance.")
            return " ".join(lines)

    # --- Multi-intent detection (plan + network) ---
    # (existing logic follows...)
    plan_pat = r"(remedy\s*0?[345]|ريميدي\s*0?[345])"
    plan_intent = re.search(plan_pat, t) and ("مميزات" in t or "benefits" in t or "summary" in t or "ملخص" in t)
    # Network: English or Arabic city+type pattern
    network_intent = (
        re.search(r"(clinics|hospitals|labs|pharmacies|عيادات|مستشفيات|تحاليل|صيدليات)", t)
        and re.search(r"(sharjah|dubai|ajman|abu dhabi|الشارقة|دبي|عجمان|ابوظبي|أبوظبي)", t)
    )
    if plan_intent and network_intent:
        plan_match = re.search(plan_pat, t)
        raw_plan = plan_match.group(0) if plan_match else ""
        # Canonicalize to user-facing label for public API
        canonical_plan = None
        # Map all variants to "Remedy 04", "Remedy 03", etc.
        plan_map = {
            "remedy 04": "Remedy 04", "remedy 4": "Remedy 04", "remedy04": "Remedy 04", "remedy4": "Remedy 04",
            "ريميدي 04": "Remedy 04", "ريميدي 4": "Remedy 04",
            "remedy 03": "Remedy 03", "remedy 3": "Remedy 03", "remedy03": "Remedy 03", "remedy3": "Remedy 03",
            "ريميدي 03": "Remedy 03", "ريميدي 3": "Remedy 03",
            "remedy 05": "Remedy 05", "remedy 5": "Remedy 05", "remedy05": "Remedy 05", "remedy5": "Remedy 05",
            "ريميدي 05": "Remedy 05", "ريميدي 5": "Remedy 05",
            "remedy 02": "Remedy 02", "remedy 2": "Remedy 02", "remedy02": "Remedy 02", "remedy2": "Remedy 02",
            "ريميدي 02": "Remedy 02", "ريميدي 2": "Remedy 02"
        }
        raw_plan_norm = raw_plan.replace(" ", "").lower()
        for k, v in plan_map.items():
            if raw_plan_norm == k.replace(" ", "").lower():
                canonical_plan = v
                break
        lang = "ar" if any(ord(c) >= 0x0600 for c in text) else "en"
        if canonical_plan:
            plan_summary = explain_plan_for_business(canonical_plan, language=lang)
        else:
            plan_summary = _fallback(lang)
        from src.query.network_lookup import get_network_lookup
        net_lookup = get_network_lookup()
        city = None
        ptype = None
        if lang == "ar":
            city_ar = re.search(r"(الشارقة|دبي|عجمان|ابوظبي|أبوظبي)", t)
            type_ar = re.search(r"(عيادات|مستشفيات|تحاليل|صيدليات)", t)
            city = city_ar.group(0) if city_ar else None
            ptype = type_ar.group(0) if type_ar else None
        else:
            city_en = re.search(r"(sharjah|dubai|ajman|abu dhabi)", t)
            type_en = re.search(r"(clinics|hospitals|labs|pharmacies)", t)
            city = city_en.group(0).title() if city_en else None
            ptype = type_en.group(0).title()[:-1] if type_en else None
        providers = ""
        # Use trusted public network query path
        network_section = ""
        if city and ptype:
            if lang == "ar":
                # Compose natural Arabic query
                network_query = f"هاتلي {ptype} في {city}"
            else:
                network_query = f"show {ptype}s in {city}"
            providers = net_lookup.answer_query(network_query)
            # Only include if providers found (not fallback)
            provider_lines = [l for l in providers.split("\n") if l.strip() and not l.startswith("[NETWORK]")]
            has_providers = len(provider_lines) > 0 and not (len(provider_lines) == 1 and (provider_lines[0].startswith("No matching") or provider_lines[0].startswith("لا يوجد")))
            if has_providers:
                network_section = providers
        # Only block technical/system terms, not legitimate medical/business terms
        forbidden_patterns = [
            r"\bretrieval\b", r"\bnormalization\b", r"\bsystem\b", r"\bstate\b", r"\bdebug\b", r"\bstable\b", r"\binternal\b",
            r"pytest", r"test result", r"tests passed", r"source code", r"commit", r"branch"
        ]
        def filter_forbidden(s):
            for pat in forbidden_patterns:
                s = re.sub(pat, "", s, flags=re.IGNORECASE)
            return s.strip()
        out = []
        # Plan section: always include if not fallback
        is_plan_fallback = plan_summary.strip().startswith("عذراً") or plan_summary.strip().startswith("No deterministic answer")
        plan_section = None
        if not is_plan_fallback:
            if lang == "ar":
                plan_section = filter_forbidden(plan_summary.replace("ملخص تنفيذي", "مميزات").replace("هذا الملخص مخصص للعرض التنفيذي أو للعميل. لا يوجد استنتاجات إضافية.", ""))
            else:
                plan_section = filter_forbidden(plan_summary.replace("Executive summary", f"{canonical_plan} Benefits").replace("This summary is for executive or client-facing use. No additional inference.", ""))
            out.append(plan_section)
        # Network section: only if providers found
        if network_section:
            out.append(filter_forbidden(network_section))
        # Always return composed output if any section is present
        sections = [s for s in out if s.strip()]
        if sections:
            return "\n\n".join(sections)
        # Only fallback if no valid sections
        return _fallback(lang)

    # --- Explicit supported stronger/weaker queries for pharmacy (English/Arabic) ---
    if t.strip() == "which plan is stronger for pharmacy?":
        return explain_plan_comparison("Remedy 02", "Remedy 03", language="en")
    if t.strip() == "ما الخطة الأقوى في الأدوية؟":
        return explain_plan_comparison("Remedy 02", "Remedy 03", language="ar")

    # Ensure fallback if no branch returned
    return _fallback(lang)

def _fallback(language: str) -> str:
    if language == "ar":
        return "عذراً، لا يمكن إعطاء إجابة حتمية لهذا السؤال."
    return "No deterministic answer is available for that query yet."
