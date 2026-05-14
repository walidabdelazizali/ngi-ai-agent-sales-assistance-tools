from pathlib import Path

from src.agent_wrapper import run_agent_wrapper
from src.query.network_lookup import NetworkLookup


def _write_network_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "network_area_test.csv"
    csv_path.write_text(
        "\n".join(
            [
                "hnm_code,hn_basic_plus,provider_name,google_name,city,type,group_name,tel_no,area,location",
                "T001,✔,Alpha Hospital,Alpha Hospital,Dubai,Hospital,G1,111,Al Barsha,Loc1",
                "T002,✔,Beta Hospital,Beta Hospital,Dubai,Hospital,G2,222,Business Bay,Loc2",
                "T003,✔,Gamma Clinic,Gamma Clinic,Dubai,Clinic,G3,333,Al Barsha South,Loc3",
                "T004,✔,Delta Hospital,Delta Hospital,Dubai,Hospital,G4,444,,Loc4",
                "T005,✔,Sharjah Muwaileh Hospital,Sharjah Muwaileh Hospital,Sharjah,Hospital,G5,555,Muwaileh Commercial - Al Zahia,Loc5",
                "T006,✔,Sharjah Muweilah Clinic,Sharjah Muweilah Clinic,Sharjah,Clinic,G6,666,MUWEILAH,Loc6",
                "T007,✔,Sharjah Nahda Clinic,Sharjah Nahda Clinic,Sharjah,Clinic,G7,777,Al Nahda,Loc7",
                "T008,✔,Sharjah Nahda1 Clinic,Sharjah Nahda1 Clinic,Sharjah,Clinic,G8,888,Al Nahda 1,Loc8",
            ]
        ),
        encoding="utf-8",
    )
    return csv_path


