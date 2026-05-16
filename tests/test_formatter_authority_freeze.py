import inspect
import warnings

import src.output as output_authority
import src.output_packaging as legacy_output_packaging


APPROVED_PLAN_CORE = {
    "ok": True,
    "intent": "plan_core",
    "plan_name": "Remedy 05",
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
}


def test_authority_module_has_no_legacy_import_dependency():
    source = inspect.getsource(output_authority)
    assert "src.output_packaging" not in source


def test_legacy_dispatcher_forwards_to_authority(monkeypatch):
    captured = {}

    def _fake_format_output(agent_response, mode, *, recipient_name=None, benefit_key=None):
        captured["mode"] = mode
        captured["recipient_name"] = recipient_name
        captured["benefit_key"] = benefit_key
        return "delegated"

    monkeypatch.setattr(output_authority, "format_output", _fake_format_output)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        out = legacy_output_packaging.format_output(
            APPROVED_PLAN_CORE,
            "email_summary",
            recipient_name="Sara",
        )

    assert out == "delegated"
    assert captured["mode"] == "email_summary"
    assert captured["recipient_name"] == "Sara"


def test_legacy_entrypoints_match_centralized_behavior():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        legacy_email = legacy_output_packaging.email_summary(APPROVED_PLAN_CORE, recipient_name="Sara")
        legacy_benefit = legacy_output_packaging.benefit_explanation(APPROVED_PLAN_CORE, "annual_limit")
        legacy_whatsapp = legacy_output_packaging.whatsapp_summary(APPROVED_PLAN_CORE)

    authority_email = output_authority.format_output(
        APPROVED_PLAN_CORE,
        "email_summary",
        recipient_name="Sara",
    )
    authority_benefit = output_authority.format_output(
        APPROVED_PLAN_CORE,
        "benefit_explanation",
        benefit_key="annual_limit",
    )
    authority_whatsapp = output_authority.format_output(APPROVED_PLAN_CORE, "whatsapp_summary")

    assert legacy_email == authority_email
    assert legacy_benefit == authority_benefit
    assert legacy_whatsapp == authority_whatsapp
