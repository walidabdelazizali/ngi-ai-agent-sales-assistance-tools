# Demo Readiness Audit

## 1. Repository Structure
- Modular src/ layout (extractors, query, normalizers, parsers, tools, validators)
- scripts/ for CLI helpers (ingestion, query, parsing)
- output/ for extracted and processed data
- tests/ for coverage of core logic

## 2. Demo Entry Points
- `python -m src` — DOCX ingestion pipeline (requires .docx files in input dir)
- `python scripts/parse_remedy.py output/HN-REMEDY-2.json` — Parse and summarize extracted Remedy plan
- `PYTHONPATH=. python scripts/ask_network.py "<query>"` — Network provider query (requires normalized CSV data)
- `python -m src.query ...` — Owner-facing CLI for plan field, comparison, summary, and free-text queries

## 3. Supported Query Types
- Plan field retrieval: `field <plan> <field>`
- Plan comparison: `compare <planA> <planB> [--field <field>] [--differences-only]`
- Plan summary: `summary <plan>`
- Free-text owner queries: `ask <question>`
- Network provider lookup: English/Arabic queries for provider status, tier, city, type

## 4. Supported Capabilities
- Plan ingestion from DOCX (if input present)
- Plan field and summary extraction from JSON
- Plan comparison (field-level and summary)
- Network provider lookup (multi-language, tier-aware)
- Output packaging for business/WhatsApp/client

## 5. Available Tests
- Smoke tests for structure/imports
- Owner query/plan comparison/summary tests
- Network lookup and extraction tests (English/Arabic)
- Extraction/normalization/validator tests
- CLI and business answer tests

## 6. Demo-Safe Scope
### What works now
- Plan JSON parsing and summary (parse_remedy.py)
- Plan field/comparison/summary queries (src.query)
- Network provider queries (ask_network.py, with correct PYTHONPATH)
- All tests pass except known skips/failures

### What is safe to demo
- CLI-based plan and network queries
- Plan comparison and summary
- Parsing of provided sample outputs

### What should NOT be demoed
- DOCX ingestion unless input files are present and validated
- Any RAG/AI/LLM features not in current baseline
- Unused or experimental scripts

### Top 5 Demo Blockers
1. No DOCX files in input — ingestion pipeline will not show extraction
2. Network queries require correct PYTHONPATH and normalized CSV
3. No web or bot interface in baseline (CLI only)
4. No user-facing error handling for missing/invalid input
5. Minimal documentation for non-CLI users

### Recommended Demo Path
- Use CLI entry points only:
  - `python -m src.query ...` for plan/owner queries
  - `python scripts/parse_remedy.py ...` for plan summary
  - `PYTHONPATH=. python scripts/ask_network.py ...` for network lookup
- Demo only with provided sample data/outputs
- Avoid live ingestion or unsupported features
