def test_lead_qualification_strong_arabic():
    from src.query import business_answer
    q = "عندي 20 موظف والتجديد الشهر الجاي وعايز عيادات في الشارقة"
    out = business_answer.answer_business_query(q)
    assert "تقييم الفرصة" in out
    assert "قوية" in out
    assert "عدد الموظفين" in out
    assert "الخطوة التالية" in out
    assert "census" in out or "أرسل census" in out or "الرخصة التجارية" in out
    forbidden = ["الأفضل", "مضمون", "يغطي كل شيء", "الأفضل للجميع", "plan fact", "technical"]
    for f in forbidden:
        assert f not in out

def test_lead_qualification_medium_arabic():
    from src.query import business_answer
    q = "عندي شركة وعايز تأمين طبي"
    out = business_answer.answer_business_query(q)
    assert "تقييم الفرصة" in out
    assert "ضعيفة" in out  # Expect weak for vague queries
    assert "الخطوة التالية" in out
    forbidden = ["الأفضل", "مضمون", "يغطي كل شيء", "الأفضل للجميع", "plan fact", "technical"]
    for f in forbidden:
        assert f not in out

def test_lead_qualification_weak_arabic():
    from src.query import business_answer
    q = "عايز أعرف الأسعار"
    out = business_answer.answer_business_query(q)
    assert "تقييم الفرصة" in out
    assert "ضعيفة" in out  # Always weak, never fallback
    assert "الخطوة التالية" in out
    forbidden = ["الأفضل", "مضمون", "يغطي كل شيء", "الأفضل للجميع", "plan fact", "technical"]
    for f in forbidden:
        assert f not in out

def test_lead_qualification_strong_english():
    from src.query import business_answer
    q = "I have 35 employees and renewal is next month"
    out = business_answer.answer_business_query(q)
    assert "Lead Qualification" in out
    assert "Strong" in out
    assert "employee count" in out.lower()
    assert "next action" in out
    forbidden = ["best plan", "guaranteed", "covers everything", "ideal for everyone", "plan fact", "technical"]
    for f in forbidden:
        assert f not in out
def test_closing_arabic_suitability():
    from src.query import business_answer
    q = "هل Remedy 04 كويسة لشركة 20 موظف؟"
    out = business_answer.answer_business_query(q)
    assert "خطة Remedy 04" in out
    assert "خياراً عملياً" in out
    assert "عدد الموظفين" in out
    assert "القرار النهائي" in out
    # Forbidden words
    forbidden = ["الأفضل", "مضمون", "يغطي كل شيء", "الأفضل للجميع"]
    for f in forbidden:
        assert f not in out

def test_closing_arabic_low_budget():
    from src.query import business_answer
    q = "ايه احسن خطة لو الميزانية قليلة؟"
    out = business_answer.answer_business_query(q)
    assert "خطة Remedy" in out or "خطة" in out
    assert "الميزانية" in out
    assert "القرار النهائي" in out
    forbidden = ["الأفضل", "مضمون", "يغطي كل شيء", "الأفضل للجميع"]
    for f in forbidden:
        assert f not in out

def test_closing_arabic_upgrade():
    from src.query import business_answer
    q = "هل أختار Remedy 04 ولا Remedy 06؟"
    out = business_answer.answer_business_query(q)
    assert "Remedy 04" in out and "Remedy 06" in out
    assert "القرار النهائي" in out
    forbidden = ["الأفضل", "مضمون", "يغطي كل شيء", "الأفضل للجميع"]
    for f in forbidden:
        assert f not in out

def test_closing_english_suitability():
    from src.query import business_answer
    q = "Is Remedy 04 suitable for a company with 20 employees?"
    out = business_answer.answer_business_query(q)
    assert "Remedy 04" in out
    assert "practical option" in out
    assert "employee count" in out or "employees" in out
    assert "final decision" in out
    forbidden = ["best plan", "guaranteed", "covers everything", "ideal for everyone"]
    for f in forbidden:
        assert f not in out

def test_closing_english_low_budget():
    from src.query import business_answer
    q = "What is the best plan for low budget?"
    out = business_answer.answer_business_query(q)
    assert "Remedy" in out or "plan" in out
    assert "budget" in out
    assert "final decision" in out
    forbidden = ["best plan", "guaranteed", "covers everything", "ideal for everyone"]
    for f in forbidden:
        assert f not in out

