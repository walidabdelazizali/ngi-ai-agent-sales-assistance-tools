"""
Deterministic provider query builder.

Mirrors the JavaScript query construction in the UI (src/api/app.py providerForm submit).
Used by the UI rendering layer and the test suite; no inference, no fuzzy logic.
"""


def build_provider_query(
    city: str,
    provider_type: str,
    plan: str,
    area: str = "",
) -> str:
    """Return a deterministic provider search query string.

    Mirrors the JS logic:
        'List <type> providers in [<area> ]<city> for <plan>'

    Returns an empty string when any required parameter (city, provider_type,
    plan) is absent, so callers can gate submission on a non-empty result.
    """
    city = city.strip()
    provider_type = provider_type.strip().lower()
    plan = plan.strip()
    area = area.strip() if area else ""

    if not city or not provider_type or not plan:
        return ""

    if area:
        return f"List {provider_type} providers in {area} {city} for {plan}"
    return f"List {provider_type} providers in {city} for {plan}"
