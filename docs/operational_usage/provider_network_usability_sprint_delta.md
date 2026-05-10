# Provider/Network Usability Sprint Delta

## Scope
- Goal: improve deterministic routing for natural provider listing queries with plan + city + provider type.
- Constraint: no fuzzy matching, no guessing, no safety model expansion.
- Change size: minimal routing enhancement only.

## Change Implemented
- Extended [src/agent_wrapper.py](src/agent_wrapper.py) to detect Arabic provider-type words in the existing `plan_network_city_type` path.
- Extended the same path to map Arabic provider types to the existing deterministic listing tool inputs.
- Reused existing normalized query text for Arabic city extraction instead of adding a new routing surface.

## What Improved
- Arabic natural listing queries now route to `plan_network_city_type` instead of falling through to `unsupported`.
- English behavior remains unchanged for already-supported plan + city + type queries.
- Ambiguity-safe provider lookup behavior remains unchanged.

## CLI Evidence
1. Query: `مستشفيات Remedy 5 في دبي؟`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 05`
   - Message: `No matching providers found in HN Basic Plus network.`
2. Query: `عيادات Remedy 6 في الشارقة؟`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 06`
   - Message: `No matching providers found in HN Basic Plus network.`
3. Query: `hospitals in Remedy 5 in Dubai`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 05`
4. Query: `Is Burjeel in the network?`
   - Result: `ok=false`, `intent=network_lookup`
   - Message: ambiguity-safe candidate list returned, no guessed provider.

## Validation
- Focused suite: `tests/test_natural_provider_queries.py` -> 44 passed
- Full regression: 754 passed, 2 skipped

## Remaining Limits
- Provider listing still depends on the current deterministic provider-list implementation and dataset coverage.
- The current listing response for these Arabic natural queries is safe but may legitimately return no matches.
- This sprint did not expand provider data, inverse tier listing, shorthand plan aliases, or free-form broker-summary phrasing.

## Recommendation
- Next sprint should target provider dataset and city/type coverage gaps, not routing safety.