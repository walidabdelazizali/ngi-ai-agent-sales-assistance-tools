import pytest
import pandas as pd
from pathlib import Path
from src.query.network_lookup import NetworkLookup

TEST_CSV = Path(__file__).parent / "fixtures/network_list_test.csv"

@pytest.fixture(scope="module")
def test_lookup():
    return NetworkLookup(TEST_CSV)

def test_exact_provider_name_match(test_lookup):
    result = test_lookup.provider_details("Test Provider One")
    assert result["found"]
    assert result["provider_name"] == "Test Provider One"
    assert "hn_exclusive" in result["available_network_tiers"]

def test_exact_google_name_match(test_lookup):
    result = test_lookup.provider_details("Test Google Two")
    assert result["found"]
    assert result["google_name"] == "Test Google Two"
    assert "hn_premier" in result["available_network_tiers"]

def test_english_query_extraction():
    extracted = NetworkLookup.extract_provider_from_query("Is Test Provider One in the network?")
    assert extracted == "Test Provider One"

def test_arabic_query_extraction():
    extracted = NetworkLookup.extract_provider_from_query("هل Test Provider Two داخل الشبكة؟")
    assert extracted == "Test Provider Two"

def test_unique_contains_fallback(test_lookup):
    result = test_lookup.provider_details("Provider Three")
    assert result["found"]
    assert result["provider_name"] == "Test Provider Three"

def test_ambiguous_multiple_match(test_lookup):
    result = test_lookup.provider_details("Ambiguous Provider")
    assert not result["found"] and result.get("ambiguous", False)

def test_provider_not_found(test_lookup):
    result = test_lookup.provider_details("Nonexistent Provider")
    assert not result["found"]

def test_smoke_real_network_file():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    assert len(lookup.df) > 0
    # Try a real provider from the file
    found = False
    for name in lookup.df["provider_name"]:
        if name.strip():
            result = lookup.provider_details(name)
            if result["found"]:
                found = True
                break
    assert found, "No provider found in real file"
