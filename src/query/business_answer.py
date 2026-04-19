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
    """
    Deterministic router for business-style questions.
    """
    # Route to supported business question families
    t = text.strip().lower()
    # Executive summary
    if any(x in t for x in ["executive summary", "client-facing summary", "short summary", "ملخص تنفيذي", "ملخص للعميل"]):
        if "remedy 03" in t or "ريميدي 03" in t:
            return explain_plan_for_business("Remedy 03", language="ar" if "ملخص" in t and "تنفيذي" in t else "en")
        if "remedy 02" in t or "ريميدي 02" in t:
            return explain_plan_for_business("Remedy 02", language="ar" if "ملخص" in t and "تنفيذي" in t else "en")

    # Explicit supported stronger/weaker queries for pharmacy (English/Arabic)
    if t.strip() == "which plan is stronger for pharmacy?":
        return explain_plan_comparison("Remedy 02", "Remedy 03", language="en")
    if t.strip() == "ما الخطة الأقوى في الأدوية؟":
        return explain_plan_comparison("Remedy 02", "Remedy 03", language="ar")

    # Comparison
    if any(x in t for x in ["compare", "comparison", "مقارنة", "stronger", "weaker", "أقوى", "أضعف", "upgrade", "تحسينات", "differences", "الفرق"]):
        if ("remedy 02" in t or "ريميدي 02" in t) and ("remedy 03" in t or "ريميدي 03" in t):
            return explain_plan_comparison("Remedy 02", "Remedy 03", language="ar" if "مقارنة" in t else "en")
    # Key upgrades
    if any(x in t for x in ["key upgrades", "أهم التحسينات"]):
        if "remedy 03" in t or "ريميدي 03" in t:
            return explain_plan_comparison("Remedy 02", "Remedy 03", language="ar" if "أهم" in t else "en")
    # Field-specific stronger/weaker
    for field in ["pharmacy", "maternity", "outpatient", "diagnostics", "physiotherapy", "الصيدلية", "الحمل", "العلاج الطبيعي", "التحاليل"]:
        if field in t and any(x in t for x in ["stronger", "better", "higher", "أقوى", "أفضل", "أعلى"]):
            if ("remedy 02" in t or "ريميدي 02" in t) and ("remedy 03" in t or "ريميدي 03" in t):
                lang = "ar" if any(ar in t for ar in ["أقوى", "أفضل", "أعلى"]) else "en"
                return explain_plan_comparison("Remedy 02", "Remedy 03", language=lang)
    # Fallback
    return _fallback("ar" if any(ord(c) >= 0x0600 for c in text) else "en")

def _fallback(language: str) -> str:
    if language == "ar":
        return "عذراً، لا يمكن إعطاء إجابة حتمية لهذا السؤال."
    return "No deterministic answer is available for that query yet."
