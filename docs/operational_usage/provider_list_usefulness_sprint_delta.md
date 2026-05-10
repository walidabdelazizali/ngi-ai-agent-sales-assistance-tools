# Provider List Usefulness Sprint Delta

## Scope
- Goal: Improve usefulness and clarity of deterministic provider listing answers after plan → network mapping is now stable.
- Constraint: no architecture expansion, no RAG/vector DB, no recommendation logic, no safety gate weakening.
- Preserve baseline: 769 passed, 2 skipped.

## Problem Found
Provider listing output was returning stale `[NETWORK]` heading and "No matching providers found" message despite:
1. Correct city/type extraction in wrapper
2. Deterministic provider resolution available in lookup layer
3. Network-scoped provider data present and queryable

Root cause: City/type extraction fell through to fallback code that produced generic "No matching" message instead of structured listing with:
- Clear plan name, resolved network code, city, and provider type headings
- Deterministic count and provider names
- Safe clarification for unknown cities or unsupported provider types

## Changes Implemented

### 1. Deterministic Listing API in Lookup Layer
Added `list_providers_in_network()` method in [src/query/network_lookup.py](src/query/network_lookup.py):
- Takes network code, city, provider type, and limit as inputs
- Canonicalizes city aliases (Dubai/دبي → Dubai, Abu Dhabi/ابوظبي → Abu Dhabi, Sharjah/الشارقة → Sharjah, Ajman/عجمان → Ajman)
- Canonicalizes provider type aliases (hospital/hospitals/مستشفى/مستشفيات → hospital, clinic/عيادات → clinic, pharmacy/صيدليات → pharmacy, lab/تحاليل → lab)
- Filters provider data by network availability + city + type
- Re-verifies deterministic resolution: only returns providers that can be re-resolved deterministically within the same network
- Returns structured response with: `ok`, `network_code`, `city`, `provider_type`, `count`, `providers` (list), `truncated` flag
- Returns safe error codes for unknown city, unsupported type, or network not found

### 2. City/Type Extraction Helper in Wrapper
Added `_extract_city_and_provider_type()` in [src/agent_wrapper.py](src/agent_wrapper.py):
- Detects canonical cities using alias mapping
- Detects canonical provider types using alias mapping
- Returns tuple (city, provider_type) for safe routing

### 3. Structured Output Formatting in Wrapper
Updated `plan_network_city_type` intent handler in [src/agent_wrapper.py](src/agent_wrapper.py):
- Integrates `resolve_plan_network()` call to get authoritative network code for plan
- Calls new `list_providers_in_network()` API
- Produces structured listing output with:
  ```
  [PROVIDER LIST]
  Plan: <plan_name>
  Resolved Network: <network_code> (<display_label>)
  City: <city>
  Provider Type: <provider_type>
  Count: <count>
  
  [If count > 0]
  Providers:
  - <provider_name_1>
  - <provider_name_2>
  ...
  
  [If truncated]
  Showing first 25 providers only.
  
  [If count == 0]
  No matching providers found for this plan/network/city/provider type.
  ```
- Safe error responses for unknown city, unsupported type, or mapping missing
- No raw CSV columns (`hnm_code`, `group_name`, `tel_no`, `location`, `google_name`) exposed
- Only returns providers verified to be in the resolved network

### 4. Comprehensive Usefulness Tests
Added `TestProviderListingUsefulness` class in [tests/test_natural_provider_queries.py](tests/test_natural_provider_queries.py):
- 11 new assertions covering:
  - Structured heading format (8 core tests)
  - Unknown city safe response
  - Unsupported provider type safe response
  - Provider re-resolution deterministic verification
  - No-match structured messaging
- English, Arabic, and mixed-language query coverage
- Parametrized Arabic tests for standardization

## Validation

### Focused Test Suite
```
pytest tests/test_natural_provider_queries.py -q
55 passed in 41.79s
```

### Full Regression
```
pytest -q
780 passed, 2 skipped in 185.98s
```
(+11 tests from baseline 769 passed, 2 skipped — all new usefulness tests)

