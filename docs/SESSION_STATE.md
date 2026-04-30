



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

## Important decision
- Do NOT continue Sales Core implementation until Source Boundary Lock is fixed.
- Do NOT delete or move output files yet.
- First patch must remove customer-answer dependency/trust in stale output JSON without breaking tests.
- Remedy 04 must remain draft/blocked.
- Do not change approval_status.

## Next session priority
Source Boundary Lock only.

## Next-session Copilot prompt
Task: Source Boundary Lock only.

Do not delete output files.

Patch load_plan() in src/query/plan_query.py so customer-facing answers must not trust legacy output/*.json.

Before patching:
1. Show current load_plan() logic lines 341–370.
2. Show where output/*.json is used.
3. Show where plan data enters customer answer flow.
4. Propose smallest safe patch that keeps tests stable.
5. Add regression tests preventing HN-REMEDY-5 legacy values:
	- 1,000,000
	- hn_elite
6. Do not continue Sales Core work.
7. Do not commit until pytest passes and changes are reviewed.

## End state
- HN-REMEDY-5.json restored.
- Source contamination risk still exists.
- Work paused intentionally.
