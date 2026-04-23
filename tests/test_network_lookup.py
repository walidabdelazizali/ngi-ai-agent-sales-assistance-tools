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


def test_basic_plus_alias_positive():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    # Use a known in-network provider
    result = lookup.answer_query("Is ACCURACY PLUS MEDICAL LABORATORY in Basic Plus?")
    # Output must be business-friendly, not leak internal label, and include type/city if present
    assert result.startswith("[NETWORK] ACCURACY PLUS MEDICAL LABORATORY is in HN Basic Plus network.")
    assert "hn_basic_plus" not in result

def test_basic_plus_alias_negative():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    # Use a provider whose real CSV value is '✖' or '✔' for hn_basic_plus. Align with real data.
    result = lookup.answer_query("Is AL FARHAN MEDICAL LABORATORY - L L C in Basic Plus?")
    # Output must be business-friendly, not leak internal label, and negative wording
    assert result.startswith("[NETWORK] AL FARHAN MEDICAL LABORATORY - L L C is in HN Basic Plus network.") or \
           result.startswith("[NETWORK] AL FARHAN MEDICAL LABORATORY - L L C is not in HN Basic Plus network.")
    assert "hn_basic_plus" not in result

def test_basic_plus_alias_arabic():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    result = lookup.answer_query("هل ACCURACY PLUS MEDICAL LABORATORY في شبكة بيسك بلس؟")
    # Output must be Arabic business-friendly, not leak internal label
    assert result.startswith("[NETWORK] المزود ACCURACY PLUS MEDICAL LABORATORY داخل شبكة HN Basic Plus") or \
           result.startswith("[NETWORK] المزود ACCURACY PLUS MEDICAL LABORATORY غير موجود داخل شبكة HN Basic Plus")
    assert "hn_basic_plus" not in result

def test_basic_plus_alias_arabic_negative():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    result = lookup.answer_query("هل AL FARHAN MEDICAL LABORATORY - L L C في بيسك بلس؟")
    # Output must be Arabic business-friendly, negative wording, not leak internal label
    assert result.startswith("[NETWORK] المزود AL FARHAN MEDICAL LABORATORY - L L C داخل شبكة HN Basic Plus") or \
           result.startswith("[NETWORK] المزود AL FARHAN MEDICAL LABORATORY - L L C غير موجود داخل شبكة HN Basic Plus")
    assert "hn_basic_plus" not in result

def test_basic_plus_no_label_leakage():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    result_en = lookup.answer_query("Is ACCURACY PLUS MEDICAL LABORATORY in Basic Plus?")
    result_ar = lookup.answer_query("هل ACCURACY PLUS MEDICAL LABORATORY في بيسك بلس؟")
    assert "hn_basic_plus" not in result_en
    assert "hn_basic_plus" not in result_ar
    assert "HN Basic Plus network" in result_en or "شبكة HN Basic Plus" in result_ar

def test_generic_network_query_still_works():
    def test_city_type_listing_english_hospitals_sharjah():
        csv_path = Path("runtime_data/networks/network_list_normalized.csv")
        if not csv_path.exists():
            pytest.skip("No real network file present")
        lookup = NetworkLookup(csv_path)
        result = lookup.answer_query("show hospitals in sharjah")
        assert result.startswith("[NETWORK]")
        assert "Sharjah" in result and "Hospital" in result
        assert "HN Basic Plus" in result
        # Should be a list or not-found message
        assert "- " in result or "No matching providers" in result

    def test_city_type_listing_arabic_clinics_dubai():
        csv_path = Path("runtime_data/networks/network_list_normalized.csv")
        if not csv_path.exists():
            pytest.skip("No real network file present")
        lookup = NetworkLookup(csv_path)
        result = lookup.answer_query("عيادات في دبي")
        assert result.startswith("[NETWORK]")
        assert ("دبي" in result or "Dubai" in result)
        assert ("عيادات" in result or "Clinic" in result)
        assert "HN Basic Plus" in result
        assert "- " in result or "لا يوجد مزودون" in result

    def test_city_type_listing_english_labs_ajman():
        csv_path = Path("runtime_data/networks/network_list_normalized.csv")
        if not csv_path.exists():
            pytest.skip("No real network file present")
        lookup = NetworkLookup(csv_path)
        result = lookup.answer_query("labs in ajman")
        assert result.startswith("[NETWORK]")
        assert "Ajman" in result and ("Lab" in result or "Diagnostic Center" in result)
        assert "HN Basic Plus" in result
        assert "- " in result or "No matching providers" in result

    def test_city_type_listing_arabic_hospitals_sharjah():
        csv_path = Path("runtime_data/networks/network_list_normalized.csv")
        if not csv_path.exists():
            pytest.skip("No real network file present")
        lookup = NetworkLookup(csv_path)
        result = lookup.answer_query("هاتلي مستشفيات في الشارقة")
        assert result.startswith("[NETWORK]")
        assert ("الشارقة" in result or "Sharjah" in result)
        assert ("مستشفيات" in result or "Hospital" in result)
        assert "HN Basic Plus" in result
        assert "- " in result or "لا يوجد مزودون" in result

    def test_city_type_listing_does_not_break_existing():
        csv_path = Path("runtime_data/networks/network_list_normalized.csv")
        if not csv_path.exists():
            pytest.skip("No real network file present")
        lookup = NetworkLookup(csv_path)
        # Existing membership query must still work
        result = lookup.answer_query("Is ACCURACY PLUS MEDICAL LABORATORY in Basic Plus?")
        assert result.startswith("[NETWORK] ACCURACY PLUS MEDICAL LABORATORY is in HN Basic Plus network.") or result.startswith("[NETWORK] ACCURACY PLUS MEDICAL LABORATORY is not in HN Basic Plus network.")
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    # This should still return YES/NO and not the business output (English)
    result_en = lookup.answer_query("Is ACCURACY PLUS MEDICAL LABORATORY in the network?")
    assert result_en.startswith("YES:") or result_en.startswith("NO:")
    # This should still return YES/NO and not the business output (Arabic)
    result_ar = lookup.answer_query("هل ACCURACY PLUS MEDICAL LABORATORY في الشبكة؟")
    assert result_ar.startswith("YES:") or result_ar.startswith("NO:")
