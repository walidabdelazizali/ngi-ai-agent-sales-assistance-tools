import subprocess
import sys
import json
import re

def run_entrypoint(args):
    cmd = [sys.executable, '-m', 'src.agent_entrypoint'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def test_plan_core_human():
    code, out, err = run_entrypoint(["What is the annual limit for Remedy 04?"])
    assert code == 0
    assert "Intent: plan_core" in out
    assert "Plan: Remedy 04" in out
    assert "annual_limit: 500,000" in out

def test_reimbursement_rules_human():
    code, out, err = run_entrypoint(["What are the reimbursement rules for Remedy 05?"])
    assert code == 0
    assert "Intent: reimbursement_rules" in out
    assert "Plan: Remedy 05" in out
    assert "reimbursement_allowed: True" in out

def test_plan_summary_human():
    code, out, err = run_entrypoint(["Give me a summary of Remedy 04"])
    assert code == 0
    assert "Intent: plan_summary" in out
    assert "Plan: Remedy 04" in out
    assert "summary_text:" in out

def test_unsupported_plan_human():
    code, out, err = run_entrypoint(["Tell me about Remedy 99"])
    assert code == 0
    assert "Intent: unsupported" in out
    assert "supported plan" in out.lower()

def test_unsupported_query_human():
    code, out, err = run_entrypoint(["How do I get a discount?"])
    assert code == 0
    assert "Intent: unsupported" in out
    assert "supported plan" in out.lower() or "not supported" in out.lower()

def test_json_mode():
    code, out, err = run_entrypoint(["--json", "What are the reimbursement rules for Remedy 05?"])
    assert code == 0
    data = json.loads(out)
    assert data["ok"] is True
    assert data["intent"] == "reimbursement_rules"
    assert data["plan_name"] == "Remedy 05"
    assert data["tool_name"] == "get_reimbursement_rules"
    assert data["data"]["reimbursement_allowed"] is True

def test_regression_safe():
    # Should not crash or throw for any input
    queries = [
        "What is the annual limit for Remedy 04?",
        "What are the reimbursement rules for Remedy 05?",
        "Give me a summary of Remedy 04",
        "Tell me about Remedy 99",
        "How do I get a discount?",
        "--json What are the reimbursement rules for Remedy 05?"
    ]
    for q in queries:
        args = q.split()
        code, out, err = run_entrypoint(args)
        assert code == 0
        assert not err
