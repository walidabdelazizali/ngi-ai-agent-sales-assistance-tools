from src.agent_wrapper import run_agent_wrapper
from src.tools import enhanced_catalog_comparison as ecc


def test_approved_classic1_vs_prime1_comparison_succeeds():
    out = run_agent_wrapper("Compare Classic 1 and Prime 1")
    assert out["ok"] is True
    assert out["intent"] == "plan_comparison"
    assert out["tool_name"] == "compare_enhanced_plans"


def test_supported_compare_phrase_variants_work():
    for query in (
        "Compare Classic 1 vs Prime 1",
        "Compare HN_CLASSIC_1 and HN_PRIME_1",
    ):
        out = run_agent_wrapper(query)
        assert out["ok"] is True
        assert out["tool_name"] == "compare_enhanced_plans"


def test_output_contains_advantage_and_advantage_plus():
    out = run_agent_wrapper("Compare Classic 1 and Prime 1")
    msg = out.get("message") or ""
    assert "Advantage" in msg
    assert "Advantage Plus" in msg


def test_output_has_no_pricing_or_recommendation_wording():
    out = run_agent_wrapper("Compare Classic 1 and Prime 1")
    msg = (out.get("message") or "").lower()
    forbidden = ["premium", "price", "pricing", "cost", "quote", "better", "best", "recommended", "upgrade"]
    for token in forbidden:
        assert token not in msg


def test_missing_required_field_blocks(monkeypatch):
    original = ecc.load_enhanced_plan

    def _fake_load(name):
        data = original(name)
        if data.get("plan_name") == "Classic 1":
            data = dict(data)
            data.pop("annual_limit", None)
        return data

    monkeypatch.setattr(ecc, "load_enhanced_plan", _fake_load)
    out = run_agent_wrapper("Compare Classic 1 and Prime 1")
    assert out["ok"] is False
    assert out["message"] == "Comparison is not available because one or more approved comparison fields are missing."


def test_unapproved_enhanced_plan_blocks(monkeypatch):
    original = ecc.load_enhanced_plan

    def _fake_load(name):
        data = original(name)
        if data.get("plan_name") == "Classic 1":
            data = dict(data)
            data["approval_status"] = "draft"
        return data

    monkeypatch.setattr(ecc, "load_enhanced_plan", _fake_load)
    out = run_agent_wrapper("Compare Classic 1 and Prime 1")
    assert out["ok"] is False
    assert out["message"] == "Comparison is not available because one or more approved comparison fields are missing."
