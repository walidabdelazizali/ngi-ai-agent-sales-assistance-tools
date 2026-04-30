import pytest
from src.query.plan_query import load_plan

def test_remedy05_annual_limit_canonical():
    plan = load_plan("Remedy 05")
    assert plan["annual_limit"].replace(",","").replace(" ","") in ["AED.150000","AED150000"], f"Remedy 05 annual_limit should be canonical, got {plan['annual_limit']}"

def test_remedy05_network_canonical():
    plan = load_plan("Remedy 05")
    assert plan["network_name"].lower() == "hn basic plus", f"Remedy 05 network_name should be canonical, got {plan['network_name']}"

def test_remedy05_annual_limit_not_legacy():
    plan = load_plan("Remedy 05")
    assert plan["annual_limit"] != "1,000,000", "Remedy 05 annual_limit must not be legacy value 1,000,000"

def test_remedy05_network_not_legacy():
    plan = load_plan("Remedy 05")
    assert plan["network_name"].lower() != "hn_elite", "Remedy 05 network_name must not be legacy value hn_elite"

def test_remedy02_still_loads():
    plan = load_plan("Remedy 02")
    assert plan["plan_name"] == "NGI Healthnet –Remedy 02"
import pytest
from src.query.plan_query import load_plan

def test_remedy05_annual_limit():
    plan = load_plan("Remedy 05")
    assert plan["annual_limit"] == "AED. 150,000", f"Expected 'AED. 150,000', got {plan['annual_limit']}"
    assert plan["annual_limit"] != "1,000,000", "Must not return legacy value '1,000,000'"

def test_remedy05_network():
    plan = load_plan("Remedy 05")
    assert plan["network_name"] == "HN Basic Plus", f"Expected 'HN Basic Plus', got {plan['network_name']}"
    assert plan["network_name"] != "hn_elite", "Must not return legacy value 'hn_elite'"

def test_remedy05_no_legacy_override():
    plan = load_plan("Remedy 05")
    # These values must not be present from legacy JSON
    assert plan["annual_limit"] != "1,000,000"
    assert plan["network_name"] != "hn_elite"