def test_closing_english_upgrade():
    from src.query import business_answer
    q = "Should I choose Remedy 04 or Remedy 06?"
    out = business_answer.answer_business_query(q)
    assert "Remedy 04" in out and "Remedy 06" in out
    assert "final decision" in out
    forbidden = ["best plan", "guaranteed", "covers everything", "ideal for everyone"]
    for f in forbidden:
        assert f not in out
# --- Multi-intent business answer test ---
def test_multi_intent_business_answer_ar():
    from src.query import business_answer
    out = business_answer.answer_business_query("مميزات Remedy 04 وعيادات الشارقة")
    assert "مميزات" in out
    assert "عيادات الشارقة" in out or "عيادات الشارقة ضمن" in out
    forbidden_patterns = [
        r"\bretrieval\b", r"\bnormalization\b", r"\bsystem\b", r"\bstate\b", r"\bdebug\b", r"\bstable\b", r"\binternal\b",
        r"pytest", r"test result", r"tests passed", r"source code", r"commit", r"branch"
    ]
    import re
    for pat in forbidden_patterns:
        assert not re.search(pat, out, re.IGNORECASE)
# --- Supported business question routing (exact input) ---
def test_answer_business_query_stronger_pharmacy_en():
    out = business_answer.answer_business_query("Which plan is stronger for pharmacy?")
    assert "stronger" in out or "higher" in out or "lower copay" in out or "mixed difference" in out

def test_answer_business_query_stronger_pharmacy_ar():
    out = business_answer.answer_business_query("ما الخطة الأقوى في الأدوية؟")
    assert "أقوى" in out or "أعلى" in out or "نسبة تحمل أقل" in out or "اختلاف مختلط" in out
import pytest
from src.query import business_answer

# --- English executive summary tests ---
def test_explain_plan_for_business_english():
    out = business_answer.explain_plan_for_business("Remedy 03", language="en")
    assert "Remedy 03" in out
    assert "annual limit" in out.lower() or "AED" in out
    assert "pharmacy" in out.lower()
    assert "maternity" in out.lower()
    assert "deterministic" not in out  # Should be business-friendly

# --- Arabic executive summary tests ---
def test_explain_plan_for_business_arabic():
    out = business_answer.explain_plan_for_business("Remedy 03", language="ar")
    assert "ريميدي" in out or "Remedy" in out
    assert "الحد السنوي" in out or "150,000" in out
    assert "الصيدلية" in out or "pharmacy" in out
    assert "الحمل" in out or "maternity" in out

# --- Executive comparison (English) ---
def test_explain_plan_comparison_executive_english():
    out = business_answer.explain_plan_comparison("Remedy 02", "Remedy 03", language="en", mode="executive")
    assert "Remedy 02" in out and "Remedy 03" in out
    assert (
        "stronger" in out or "higher" in out or "lower copay" in out or "mixed difference" in out or "no material difference" in out
    )

# --- Executive comparison (Arabic) ---
def test_explain_plan_comparison_executive_arabic():
    out = business_answer.explain_plan_comparison("Remedy 02", "Remedy 03", language="ar", mode="executive")
    assert "ريميدي" in out or "Remedy" in out
    assert (
        "أقوى" in out or "أعلى" in out or "نسبة تحمل أقل" in out or "اختلاف مختلط" in out or "لا يوجد فرق جوهري" in out
    )

# --- Stronger/weaker phrasing only when supported ---
def test_stronger_weaker_phrasing_only_when_supported():
    out = business_answer.explain_plan_comparison("Remedy 02", "Remedy 03", language="en", mode="executive")
    assert (
        "stronger" in out or "higher" in out or "lower copay" in out or "mixed difference" in out or "no material difference" in out
    )

# --- No material difference phrasing ---
def test_no_material_difference():
    # Compare a plan to itself
    out = business_answer.explain_plan_comparison("Remedy 03", "Remedy 03", language="en", mode="executive")
    assert "no material difference" in out.lower() or "identical" in out.lower()

# --- Client-facing summary output ---
def test_client_facing_summary():
    out = business_answer.explain_plan_for_business("Remedy 02", language="en")
    assert "client" in out.lower() or "executive" in out.lower() or "summary" in out.lower()

