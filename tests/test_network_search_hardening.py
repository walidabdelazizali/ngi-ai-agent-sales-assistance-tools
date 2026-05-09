from pathlib import Path

import pytest

from src.agent_wrapper import run_agent_wrapper
from src.query.network_lookup import NetworkLookup


CSV_PATH = Path("runtime_data/networks/network_list_normalized.csv")


@pytest.fixture(scope="module")
def lookup():
    if not CSV_PATH.exists():
        pytest.skip("No real network file present")
    return NetworkLookup(CSV_PATH)


def test_hospital_name_partial_match(lookup):
    result = lookup.answer_query("Is Burjeel Abu Dhabi in the network?")
    assert result.startswith("YES:")


def test_arabic_hospital_query(lookup):
    result = lookup.answer_query("هل مستشفى برجيل داخل الشبكة؟")
    assert result.startswith("YES:")


def test_mixed_arabic_english_network_query(lookup):
    result = lookup.answer_query("Burjeel Hospital في اي شبكة؟")
    assert result.startswith("Networks for")
    assert "hn_" in result


def test_provider_city_query(lookup):
    result = lookup.answer_query("What city is Burjeel Hospital located in?")
    assert "City for Burjeel Hospital" in result
    assert "ABU DHABI" in result


def test_provider_type_query(lookup):
    result = lookup.answer_query("What type of provider is Burjeel Hospital?")
    assert "Type for Burjeel Hospital" in result
    assert "HOSPITAL" in result


def test_provider_network_tier_query(lookup):
    result = lookup.answer_query("Which network tiers for Burjeel Hospital?")
    assert result.startswith("Network tiers for Burjeel Hospital")
    assert "hn_exclusive" in result


def test_safe_not_found_response(lookup):
    result = lookup.answer_query("Is Unknown Future Hospital in Basic Plus?")
    assert result == "Provider not found."


def test_wrapper_routes_network_query_safely():
    out = run_agent_wrapper("Is Burjeel Abu Dhabi in the network?")
    assert out["intent"] == "network_lookup"
    assert out["tool_name"] == "network_lookup"
    assert out["ok"] is True
    assert str(out["message"]).startswith("YES:")


def test_wrapper_safe_not_found_network_query():
    out = run_agent_wrapper("Is Unknown Future Hospital in Basic Plus?")
    assert out["intent"] == "network_lookup"
    assert out["tool_name"] == "network_lookup"
    assert out["ok"] is False
    assert "Provider not found." in str(out["message"])


def test_wrapper_routes_arabic_in_which_network_query():
    out = run_agent_wrapper("Burjeel Hospital في أي شبكة؟")
    assert out["intent"] == "network_lookup"
    assert out["tool_name"] == "network_lookup"
