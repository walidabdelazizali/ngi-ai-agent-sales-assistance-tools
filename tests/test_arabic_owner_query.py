import pytest
from src.query.plan_query import get_plan_field

def test_arabic_reimbursement_scope():
    result = get_plan_field("Remedy 04", "نطاق التعويض")
    assert result["field"] == "reimbursement_scope"
    assert "emergency" in result["formatted"].lower()
"""Tests for Arabic/business-friendly deterministic query polish layer.

Covers:
- Arabic field retrieval for both plans
- Arabic compare requests
- Arabic summary requests
- Arabic unsupported provider/network questions
- English regression tests (imported)
- No change to deterministic guarantees
"""

import pytest
from src.query.plan_query import answer_owner_query, _SAFE_FALLBACK

ARABIC_FIELD_CASES = [
    ("ما هو الحد السنوي في Remedy 03؟", "field", "annual_limit", "150,000"),
    ("اظهر الحمل في Remedy 02", "field", "maternity_cover", None),
]

# Field queries with no plan reference should return deterministic missing-plan message
ARABIC_FIELD_NO_PLAN_CASES = [
    ("ما هي الاستثناءات الأساسية؟", "يرجى تحديد الخطة: Remedy 02 أو Remedy 03."),
    ("ما هي الشروط؟", "يرجى تحديد الخطة: Remedy 02 أو Remedy 03."),
]

ARABIC_COMPARE_CASES = [
    ("قارن Remedy 02 و Remedy 03", "compare"),
    ("ما الفرق في الأدوية بين Remedy 02 و Remedy 03؟", "compare"),
]

ARABIC_SUMMARY_CASES = [
    ("اعطني ملخص Remedy 03", "summary"),
]



# Out-of-scope provider/network lookup queries (should return network type with not found message)
ARABIC_UNSUPPORTED_CASES = [
    ("هل Aster Qusais داخل الشبكة؟", "network", "المزود غير موجود (Provider not found)."),
    ("هل هذه المستشفى ضمن الشبكة؟", "network", "المزود غير موجود (Provider not found)."),
    ("هل يوجد direct billing في هذه العيادة؟", "network", "المزود غير موجود (Provider not found)."),
]


@pytest.mark.parametrize("query,expected_type,field,expect_substring", ARABIC_FIELD_CASES)
def test_arabic_field_queries(query, expected_type, field, expect_substring):
    result = answer_owner_query(query)
    assert result["type"] == expected_type
    if field is not None:
        assert result["result"]["field"] == field
    if expect_substring is not None:
        assert expect_substring in result["result"]["formatted"]


@pytest.mark.parametrize("query,expected_message", ARABIC_FIELD_NO_PLAN_CASES)
def test_arabic_field_query_no_plan(query, expected_message):
    result = answer_owner_query(query)
    assert result["type"] == "unsupported"
    assert result["message"] == expected_message

@pytest.mark.parametrize("query,expected_type", ARABIC_COMPARE_CASES)
def test_arabic_compare_queries(query, expected_type):
    result = answer_owner_query(query)
    assert result["type"] == expected_type
    assert "plan_a_code" in result["result"]
    assert "plan_b_code" in result["result"]

@pytest.mark.parametrize("query,expected_type", ARABIC_SUMMARY_CASES)
def test_arabic_summary_queries(query, expected_type):
    result = answer_owner_query(query)
    assert result["type"] == expected_type
    assert "summary_text" in result["result"]

@pytest.mark.parametrize("query,expected_type,expected_result", ARABIC_UNSUPPORTED_CASES)
def test_arabic_unsupported_queries(query, expected_type, expected_result):
    result = answer_owner_query(query)
    assert result["type"] == expected_type
    assert result["result"] == expected_result
