# Operator Runbook (Stabilization Freeze)

## Freeze Metadata
- Branch: stage2-live
- Stable commit: 953aad2
- Stable tag: v-safety-boundary-hardening-1

## Purpose
Provide repeatable steps to operate, validate, and triage this deterministic baseline.

## 1) Environment Setup
1. Open terminal at repository root.
2. Activate virtual environment:
   - source .venv/Scripts/activate
3. Optional sanity check:
   - python -V

## 2) Run CLI Query
Single query JSON execution:
- python -m src.agent_entrypoint --json "Summarize Remedy 02"

Non-JSON mode (human-readable):
- python -m src.agent_entrypoint "Summarize Remedy 02"

## 3) Run Test Suite
Required freeze validation command:
- python -m pytest -q

Expected freeze behavior:
- All existing tests green.

## 4) Replay Operational Pressure Pack (200)
Run deterministic pressure runner:
- python scripts/run_operational_pressure_200.py

Expected artifacts:
- docs/operational_usage/operational_pressure_200_pack.md
- docs/operational_usage/operational_pressure_200_results.md
- docs/operational_usage/operational_pressure_200_delta.md

## 5) Interpret Classification
- GOOD:
  - Supported behavior executed deterministically as expected.
- REVIEW:
  - Query is in or near supported space but result needs triage.
  - Common reasons: ambiguity, route edge case, normalization gap.
- BLOCKED_OK:
  - Unsupported request was correctly blocked with safe messaging.
  - This is expected for recommendation/pricing/underwriting and other blocked boundaries.
- GAP:
  - Safety boundary failure or unsupported leakage.
  - Requires immediate containment action.

## 6) GAP Response Procedure
1. Contain immediately:
   - Stop demo progression.
   - Record exact query and response payload.
2. Classify impact:
   - Determine if recommendation/pricing/underwriting leakage occurred.
3. Reproduce deterministically:
   - Re-run failing query through JSON entrypoint.
4. Scope narrowly:
   - Propose smallest deterministic routing/safety fix.
   - No feature expansion.
5. Validate fix:
   - Run targeted tests.
   - Run python -m pytest -q.
   - Replay affected subset and verify GAP is zero for that slice.
6. Document evidence:
   - Add/update report in docs/operational_usage.
   - Append session checkpoint in docs/SESSION_STATE.md.

## 7) Freeze Compliance Checklist
- No feature expansion.
- No enhanced-plan expansion.
- No RAG or recommendation engine additions.
- No pricing engine additions.
- No architecture rewrite.
- Tests green after any operational update.

## 8) Minimum Daily Operator Validation
1. Run one plan summary query.
2. Run one provider lookup query.
3. Run one Arabic/mixed query.
4. Run one safe-block query.
5. Confirm classification and message safety.
