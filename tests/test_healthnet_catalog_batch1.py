import pytest

from src.query.plan_network_lookup import resolve_plan_network
from src.query.plan_query import load_plan
from src.tool_contract import get_plan_summary
from src.agent_wrapper import run_agent_wrapper
from src.tools.enhanced_plan_loader import (
    ENHANCED_PLAN_REGISTRY,
    is_enhanced_plan,
    load_enhanced_plan,
)


BATCH1_PLANS = [
    ("Prime 1", "HN_PRIME_1", "hn_advantage_plus", "data/plans/raw/HN_PRIME_1/source_table_HN_PRIME_1.json"),
    ("Prime 2", "HN_PRIME_2", "hn_standard_plus", "data/plans/raw/HN_PRIME_2/source_table_HN_PRIME_2.json"),
    ("Classic 1", "HN_CLASSIC_1", "hn_advantage", "data/plans/raw/HN_CLASSIC_1/source_table_HN_CLASSIC_1.json"),
    ("Classic 1R", "HN_CLASSIC_1R", "hn_advantage", "data/plans/raw/HN_CLASSIC_1R/source_table_HN_CLASSIC_1R.json"),
    ("Classic 4", "HN_CLASSIC_4", "hn_basic_plus", "data/plans/raw/HN_CLASSIC_4/source_table_HN_CLASSIC_4.json"),
]


@pytest.mark.parametrize("plan_name,plan_code,expected_network,source_path", BATCH1_PLANS)
def test_batch1_is_registered_as_enhanced_plan(plan_name, plan_code, expected_network, source_path):
    assert is_enhanced_plan(plan_name)


@pytest.mark.parametrize("plan_name,plan_code,expected_network,source_path", BATCH1_PLANS)
def test_batch1_load_enhanced_plan_core(plan_name, plan_code, expected_network, source_path):
    plan = load_enhanced_plan(plan_name)

    assert plan["plan_name"] == plan_name
    assert plan["plan_code"] == plan_code
    assert plan["approval_status"] == "approved"
    assert plan["tests_passed"] is True

    assert isinstance(plan["source_trace"], dict)
    for field in (
        "plan_name",
        "plan_code",
        "network_name",
        "annual_limit",
        "area_of_coverage",
        "direct_billing",
        "referral_required",
    ):
        assert plan.get(field) is not None
        assert plan["source_trace"].get(field)
        assert plan["source_trace"][field].startswith(source_path + ":")


@pytest.mark.parametrize("plan_name,plan_code,expected_network,source_path", BATCH1_PLANS)
def test_batch1_resolve_expected_network(plan_name, plan_code, expected_network, source_path):
    result = resolve_plan_network(plan_name)
    assert result["found"] is True
    assert result["medical_network"] == expected_network


@pytest.mark.parametrize("plan_name,plan_code,expected_network,source_path", BATCH1_PLANS)
def test_batch1_load_plan_uses_enhanced_loader(plan_name, plan_code, expected_network, source_path):
    plan = load_plan(plan_name)
    assert plan["plan_name"] == plan_name
    assert plan["plan_code"] == plan_code
    for field, trace in plan["source_trace"].items():
        if field in {"approval_status", "tests_passed", "source_trace"}:
            continue
        assert trace.startswith(source_path + ":")
        assert "output/" not in trace


@pytest.mark.parametrize("plan_name,plan_code,expected_network,source_path", BATCH1_PLANS)
def test_batch1_summary_works(plan_name, plan_code, expected_network, source_path):
    summary = get_plan_summary(plan_name)
    assert summary["plan_name"] == plan_name
    assert summary["summary_text"]
    assert summary["field_count"] == 7


def test_batch1_plan_blocks_if_not_approved(monkeypatch):
    original = dict(ENHANCED_PLAN_REGISTRY["Prime 1"])
    try:
        ENHANCED_PLAN_REGISTRY["Prime 1"]["approved"] = False
        with pytest.raises(ValueError, match="Enhanced plan not ready"):
            load_enhanced_plan("Prime 1")
    finally:
        ENHANCED_PLAN_REGISTRY["Prime 1"].update(original)


def test_classic1r_canonical_core_values():
    plan = load_enhanced_plan("Classic 1R")
    assert plan["plan_code"] == "HN_CLASSIC_1R"
    assert plan["annual_limit"] == "AED 300,000"
    assert plan["network_name"] == "Advantage"


def test_classic1r_pharmacy_maternity_dental_mental_fields():
    plan = load_enhanced_plan("Classic 1R")

    # Pharmacy
    assert "AED 10,000" in plan["pharmacy_cover_summary"]
    assert "10%" in plan["pharmacy_cover_summary"]
    # Maternity
    assert "AED 15,000" in plan["maternity_cover"]
    assert "Max visits: 12" in plan["maternity_cover"]
    # Dental
    assert plan["dental"]["annual_limit"] == "AED 2,500"
    assert "AED 2,500" in plan["dental_cover_summary"]
    # Mental health
    assert plan["mental_health"]["annual_limit"] == "AED 3,000"
    assert "AED 3,000" in plan["mental_health_cover_summary"]


def test_classic1r_source_trace_presence_for_benefit_fields():
    plan = load_enhanced_plan("Classic 1R")
    trace = plan["source_trace"]

    required = [
        "annual_limit",
        "network_name",
        "pharmacy_cover_summary",
        "maternity_cover",
        "dental_cover_summary",
        "mental_health_cover_summary",
    ]
    for field in required:
        assert trace.get(field)
        assert trace[field].startswith("data/plans/raw/HN_CLASSIC_1R/source_table_HN_CLASSIC_1R.json:")


@pytest.mark.parametrize(
    "query,expected_fragments",
    [
        ("What is the pharmacy benefit for Classic 1R?", ["pharmacy", "aed 10,000", "10%"]),
        ("What is the maternity limit for Classic 1R?", ["maternity", "aed 15,000"]),
        ("Does Classic 1R cover dental?", ["dental", "aed 2,500", "20%"]),
        ("What is the mental health cover for Classic 1R?", ["mental", "aed 3,000", "20%"]),
        ("What is the annual limit for Classic 1R?", ["annual", "aed 300,000"]),
        ("What is the network for Classic 1R?", ["network", "advantage"]),
    ],
)
def test_classic1r_benefit_queries_route_to_deterministic_answers(query, expected_fragments):
    result = run_agent_wrapper(query)
    assert result.get("ok") is True
    assert result.get("intent") != "unsupported"
    msg = (result.get("message") or "").lower()
    # Must not leak full plan summary when a specific benefit is requested.
    if "pharmacy" in query.lower() or "maternity" in query.lower() or "dental" in query.lower() or "mental" in query.lower():
        assert "area:" not in msg
        assert "direct billing:" not in msg
    for frag in expected_fragments:
        assert frag in msg
