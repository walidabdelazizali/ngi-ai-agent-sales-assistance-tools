import pytest
from src.query.network_lookup import NetworkLookup
from pathlib import Path

def test_armada_included_in_dubai_hospital_listing():
    csv_path = Path("runtime_data/networks/network_list_normalized.csv")
    if not csv_path.exists():
        pytest.skip("No real network file present")
    lookup = NetworkLookup(csv_path)
    result = lookup.answer_query("List hospitals in Dubai under HN Basic Plus")
    assert "ARMADA ONE DAY SURGICAL CENTER DMCC" in result, "ARMADA ONE DAY SURGICAL CENTER DMCC should be included in Dubai hospital listing for HN Basic Plus."
