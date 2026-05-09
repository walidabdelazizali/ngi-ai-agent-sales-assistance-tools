import subprocess
import sys
def test_plan_recommendation_better():
    # Run the agent_entrypoint for a plan recommendation query (non-JSON mode)
    query = "Which plan is better, Remedy 05 or Remedy 06?"
    result = subprocess.run(
        [sys.executable, "-m", "src.agent_entrypoint", query],
        capture_output=True, text=True, check=True
    )
    output = result.stdout
    # Recommendation-style plan selection must be blocked safely.
    assert "Intent: unsupported" in output
    assert "Recommendation-style plan selection is not supported" in output
    # Should be ok (exit code 0)
    assert result.returncode == 0
