import subprocess
import json
import sys

def test_agent_entrypoint_json_summarize_classic2():
    result = subprocess.run(
        [sys.executable, "-m", "src.agent_entrypoint", "--json", "Summarize Classic 2"],
        capture_output=True, text=True, check=True
    )
    output = result.stdout.strip()
    # Should be valid JSON
    data = json.loads(output)
    assert data["ok"] is True
    assert data["intent"] == "plan_summary"
    assert data["plan_name"] == "Classic 2"
    assert data["tool_name"] == "get_plan_summary"
    assert "annual_limit" in data["data"]
    assert data["data"]["annual_limit"] == "AED 250,000"
    # No internal metadata
    forbidden = ["approval_status", "tests_passed", "source_trace"]
    for key in forbidden:
        assert key not in data["data"]
