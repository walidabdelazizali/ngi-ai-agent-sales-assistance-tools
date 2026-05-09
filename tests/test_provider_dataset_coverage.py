import pytest
from pathlib import Path

from src.query.network_lookup import NetworkLookup


CSV_PATH = Path("runtime_data/networks/network_list_normalized.csv")


@pytest.fixture(scope="module")
def lookup():
    if not CSV_PATH.exists():
        pytest.skip("No real network file present")
    return NetworkLookup(CSV_PATH)


def test_aster_qsais_alias_resolves(lookup):
    result = lookup.provider_details("Aster Qsais")
    assert result.get("found", False), result
    assert "ASTER" in result.get("provider_name", "").upper()
    assert "QUSAIS" in result.get("provider_name", "").upper()


def test_burjeel_auh_alias_resolves(lookup):
    result = lookup.provider_details("Burjeel AUH")
    assert result.get("found", False), result
    assert "BURJEEL HOSPITAL" in result.get("provider_name", "").upper()


def test_nmc_royal_is_ambiguity_safe(lookup):
    result = lookup.provider_details("NMC Royal")
    assert not result.get("found", False), result
    assert result.get("ambiguous", False), result
    assert len(result.get("candidates", [])) >= 2


def test_arabic_transliteration_aster(lookup):
    result = lookup.provider_details("استر القصيص")
    assert result.get("found", False), result
    assert "ASTER" in result.get("provider_name", "").upper()


def test_ambiguous_response_lists_candidates_en(lookup):
    text = lookup.answer_query("Is Burjeel in the network?")
    assert text.startswith("Ambiguous provider match."), text
    assert "More than one provider matched:" in text


def test_ambiguous_response_lists_candidates_ar(lookup):
    text = lookup.answer_query("هل برجيل في الشبكة؟")
    assert "Ambiguous provider match" in text
    assert "أكثر من مزود مطابق" in text


def test_arabic_nmc_royal_is_ambiguity_safe(lookup):
    text = lookup.answer_query("هل ان ام سي رويال في الشبكة؟")
    assert "Ambiguous provider match" in text
    assert "أكثر من مزود مطابق" in text


def test_arabic_mediclinic_al_qusais_resolves(lookup):
    result = lookup.provider_details("ميديكلينيك القصيص")
    assert result.get("found", False), result
    assert "MEDICLINIC AL QUSAIS" in result.get("provider_name", "").upper()


def test_nmc_royal_tiers_query_is_ambiguity_safe(lookup):
    text = lookup.answer_query("Which network tiers for NMC Royal?")
    assert text.startswith("Ambiguous provider match."), text
    assert "More than one provider matched:" in text
