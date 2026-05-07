from src.tool_contract import get_plan_core

def test_get_plan_core_classic2():
    result = get_plan_core("Classic 2")
    assert result["plan_name"] == "Classic 2"
    assert result["plan_code"] == "HN_CLASSIC_2"
    assert result["network_name"] == "Standard Plus"
    assert result["annual_limit"] == "AED 250,000"
    # Only approved fields
    assert "approval_status" not in result
    assert "tests_passed" not in result
    assert "source_trace" not in result

def test_get_plan_core_hn_classic2():
    result = get_plan_core("HN_CLASSIC_2")
    assert result["plan_name"] == "Classic 2"
    assert result["plan_code"] == "HN_CLASSIC_2"
    assert result["network_name"] == "Standard Plus"
    assert result["annual_limit"] == "AED 250,000"
    # Only approved fields
    assert "approval_status" not in result
    assert "tests_passed" not in result
    assert "source_trace" not in result
