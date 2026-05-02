# Deterministic WhatsApp client message formatter
def format_whatsapp_client_message(obj, mode, *, greeting="Hello,", closing="Would you like to proceed?"):
    """
    Deterministically format a summary, comparison, or recommendation as a professional WhatsApp client message.

    - obj: dict (allowed keys: plan_name, plan_code, summary_text, recommendation) or str (already formatted body)
    - mode: "summary" | "comparison" | "recommendation"
    - greeting: str (default "Hello,")
    - closing: str (default "Would you like to proceed?")
    Returns: str (client-ready WhatsApp message)
    """
    allowed_modes = {"summary", "comparison", "recommendation"}
    if mode not in allowed_modes:
        return "Sorry, a client-ready message is not available for this request."

    # Handle string input as already formatted body
    if isinstance(obj, str):
        body = obj.strip()
    elif isinstance(obj, dict):
        # Only use allowed keys, ignore all others
        plan_name = obj.get("plan_name", "") or obj.get("plan_code", "")
        summary = obj.get("summary_text", "")
        recommendation = obj.get("recommendation", "")
        # Only use above variables; ignore any keys starting with _ or unknown fields
        if mode == "summary":
            if plan_name and summary:
                body = f"{plan_name}: {summary.splitlines()[0]}"
            elif summary:
                body = summary.splitlines()[0]
            else:
                body = "Your plan details are ready."
        elif mode == "comparison":
            # For comparison, expect summary_text to contain a comparison line
            if summary:
                body = summary.splitlines()[0]
            else:
                body = "Comparison details are ready."
        elif mode == "recommendation":
            if plan_name and recommendation:
                body = f"Our recommendation: {plan_name} — {recommendation.splitlines()[0]}"
            elif recommendation:
                body = f"Our recommendation: {recommendation.splitlines()[0]}"
            else:
                body = "We have a recommendation ready for you."
    else:
        return "Sorry, a client-ready message is not available for this request."

    # Final message assembly, always short and client-friendly
    message = f"{greeting}\n{body}\n{closing}"
    # Ensure no leakage of internal/debug fields or raw fragments
    lower_msg = message.lower()
    forbidden = ["{", "}", "[", "]", "raw", "debug", "internal", "traceback"]
    if any(x in lower_msg for x in forbidden):
        return "Sorry, a client-ready message is not available for this request."
    return message
"""
Deterministic, channel-oriented output packaging for Remedy plans.
- WhatsApp-ready short outputs
- Client-facing summaries
- Internal executive notes
- Comparison briefs
- Bullet summaries
- Arabic and English support
- All outputs grounded in deterministic query/business layers
"""

from src.query.business_answer import explain_plan_for_business, explain_plan_comparison, answer_business_query
from src.query.plan_query import summarize_plan

_SUPPORTED_FORMATS = {"whatsapp_short", "client_summary", "executive_note", "comparison_brief", "bullet_summary"}

# --- Public API ---
def format_plan_output(plan_name, format_type, language="en"):
    """
    Deterministically package a plan summary for a given channel/format.
    """
    if format_type not in _SUPPORTED_FORMATS:
        return _fallback(language)
    summary = summarize_plan(plan_name)
    if not summary:
        return _fallback(language)
    if format_type == "whatsapp_short":
        return _format_whatsapp_short(summary, language)
    if format_type == "client_summary":
        return _format_client_summary(summary, language)
    if format_type == "executive_note":
        return _format_executive_note(summary, language)
    if format_type == "bullet_summary":
        return _format_bullet_summary(summary, language)
    return _fallback(language)

def format_comparison_output(plan_a, plan_b, format_type, language="en"):
    """
    Deterministically package a comparison for a given channel/format.
    """
    if format_type not in _SUPPORTED_FORMATS:
        return _fallback(language)
    comp = explain_plan_comparison(plan_a, plan_b, language=language, mode="executive")
    if not comp:
        return _fallback(language)
    if format_type == "whatsapp_short":
        return _format_comparison_whatsapp_short(comp, language)
    if format_type == "client_summary":
        return _format_comparison_client_summary(comp, language)
    if format_type == "executive_note":
        return _format_comparison_executive_note(comp, language)
    if format_type == "comparison_brief":
        return _format_comparison_brief(comp, language)
    if format_type == "bullet_summary":
        return _format_comparison_bullet_summary(comp, language)
    return _fallback(language)

