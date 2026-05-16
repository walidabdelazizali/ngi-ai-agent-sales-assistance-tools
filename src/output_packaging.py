"""
output_packaging.py - Deprecated compatibility shim.

Production formatter authority is src/output. This module remains only to keep
legacy imports stable and forwards all execution to the centralized authority.
"""

from __future__ import annotations

from typing import Optional
from warnings import warn

from src.output.legacy_modes import benefit_explanation as _authority_benefit_explanation
from src.output.legacy_modes import email_summary as _authority_email_summary
from src.output.shared_helpers import _MISSING, _SAFE_REFUSAL
from src.output.whatsapp_formatter import whatsapp_summary as _authority_whatsapp_summary


SUPPORTED_MODES = frozenset({"whatsapp_summary", "email_summary", "benefit_explanation"})


def _warn_deprecated() -> None:
    warn(
        "src.output_packaging is deprecated. Use src.output formatters instead.",
        DeprecationWarning,
        stacklevel=2,
    )


def whatsapp_summary(agent_response: dict) -> str:
    _warn_deprecated()
    return _authority_whatsapp_summary(agent_response)


def email_summary(agent_response: dict, recipient_name: Optional[str] = None) -> str:
    _warn_deprecated()
    return _authority_email_summary(agent_response, recipient_name=recipient_name)


def benefit_explanation(agent_response: dict, benefit_key: str) -> str:
    _warn_deprecated()
    return _authority_benefit_explanation(agent_response, benefit_key)


def format_output(
    agent_response: dict,
    mode: str,
    *,
    recipient_name: Optional[str] = None,
    benefit_key: Optional[str] = None,
) -> str:
    """Forward legacy dispatcher calls to src/output authority."""
    _warn_deprecated()

    from src import output as output_authority

    inferred_benefit_key = benefit_key
    if (mode or "").strip().lower() == "benefit_explanation" and not inferred_benefit_key:
        data = agent_response.get("data") or {}
        if isinstance(data, dict):
            inferred_benefit_key = data.get("field") or data.get("label")

    return output_authority.format_output(
        agent_response,
        mode,
        recipient_name=recipient_name,
        benefit_key=inferred_benefit_key,
    )