def test_area_normalized_narrowing_match(tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Dubai",
        provider_type="hospital",
        area="Al Barsha",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is True
    assert result["area_fallback_to_city"] is False
    assert result["count"] == 1
    assert result["providers"] == ["Alpha Hospital"]


def test_area_no_match_falls_back_to_city_level(tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Dubai",
        provider_type="hospital",
        area="Dubai South",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is False
    assert result["area_fallback_to_city"] is True
    assert result["count"] == 3
    assert "Alpha Hospital" in result["providers"]
    assert "Beta Hospital" in result["providers"]
    assert "Delta Hospital" in result["providers"]


def test_city_only_behavior_unchanged_without_area(tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Dubai",
        provider_type="hospital",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is False
    assert result["area_fallback_to_city"] is False
    assert result["count"] == 3


def test_wrapper_adds_safe_area_fallback_message(monkeypatch):
    class FakeLookup:
        def list_providers_in_network(self, **kwargs):
            return {
                "ok": True,
                "network_code": "hn_basic_plus",
                "city": "Dubai",
                "provider_type": "hospital",
                "requested_area": "Al Barsha",
                "area_filter_applied": False,
                "area_fallback_to_city": True,
                "count": 1,
                "providers": ["Fallback Provider"],
                "truncated": False,
            }

        def provider_details(self, _name):
            return {"found": False, "area": ""}

    monkeypatch.setattr("src.query.plan_network_lookup.resolve_plan_network", lambda _plan: {"found": True, "medical_network": "hn_basic_plus"})
    monkeypatch.setattr("src.query.network_lookup.get_network_lookup", lambda: FakeLookup())

    out = run_agent_wrapper("List hospital providers in Al Barsha Dubai for Remedy 6")

    assert out["ok"] is True
    assert out["intent"] == "plan_network_city_type"
    assert "Area Match Mode: CITY FALLBACK" in out["message"]
    assert "Exact area-filtered providers were not found." in out["message"]
    assert "Showing broader Dubai city-level providers instead." in out["message"]


def test_wrapper_adds_active_area_match_mode_message(monkeypatch):
    class FakeLookup:
        def list_providers_in_network(self, **kwargs):
            return {
                "ok": True,
                "network_code": "hn_basic_plus",
                "city": "Dubai",
                "provider_type": "hospital",
                "requested_area": "Al Barsha",
                "area_filter_applied": True,
                "area_fallback_to_city": False,
                "count": 2,
                "providers": ["P1", "P2"],
                "truncated": False,
            }

        def provider_details(self, _name):
            return {"found": False, "area": ""}

    monkeypatch.setattr("src.query.plan_network_lookup.resolve_plan_network", lambda _plan: {"found": True, "medical_network": "hn_basic_plus"})
    monkeypatch.setattr("src.query.network_lookup.get_network_lookup", lambda: FakeLookup())

    out = run_agent_wrapper("List hospital providers in Al Barsha Dubai for Remedy 6")

    assert out["ok"] is True
    assert out["intent"] == "plan_network_city_type"
    assert "Area Match Mode: ACTIVE" in out["message"]
    assert "Matched Providers Count: 2" in out["message"]


def test_wrapper_renders_provider_area_inline_from_dataset(monkeypatch, tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    monkeypatch.setattr("src.query.plan_network_lookup.resolve_plan_network", lambda _plan: {"found": True, "medical_network": "hn_basic_plus"})
    monkeypatch.setattr("src.query.network_lookup.get_network_lookup", lambda: lookup)

    out = run_agent_wrapper("List hospital providers in Dubai for Remedy 6")

    assert out["ok"] is True
    assert out["intent"] == "plan_network_city_type"
    assert "- Alpha Hospital [Al Barsha]" in out["message"]
    assert "- Beta Hospital [Business Bay]" in out["message"]


def test_wrapper_keeps_provider_without_area_name_only(monkeypatch, tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    monkeypatch.setattr("src.query.plan_network_lookup.resolve_plan_network", lambda _plan: {"found": True, "medical_network": "hn_basic_plus"})
    monkeypatch.setattr("src.query.network_lookup.get_network_lookup", lambda: lookup)

    out = run_agent_wrapper("List hospital providers in Dubai for Remedy 6")

    assert out["ok"] is True
    assert out["intent"] == "plan_network_city_type"
    assert "- Delta Hospital" in out["message"]
    assert "- Delta Hospital [" not in out["message"]


def test_muwaileh_commercial_variant_resolves_active(tmp_path):
    """Dataset AREA 'Muwaileh Commercial - Al Zahia' should match user query 'Muwaileh'."""
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Sharjah",
        provider_type="hospital",
        area="Muwaileh",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is True
    assert result["area_fallback_to_city"] is False
    assert result["count"] == 1
    assert result["providers"] == ["Sharjah Muwaileh Hospital"]


def test_al_nahda_1_variant_resolves_active(tmp_path):
    """Dataset AREA 'Al Nahda 1' should match user query 'Al Nahda'."""
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Sharjah",
        provider_type="clinic",
        area="Al Nahda",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is True
    assert result["area_fallback_to_city"] is False
    # Both 'Al Nahda' and 'Al Nahda 1' rows must match
    assert result["count"] == 2
    assert "Sharjah Nahda Clinic" in result["providers"]
    assert "Sharjah Nahda1 Clinic" in result["providers"]


def test_muwaileh_alias_resolves_active_with_dataset_variant(tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Sharjah",
        provider_type="clinic",
        area="Muwaileh",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is True
    assert result["area_fallback_to_city"] is False
    assert result["count"] == 1
    assert result["providers"] == ["Sharjah Muweilah Clinic"]


def test_al_nahda_alias_resolves_active_with_dataset_variant(tmp_path):
    lookup = NetworkLookup(_write_network_csv(tmp_path))

    result = lookup.list_providers_in_network(
        network_code="hn_basic_plus",
        city="Sharjah",
        provider_type="clinic",
        area="Al Nahda",
    )

    assert result["ok"] is True
    assert result["area_filter_applied"] is True
    assert result["area_fallback_to_city"] is False
    assert result["count"] == 2
    assert "Sharjah Nahda Clinic" in result["providers"]
    assert "Sharjah Nahda1 Clinic" in result["providers"]


def test_wrapper_area_debug_block_visible_when_enabled(monkeypatch):
    import src.agent_wrapper as wrapper

    class FakeLookup:
        def list_providers_in_network(self, **kwargs):
            return {
                "ok": True,
                "network_code": "hn_basic_plus",
                "city": "Sharjah",
                "provider_type": "clinic",
                "requested_area": "Al Nahda",
                "area_filter_applied": False,
                "area_fallback_to_city": True,
                "count": 1,
                "providers": ["Sharjah Nahda Clinic"],
                "truncated": False,
                "area_debug": {
                    "raw_area_query": "Al Nahda",
                    "normalized_area_query": "al nahda",
                    "expanded_alias_terms": ["al nahda", "al nahda st", "al nahda shj"],
                    "provider_area_checks": [
                        {
                            "provider": "Sharjah Nahda Clinic",
                            "raw_area": "AL NAHDA ST",
                            "normalized_area": "al nahda",
                            "matched": True,
                        }
                    ],
                },
            }

        def provider_details(self, _name):
            return {"found": True, "area": "AL NAHDA ST"}

    monkeypatch.setattr("src.query.plan_network_lookup.resolve_plan_network", lambda _plan: {"found": True, "medical_network": "hn_basic_plus"})
    monkeypatch.setattr("src.query.network_lookup.get_network_lookup", lambda: FakeLookup())
    monkeypatch.setattr(wrapper, "DEBUG_AREA_MATCHING", True)

    out = run_agent_wrapper("List clinic providers in Al Nahda Sharjah for Remedy 6")

    assert out["ok"] is True
    assert "[AREA DEBUG]" in out["message"]
    assert "Raw Area Query: Al Nahda" in out["message"]
    assert "Normalized Area Query: al nahda" in out["message"]
    assert "- al nahda st" in out["message"]
    assert "Matched: YES" in out["message"]