def answer_packaged_query(text):
    """
    Deterministic router for packaged output queries (English/Arabic).
    """
    t = text.strip().lower()
    # WhatsApp short
    if any(x in t for x in ["whatsapp-ready", "whatsapp short", "ملخص واتساب"]):
        if "remedy 03" in t:
            return format_plan_output("Remedy 03", "whatsapp_short", language="ar" if "ملخص" in t else "en")
        if "remedy 02" in t:
            return format_plan_output("Remedy 02", "whatsapp_short", language="ar" if "ملخص" in t else "en")
    # Client summary
    if any(x in t for x in ["client-facing explanation", "client summary", "شرح قصير للعميل"]):
        if "remedy 03" in t:
            return format_plan_output("Remedy 03", "client_summary", language="ar" if "شرح" in t else "en")
        if "remedy 02" in t:
            return format_plan_output("Remedy 02", "client_summary", language="ar" if "شرح" in t else "en")
    # Executive note
    if any(x in t for x in ["executive note", "internal note", "ملاحظة تنفيذية"]):
        if "remedy 02" in t and "remedy 03" in t:
            return format_comparison_output("Remedy 02", "Remedy 03", "executive_note", language="ar" if "ملاحظة" in t else "en")
    # Comparison brief
    if any(x in t for x in ["comparison brief", "مقارنة مختصرة"]):
        if "remedy 02" in t and "remedy 03" in t:
            return format_comparison_output("Remedy 02", "Remedy 03", "comparison_brief", language="ar" if "مقارنة" in t else "en")
    # Fallback
    return _fallback("ar" if any(ord(c) >= 0x0600 for c in text) else "en")

# --- Format helpers ---
def _format_whatsapp_short(summary, language):
    if language == "ar":
        plan_name = summary.get('plan_name', '').replace('', '').strip()
        plan_code = summary.get('plan_code', '').replace('', '').strip()
        ann_limit = ""
        network = ""
        for line in summary['summary_text'].splitlines():
            if line.startswith("Annual Limit"):
                ann_limit = line.split(":",1)[-1].strip()
            if line.startswith("Network"):
                network = line.split(":",1)[-1].strip()
        parts = ["ملخص واتساب"]
        if plan_name:
            parts.append(f"اسم الخطة: {plan_name}")
        elif plan_code:
            parts.append(f"رمز الخطة: {plan_code}")
        if ann_limit:
            parts.append(f"الحد السنوي: {ann_limit}")
        if network:
            parts.append(f"الشبكة: {network}")
        return " | ".join(parts)
    plan_code = summary.get('plan_code', '').replace('', '').strip()
    return f"WhatsApp: {plan_code} - {summary['summary_text'].splitlines()[0]}"

def _format_client_summary(summary, language):
    if language == "ar":
        return f"ملخص للعميل: {summary['plan_code']}\n{summary['summary_text'].splitlines()[0]}"
    return f"Client summary: {summary['plan_code']}\n{summary['summary_text'].splitlines()[0]}"

def _format_executive_note(summary, language):
    if language == "ar":
        return f"ملاحظة تنفيذية: {summary['plan_code']}\n{summary['summary_text']}"
    return f"Executive note: {summary['plan_code']}\n{summary['summary_text']}"

