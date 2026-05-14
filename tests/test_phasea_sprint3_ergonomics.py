"""
Phase A Sprint 3 – Provider lookup ergonomics regression tests.

Tests:
- Deterministic query construction via build_provider_query()
- City, provider-type, and plan persistence rebuild logic
- Missing-parameter guard (returns empty string, not a guess)
- Backend routing unchanged for UI-constructed queries
- Unsupported query preservation
- Existing provider lookup preservation (provider engine untouched)
"""
import pytest
from src.ui_query_builder import build_provider_query
from src.agent_wrapper import run_agent_wrapper


# ---------------------------------------------------------------------------
# Part D – Deterministic query reconstruction
# ---------------------------------------------------------------------------

class TestBuildProviderQuery:
    """build_provider_query mirrors the JS form-submit query construction."""

    def test_hospital_dubai_remedy5(self):
        q = build_provider_query("Dubai", "hospital", "Remedy 5")
        assert q == "List hospital providers in Dubai for Remedy 5"

    def test_clinic_sharjah_remedy6(self):
        q = build_provider_query("Sharjah", "clinic", "Remedy 6")
        assert q == "List clinic providers in Sharjah for Remedy 6"

    def test_pharmacy_abudhabi_classic1(self):
        q = build_provider_query("Abu Dhabi", "pharmacy", "Classic 1")
        assert q == "List pharmacy providers in Abu Dhabi for Classic 1"

    def test_lab_abudhabi_prime1(self):
        q = build_provider_query("Abu Dhabi", "lab", "Prime 1")
        assert q == "List lab providers in Abu Dhabi for Prime 1"

    def test_with_area_included(self):
        q = build_provider_query("Dubai", "clinic", "Classic 1", area="Deira")
        assert q == "List clinic providers in Deira Dubai for Classic 1"

    def test_type_lowercased(self):
        """Provider type is normalised to lower-case."""
        q = build_provider_query("Dubai", "Hospital", "Remedy 5")
        assert q == "List hospital providers in Dubai for Remedy 5"

    def test_whitespace_stripped(self):
        q = build_provider_query("  Dubai  ", "  hospital  ", "  Remedy 5  ")
        assert q == "List hospital providers in Dubai for Remedy 5"


# ---------------------------------------------------------------------------
# Part D – Persistence: changing one dimension rebuilds deterministically
# ---------------------------------------------------------------------------

class TestPersistenceRebuild:
    """Simulates clicking a quick-filter chip after a previous selection."""

    def test_city_persistence_dubai_to_sharjah(self):
        """Switching city keeps last type and plan."""
        first = build_provider_query("Dubai", "hospital", "Remedy 5")
        assert first == "List hospital providers in Dubai for Remedy 5"
        # Operator clicks Sharjah city chip — type and plan unchanged
        second = build_provider_query("Sharjah", "hospital", "Remedy 5")
        assert second == "List hospital providers in Sharjah for Remedy 5"

    def test_provider_type_persistence_hospital_to_labs(self):
        """Switching provider type keeps last city and plan."""
        first = build_provider_query("Dubai", "hospital", "Remedy 5")
        assert first == "List hospital providers in Dubai for Remedy 5"
        # Operator clicks Labs chip — city and plan unchanged
        second = build_provider_query("Dubai", "lab", "Remedy 5")
        assert second == "List lab providers in Dubai for Remedy 5"

    def test_plan_persistence_remedy5_to_classic1(self):
        """Switching plan keeps last city and type."""
        first = build_provider_query("Dubai", "hospital", "Remedy 5")
        assert first == "List hospital providers in Dubai for Remedy 5"
        # Operator clicks Classic 1 plan chip — city and type unchanged
        second = build_provider_query("Dubai", "hospital", "Classic 1")
        assert second == "List hospital providers in Dubai for Classic 1"

    def test_all_quick_plan_filters_produce_valid_queries(self):
        """All four quick plan filter buttons (Part C) produce valid queries."""
        quick_plans = ["Remedy 5", "Remedy 6", "Classic 1", "Prime 1"]
        for plan in quick_plans:
            q = build_provider_query("Dubai", "hospital", plan)
            assert q.startswith("List hospital providers in Dubai for ")
            assert plan in q

    def test_all_quick_city_filters_produce_valid_queries(self):
        """All three quick city filter buttons (Part B) produce valid queries."""
        quick_cities = ["Dubai", "Sharjah", "Abu Dhabi"]
        for city in quick_cities:
            q = build_provider_query(city, "hospital", "Remedy 5")
            assert q.startswith("List hospital providers in ")
            assert city in q

    def test_all_provider_type_filters_produce_valid_queries(self):
        """All four provider-type chips (Part A) produce valid queries."""
        quick_types = ["hospital", "clinic", "pharmacy", "lab"]
        for ptype in quick_types:
            q = build_provider_query("Dubai", ptype, "Remedy 5")
            assert f"List {ptype} providers in Dubai for Remedy 5" == q


# ---------------------------------------------------------------------------
# Missing-parameter guard — no hallucinated defaults
# ---------------------------------------------------------------------------

class TestMissingParameterGuard:
    def test_missing_city_returns_empty(self):
        assert build_provider_query("", "hospital", "Remedy 5") == ""

    def test_missing_type_returns_empty(self):
        assert build_provider_query("Dubai", "", "Remedy 5") == ""

    def test_missing_plan_returns_empty(self):
        assert build_provider_query("Dubai", "hospital", "") == ""

    def test_all_missing_returns_empty(self):
        assert build_provider_query("", "", "") == ""


# ---------------------------------------------------------------------------
# Backend routing unchanged for UI-constructed queries
# ---------------------------------------------------------------------------

class TestBackendRoutingPreserved:
    def test_hospital_dubai_remedy5_routes_to_city_type(self):
        result = run_agent_wrapper("List hospital providers in Dubai for Remedy 5")
        assert result.get("intent") == "plan_network_city_type"
        assert result.get("ok") is True

    def test_lab_sharjah_remedy6_routes_to_city_type(self):
        result = run_agent_wrapper("List lab providers in Sharjah for Remedy 6")
        assert result.get("intent") == "plan_network_city_type"
        assert result.get("ok") is True

    def test_pharmacy_abudhabi_classic1_routes_to_city_type(self):
        result = run_agent_wrapper("List pharmacy providers in Abu Dhabi for Classic 1")
        assert result.get("intent") == "plan_network_city_type"
        assert result.get("ok") is True

    def test_clinic_dubai_remedy5_routes_to_city_type(self):
        result = run_agent_wrapper("List clinic providers in Dubai for Remedy 5")
        assert result.get("intent") == "plan_network_city_type"
        assert result.get("ok") is True


# ---------------------------------------------------------------------------
# Unsupported query preservation unchanged
# ---------------------------------------------------------------------------

class TestUnsupportedPreservation:
    def test_empty_query_is_unsupported(self):
        result = run_agent_wrapper("")
        assert result.get("ok") is False

    def test_recommendation_style_still_blocked(self):
        result = run_agent_wrapper("Which plan is best for my family?")
        assert result.get("ok") is False

    def test_planless_provider_listing_does_not_auto_guess_plan(self):
        """A planless listing query must NOT route to plan_network_city_type with ok=True."""
        result = run_agent_wrapper("List hospital providers in Dubai")
        # May be unsupported or route differently, but must NOT succeed as plan_network_city_type
        is_plan_routed_ok = (
            result.get("intent") == "plan_network_city_type" and result.get("ok") is True
        )
        assert not is_plan_routed_ok, (
            "Planless provider query should not route successfully to plan_network_city_type"
        )
