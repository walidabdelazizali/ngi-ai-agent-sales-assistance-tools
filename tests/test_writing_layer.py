"""
tests/test_writing_layer.py — Controlled AI writing layer safety tests.

Validates src/output_packaging.py (whatsapp_summary, email_summary,
benefit_explanation, format_output). All tests are offline/deterministic
(no plan file I/O) — fixtures simulate approved agent responses.

Safety coverage:
    - ok=False always returns safe refusal
    - Unsupported intent always returns safe refusal
    - No hallucinated facts
    - No pricing invented
    - No unsupported recommendations
    - No internal/source_trace field leakage
    - Graceful fallback when facts are missing
    - All three modes produce valid non-empty strings for approved inputs
"""

import pytest
from src.output_packaging import (
    whatsapp_summary,
    email_summary,
    benefit_explanation,
    format_output,
    SUPPORTED_MODES,
    _MISSING,
    _SAFE_REFUSAL,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

APPROVED_PLAN_CORE = {
    "ok": True,
    "intent": "plan_core",
    "plan_name": "Remedy 05",
    "tool_name": "get_plan_core",
    "data": {
        "plan_name": "Remedy 05",
        "plan_code": "HN-REMEDY-05",
        "network_name": "Remedy Network 05",
        "annual_limit": "AED 1,000,000",
        "area_of_coverage": "UAE",
        "direct_billing": True,
        "referral_required": False,
        "maternity_cover": "AED 10,000 per confinement",
    },
    "message": "Plan: Remedy 05\nAnnual limit: AED 1,000,000",
    "normalized": {"status": "ok", "tool": "get_plan_core", "answer": {}, "errors": []},
}

APPROVED_PLAN_SUMMARY = {
    "ok": True,
    "intent": "plan_summary",
    "plan_name": "Classic 1R",
    "tool_name": "get_plan_summary",
    "data": {
        "plan_name": "Classic 1R",
        "plan_code": "HN-CLASSIC-1R",
        "network_name": "Classic Network 1R",
        "annual_limit": "AED 500,000",
        "area_of_coverage": "UAE",
        "direct_billing": True,
        "referral_required": False,
        "pharmacy_cover_summary": "20% copay, max AED 1,500 per year",
        "dental_cover_summary": "Not covered",
        "mental_health_cover_summary": "AED 5,000 per year",
    },
    "message": "Classic 1R summary",
    "normalized": {"status": "ok", "tool": "get_plan_summary", "answer": {}, "errors": []},
}

APPROVED_PLAN_FIELD = {
    "ok": True,
    "intent": "plan_field",
    "plan_name": "Remedy 05",
    "tool_name": "get_plan_field",
    "data": {
        "plan_name": "Remedy 05",
        "field": "annual_limit",
        "label": "Annual Limit",
        "value": "AED 1,000,000",
        "formatted": "AED 1,000,000",
    },
    "message": "Annual Limit: AED 1,000,000",
    "normalized": {"status": "ok", "tool": "get_plan_field", "answer": {}, "errors": []},
}

FAILED_RESPONSE = {
    "ok": False,
    "intent": "unsupported",
    "plan_name": None,
    "tool_name": None,
    "data": None,
    "message": "Sorry, this query is not supported.",
    "normalized": {"status": "not_found", "tool": None, "answer": None, "errors": []},
}

UNSUPPORTED_INTENT_RESPONSE = {
    "ok": True,
    "intent": "network_lookup",
    "plan_name": None,
    "tool_name": "network_lookup",
    "data": {"result": "Provider found in Remedy 05"},
    "message": "Provider found",
    "normalized": {"status": "ok", "tool": "network_lookup", "answer": {}, "errors": []},
}


# ---------------------------------------------------------------------------
# SAFETY: ok=False always returns safe refusal
# ---------------------------------------------------------------------------

class TestSafeRefusalOnFailure:

    def test_whatsapp_ok_false_returns_refusal(self):
        assert whatsapp_summary(FAILED_RESPONSE) == _SAFE_REFUSAL

    def test_email_ok_false_returns_refusal(self):
        assert email_summary(FAILED_RESPONSE) == _SAFE_REFUSAL

    def test_benefit_ok_false_returns_refusal(self):
        assert benefit_explanation(FAILED_RESPONSE, "annual_limit") == _SAFE_REFUSAL

    def test_format_output_ok_false_returns_refusal(self):
        assert format_output(FAILED_RESPONSE, "whatsapp_summary") == _SAFE_REFUSAL


# ---------------------------------------------------------------------------
# SAFETY: Unsupported intent always returns safe refusal
# ---------------------------------------------------------------------------

class TestSafeRefusalOnUnsupportedIntent:

    def test_whatsapp_unsupported_intent(self):
        assert whatsapp_summary(UNSUPPORTED_INTENT_RESPONSE) == _SAFE_REFUSAL

    def test_email_unsupported_intent(self):
        assert email_summary(UNSUPPORTED_INTENT_RESPONSE) == _SAFE_REFUSAL

    def test_benefit_unsupported_intent(self):
        assert benefit_explanation(UNSUPPORTED_INTENT_RESPONSE, "annual_limit") == _SAFE_REFUSAL


# ---------------------------------------------------------------------------
# SAFETY: No internal field leakage
# ---------------------------------------------------------------------------

class TestNoInternalLeakage:

    _BLOCKED = ("source_trace", "debug_value", "unapproved_fact")

    def _base_with_poison(self):
        return {
            **APPROVED_PLAN_CORE,
            "data": {
                **APPROVED_PLAN_CORE["data"],
                "source_trace": "trace_xyz",
                "debug": "debug_value",
                "unapproved": "unapproved_fact",
            },
        }

    def test_whatsapp_blocks_internal_fields(self):
        result = whatsapp_summary(self._base_with_poison())
        assert "trace_xyz" not in result
        assert "debug_value" not in result
        assert "unapproved_fact" not in result

    def test_email_blocks_internal_fields(self):
        result = email_summary(self._base_with_poison())
        assert "trace_xyz" not in result

    def test_benefit_blocks_review_tagged_value(self):
        response = {
            **APPROVED_PLAN_CORE,
            "data": {**APPROVED_PLAN_CORE["data"], "annual_limit": "REVIEW:internal_check"},
        }
        result = benefit_explanation(response, "annual_limit")
        assert "REVIEW:internal_check" not in result

    def test_whatsapp_contains_only_whitelisted_facts(self):
        """Data values from the fixture must appear; invented values must not."""
        result = whatsapp_summary(APPROVED_PLAN_CORE)
        assert "AED 1,000,000" in result          # from fixture
        assert "AED 99,000,000" not in result     # invented


# ---------------------------------------------------------------------------
# SAFETY: No unsupported recommendations
# ---------------------------------------------------------------------------

class TestNoUnsupportedRecommendations:

    _TRIGGERS = ("we recommend", "you should buy", "best plan", "better than", "upgrade to")

    def _has_rec(self, text):
        tl = text.lower()
        return any(t in tl for t in self._TRIGGERS)

    def test_whatsapp_no_recommendations(self):
        assert not self._has_rec(whatsapp_summary(APPROVED_PLAN_CORE))

    def test_email_no_recommendations(self):
        assert not self._has_rec(email_summary(APPROVED_PLAN_CORE))

    def test_benefit_no_recommendations(self):
        assert not self._has_rec(benefit_explanation(APPROVED_PLAN_CORE, "annual_limit"))


# ---------------------------------------------------------------------------
# SAFETY: Graceful fallback when facts are missing
# ---------------------------------------------------------------------------

class TestGracefulFallback:

    _MINIMAL = {
        "ok": True,
        "intent": "plan_core",
        "plan_name": "Stub Plan",
        "tool_name": "get_plan_core",
        "data": {"plan_name": "Stub Plan"},
        "message": "Stub",
        "normalized": {},
    }

    def test_whatsapp_minimal_data_non_empty(self):
        result = whatsapp_summary(self._MINIMAL)
        assert isinstance(result, str) and len(result) > 0
        assert "Stub Plan" in result

    def test_email_minimal_data_non_empty(self):
        result = email_summary(self._MINIMAL)
        assert isinstance(result, str) and len(result) > 0
        assert "Stub Plan" in result

    def test_benefit_missing_field_descriptive_not_refusal(self):
        """When a benefit field is absent, return a descriptive message — not the safe refusal."""
        result = benefit_explanation(self._MINIMAL, "maternity")
        assert isinstance(result, str) and len(result) > 0
        assert result != _SAFE_REFUSAL

    def test_whatsapp_none_fields_not_rendered(self):
        response = {
            "ok": True,
            "intent": "plan_core",
            "plan_name": "Remedy 05",
            "tool_name": "get_plan_core",
            "data": {"plan_name": "Remedy 05", "annual_limit": None, "network_name": None},
            "message": "",
            "normalized": {},
        }
        result = whatsapp_summary(response)
        assert "None" not in result
        assert _MISSING not in result  # _MISSING is omitted, not displayed


# ---------------------------------------------------------------------------
# POSITIVE: All three modes produce valid non-empty strings for supported plans
# ---------------------------------------------------------------------------

class TestPositiveOutputModes:

    def test_whatsapp_remedy05_contains_plan_and_limit(self):
        result = whatsapp_summary(APPROVED_PLAN_CORE)
        assert "Remedy 05" in result
        assert "AED 1,000,000" in result

    def test_whatsapp_remedy05_direct_billing_yes(self):
        result = whatsapp_summary(APPROVED_PLAN_CORE)
        assert "Direct Billing: Yes" in result

    def test_whatsapp_remedy05_referral_no(self):
        result = whatsapp_summary(APPROVED_PLAN_CORE)
        assert "Referral Required: No" in result

    def test_whatsapp_classic1r_pharmacy_shown(self):
        result = whatsapp_summary(APPROVED_PLAN_SUMMARY)
        assert "20% copay" in result

    def test_email_remedy05_contains_key_fields(self):
        result = email_summary(APPROVED_PLAN_CORE)
        assert "Remedy 05" in result
        assert "AED 1,000,000" in result
        assert "NGI Health Insurance Team" in result

    def test_email_with_recipient_name(self):
        result = email_summary(APPROVED_PLAN_CORE, recipient_name="Ahmad")
        assert "Dear Ahmad," in result

    def test_email_no_recipient_uses_default_greeting(self):
        result = email_summary(APPROVED_PLAN_CORE)
        assert "Dear Valued Client," in result

    def test_email_closing_disclaimer_present(self):
        result = email_summary(APPROVED_PLAN_CORE)
        assert "official policy document" in result

    def test_benefit_annual_limit_contains_value(self):
        result = benefit_explanation(APPROVED_PLAN_CORE, "annual_limit")
        assert "AED 1,000,000" in result

    def test_benefit_maternity_contains_value(self):
        result = benefit_explanation(APPROVED_PLAN_CORE, "maternity")
        assert "AED 10,000" in result

    def test_benefit_network_contains_network_name(self):
        result = benefit_explanation(APPROVED_PLAN_SUMMARY, "network")
        assert "Classic Network 1R" in result

    def test_benefit_pharmacy_contains_value(self):
        result = benefit_explanation(APPROVED_PLAN_SUMMARY, "pharmacy")
        assert "20% copay" in result

    def test_benefit_from_plan_field_response(self):
        """plan_field data payload (label/value/formatted) works for benefit_explanation."""
        result = benefit_explanation(APPROVED_PLAN_FIELD, "annual_limit")
        assert "AED 1,000,000" in result


# ---------------------------------------------------------------------------
# format_output dispatcher
# ---------------------------------------------------------------------------

class TestFormatOutputDispatcher:

    def test_whatsapp_mode_dispatches_correctly(self):
        result = format_output(APPROVED_PLAN_CORE, "whatsapp_summary")
        assert "Remedy 05" in result

    def test_email_mode_dispatches_with_recipient(self):
        result = format_output(APPROVED_PLAN_CORE, "email_summary", recipient_name="Sara")
        assert "Dear Sara," in result

    def test_benefit_mode_dispatches_with_key(self):
        result = format_output(APPROVED_PLAN_CORE, "benefit_explanation", benefit_key="annual_limit")
        assert "AED 1,000,000" in result

    def test_invalid_mode_returns_informative_error(self):
        result = format_output(APPROVED_PLAN_CORE, "json_export")
        assert "json_export" in result
        assert "not supported" in result.lower()

    def test_invalid_benefit_key_returns_informative_error(self):
        result = format_output(APPROVED_PLAN_CORE, "benefit_explanation", benefit_key="invalid_key")
        assert "not supported" in result.lower()

    def test_supported_modes_constant_has_all_three(self):
        assert "whatsapp_summary" in SUPPORTED_MODES
        assert "email_summary" in SUPPORTED_MODES
        assert "benefit_explanation" in SUPPORTED_MODES
