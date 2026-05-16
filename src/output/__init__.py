"""
src/output/__init__.py — Unified export/output formatting layer.

Central dispatcher for all output modes:
- whatsapp_summary
- arabic_summary
- compact_summary
- comparison_summary
- email_summary (legacy from output_packaging)
- benefit_explanation (legacy from output_packaging)

All formatters are deterministic, safe-fallback enabled, and operationally hardened.
"""

from typing import Any, Optional, Union

from src.output.shared_helpers import (
    _SAFE_REFUSAL,
    assert_approved,
    detect_language,
)
from src.output.whatsapp_formatter import whatsapp_summary
from src.output.arabic_formatter import (
    arabic_plan_summary,
    arabic_reimbursement_summary,
    arabic_comparison_summary,
)
from src.output.compact_formatter import compact_summary
from src.output.comparison_formatter import english_comparison_summary, comparison_summary

# Re-export legacy formatters from original output_packaging
from src.output_packaging import (
    email_summary,
    benefit_explanation,
    _SAFE_REFUSAL as LEGACY_SAFE_REFUSAL,
)


# Supported output modes
SUPPORTED_MODES = frozenset({
    "whatsapp_summary",
    "arabic_summary",
    "compact_summary",
    "comparison_summary",
    "email_summary",
    "benefit_explanation",
})


def format_output(
    agent_response: dict,
    mode: str,
    *,
    recipient_name: Optional[str] = None,
    benefit_key: Optional[str] = None,
) -> str:
    """
    Unified entry point for all output formatting modes.
    
    Parameters
    ----------
    agent_response : dict
        The dict returned by agent (must have ok=True and valid intent).
    mode : str
        One of: whatsapp_summary, arabic_summary, compact_summary, 
        comparison_summary, email_summary, benefit_explanation.
    recipient_name : str | None
        Optional name for email greeting.
    benefit_key : str | None
        Required when mode='benefit_explanation'.
    
    Returns
    -------
    str
        Formatted output. Never raises; returns safe refusal on error.
    """
    m = (mode or "").strip().lower()
    
    # Validate mode
    if m not in SUPPORTED_MODES:
        return (
            f"Output mode '{mode}' is not supported. "
            f"Supported modes: {', '.join(sorted(SUPPORTED_MODES))}."
        )
    
    try:
        # Route to appropriate formatter
        if m == "whatsapp_summary":
            return whatsapp_summary(agent_response)
        
        elif m == "arabic_summary":
            return format_arabic_summary(agent_response)
        
        elif m == "compact_summary":
            return compact_summary(agent_response)
        
        elif m == "comparison_summary":
            return format_comparison_summary(agent_response)
        
        elif m == "email_summary":
            return email_summary(agent_response, recipient_name=recipient_name)
        
        elif m == "benefit_explanation":
            return benefit_explanation(agent_response, benefit_key=benefit_key or "")
    
    except Exception:
        # All formatters should handle errors internally, but catch any
        # unexpected exceptions to ensure safe fallback
        return _SAFE_REFUSAL
    
    return _SAFE_REFUSAL


def format_arabic_summary(agent_response: dict) -> str:
    """
    Format response in Arabic based on intent.
    
    Routes to appropriate Arabic formatter.
    """
    try:
        intent = agent_response.get("intent", "")
        
        if intent == "plan_comparison":
            # For comparison, need to extract message and plan names
            msg = agent_response.get("message", "")
            data = agent_response.get("data", {})
            plan1 = data.get("plan_a_name", "") or agent_response.get("plan_name", "")
            plan2 = data.get("plan_b_name", "")
            
            if msg and plan1 and plan2:
                return arabic_comparison_summary(msg, plan1, plan2)
            else:
                return _SAFE_REFUSAL
        
        elif intent == "reimbursement_rules":
            return arabic_reimbursement_summary(agent_response)
        
        elif intent in {"plan_core", "plan_summary", "plan_field"}:
            return arabic_plan_summary(agent_response)
        
        else:
            return _SAFE_REFUSAL
    
    except Exception:
        return _SAFE_REFUSAL


def format_comparison_summary(agent_response: dict) -> str:
    """
    Format comparison response with proper cleaning and normalization.
    
    Detects language from original query if present.
    """
    try:
        msg = agent_response.get("message", "")
        if not msg:
            return _SAFE_REFUSAL
        
        # Try to detect language from user query
        user_query = agent_response.get("user_query") or agent_response.get("_user_query", "")
        language = detect_language(user_query) if user_query else "en"
        
        return comparison_summary(msg, language=language)
    
    except Exception:
        return _SAFE_REFUSAL
