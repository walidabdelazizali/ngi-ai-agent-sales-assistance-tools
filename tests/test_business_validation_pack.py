"""
Business-facing validation tests for approved Remedy plans (Sprint 1).
Covers Remedy 02, Remedy 03, Remedy 04, Remedy 05, Remedy 06.
Each plan: 10 business-facing questions.
"""
import pytest
from src.query.plan_query import get_plan_field

# Remedy 03, 04, 06 business validation questions (same pattern)
REMEDY_03_QUESTIONS = [
    ("annual limit", "What is the annual limit for Remedy 03?", True, False),
    ("network", "What is the network for Remedy 03?", True, False),
    ("area of coverage", "What is the area of coverage for Remedy 03?", True, False),
    ("inpatient", "What is the inpatient cover for Remedy 03?", True, True),
    ("outpatient", "What is the outpatient cover for Remedy 03?", True, True),
    ("pharmacy", "What is the pharmacy cover for Remedy 03?", True, True),
    ("maternity", "What is the maternity cover for Remedy 03?", True, True),
    ("dental", "What is the dental cover for Remedy 03?", False, False),
    ("referral required", "Is referral required for Remedy 03?", True, True),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 03?", True, True),
]

REMEDY_04_QUESTIONS = [
    # All fields expected to fail safety gate (not approved)
    ("annual limit", "What is the annual limit for Remedy 04?", False, False),
    ("network", "What is the network for Remedy 04?", False, False),
    ("area of coverage", "What is the area of coverage for Remedy 04?", False, False),
    ("inpatient", "What is the inpatient cover for Remedy 04?", False, False),
    ("outpatient", "What is the outpatient cover for Remedy 04?", False, False),
    ("pharmacy", "What is the pharmacy cover for Remedy 04?", False, False),
    ("maternity", "What is the maternity cover for Remedy 04?", False, False),
    ("dental", "What is the dental cover for Remedy 04?", False, False),
    ("referral required", "Is referral required for Remedy 04?", False, False),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 04?", False, False),
]

REMEDY_06_QUESTIONS = [
    ("annual limit", "What is the annual limit for Remedy 06?", False, False),
    ("network", "What is the network for Remedy 06?", False, False),
    ("area of coverage", "What is the area of coverage for Remedy 06?", False, False),
    ("inpatient", "What is the inpatient cover for Remedy 06?", False, False),
    ("outpatient", "What is the outpatient cover for Remedy 06?", False, False),
    ("pharmacy", "What is the pharmacy cover for Remedy 06?", False, False),
    ("maternity", "What is the maternity cover for Remedy 06?", False, False),
    ("dental", "What is the dental cover for Remedy 06?", False, False),
    ("referral required", "Is referral required for Remedy 06?", False, False),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 06?", False, False),
]

@pytest.mark.parametrize("field, question, expect_ok, expect_not_available_ok", REMEDY_03_QUESTIONS)
def test_remedy_03_business_fields(field, question, expect_ok, expect_not_available_ok):
    _run_business_field_test("Remedy 03", field, expect_ok, expect_not_available_ok)

@pytest.mark.parametrize("field, question, expect_ok, expect_not_available_ok", REMEDY_04_QUESTIONS)
def test_remedy_04_business_fields(field, question, expect_ok, expect_not_available_ok):
    _run_business_field_test("Remedy 04", field, expect_ok, expect_not_available_ok)

@pytest.mark.parametrize("field, question, expect_ok, expect_not_available_ok", REMEDY_06_QUESTIONS)
def test_remedy_06_business_fields(field, question, expect_ok, expect_not_available_ok):
    _run_business_field_test("Remedy 06", field, expect_ok, expect_not_available_ok)
"""
Business-facing validation tests for approved Remedy plans (Sprint 1).
Covers Remedy 02 and Remedy 05 only.
Each plan: 10 business-facing questions.
"""
import pytest
from src.query.plan_query import get_plan_field

