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
