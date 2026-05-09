



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

### Arabic / Mixed Query Normalization Sprint
1. Added deterministic pre-routing normalization in [src/agent_wrapper.py](src/agent_wrapper.py) for Arabic/mixed aliases and spacing/number variants.
2. Added deterministic network/provider query normalization in [src/query/network_lookup.py](src/query/network_lookup.py), including known transliterations and shorthand forms.
3. Added focused regression coverage in [tests/test_arabic_mixed_normalization.py](tests/test_arabic_mixed_normalization.py).
4. Preserved safety boundaries: no recommendation expansion, no comparison expansion, no enhanced plan expansion.
5. Full validation: pytest 665 passed, 2 skipped.

### Real Usage Evidence Rerun (100 Questions)
1. Re-ran the same evidence pack and updated [docs/operational_usage/real_usage_evidence_pack_100_results.md](docs/operational_usage/real_usage_evidence_pack_100_results.md).
2. Added delta analysis at [docs/operational_usage/real_usage_evidence_pack_100_delta.md](docs/operational_usage/real_usage_evidence_pack_100_delta.md).
3. Evidence delta:
	- GOOD: 58 -> 63 (+5)
	- REVIEW: 24 -> 19 (-5)
	- BLOCKED_OK: 13 -> 13
	- GAP: 5 -> 5