# List of (field, business question, expected_ok, expect_not_available_ok)
REMEDY_02_QUESTIONS = [
    ("annual limit", "What is the annual limit for Remedy 02?", True, False),
    ("network", "What is the network for Remedy 02?", True, False),
    ("area of coverage", "What is the area of coverage for Remedy 02?", True, False),
    ("inpatient", "What is the inpatient cover for Remedy 02?", True, True),
    ("outpatient", "What is the outpatient cover for Remedy 02?", True, True),
    ("pharmacy", "What is the pharmacy cover for Remedy 02?", True, True),
    ("maternity", "What is the maternity cover for Remedy 02?", True, True),
    ("dental", "What is the dental cover for Remedy 02?", False, False),
    ("referral required", "Is referral required for Remedy 02?", True, True),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 02?", True, True),
]

REMEDY_05_QUESTIONS = [
    # All fields expected to fail safety gate (not approved)
    ("annual limit", "What is the annual limit for Remedy 05?", False, False),
    ("network", "What is the network for Remedy 05?", False, False),
    ("area of coverage", "What is the area of coverage for Remedy 05?", False, False),
    ("inpatient", "What is the inpatient cover for Remedy 05?", False, False),
    ("outpatient", "What is the outpatient cover for Remedy 05?", False, False),
    ("pharmacy", "What is the pharmacy cover for Remedy 05?", False, False),
    ("maternity", "What is the maternity cover for Remedy 05?", False, False),
    ("dental", "What is the dental cover for Remedy 05?", False, False),
    ("referral required", "Is referral required for Remedy 05?", False, False),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 05?", False, False),
]

def _run_business_field_test(plan, field, expect_ok, expect_not_available_ok):
    try:
        result = get_plan_field(plan, field)
    except ValueError as e:
        # Treat unknown plan as ok=False with safe fallback
        result = {"ok": False, "formatted": str(e)}
    if expect_ok:
        assert result["ok"] is True, f"Expected ok=True for {plan} {field}, got {result}"
        formatted = result["formatted"]
        # If value is 'not available', must still be ok=True and business-friendly
        if expect_not_available_ok and "not available" in formatted.lower():
            assert result["ok"] is True
            assert "not available" in formatted.lower()
        else:
            assert "not available" not in formatted.lower(), f"Unexpected 'not available' for {plan} {field}: {formatted}"
        # Must be a non-empty, business-friendly string (not JSON, not fallback, not internal label)
        assert isinstance(formatted, str) and formatted.strip(), f"Empty or invalid business answer for {plan} {field}: {formatted}"
        assert not formatted.strip().startswith("{") and not formatted.strip().startswith("["), f"Raw JSON in answer for {plan} {field}: {formatted}"
        assert "no deterministic answer" not in formatted.lower(), f"Fallback in business answer for {plan} {field}: {formatted}"
        assert "internal" not in formatted.lower(), f"Internal label in business answer for {plan} {field}: {formatted}"
    else:
        assert result["ok"] is False, f"Expected ok=False for {plan} {field}, got {result}"
        formatted_lower = result["formatted"].lower()
        assert (
            "not available" in formatted_lower
            or "no deterministic answer" in formatted_lower
            or "unknown plan" in formatted_lower
        ), f"Missing fallback for {plan} {field}: {result['formatted']}"

@pytest.mark.parametrize("field, question, expect_ok, expect_not_available_ok", REMEDY_04_QUESTIONS)
def test_remedy_04_business_fields_safety_gate(field, question, expect_ok, expect_not_available_ok):
    """Remedy 04 is not approved; all fields must fail safety gate and return safe fallback."""
    _run_business_field_test("Remedy 04", field, expect_ok, expect_not_available_ok)

@pytest.mark.parametrize("field, question, expect_ok, expect_not_available_ok", REMEDY_05_QUESTIONS)
def test_remedy_05_business_fields_safety_gate(field, question, expect_ok, expect_not_available_ok):
    """Remedy 05 is not approved; all fields must fail safety gate and return safe fallback."""
    _run_business_field_test("Remedy 05", field, expect_ok, expect_not_available_ok)
