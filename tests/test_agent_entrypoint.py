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
    assert "annual limit" in out.lower()

def test_reimbursement_rules_human():
    code, out, err = run_entrypoint(["What are the reimbursement rules for Remedy 05?"])
    assert code == 0
    assert "Intent: reimbursement_rules" in out
    assert "Plan: Remedy 05" in out
    assert "reimbursement allowed" in out.lower() or "تعويض" in out

def test_plan_summary_human():
    code, out, err = run_entrypoint(["Give me a summary of Remedy 04"])
    assert code == 0
    assert "Intent: plan_summary" in out
    assert "Plan: Remedy 04" in out
    assert "summary" in out.lower()

def test_unsupported_plan_human():
    code, out, err = run_entrypoint(["Tell me about Remedy 99"])
    assert code == 0
    assert "Intent: unsupported" in out
    assert "not available" in out.lower() or "غير متاحة" in out

def test_unsupported_query_human():
    code, out, err = run_entrypoint(["How do I get a discount?"])
    assert code == 0
    assert "Intent: unsupported" in out
    assert "supported plan" in out.lower() or "not supported" in out.lower()

def test_json_mode():
    code, out, err = run_entrypoint(["--json", "What are the reimbursement rules for Remedy 05?"])
    assert code == 0
    data = json.loads(out)
    # Remedy 05 is now approved: expect ok=True and valid data
    assert data["ok"] is True
    assert "reimbursement allowed" in data["message"].lower() or "تعويض" in data["message"]
    # Ensure valid JSON structure
    assert "intent" in data
    assert "plan_name" in data
    assert "tool_name" in data
    assert "data" in data

def test_classic2_summarize_json_routes_to_plan_summary():
    code, out, err = run_entrypoint(["--json", "Summarize Classic 2"])
    assert code == 0
    assert not err
    data = json.loads(out)
    assert data["ok"] is True
    assert data["intent"] == "plan_summary"
    assert data["plan_name"] == "Classic 2"
    assert data["tool_name"] == "get_plan_summary"

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

def test_classic3_summarize_json_routes_to_plan_summary():
    code, out, err = run_entrypoint(["--json", "Summarize Classic 3"])
    assert code == 0
    assert not err
    data = json.loads(out)
    assert data["ok"] is True
    assert data["intent"] == "plan_summary"
    assert data["plan_name"] == "Classic 3"
    assert data["tool_name"] == "get_plan_summary"

def test_classic3_annual_limit_json_routes_to_plan_core():
    code, out, err = run_entrypoint(["--json", "What is the annual limit for Classic 3?"])
    assert code == 0
    assert not err
    data = json.loads(out)
    assert data["ok"] is True
    assert data["intent"] == "plan_core"
    assert data["plan_name"] == "Classic 3"
    assert data["tool_name"] == "get_plan_core"
