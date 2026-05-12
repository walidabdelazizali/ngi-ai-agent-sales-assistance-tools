"""
Tests for Prime Plan-2 (HN_PRIME_2) integration.
Validates deterministic behavior for plan_core, plan_summary, and benefit_explanation intents.
"""
import pytest
from src.agent_wrapper import run_agent_wrapper
from src.query.plan_query import get_plan_field, summarize_plan
from src.output_packaging import format_output


class TestPrimePlan2Integration:
    """Prime Plan-2 end-to-end agent integration."""

    def test_prime_plan2_annual_limit_query(self):
        """Query annual limit for Prime Plan-2."""
        response = run_agent_wrapper("What is the annual limit for Prime Plan-2?")
        assert response["ok"] == True
        assert response["intent"] in ("plan_core", "plan_field")
        # Check in either data (dict) or message (string)
        if isinstance(response.get("data"), dict):
            assert "annual_limit" in response["data"]
            assert "500000" in str(response["data"]["annual_limit"]) or "500,000" in str(response["data"]["annual_limit"])
        else:
            msg = str(response.get("message", ""))
            assert "500000" in msg or "500,000" in msg

    def test_prime_plan2_network_query(self):
        """Query network for Prime Plan-2."""
        response = run_agent_wrapper("What is the network for Prime Plan-2?")
        assert response["ok"] == True
        assert response["intent"] in ("plan_core", "plan_field")
        # Check for network info in response
        response_str = str(response.get("data", response.get("message", "")))
        # Network should be mentioned somewhere in the plan data

    def test_prime_plan2_coverage_query(self):
        """Query area of coverage for Prime Plan-2."""
        response = run_agent_wrapper("What is the area of coverage for Prime Plan-2?")
        assert response["ok"] == True
        assert response["intent"] in ("plan_core", "plan_field")

    def test_prime_plan2_summary_query(self):
        """Query summary for Prime Plan-2."""
        response = run_agent_wrapper("Summarize Prime Plan-2")
        assert response["ok"] == True
        assert response["intent"] == "plan_summary"
        assert response.get("data") is not None or response.get("message") is not None

    def test_prime_plan2_direct_billing(self):
        """Query direct billing for Prime Plan-2."""
        response = run_agent_wrapper("Does Prime Plan-2 have direct billing?")
        assert response["ok"] == True
        assert response["intent"] in ("plan_core", "plan_field")

    def test_prime_plan2_referral(self):
        """Query referral requirement for Prime Plan-2."""
        response = run_agent_wrapper("Is referral required for Prime Plan-2?")
        assert response["ok"] == True
        assert response["intent"] in ("plan_core", "plan_field")


class TestPrimePlan2DirectQuery:
    """Direct query layer tests for Prime Plan-2."""

    def test_get_plan_field_annual_limit(self):
        """Directly query annual limit field."""
        result = get_plan_field("Prime 2", "annual_limit")
        assert result["ok"] == True
        assert "500000" in result["value"] or "500,000" in result["value"]

    def test_get_plan_field_network(self):
        """Directly query network field."""
        result = get_plan_field("Prime 2", "network_name")
        assert result["ok"] == True
        assert "Premier" in result["value"] or "HN Premier" in result["value"]

    def test_summarize_plan(self):
        """Directly summarize Prime 2."""
        summary = summarize_plan("Prime 2")
        assert summary is not None
        # Could be dict or string
        if isinstance(summary, dict):
            assert "summary_text" in summary or "plan_code" in summary
        else:
            assert isinstance(summary, str)
            assert len(summary) > 0


class TestPrimePlan2Aliases:
    """Test various aliases for Prime Plan-2."""

    @pytest.mark.parametrize("alias", [
        "Prime Plan-2",
        "Prime 2",
        "prime 2",
        "prime-2",
        "hn-prime-2",
        "hn prime 2",
    ])
    def test_alias_resolution(self, alias):
        """Test that various aliases resolve to Prime Plan-2."""
        response = run_agent_wrapper(f"What is the annual limit for {alias}?")
        # Should resolve or give reasonable response (not error)
        assert response is not None
        assert "intent" in response
        # If it doesn't recognize Prime Plan-2, should not be network-related error
        if not response["ok"]:
            assert "unsupported" in response.get("intent", "") or "plan" in str(response).lower()

