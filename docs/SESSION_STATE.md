



# SESSION_STATE.md

## Project
NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS

## Current branch
stage2-live

## Stable baseline before today’s risky work
- Commit: 7497354
- Tag: v1-demo-ready-maternity-fix
- Tests at baseline: 449 passed, 2 skipped
- Working tree was clean

## Today’s work
1. Started Remedy 02–06 data stabilization.
2. Added/considered SALES_CORE_FIELDS separately from REQUIRED_FIELDS.
3. Detected critical Source Boundary issue:
	- HN-REMEDY-5 was resolving from stale output/HN-REMEDY-5.json.
	- Wrong stale values:
	  - annual_limit = 1,000,000
	  - area_of_coverage = Worldwide excluding USA
	  - medical_network = hn_elite
	- Correct DOCX values:
	  - annual_limit = AED. 150,000
	  - area_of_coverage = UAE & Indian Sub-continent & South East Asia, excluding Hong Kong & Singapore
	  - medical_network = HN Basic Plus
4. Confirmed stale read location:
	- src/query/plan_query.py
	- function: load_plan(name: str, *, output_dir: Optional[Path] = None)
	- around lines 341–370
	- reads output JSON using path.read_text()
5. Attempted quarantine/delete of output/HN-REMEDY-5.json caused test collection failures because current system still depends on output JSON.
6. Restored output/HN-REMEDY-5.json to recover temporary stability.
7. Stopped feature work due to Source Boundary risk and Copilot rate limit.
8. Ran real usage evidence sprint for Classic 3.
9. Created evidence pack at docs/rollout_validation/real_usage_validation_pack_classic3.md.
10. Created replay report at docs/rollout_validation/real_usage_validation_run_classic3.md.
11. Full pytest remained green at 578 passed, 2 skipped.
12. Real-usage replay found remaining unsupported/ambiguous phrasing for a few broker-style and Arabic variants, but no internal leakage or malformed JSON.
13. Ran broker phrasing hardening sprint for Classic 3 shorthand and mixed-language usage.
14. Created evidence report at docs/rollout_validation/broker_phrasing_hardening_report.md.
15. Final validation remained green at 591 passed, 2 skipped.
16. Hardened deterministic routing for collapsed-spacing and shorthand usage while keeping plan-less Arabic prompts safely unsupported.

## Important decision
- Do NOT continue Sales Core implementation until Source Boundary Lock is fixed.
- Do NOT delete or move output files yet.
- First patch must remove customer-answer dependency/trust in stale output JSON without breaking tests.
- Remedy 04 must remain draft/blocked.
- Do not change approval_status.

## Latest Work Session

### Review-driven Hardening Sprint
1. Extracted REVIEW and GAP rows from professional simulation results.
2. Created [docs/operational_usage/professional_simulation_review_actions.md](docs/operational_usage/professional_simulation_review_actions.md) with action classification.
3. Applied user rules: no patches, only action planning; no pharmacy/maternity exposure; no comparison enablement.
4. Result: all 12 items classified; none marked patch-now; defer and block decisions documented.
5. pytest: 641 passed, 2 skipped.

### Minimal Local Usage UI
1. Added browser page at `GET /` to [src/api/app.py](src/api/app.py).
2. UI displays: question textbox, Ask button, intent/plan/answer/status fields.
3. Status classification: GOOD / REVIEW / BLOCKED_OK / GAP (client-side logic only).
4. Reuses existing deterministic agent and /ask JSON API without behavior changes.
5. No runtime logic changes, no routing changes, no plan expansion, no comparison enablement.
6. Tested all five required scenarios through browser:
   - classic3 limit → GOOD / plan_core / Classic 3 ✓
   - classic2r limit → GOOD / plan_core / Classic 2R ✓
   - Summarize Classic 2 → GOOD / plan_summary / Classic 2 ✓
   - Compare Classic 2R and Classic 3 → BLOCKED_OK / plan_comparison ✓
   - pharmacy Classic 3 → GAP / unsupported / Classic 3 ✓
7. pytest: 642 passed, 2 skipped (added one new test for `GET /`).

## Next Session Priority
- Source Boundary Lock: Patch load_plan() in [src/query/plan_query.py](src/query/plan_query.py) to remove dependency on legacy output/*.json.
- Do not delete output files yet.
- Do not continue Sales Core work until source boundary is secure.

## End State
- Deterministic insurance assistant is now usable via browser UI.
- All backend behavior and JSON contract unchanged.
- Tests remain fully green (642 passed, 2 skipped).
- Ready for daily operational usage without CLI.
