# Rollback Plan: Controlled Pilot

## Trigger
- Any regression, unsupported field exposure, or critical pilot issue

## Steps
1. Notify all pilot users of immediate suspension
2. Disable pilot user access (remove from pilot user group or revoke credentials)
3. Confirm system reverts to Phase 2 validated state
4. Log rollback event in executive status update

## Owner
- Rollout lead: Walid Abdelaziz Ali (walid.abdelaziz@ngi.com)
- Escalation: QA manager (qa.manager@ngi.com) if lead unavailable
