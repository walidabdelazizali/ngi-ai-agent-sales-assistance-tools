from scripts.run_adversarial_validation_500 import CASES, EXPECTED_SECTION_COUNTS, convert_base_case
from scripts.run_operational_pressure_200 import CASES as BASE_200_CASES


def test_adversarial_pack_counts_and_uniqueness():
    counts = {}
    queries = []
    for case in CASES:
        counts[case.section] = counts.get(case.section, 0) + 1
        queries.append(case.query)
    assert len(CASES) == 500
    assert counts == EXPECTED_SECTION_COUNTS
    assert len(queries) == len(set(queries))


def test_legacy_supported_comparison_does_not_require_plan_name():
    base_case = next(case for case in BASE_200_CASES if case.query == "compare Remedy 02 and Remedy 05")
    converted = convert_base_case(base_case)
    assert converted.section == "comparison_adversarial"
    assert converted.expected_plan is None
