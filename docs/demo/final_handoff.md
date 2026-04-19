# Final Handoff: Director Demo Package

## Exact Demo Entrypoint
- Run the demo pack: `python scripts/run_demo_pack.py`

## Files to Open During the Meeting
- docs/demo/director_one_pager.md
- docs/demo/system_overview.md
- docs/demo/demo_queries.md
- docs/demo/demo_expected_outcomes.md
- docs/demo/director_demo_script.md
- docs/demo/demo_rehearsal_runbook.md
- docs/demo/known_scope_and_limitations.md
- docs/demo/next_phase_roadmap.md

## Exact Order of the Live Demo
1. Open with the business problem and system overview (one_pager, system_overview)
2. Introduce demo queries and expected outcomes (demo_queries, demo_expected_outcomes)
3. Run the demo pack script live (`python scripts/run_demo_pack.py`)
4. Narrate each query and result using the director_demo_script.md
5. If a fallback or error appears, use the fallback line from demo_rehearsal_runbook.md
6. Close with known limitations and next-phase roadmap

## Files NOT to Open
- Any code files (src/, scripts/ except run_demo_pack.py)
- Any data files or test files
- Any non-demo scripts

## Exact Known Limitations
- Demo pack and tests require a working pandas installation (with C extensions)
- No DOCX ingestion or live data integration
- CLI only; no web or bot interface
- Only curated plans/providers are supported
- No AI, RAG, or LLM features
- Some queries may fail if dependencies are not installed or data is missing

## Next-Phase Recommendation After Director Approval
- Fix and harden Python environment and dependencies (esp. pandas)
- Expand plan and provider data coverage
- Add user-friendly interfaces (web, chat, etc.)
- Integrate with live data sources
- Consider AI/RAG features only after core system is stable and approved
