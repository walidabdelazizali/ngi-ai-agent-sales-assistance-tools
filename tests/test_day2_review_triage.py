"""
Day 2 — REVIEW Friction Triage regression tests.

Covers the 3 REVIEW cases that received deterministic patches and
the 3 cases intentionally deferred (confirmed safe behavior).
"""

import pytest
from src.agent_wrapper import run_agent_wrapper


# --- Fixed cases ---

def test_nmc_royal_hospital_dxb_remedy5_resolves():
    """Case 3: 'Provider NMC ROYAL HOSPITAL DXB in Remedy 5 network?' — alias now resolves to
    NMC ROYAL HOSPITAL LLC(DXB), which is in Remedy 05's network (hn_basic_plus). Expect ok=True."""
    out = run_agent_wrapper("Provider NMC ROYAL HOSPITAL DXB in Remedy 5 network?")
    assert out.get("intent") == "plan_network_provider"
    assert out.get("ok") is True, f"Expected ok=True, got: {out.get('message')}"
    assert "NMC" in (out.get("message") or "").upper()


def test_accuracy_plus_arabic_mixed_remedy5_routes_membership():
    """Case 6: 'ACCURACY PLUS في شبكة Remedy 05؟' — new mixed Arabic membership pattern routes
    to plan_network_provider and alias resolves ACCURACY PLUS → ACCURACY PLUS MEDICAL LABORATORY."""
    out = run_agent_wrapper("ACCURACY PLUS في شبكة Remedy 05؟")
    assert out.get("intent") == "plan_network_provider", (
        f"Expected plan_network_provider, got: {out.get('intent')}"
    )
    assert out.get("ok") is True, f"Expected ok=True, got: {out.get('message')}"
    assert "ACCURACY PLUS" in (out.get("message") or "").upper()


def test_dental_clinics_listing_blocked():
    """Case 5: 'dental clinics Remedy 6 Sharjah' — dental is an unsupported type modifier.
    Must NOT return a generic clinic list. Expect unsupported/ok=False."""
    out = run_agent_wrapper("dental clinics Remedy 6 Sharjah")
    assert out.get("ok") is False, (
        f"Expected ok=False (unsupported dental type), got ok=True with: {out.get('message','')[:120]}"
    )


# --- Deferred cases (confirming safe behavior unchanged) ---

def test_aster_hospital_remedy5_remains_ambiguous():
    """Case 1 (deferred): 'Is ASTER HOSPITAL in Remedy 5 network?' — ASTER HOSPITAL maps to 2
    distinct providers (Mankhool + Sonapur). Must remain ambiguous, not pick one silently."""
    out = run_agent_wrapper("Is ASTER HOSPITAL in Remedy 5 network?")
    assert out.get("intent") == "plan_network_provider"
    assert out.get("ok") is False
    msg = (out.get("message") or "").lower()
    assert "ambiguous" in msg or "غامض" in msg, f"Expected ambiguous message, got: {msg}"


def test_aster_hospital_arabic_remedy5_remains_ambiguous():
    """Case 4 (deferred): 'هل ASTER HOSPITAL في شبكة Remedy 05؟' — same root as Case 1."""
    out = run_agent_wrapper("هل ASTER HOSPITAL في شبكة Remedy 05؟")
    assert out.get("intent") == "plan_network_provider"
    assert out.get("ok") is False
    msg = (out.get("message") or "").lower()
    assert "ambiguous" in msg or "غامض" in msg, f"Expected ambiguous message, got: {msg}"


def test_24hour_pharmacy_remedy6_remains_not_found():
    """Case 2 (deferred): 'Is 24HOUR PHARMACY in Remedy 6 network?' — 2 different 24HOUR PHARMACY
    entities (DXB + SHJ), cannot safely disambiguate without city. Expect ok=False."""
    out = run_agent_wrapper("Is 24HOUR PHARMACY in Remedy 6 network?")
    assert out.get("intent") == "plan_network_provider"
    assert out.get("ok") is False
