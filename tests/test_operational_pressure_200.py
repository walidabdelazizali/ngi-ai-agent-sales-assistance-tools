from collections import Counter

from scripts.run_operational_pressure_200 import CASES, EXPECTED_SECTION_COUNTS, PressureCase, classify_case


def test_operational_pressure_pack_counts():
    counts = Counter(case.section for case in CASES)
    assert len(CASES) == 200
    assert counts == EXPECTED_SECTION_COUNTS


def test_operational_pressure_queries_are_unique():
    queries = [case.query for case in CASES]
    assert len(queries) == len(set(queries))


def test_supported_case_classifies_good():
    case = PressureCase("remedy_core_pressure", "What is the annual limit for Remedy 02?", "supported", "annual_limit", ())
    result = {
        "ok": True,
        "intent": "plan_core",
        "tool_name": "get_plan_core",
        "message": "Plan: Remedy 02",
    }
    classification, reason, pattern = classify_case(case, result)
    assert classification == "GOOD"
    assert "Deterministic supported response returned" in reason
    assert pattern is None


def test_blocked_case_classifies_blocked_ok():
    case = PressureCase("recommendation_oos_pressure", "What is the best value plan?", "blocked", "recommendation", ("recommendation",))
    result = {
        "ok": False,
        "intent": "unsupported",
        "tool_name": None,
        "message": "Sorry, this query is not supported or not available. Please specify a supported plan or question.",
    }
    classification, _, pattern = classify_case(case, result)
    assert classification == "BLOCKED_OK"
    assert pattern == "safe_recommendation_block"


def test_ambiguity_case_classifies_blocked_ok():
    case = PressureCase("provider_network_pressure", "Is Burjeel Hospital in the network?", "ambiguity_safe", "provider_ambiguity", ("provider", "ambiguous"))
    result = {
        "ok": False,
        "intent": "network_lookup",
        "tool_name": "network_lookup",
        "message": "Ambiguous provider match. Please specify the branch.",
    }
    classification, _, pattern = classify_case(case, result)
    assert classification == "BLOCKED_OK"
    assert pattern == "safe_provider_ambiguity_block"


def test_not_found_case_classifies_blocked_ok():
    case = PressureCase("provider_network_pressure", "Is Unknown Future Hospital in the network?", "not_found_safe", "provider_not_found", ("provider",))
    result = {
        "ok": False,
        "intent": "network_lookup",
        "tool_name": "network_lookup",
        "message": "Provider not found.",
    }
    classification, _, pattern = classify_case(case, result)
    assert classification == "BLOCKED_OK"
    assert pattern == "safe_provider_not_found_block"