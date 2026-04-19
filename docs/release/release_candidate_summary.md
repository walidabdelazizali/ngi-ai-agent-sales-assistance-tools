# Release Candidate Summary: Hardening + Batch 1 + Controlled Rollout

## What is stable now
- Deterministic CLI query system for Remedy 02, Remedy 03, and Remedy 04 (minimal fields only)
- All regression and smoke tests pass
- Environment and setup instructions validated

## What was added in this cycle
- Batch 1: Remedy 04 plan (minimal deterministic support: plan_name, plan_code, network_name)
- Controlled rollout documentation and operational plan
- Explicit pilot user guide, issue log, rollback, and escalation paths

## What is safe for pilot use
- CLI queries for Remedy 02, Remedy 03 (all previously validated deterministic fields)
- CLI queries for Remedy 04: plan_name, plan_code, network_name only
- Pilot user group and support/escalation structure

## What is explicitly deferred
- All non-deterministic, AI, fuzzy, or RAG-based queries
- Any Remedy 04 fields beyond plan_name, plan_code, network_name
- UI, API, batch, or database expansion
- Any new plan or data batch

## Known limitations
- Remedy 04: Only minimal deterministic fields are supported
- No UI, API, or batch mode
- Internal identifiers may differ from display names
- All unsupported fields are deferred and not available in pilot

## Next recommended action
- Proceed to controlled pilot rollout as documented
- Capture all pilot issues using the provided template and escalation path
- Do not expand scope or enable unsupported fields until pilot feedback and stability are confirmed
