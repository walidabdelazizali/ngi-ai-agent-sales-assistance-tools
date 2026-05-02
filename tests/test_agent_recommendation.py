import subprocess
import sys
import re

def test_plan_recommendation_better():
    # Run the agent_entrypoint for a plan recommendation query (non-JSON mode)
    query = "Which plan is better, Remedy 05 or Remedy 06?"
    result = subprocess.run(
        [sys.executable, "-m", "src.agent_entrypoint", query],
        capture_output=True, text=True, check=True
    )
    output = result.stdout
    # Should mention both plans
    assert "Remedy 05" in output and "Remedy 06" in output, f"Output missing plan names: {output}"
    # Should not be unsupported
    assert "not supported" not in output.lower(), f"Output incorrectly says unsupported: {output}"
    # Should include recommendation/reason wording
    rec_patterns = [
        r"recommend", r"better", r"prefer", r"should offer", r"advantage", r"difference", r"stronger", r"similar"
    ]
    assert any(re.search(pat, output, re.I) for pat in rec_patterns), f"No recommendation wording in output: {output}"
    # Should be ok (exit code 0)
    assert result.returncode == 0
