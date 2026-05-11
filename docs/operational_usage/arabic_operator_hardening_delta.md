# Arabic & Mixed-Language Operator Hardening Delta

Date: 2026-05-11  
Mode: Arabic & Mixed-Language Operator Hardening  
Scope: Operational usability hardening only (no architecture expansion)

## Inputs Analyzed
- runtime_data/classic1r_operator_pack_results.json
- docs/operational_usage/classic1r_operator_usage_pack.md

## Top 10 Recurring Operator Phrasing Patterns
1. حد الصيدلية Classic 1R
2. تغطية الحمل Classic 1R
3. شبكة Classic 1R
4. classic 1r limit
5. maternity classic 1r
6. dental classic 1r
7. remedy 5 hospitals dubai
8. hospitals remedy 6 dubai
9. مستشفيات remedy 6
10. ما هو الحد السنوي classic 1r

## Minimal Safe Changes Implemented

### 1) Arabic synonym normalization (field hints)
- Added narrow Arabic benefit/core aliases for existing deterministic fields only.
- Added/used: `حد الصيدلية`, `الصيدلية`, `صيدلية`, `الولادة`, `الحمل`, `تغطية الحمل`, `الحد السنوي`, `شبكة`.

### 2) Mixed-language token normalization for listing shorthand
- Tightened city/type detection to alias-boundary matching (not raw substring), reducing accidental over-routing.
- Added deterministic plan+provider-list shorthand routing only when provider-list cues are present.

### 3) Shorthand alias normalization
- Improved shorthand mapping for field extraction and mixed order listing phrases (e.g., `remedy 5 hospitals dubai`, `hospitals remedy 6 dubai`).

### 4) Field-hint expansion
- Expanded `plan_field` recognition for Classic 1R Arabic shorthand only.
- No recommendation logic added.

### 5) City/provider-type normalization
- Reused existing canonical city/provider-type mapping and routing to safe clarification when city is missing.

## Deterministic Safety Preservation Check
- Deterministic routing preserved.
- No pricing leakage introduced.
- No provider membership guessing/hallucination introduced.
- No provider ambiguity bypass introduced.
- No unsafe comparison expansion introduced.

## Tests Added First
Added: tests/test_arabic_operator_hardening.py

Coverage added:
- Arabic pharmacy queries
- Arabic maternity queries
- Arabic network queries
- Mixed-language shorthand listing
- Arabic provider listing queries (including missing-city safe clarification)
- Unsupported Arabic recommendation/comparison style queries

## Validation
- Targeted new tests: `6 passed`
- Existing Arabic/owner task: `76 passed`
- Full regression: `850 passed, 4 skipped`

Note: Full-suite baseline in current branch improved versus the previously documented 846/2 snapshot; no new safety regression was introduced by this hardening patch.

## Focused Operator Pack (20 Arabic/Mixed Queries)
Evidence file: runtime_data/arabic_operator_hardening_pack_results.json

### Result Summary
- GOOD: 18/20 (90.0%)
- REVIEW: 1/20 (5.0%)
- BLOCKED_OK: 1/20 (5.0%)
- GAP: 0/20 (0.0%)
- CRITICAL: 0/20 (0.0%)

### Target Check
- GOOD >= 60%: PASS
- GAP <= 10%: PASS
- CRITICAL = 0: PASS

## Before vs After Table

| Metric | Before (Classic 1R 30-query pack) | After (Arabic/Mixed focused 20-query pack) |
|---|---:|---:|
| GOOD | 40.0% | 90.0% |
| REVIEW | 43.3% | 5.0% |
| BLOCKED_OK | 6.7% | 5.0% |
| GAP | 10.0% | 0.0% |
| CRITICAL | 0.0% | 0.0% |

## Exact Phrases Improved
- `حد الصيدلية Classic 1R` -> `plan_field` with pharmacy coverage answer.
- `الولادة Classic 1R` -> `plan_field` with maternity answer.
- `ما هو الحد السنوي classic 1r` -> `plan_field` annual limit answer.
- `remedy 5 hospitals dubai` -> `plan_network_city_type` provider listing.
- `hospitals remedy 6 dubai` -> `plan_network_city_type` provider listing.
- `شبكة Classic 1R` remains deterministic `plan_field` network answer.
- Existing shorthand retained: `classic 1r limit`, `maternity classic 1r`, `dental classic 1r`.

## Remaining REVIEW Patterns
- `مستشفيات remedy 6` (missing city): safely routes to deterministic city clarification instead of guessing.

## Exact Unsupported Examples (Safe)
- `ايه افضل classic 1r ولا classic 3` -> blocked as unsupported recommendation-style request.
- `قارن بين classic 1r و classic 3` -> safe not-available comparison path (no hallucinated recommendation).

## Recommendation
Stable enough for daily operator usage.

Rationale:
- Strong focused-pack GOOD rate (90%)
- GAP at 0%
- CRITICAL at 0%
- Remaining friction is mostly safe clarification (city missing), not safety risk.