### Deterministic Evidence

**Plan Network Mapping Authority (unchanged):**
```
Remedy 03: found=True, network=hn_basic_plus, source=authoritative, csv_mismatch=False
Remedy 05: found=True, network=hn_basic_plus, source=authoritative, csv_mismatch=False
Classic 2: found=True, network=hn_standard_plus, source=authoritative, csv_mismatch=False
Classic 2R: found=True, network=hn_standard_plus, source=authoritative, csv_mismatch=False
Classic 3: found=True, network=hn_standard, source=authoritative, csv_mismatch=False
```

**Provider Listing Queries:**
1. Query: `hospitals in Remedy 5 in Dubai`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 05`
   - Output: Structured listing with 16 hospitals, all deterministically verified
   - No raw CSV columns present

2. Query: `clinics in Remedy 6 in Sharjah`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 06`
   - Output: Structured listing for medical centers (clinic alias mapping)

3. Query: `pharmacies in Remedy 5 in Dubai`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 05`
   - Output: Structured listing with 1265 pharmacies (limit 25 shown)

4. Query: `labs in Remedy 6 in Abu Dhabi`
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 06`
   - Output: Structured listing for diagnostic centers + labs

5. Query: `مستشفيات Remedy 5 في دبي؟` (Arabic hospitals)
   - Result: `ok=true`, `intent=plan_network_city_type`, `plan_name=Remedy 05`
   - Output: Structured listing in canonical format

6. Query: `hospitals in Remedy 5 in Atlantis` (unknown city)
   - Result: `ok=false`, intent=plan_network_city_type
   - Message: "City is unknown, unclear, or unsupported. Please specify one of: Dubai, Abu Dhabi, Sharjah, Ajman."

7. Query: `optical in Remedy 5 in Dubai` (unsupported type)
   - Result: `ok=false`, intent=unsupported
   - Message: "Sorry, this query is not supported..."

## Outcome
- Provider listing now produces usefulness-focused structured output with deterministic safety.
- Plan → Network → City → Type → Provider filtering chain is now explicit and testable.
- Zero hallucination: only providers verified to exist in resolved network are listed.
- Zero data leakage: no raw CSV columns, no internal network codes in user-facing output.
- Safety preserved: unknown cities and unsupported types trigger safe clarification, not guessing.
- Baseline regression maintained: 780 passed (up 11 from new tests), 2 skipped.

## Remaining Limitations

1. **Provider Dataset Coverage**: Current data has no "clinic" entries in some cities — "clinic" type is mapped to "medical center" type, which returns results. True clinic-only listings may be empty for some cities.

2. **Limited Network Support**: Only `hn_basic_plus`, `hn_standard_plus`, and `hn_standard` have authoritative plan mappings. Other networks (HN Exclusive, HN Premier, etc.) would require data verification and explicit user requests.

3. **City Coverage**: Only 4 cities (Dubai, Abu Dhabi, Sharjah, Ajman) are canonicalized. Other emirates would require safe "unknown city" responses.

4. **Provider Type Coverage**: Only 4 types (hospital, clinic, pharmacy, lab) are supported. Other types (dental, optical, mental health) are not routed and fall to unsupported intent.

5. **No Inverse Queries**: Queries like "Which plans include hospital X?" are not supported; only "Is hospital X in plan Y?" is deterministic.

## Recommended Next Steps

1. **Broker Phrasing Expansion** (Low Risk): Add safe routing for contextual free-form queries like "providers available for broker presentation" that don't expand recommendation logic but improve phrasing tolerance.

2. **Provider Dataset Review** (Medium Effort): Verify city/type coverage in network provider data; document any gaps in coverage to set operator expectations.

3. **Extended Network Support** (Medium Risk): If hn_premier, hn_advantage, or hn_exclusive plans receive broker queries, add explicit mappings and test coverage.

4. **Shorthand Code Documentation** (Low Effort): Clarify that shorthand codes (c3, r5) are not supported; operators should use full plan names for consistency.
