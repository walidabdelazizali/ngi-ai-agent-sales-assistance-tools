import subprocess
import sys
import re

def test_remedy06_no_raw_fields_in_cli():
    # Run the agent_entrypoint for a Remedy 06 query (non-JSON mode)
    result = subprocess.run(
        [sys.executable, "-m", "src.agent_entrypoint", "What is the annual limit for Remedy 06?"],
        capture_output=True, text=True, check=True
    )
    output = result.stdout
    # Forbidden raw fields
    forbidden = [
        "annual_limit:", "area_of_coverage:", "plan_code:", "plan_name:", "referral_required:"
    ]
    for key in forbidden:
        assert key not in output, f"Raw field {key} leaked in CLI output: {output}"
    # Required business fields (case-insensitive, allow Arabic/English)
    required = [
        r"Plan:", r"Annual limit:", r"Referral required:"
    ]
    for pat in required:
        assert re.search(pat, output, re.I), f"Missing required business field: {pat}"
    # Accept either 'Network:' or Arabic 'الشبكة:'
    assert re.search(r"Network", output, re.I) or "الشبكة:" in output, "Missing network field in any language"
    # Message block must be present
    assert "Message:" in output
