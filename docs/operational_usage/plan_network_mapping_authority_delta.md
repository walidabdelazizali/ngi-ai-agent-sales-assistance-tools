# Plan-Network Mapping Authority Delta

## Scope
- Goal: lock deterministic plan-to-network resolution to approved sources and eliminate stale CSV drift.
- Constraint: no recommendation expansion, no fuzzy routing, no architecture drift.

## Problem Found
- Prior mapping CSV had only 4 rows and stale values for Remedy plans:
  - Remedy 03 -> `hn_basic` (stale)
  - Remedy 04 -> `hn_premier` (stale)
  - Remedy 05 -> `hn_elite` (stale)
- Missing rows:
  - Remedy 06
  - Classic 2
  - Classic 2R
  - Classic 3
- Effect: deterministic provider-in-network checks were producing incorrect network requirements for some plans.

## Authoritative Source Check
- Remedy plans (02-06): loaded from `src/v2_plan_loader.py` via `load_clean_plan` and normalize to `hn_basic_plus`.
- Classic plans (2/2R/3): loaded from `src/tools/enhanced_plan_loader.py` via `load_enhanced_plan` and normalize to:
  - Classic 2 -> `hn_standard_plus`
  - Classic 2R -> `hn_standard_plus`
  - Classic 3 -> `hn_standard`

## Changes Implemented
1. Updated resolver behavior in [src/query/plan_network_lookup.py](src/query/plan_network_lookup.py):
   - `resolve_plan_network()` now resolves approved plans from authoritative loaders first.
   - CSV lookup remains fallback for non-approved/unknown plans.
   - Added auditable metadata (`source`, `csv_mismatch`).
2. Corrected [data/plans/plan_network_mapping.csv](data/plans/plan_network_mapping.csv) to include all 8 approved rows:
   - `HN-REMEDY-2,Remedy 02,hn_basic_plus`
   - `HN-REMEDY-3,Remedy 03,hn_basic_plus`
   - `HN-REMEDY-4,Remedy 04,hn_basic_plus`
   - `HN-REMEDY-5,Remedy 05,hn_basic_plus`
   - `HN-REMEDY-6,Remedy 06,hn_basic_plus`
   - `HN_CLASSIC_2,Classic 2,hn_standard_plus`
   - `HN_CLASSIC_2R,Classic 2R,hn_standard_plus`
   - `HN_CLASSIC_3,Classic 3,hn_standard`
3. Strengthened tests in [tests/test_plan_network_lookup.py](tests/test_plan_network_lookup.py):
   - Approved names/codes expectations.
   - Stale CSV override resistance.
   - Missing-row resilience.
4. Updated stale end-to-end expectations in [tests/test_router_plan_network_queries.py](tests/test_router_plan_network_queries.py) for Remedy 03.

## Validation
- Focused mapping suite: `pytest tests/test_plan_network_lookup.py -q` -> 22 passed.
- Router mapping suite: `pytest tests/test_router_plan_network_queries.py -q` -> 11 passed.
- Full regression: `pytest -q` -> **769 passed, 2 skipped**.

## Deterministic Evidence
1. `resolve_plan_network("Remedy 03")` -> `found=True, medical_network=hn_basic_plus, source=authoritative, csv_mismatch=False`
2. `resolve_plan_network("Remedy 05")` -> `found=True, medical_network=hn_basic_plus, source=authoritative, csv_mismatch=False`
3. `resolve_plan_network("Classic 2")` -> `found=True, medical_network=hn_standard_plus, source=authoritative, csv_mismatch=False`
4. `answer_owner_query("What is the network for Remedy 03?")` -> `[PLAN NETWORK] ... Medical Network: hn_basic_plus`
5. `answer_owner_query("Is Accuracy Plus Medical Laboratory in Remedy 03 network?")` -> `Required Network: hn_basic_plus | Status: In network`

## Outcome
- Plan-network mapping is now source-anchored and deterministic for all approved plans.
- Stale CSV content can no longer silently change approved plan-network results.
- Regression baseline moved from 754/2 to 769/2 with mapping authority checks in place.
