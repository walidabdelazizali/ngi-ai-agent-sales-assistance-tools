# Demo Rehearsal Runbook

## How to Run the Demo
1. Activate your Python virtual environment if needed.
2. From the project root, run:
   ```sh
   python scripts/run_demo_pack.py
   ```
3. The script will execute all demo queries in order, printing each result clearly.

## What to Say During Each Step
- Briefly introduce the type of query (provider, plan, Arabic, etc.)
- Read the query aloud, then show the output
- Highlight business value (speed, accuracy, bilingual support)
- If a fallback or not-found message appears, explain it as a safe, expected outcome

## What to Avoid During Director Review
- Do not open or run any scripts not in the demo pack
- Do not attempt DOCX ingestion or upload new data
- Do not click into code or data files live
- Do not run ad-hoc queries outside the prepared list

## Fallback Line for Non-Demo Queries
"This demo is intentionally limited to validated queries and data for stability. Broader questions will be supported in a future phase after leadership approval."
