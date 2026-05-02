import pytest
from src.query.plan_query import get_plan_field

# =========================
# Remedy 02 (Approved)
# =========================
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

# =========================
# Remedy 03 (Approved)
# =========================
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

# =========================
REMEDY_04_QUESTIONS = [
    ("annual limit", "What is the annual limit for Remedy 04?", True, False),
    ("network", "What is the network for Remedy 04?", True, False),
    ("area of coverage", "What is the area of coverage for Remedy 04?", True, False),
    ("inpatient", "What is the inpatient cover for Remedy 04?", True, True),
    ("outpatient", "What is the outpatient cover for Remedy 04?", True, True),
    ("pharmacy", "What is the pharmacy cover for Remedy 04?", True, True),
    ("maternity", "What is the maternity cover for Remedy 04?", True, True),
    ("dental", "What is the dental cover for Remedy 04?", False, False),
    ("referral required", "Is referral required for Remedy 04?", True, True),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 04?", True, True),
]

# =========================
# Remedy 05 (Blocked)
# =========================
REMEDY_05_QUESTIONS = [
    ("annual limit", "What is the annual limit for Remedy 05?", True, False),
    ("network", "What is the network for Remedy 05?", True, False),
    ("area of coverage", "What is the area of coverage for Remedy 05?", True, False),
    ("inpatient", "What is the inpatient cover for Remedy 05?", True, True),
    ("outpatient", "What is the outpatient cover for Remedy 05?", True, True),
    ("pharmacy", "What is the pharmacy cover for Remedy 05?", True, True),
    ("maternity", "What is the maternity cover for Remedy 05?", True, True),
    ("dental", "What is the dental cover for Remedy 05?", False, False),
    ("referral required", "Is referral required for Remedy 05?", True, True),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 05?", True, True),
]

# =========================
# Remedy 06 (Unknown)
# =========================
REMEDY_06_QUESTIONS = [
    ("annual limit", "What is the annual limit for Remedy 06?", True, False),
    ("network", "What is the network for Remedy 06?", True, False),
    ("area of coverage", "What is the area of coverage for Remedy 06?", True, False),
    ("inpatient", "What is the inpatient cover for Remedy 06?", True, True),
    ("outpatient", "What is the outpatient cover for Remedy 06?", True, True),
    ("pharmacy", "What is the pharmacy cover for Remedy 06?", True, True),
    ("maternity", "What is the maternity cover for Remedy 06?", True, True),
    ("dental", "What is the dental cover for Remedy 06?", False, False),
    ("referral required", "Is referral required for Remedy 06?", True, True),
    ("outside network reimbursement", "What is the outside network reimbursement for Remedy 06?", True, True),
]


def _run(plan, field, expect_ok):
    try:
        result = get_plan_field(plan, field)
    except ValueError as e:
        result = {"ok": False, "formatted": str(e)}

    if expect_ok:
        assert result["ok"] is True
    else:
        assert result["ok"] is False


@pytest.mark.parametrize("field, q, ok, _", REMEDY_02_QUESTIONS)
def test_remedy_02(field, q, ok, _):
    _run("Remedy 02", field, ok)


@pytest.mark.parametrize("field, q, ok, _", REMEDY_03_QUESTIONS)
def test_remedy_03(field, q, ok, _):
    _run("Remedy 03", field, ok)


@pytest.mark.parametrize("field, q, ok, _", REMEDY_04_QUESTIONS)
def test_remedy_04(field, q, ok, _):
    _run("Remedy 04", field, ok)


@pytest.mark.parametrize("field, q, ok, _", REMEDY_05_QUESTIONS)
def test_remedy_05(field, q, ok, _):
    _run("Remedy 05", field, ok)


@pytest.mark.parametrize("field, q, ok, _", REMEDY_06_QUESTIONS)
def test_remedy_06(field, q, ok, _):
    _run("Remedy 06", field, ok)