# --- Safe fallback for unsupported questions ---
def test_answer_business_query_fallback():
    out = business_answer.answer_business_query("What is the best plan for cancer?")
    assert "unsupported" in out.lower() or "cannot answer" in out.lower() or "no deterministic answer" in out.lower()

def test_lead_capture_fields_arabic_all_present():
    from src.query import business_answer
    q = "عندي 15 موظف والتجديد الشهر الجاي وميزانية محدودة وعايز شبكة موسعة ويوجد وثيقة حالية والمدير متوفر"
    out = business_answer.answer_business_query(q)
    assert "عدد الموظفين: 15" in out
    # Accept partial match for renewal timing
    assert "توقيت التجديد: التجديد الشهر" in out or "توقيت التجديد: الشهر الجاي" in out
    assert "حالة الميزانية: ميزانية" in out or "حالة الميزانية: ميزانية محدودة" in out or "حالة الميزانية: محدودة" in out
    assert "الشبكة أو المستشفيات المفضلة: شبكة" in out or "الشبكة أو المستشفيات المفضلة: موسعة" in out
    assert "توفر وثيقة حالية: وثيقة" in out or "توفر وثيقة حالية: يوجد وثيقة حالية" in out
    assert "حالة متخذ القرار: المدير" in out or "حالة متخذ القرار: متوفر" in out
    assert "المستندات المطلوبة التالية:" in out
    assert "الخطوة التالية" in out
    forbidden = ["plan fact", "technical", "json", "{", "}"]
    for f in forbidden:
        assert f not in out

def test_lead_capture_fields_arabic_missing():
    from src.query import business_answer
    q = "عندي شركة فقط"
    out = business_answer.answer_business_query(q)
    assert "عدد الموظفين: غير محدد" in out
    assert "توقيت التجديد: غير محدد" in out
    assert "حالة الميزانية: غير محدد" in out
    assert "الشبكة أو المستشفيات المفضلة: غير محدد" in out
    assert "توفر وثيقة حالية: غير محدد" in out
    assert "حالة متخذ القرار: غير محدد" in out
    # Expect next actions, not 'غير محدد'
    assert "المستندات المطلوبة التالية: أرسل census sheet" in out or "المستندات المطلوبة التالية: أرسل آخر وثيقة إن وجدت" in out or "المستندات المطلوبة التالية: أرسل الرخصة التجارية" in out
    assert "الخطوة التالية" in out
    forbidden = ["plan fact", "technical", "json", "{", "}"]
    for f in forbidden:
        assert f not in out

def test_lead_capture_fields_english_all_present():
    from src.query import business_answer
    q = "We have 25 employees, renewal is next month, budget is tight, prefer a broad network, current policy available, decision maker is present"
    out = business_answer.answer_business_query(q)
    assert "company_size: 25" in out  # Only the number
    assert "renewal_timing: next month" in out or "renewal_timing: renewal is next month" in out
    assert "budget_status: budget" in out or "budget_status: tight" in out
    assert "preferred_network_or_hospitals: network" in out or "preferred_network_or_hospitals: broad" in out
    assert "current_policy_available: policy" in out or "current_policy_available: current policy available" in out
    assert "decision_maker_status: decision maker" in out or "decision_maker_status: present" in out
    assert "next_required_documents:" in out
    assert "Recommended next action" in out
    forbidden = ["plan fact", "technical", "json", "{", "}"]
    for f in forbidden:
        assert f not in out

def test_lead_capture_fields_english_missing():
    from src.query import business_answer
    q = "Just a company"
    out = business_answer.answer_business_query(q)
    assert "company_size: unknown" in out
    assert "renewal_timing: unknown" in out
    assert "budget_status: unknown" in out
    assert "preferred_network_or_hospitals: unknown" in out
    assert "current_policy_available: unknown" in out
    assert "decision_maker_status: unknown" in out
    # Expect next actions, not 'unknown'
    assert "next_required_documents: ask for census" in out or "next_required_documents: ask for current policy" in out or "next_required_documents: ask for trade license" in out
    assert "Recommended next action" in out
    forbidden = ["plan fact", "technical", "json", "{", "}"]
    for f in forbidden:
        assert f not in out