## Next Session Priority
- Source Boundary Lock: Patch load_plan() in [src/query/plan_query.py](src/query/plan_query.py) to remove dependency on legacy output/*.json.
- Do not delete output files yet.
- Do not continue Sales Core work until source boundary is secure.

## End State
- Deterministic insurance assistant is now usable via browser UI.
- All backend behavior and JSON contract unchanged.
- Tests remain fully green (642 passed, 2 skipped).
- Ready for daily operational usage without CLI.

## Latest Work Session (Provider Dataset Coverage Sprint)

### Provider Dataset Coverage Sprint
1. Hardened provider alias coverage in [src/query/network_lookup.py](src/query/network_lookup.py) for:
	- Aster Qsais / Aster Al Qusais
	- Burjeel AUH / Burjeel Abu Dhabi
	- Mediclinic Qusais (Arabic transliteration path)
2. Added Arabic/mixed normalization aliases for provider families and branch tokens (`برجيل`, `أستر/استر`, `ان ام سي`, `ميديكلينيك`, `رويال`, `qsais -> qusais`, `auh -> abu dhabi`).
3. Implemented deterministic ambiguity-safe messaging with candidate previews for family-name matches (e.g., Burjeel/NMC Royal), instead of silent not-found behavior.
4. Fixed wrapper routing gap for normalized Arabic phrasing (`في أي network ...`) in [src/agent_wrapper.py](src/agent_wrapper.py), so mixed Arabic/English provider-network questions route to network lookup.
5. Fixed Windows JSON output crash in [src/agent_entrypoint.py](src/agent_entrypoint.py) by enforcing UTF-8 output only in `--json` mode.
6. Added new regression coverage:
	- [tests/test_provider_dataset_coverage.py](tests/test_provider_dataset_coverage.py)
	- Added Arabic routing assertion in [tests/test_network_search_hardening.py](tests/test_network_search_hardening.py)
7. Added evidence report: [docs/operational_usage/provider_dataset_coverage_delta.md](docs/operational_usage/provider_dataset_coverage_delta.md).
8. Full validation is green after sprint: 675 passed, 2 skipped.

### Evidence Pack Refresh (100-Query Rerun)
1. Re-ran all 100 queries against current system post-provider-coverage sprint.
2. Updated [docs/operational_usage/real_usage_evidence_pack_100_results.md](docs/operational_usage/real_usage_evidence_pack_100_results.md).
3. Updated [docs/operational_usage/real_usage_evidence_pack_100_delta.md](docs/operational_usage/real_usage_evidence_pack_100_delta.md).
4. Delta vs prior run: GOOD 63→71 (+8), REVIEW 19→16 (-3), BLOCKED_OK 13→8 (-5), GAP 5→5 (0).
5. No product code changes.

### Enhanced Plan Baseline Sprint — Classic 2R (HN_CLASSIC_2R)
1. Confirmed Classic 2R already fully registered:
   - [src/tools/enhanced_plan_loader.py](src/tools/enhanced_plan_loader.py): `ENHANCED_PLAN_REGISTRY` entry with `approved=True`.
   - [src/agent_wrapper.py](src/agent_wrapper.py): `SUPPORTED_PLANS` includes all Classic 2R aliases.
   - Source data: `data/plans/raw/HN_CLASSIC_2R/source_table_HN_CLASSIC_2R.json` — confirmed present.
2. Verified end-to-end field values from `load_enhanced_plan("Classic 2R")`:
   - `plan_name`: "Classic 2R", `plan_code`: "HN_CLASSIC_2R"
   - `network_name`: "Standard Plus", `annual_limit`: "AED 250,000"
   - `area_of_coverage`: "Worldwide Excluding USA and Canada"
   - `direct_billing`: True, `referral_required`: False
3. Verified unsupported benefit blocking: maternity, pharmacy, dental, optical all return `intent="unsupported"` — no data leakage.
4. Verified Arabic alias routing: `ملخص كلاسيك 2r` → `plan_summary`, `شبكة كلاسيك 2r` → `plan_core`.
5. Created new regression test file: [tests/test_classic2r_baseline.py](tests/test_classic2r_baseline.py) — 19 tests covering:
   - All 6 core field values at tool-contract level (`get_plan_core`, `get_plan_summary`)
   - End-to-end `run_agent_wrapper` data dict assertions
   - Arabic alias routing (3 parametrized)
   - Unsupported benefit blocking (4 parametrized: maternity, pharmacy, dental, optical)
6. Full validation: **694 passed, 2 skipped** (up from 675; 19 new tests added, no regressions).

## Next Session Priority
- Source Boundary Lock: Patch `load_plan()` in [src/query/plan_query.py](src/query/plan_query.py) to remove dependency on legacy `output/*.json`.
- Do not delete output files yet.
- Do not continue Sales Core work until source boundary is secure.

## End State (Post Enhanced Plan Baseline Sprint)
- Classic 2R is fully registered, tested, and verified end-to-end as a deterministic baseline plan.
- All field values confirmed against source_table_HN_CLASSIC_2R.json.
- No product code changes were required — infrastructure was already in place.
- Test suite: 694 passed, 2 skipped.

## Latest Work Session (Operational Pressure Sprint - 200 Queries)

### Operational Pressure Evidence Sprint
1. Added deterministic evidence runner: [scripts/run_operational_pressure_200.py](scripts/run_operational_pressure_200.py).
2. Built a 200-query pressure pack with strict required distribution:
	- Remedy/core: 40
	- Provider/network: 50
	- Enhanced baseline Classic 2R: 40
	- Comparison pressure: 30
	- Recommendation/out-of-scope: 20
	- Real broker-style Arabic phrasing: 20
3. Enforced deterministic classification for each query:
	- GOOD / REVIEW / BLOCKED_OK / GAP
	- with reason and failure-pattern tagging.
4. Added regression coverage for pack integrity and classifier behavior:
	- [tests/test_operational_pressure_200.py](tests/test_operational_pressure_200.py)
5. Generated evidence artifacts:
	- [docs/operational_usage/operational_pressure_200_pack.md](docs/operational_usage/operational_pressure_200_pack.md)
	- [docs/operational_usage/operational_pressure_200_results.md](docs/operational_usage/operational_pressure_200_results.md)
	- [docs/operational_usage/operational_pressure_200_delta.md](docs/operational_usage/operational_pressure_200_delta.md)
6. Operational replay summary (200 queries):
	- GOOD: 111
	- REVIEW: 22
	- BLOCKED_OK: 66
	- GAP: 1
7. Safety and scope checks:
	- Unsupported recommendation/pricing/underwriting set: 20/20 BLOCKED_OK.
	- Enhanced unsupported benefits for Classic 2R remained blocked in pressure run.
8. Full validation after sprint: **702 passed**.

## Next Session Priority
- Keep scope evidence-first and run a narrow hardening sprint for operational weaknesses identified in the 200-pack delta:
  - provider ambiguity handling
  - provider routing-to-unsupported fallthroughs
  - provider alias/dataset normalization gaps
- Replay the same 200-pack after targeted hardening.

## Latest Work Session (Safety Boundary Hardening - Recommendation-Style Comparison)

### Safety Boundary GAP Closure
1. Investigated comparison routing and confirmed the single GAP leak from:
	- `Which is better, Remedy 02 or Remedy 05?`
2. Hardened deterministic routing in [src/agent_wrapper.py](src/agent_wrapper.py):
	- Added recommendation-style comparison detection (EN/AR terms).
	- Blocked recommendation-style plan selection with explicit safe message.
	- Preserved factual comparisons (`Compare X and Y`, `قارن بين X و Y`, `الفرق بين X و Y`).
	- Removed recommendation text generation from factual comparison output path.
3. Added/updated regression coverage:
	- [tests/test_safety_boundary_recommendation_comparison.py](tests/test_safety_boundary_recommendation_comparison.py)
	- [tests/test_agent_recommendation.py](tests/test_agent_recommendation.py)
4. Validation:
	- Focused safety/comparison suites: 100 passed.
	- Full pytest: **706 passed**.
5. Replayed affected operational subset only (comparison + recommendation + former GAP case):
	- GOOD: 10
	- REVIEW: 0
	- BLOCKED_OK: 40
	- GAP: 0
6. Report generated:
	- [docs/operational_usage/safety_boundary_gap_fix.md](docs/operational_usage/safety_boundary_gap_fix.md)

## Next Session Priority
- Continue narrow hardening from operational pressure deltas:
  - provider ambiguity handling
  - provider routing-to-unsupported fallthroughs
  - provider alias/dataset normalization gaps
- Replay full 200-pack after each focused hardening slice.

## Latest Work Session (Stabilization Freeze Sprint)

### Stabilization Freeze Checkpoint
1. Established controlled baseline checkpoint metadata:
	- Branch: stage2-live
	- Commit: 953aad2
	- Tag: v-safety-boundary-hardening-1
2. Added freeze documentation set:
	- [docs/SUPPORTED_CAPABILITIES.md](docs/SUPPORTED_CAPABILITIES.md)
	- [docs/SAFE_USAGE_BOUNDARIES.md](docs/SAFE_USAGE_BOUNDARIES.md)
	- [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)
	- [docs/INTERNAL_DEMO_SCRIPT.md](docs/INTERNAL_DEMO_SCRIPT.md)
	- [docs/OPERATOR_RUNBOOK.md](docs/OPERATOR_RUNBOOK.md)
3. Documented supported deterministic capabilities:
	- plan summary
	- plan core fields
	- provider/network lookup
	- Arabic/mixed routing
	- Classic 2R enhanced baseline
	- factual comparisons
	- safe blocking behavior
4. Documented unsupported and safely blocked boundaries:
	- recommendation-style plan selection
	- pricing advice
	- underwriting advice
	- unapproved enhanced benefits
	- unknown provider guessing
	- broad business advice
5. Added internal demo flow with fixed query set:
	- 5 plan questions
	- 5 provider/network questions
	- 5 Arabic/mixed questions
	- 3 Classic 2R questions
	- 3 safe-block examples
6. Added operator runbook with reproducible commands for:
	- CLI execution
	- pytest execution
	- 200-pack operational replay
	- classification interpretation (GOOD / REVIEW / BLOCKED_OK / GAP)
	- GAP containment and triage procedure

## Next Session Priority
- Keep freeze mode in effect and process only narrow, evidence-backed changes.
- Any change request must preserve deterministic boundaries and pass full pytest.
