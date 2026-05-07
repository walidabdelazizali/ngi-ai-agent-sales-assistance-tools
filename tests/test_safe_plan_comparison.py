import pytest
from src.agent_wrapper import run_agent_wrapper

def test_compare_classic2_and_remedy03_no_crash():
    out = run_agent_wrapper("compare Classic 2 and Remedy 03")
    assert out["ok"] is False or out["ok"] is True  # Should not crash
    assert "not supported" in out["message"].lower() or "not available" in out["message"].lower() or out["intent"] == "plan_comparison"

def test_which_plan_better_classic2_remedy03_no_crash():
    out = run_agent_wrapper("Which plan is better, Classic 2 or Remedy 03?")
    assert out["ok"] is False or out["ok"] is True  # Should not crash
    assert "not supported" in out["message"].lower() or "not available" in out["message"].lower() or out["intent"] == "plan_comparison"

def test_compare_classic2_and_remedy99_blocks():
    out = run_agent_wrapper("compare Classic 2 and Remedy 99")
    assert out["ok"] is False
    assert "not supported" in out["message"].lower() or "not available" in out["message"].lower()
