import pytest
import src.query.plan_network_lookup as plan_network_lookup
from src.query.plan_network_lookup import load_plan_network_mapping, resolve_plan_network, get_medical_network_for_plan


APPROVED_PLAN_NETWORKS = {
    "Remedy 02": "hn_basic_plus",
    "Remedy 03": "hn_basic_plus",
    "Remedy 04": "hn_basic_plus",
    "Remedy 05": "hn_basic_plus",
    "Remedy 06": "hn_basic_plus",
    "Classic 2": "hn_standard_plus",
    "Classic 2R": "hn_standard_plus",
    "Classic 3": "hn_standard",
}


def test_load_mapping():
    mapping = load_plan_network_mapping()
    assert isinstance(mapping, list)
    assert any(row["plan_name"] == "Remedy 02" for row in mapping)


@pytest.mark.parametrize("plan_name,expected_network", APPROVED_PLAN_NETWORKS.items())
def test_approved_plan_resolves_expected_network(plan_name, expected_network):
    result = resolve_plan_network(plan_name)
    assert result["found"]
    assert result["medical_network"] == expected_network


@pytest.mark.parametrize(
    "plan_code,expected_network",
    [
        ("HN-REMEDY-2", "hn_basic_plus"),
        ("HN-REMEDY-3", "hn_basic_plus"),
        ("HN-REMEDY-4", "hn_basic_plus"),
        ("HN-REMEDY-5", "hn_basic_plus"),
        ("HN-REMEDY-6", "hn_basic_plus"),
        ("HN_CLASSIC_2", "hn_standard_plus"),
        ("HN_CLASSIC_2R", "hn_standard_plus"),
        ("HN_CLASSIC_3", "hn_standard"),
    ],
)
def test_approved_plan_code_resolves_expected_network(plan_code, expected_network):
    result = resolve_plan_network(plan_code)
    assert result["found"]
    assert result["medical_network"] == expected_network


def test_resolve_unknown_plan():
    result = resolve_plan_network("Unknown Plan")
    assert not result["found"]


def test_get_medical_network_for_unknown_plan_blocks_safely():
    net = get_medical_network_for_plan("Nonexistent Plan")
    assert net is None


def test_stale_csv_mapping_does_not_silently_pass(tmp_path, monkeypatch):
    csv_path = tmp_path / "plan_network_mapping.csv"
    csv_path.write_text(
        "plan_code,plan_name,medical_network\n"
        "HN-REMEDY-5,Remedy 05,hn_elite\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(plan_network_lookup, "MAPPING_CSV", csv_path)

    result = resolve_plan_network("Remedy 05")

    assert result["found"]
    assert result["medical_network"] == "hn_basic_plus"


def test_missing_csv_row_does_not_hide_approved_mapping(tmp_path, monkeypatch):
    csv_path = tmp_path / "plan_network_mapping.csv"
    csv_path.write_text(
        "plan_code,plan_name,medical_network\n"
        "HN-REMEDY-2,Remedy 02,hn_basic_plus\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(plan_network_lookup, "MAPPING_CSV", csv_path)

    result = resolve_plan_network("Remedy 06")

    assert result["found"]
    assert result["medical_network"] == "hn_basic_plus"


def test_normalization():
    assert resolve_plan_network("remedy02")["found"]
    assert resolve_plan_network("REMEDY 02")["found"]
    assert resolve_plan_network("remedy-02")["found"]
