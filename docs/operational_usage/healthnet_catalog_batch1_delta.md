# HealthNet Catalog Completion Sprint - Batch 1 Delta

Date: 2026-05-10
Mode: Structured catalog entries only (no architecture expansion)

## Scope
Added Batch 1 HealthNet enhanced plans:
- Prime 1 (`HN_PRIME_1`)
- Prime 2 (`HN_PRIME_2`)
- Classic 1 (`HN_CLASSIC_1`)
- Classic 1R (`HN_CLASSIC_1R`)
- Classic 4 (`HN_CLASSIC_4`)

## Deterministic Network Mapping
Canonical mapping implemented:
- Prime 1 -> `hn_advantage_plus`
- Prime 2 -> `hn_standard_plus`
- Classic 1 -> `hn_advantage`
- Classic 1R -> `hn_advantage`
- Classic 4 -> `hn_basic_plus`

Updated mapping surfaces:
- `data/plans/plan_network_mapping.csv`
- `src/query/plan_network_lookup.py` (`APPROVED_PLAN_CODES`, `APPROVED_PLAN_LOADERS`)
- `src/query/plan_network_lookup.py` network normalization supports `hn_advantage_plus` and `hn_advantage`

## Source Files Added
Structured source files were added under `data/plans/raw/`:
- `HN_PRIME_1/source_table_HN_PRIME_1.json`
- `HN_PRIME_2/source_table_HN_PRIME_2.json`
- `HN_CLASSIC_1/source_table_HN_CLASSIC_1.json`
- `HN_CLASSIC_1R/source_table_HN_CLASSIC_1R.json`
- `HN_CLASSIC_4/source_table_HN_CLASSIC_4.json`

## Data Completeness and Safety
Source documents for these five plans were not present in the repository at sprint time.
Per critical rule (no guessing), unavailable fields were explicitly marked as REVIEW/BLOCKED in structured source entries.

Marked REVIEW:
- `annual_limit`
- `area_of_coverage`
- `key_inpatient_benefits`
- `key_outpatient_benefits`
- `copays`

Marked BLOCKED:
- `pharmacy`
- `maternity`
- `dental_optical`

Conservative booleans used for safety (under-promise vs over-promise):
- `direct_billing`: `false`
- `referral_required`: `true`

## Loader/Registry Changes
- `src/tools/enhanced_plan_loader.py`
  - Registered Batch 1 plans in `ENHANCED_PLAN_REGISTRY`
  - Added aliases for each new plan
  - Extended parser support for Batch 1 raw schema
  - Preserved approval gates and source-trace generation
  - Included optional catalog fields in returned normalized plan (`key_inpatient_benefits`, `key_outpatient_benefits`, `pharmacy`, `maternity`, `dental_optical`, `copays`)

- `src/agent_wrapper.py`
  - Added plan aliases to `SUPPORTED_PLANS` for deterministic extraction and summary routing

## Test Coverage Added/Updated
New test file:
- `tests/test_healthnet_catalog_batch1.py`
  - enhanced registration checks
  - plan load checks
  - deterministic network resolution checks
  - plan summary checks
  - approval-gate blocking check (`approved=False` monkeypatch)
  - source-trace checks for customer-facing core fields

Updated tests:
- `tests/test_enhanced_plan_loader.py`
- `tests/test_plan_network_lookup.py`

## Validation Results
Focused Batch 1 tests:
- `python -m pytest tests/test_healthnet_catalog_batch1.py -q`
- Result: `26 passed`

Focused enhanced + mapping tests:
- `python -m pytest tests/test_healthnet_catalog_batch1.py tests/test_enhanced_plan_loader.py tests/test_plan_network_lookup.py -q`
- Result: `71 passed`

Existing provider/network regression safety:
- `python -m pytest tests/test_natural_provider_queries.py -q`
- Result: `76 passed`

Full regression:
- `python -m pytest -q`
- Result: `837 passed, 2 skipped`

## CLI Evidence
Executed:
- `python -m src.agent_entrypoint --json "Summarize Prime 1"`
- `python -m src.agent_entrypoint --json "Summarize Prime 2"`
- `python -m src.agent_entrypoint --json "Summarize Classic 1"`
- `python -m src.agent_entrypoint --json "Summarize Classic 1R"`
- `python -m src.agent_entrypoint --json "Summarize Classic 4"`

Outcome:
- All 5 returned `ok=true`, `intent=plan_summary`, deterministic summaries, and mapped networks.
- Unknown/unavailable core content remains explicitly tagged REVIEW in summaries.

## Next Recommended Batch
- Batch 2 candidate set (same workflow): remaining approved HealthNet plans not yet in enhanced registry.
- Precondition before promoting REVIEW fields to factual values: add authoritative source documents for Batch 1 plans into repository and replace REVIEW/BLOCKED placeholders field-by-field with source-traced values.
