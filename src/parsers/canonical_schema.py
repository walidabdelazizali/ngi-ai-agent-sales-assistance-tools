"""Canonical shared schema for structured Remedy plan output.

This module defines the frozen field contract that all parsed Remedy plans
must conform to. It is the single source of truth for field names, types,
and groupings across Remedy 02, Remedy 03, and any future plan variants.

Design rules
------------
* All fields are optional at the value level (None / [] is valid).
* The *set of keys* is mandatory — every parsed plan dict must contain
  exactly these keys (plus ``raw_section_map`` for internal use).
* No provider-level network intelligence is encoded here — only
  capture/preparation fields.
"""

from __future__ import annotations

CANONICAL_SCHEMA_VERSION = "1.0"

# ---------------------------------------------------------------------------
# Field definitions grouped by domain
# ---------------------------------------------------------------------------

IDENTITY_FIELDS: dict[str, type] = {
    "plan_name": (str, type(None)),
    "plan_code": (str, type(None)),
    "insurer_name": (str, type(None)),
    "network_name": (str, type(None)),
}

COVERAGE_CORE_FIELDS: dict[str, type] = {
    "area_of_coverage": (str, type(None)),
    "annual_limit": (str, type(None)),
    "direct_billing": (bool, type(None)),
    "reimbursement_allowed": (bool, type(None)),
    "referral_required": (bool, type(None)),
}

BENEFIT_SUMMARY_FIELDS: dict[str, type] = {
    "maternity_cover": (str, type(None)),
    "inpatient_cover_summary": (str, type(None)),
    "outpatient_cover_summary": (str, type(None)),
    "pharmacy_cover_summary": (str, type(None)),
    "diagnostics_cover_summary": (str, type(None)),
    "physiotherapy_cover_summary": (str, type(None)),
}

RULES_FIELDS: dict[str, type] = {
    "pre_existing_condition_rule": (str, type(None)),
    "chronic_condition_rule": (str, type(None)),
    "outside_network_rule": (str, type(None)),
    "outside_uae_rule": (str, type(None)),
    "approval_rule_summary": (str, type(None)),
}

EXCLUSIONS_FIELDS: dict[str, type] = {
    "key_exclusions": (list,),
}

# Network preparation fields — capture only, NOT provider intelligence.
NETWORK_PREP_FIELDS: dict[str, type] = {
    "network_access_notes": (str, type(None)),
    "clinic_only_flag": (bool, type(None)),
    "hospital_access_notes": (str, type(None)),
    "direct_access_hospitals_raw": (list,),
    "direct_billing_notes": (str, type(None)),
    "referral_behavior_notes": (str, type(None)),
}

# Internal/meta fields (not part of the business contract but always present)
INTERNAL_FIELDS: dict[str, type] = {
    "raw_section_map": (dict,),
}

# ---------------------------------------------------------------------------
# Composite: all canonical fields in order
# ---------------------------------------------------------------------------

CANONICAL_FIELDS: tuple[str, ...] = (
    # Identity
    "plan_name",
    "plan_code",
    "insurer_name",
    "network_name",
    # Coverage core
    "area_of_coverage",
    "annual_limit",
    "direct_billing",
    "reimbursement_allowed",
    "reimbursement_scope",
    "outside_network_reimbursement",
    "outside_uae_reimbursement",
    "reimbursement_basis",
    "reimbursement_conditions",
    "reimbursement_documents_required",
    "referral_required",
    # Benefit summaries
    "maternity_cover",
    "inpatient_cover_summary",
    "outpatient_cover_summary",
    "pharmacy_cover_summary",
    "diagnostics_cover_summary",
    "physiotherapy_cover_summary",
    # Rules
    "pre_existing_condition_rule",
    "chronic_condition_rule",
    "outside_network_rule",
    "outside_uae_rule",
    "approval_rule_summary",
    # Exclusions
    "key_exclusions",
    # Network prep (capture only)
    "network_access_notes",
    "clinic_only_flag",
    "hospital_access_notes",
    "direct_access_hospitals_raw",
    "direct_billing_notes",
    "referral_behavior_notes",
    # Internal
    "raw_section_map",
)

# Business-facing fields (excludes internal/meta)
BUSINESS_FIELDS: tuple[str, ...] = tuple(
    f for f in CANONICAL_FIELDS if f != "raw_section_map"
)

# All field groups for programmatic access
ALL_FIELD_GROUPS = {
    "identity": IDENTITY_FIELDS,
    "coverage_core": COVERAGE_CORE_FIELDS,
    "benefit_summaries": BENEFIT_SUMMARY_FIELDS,
    "rules": RULES_FIELDS,
    "exclusions": EXCLUSIONS_FIELDS,
    "network_prep": NETWORK_PREP_FIELDS,
    "internal": INTERNAL_FIELDS,
}


# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------

def validate_canonical_shape(parsed: dict) -> list[str]:
    """Check that a parsed plan dict conforms to the canonical schema.

    Returns a list of error strings (empty means valid).
    """
    errors: list[str] = []

    # Check for missing fields
    for field in CANONICAL_FIELDS:
        if field not in parsed:
            errors.append(f"missing field: {field}")

    # Check for unexpected fields
    canonical_set = set(CANONICAL_FIELDS)
    for key in parsed:
        if key not in canonical_set:
            errors.append(f"unexpected field: {key}")

    # Type checks for list fields
    if "key_exclusions" in parsed:
        if not isinstance(parsed["key_exclusions"], list):
            errors.append("key_exclusions must be a list")
    if "direct_access_hospitals_raw" in parsed:
        if not isinstance(parsed["direct_access_hospitals_raw"], list):
            errors.append("direct_access_hospitals_raw must be a list")
    if "raw_section_map" in parsed:
        if not isinstance(parsed["raw_section_map"], dict):
            errors.append("raw_section_map must be a dict")

    return errors
