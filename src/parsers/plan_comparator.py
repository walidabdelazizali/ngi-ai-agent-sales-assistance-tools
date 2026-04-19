"""Deterministic comparison helper for parsed Remedy plans.

Compares two parsed plan dicts field-by-field using canonical schema fields.
Produces a simple data-driven diff showing which fields match, differ, or
are missing in either plan.

NOT a provider-level network intelligence engine.
"""

from __future__ import annotations

from typing import Any

from src.parsers.canonical_schema import BUSINESS_FIELDS


def compare_plans(plan_a: dict[str, Any],
                  plan_b: dict[str, Any]) -> dict[str, Any]:
    """Compare two parsed plan dicts by canonical business fields.

    Parameters
    ----------
    plan_a, plan_b : dict
        Output from ``parse_remedy_plan()``.

    Returns
    -------
    dict with keys:
        - plan_a_code: str | None
        - plan_b_code: str | None
        - matched: list of field names where values are identical
        - differing: dict of {field: {plan_a: val, plan_b: val}}
        - missing_in_a: list of fields absent from plan_a
        - missing_in_b: list of fields absent from plan_b
    """
    result: dict[str, Any] = {
        "plan_a_code": plan_a.get("plan_code"),
        "plan_b_code": plan_b.get("plan_code"),
        "matched": [],
        "differing": {},
        "missing_in_a": [],
        "missing_in_b": [],
    }

    for field in BUSINESS_FIELDS:
        in_a = field in plan_a
        in_b = field in plan_b

        if not in_a and not in_b:
            continue
        if not in_a:
            result["missing_in_a"].append(field)
            continue
        if not in_b:
            result["missing_in_b"].append(field)
            continue

        val_a = plan_a[field]
        val_b = plan_b[field]

        if val_a == val_b:
            result["matched"].append(field)
        else:
            result["differing"][field] = {
                "plan_a": val_a,
                "plan_b": val_b,
            }

    return result
