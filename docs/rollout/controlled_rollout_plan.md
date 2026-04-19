# Controlled Internal Pilot Rollout Plan

## Supported Scope
- Only validated deterministic queries for Remedy 02, Remedy 03, and Remedy 04 (minimal fields only)
- Entrypoint: `.venv/Scripts/python.exe -m src.query field <plan> <field>`
- Supported fields: plan_name, plan_code, network_name (Remedy 04: only these fields are deterministic)
- No AI/fuzzy, RAG, or database expansion

## Pilot User Types
- Internal business analysts
- Solution architects
- Designated QA testers

## Allowed Query Classes
- Plan identity queries (plan_name, plan_code)
- Network mapping queries (network_name)

## Disallowed Query Classes
- All benefit, limit, exclusion, or summary fields not validated for Remedy 04
- Any queries requiring fuzzy/AI logic
- Any queries for plans outside Remedy 02, 03, 04

## Known Limitations
- Remedy 04: Only plan_name, plan_code, network_name are deterministic
- No UI or API interface; CLI only
- Internal identifiers may differ from display names
- No support for unvalidated fields or plans


## Support Owner
- Rollout lead: Walid Abdelaziz Ali (walid.abdelaziz@ngi.com)

## Escalation Path
- 1st: Rollout lead (email above)
- 2nd: Internal QA manager (qa.manager@ngi.com)
- 3rd: Executive sponsor (exec.sponsor@ngi.com)

## Issue Logging Method
- All pilot issues must be logged using `docs/rollout/pilot_issue_log_template.md` and emailed to rollout lead

## Rollback Trigger
- Any regression, unsupported field exposure, or critical pilot issue

## Rollback Execution Command/Path
- Remove pilot user credentials or group membership
- Confirm system reverts to Phase 2 validated state

## Success Metrics
- 100% deterministic answers for supported queries
- All pilot issues logged and triaged within 1 business day
- No regression in Phase 1/2 test suite

## Go/No-Go Criteria
- Go: All pilot users confirm deterministic answers for allowed queries; no critical issues open
- No-Go: Any regression, unsupported field exposure, or critical pilot issue