def _format_bullet_summary(summary, language):
    bullets = summary['summary_text'].splitlines()
    # Remove duplicate Plan Name/Code lines (EN/AR)
    def is_plan_code_line(line):
        return line.strip().startswith("Plan Code") or line.strip().startswith("رمز الخطة")
    def is_plan_name_line(line):
        return line.strip().startswith("Plan Name") or line.strip().startswith("اسم الخطة")
    seen_plan_name = False
    seen_plan_code = False
    if language == "ar":
        label_map = {
            "Plan Name": "اسم الخطة",
            "Plan Code": "رمز الخطة",
            "Network": "الشبكة",
            "Annual Limit": "الحد السنوي",
            "Area of Coverage": "نطاق التغطية",
            "Direct Billing": "الدفع المباشر",
            "Referral Required": "الإحالة مطلوبة",
            "Maternity Cover": "تغطية الحمل",
            "Inpatient Cover": "تغطية التنويم",
            "Outpatient Cover": "تغطية العيادات الخارجية",
            "Pharmacy Cover": "تغطية الأدوية",
            "Key Exclusions": "أهم الاستثناءات",
        }
        def translate_line(line):
            for en, ar in label_map.items():
                if line.startswith(en):
                    line = line.replace(en, ar, 1)
            line = line.replace(": Yes", ": نعم")
            line = line.replace(": No", ": لا")
            line = line.replace("listed", "مدرجة")
            return line
        ar_bullets = []
        # Clean plan_name/code for mojibake and replacement char
        plan_name = summary.get('plan_name', '').replace('', '').strip()
        plan_code = summary.get('plan_code', '').replace('', '').strip()
        if plan_name:
            ar_bullets.append(f"• اسم الخطة: {plan_name}")
            seen_plan_name = True
        if plan_code:
            ar_bullets.append(f"• رمز الخطة: {plan_code}")
            seen_plan_code = True
        for b in bullets:
            if is_plan_name_line(b):
                if seen_plan_name:
                    continue
                seen_plan_name = True
            if is_plan_code_line(b):
                if seen_plan_code:
                    continue
                seen_plan_code = True
            ar_bullets.append(f"• {translate_line(b)}")
        return "\n".join(ar_bullets)
    en_bullets = []
    # Clean plan_name/code for mojibake and replacement char
    plan_name = summary.get('plan_name', '').replace('', '').strip()
    plan_code = summary.get('plan_code', '').replace('', '').strip()
    if plan_name:
        en_bullets.append(f"- Plan Name: {plan_name}")
        seen_plan_name = True
    if plan_code:
        en_bullets.append(f"- Plan Code: {plan_code}")
        seen_plan_code = True
    for b in bullets:
        if is_plan_name_line(b):
            if seen_plan_name:
                continue
            seen_plan_name = True
        if is_plan_code_line(b):
            if seen_plan_code:
                continue
            seen_plan_code = True
        en_bullets.append(f"- {b}")
    return "\n".join(en_bullets)

def _format_comparison_whatsapp_short(comp, language):
    lines = comp.splitlines()
    if language == "ar":
        return f"مقارنة واتساب: {lines[1] if len(lines)>1 else lines[0]}"
    return f"WhatsApp comparison: {lines[1] if len(lines)>1 else lines[0]}"

def _format_comparison_client_summary(comp, language):
    lines = comp.splitlines()
    if language == "ar":
        return f"ملخص مقارنة للعميل: {lines[1] if len(lines)>1 else lines[0]}"
    return f"Client comparison summary: {lines[1] if len(lines)>1 else lines[0]}"

def _format_comparison_executive_note(comp, language):
    if language == "ar":
        return f"ملاحظة تنفيذية مقارنة:\n{comp}"
    return f"Executive comparison note:\n{comp}"

def _format_comparison_brief(comp, language):
    lines = comp.splitlines()
    brief = "\n".join(lines[1:3]) if len(lines) > 2 else comp
    if language == "ar":
        return f"مقارنة مختصرة:\n{brief}"
    return f"Comparison brief:\n{brief}"

def _format_comparison_bullet_summary(comp, language):
    lines = comp.splitlines()
    if language == "ar":
        return "\n".join([f"• {l}" for l in lines if l.strip()])
    return "\n".join([f"- {l}" for l in lines if l.strip()])

def _fallback(language):
    if language == "ar":
        return "عذراً، لا يمكن إعطاء إجابة حتمية لهذا الطلب."
    return "No deterministic packaged output is available for that request."
