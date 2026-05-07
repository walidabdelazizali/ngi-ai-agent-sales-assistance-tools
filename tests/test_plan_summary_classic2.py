from src.tool_contract import get_plan_summary

def test_get_plan_summary_classic2():
    result = get_plan_summary("Classic 2")
    assert result["plan_name"] == "Classic 2"
    assert result["plan_code"] == "HN_CLASSIC_2"
    assert result["network_name"] == "Standard Plus"
    assert result["annual_limit"] == "AED 250,000"
    assert result["summary_text"]
    # Only customer-safe fields
    forbidden = ["approval_status", "tests_passed", "source_trace"]
    for key in forbidden:
        assert key not in result

def test_get_plan_summary_unknown():
    result = get_plan_summary("Remedy 99")
    assert result["plan_name"] is None
    assert result["summary_text"] is None
    assert result["field_count"] == 0
