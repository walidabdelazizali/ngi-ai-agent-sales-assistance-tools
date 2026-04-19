# NGI AI Agent Sales Assistance Tools — Demo Runbook

## Prerequisites
- Python 3.8+
- All dependencies installed: `pip install -r requirements.txt`
- Virtual environment activated (if used)

## 1. Ingestion Pipeline (DOCX Extraction)
- **Command:**
  ```sh
  python -m src
  ```
- **Expected Output:**
  - If no DOCX files: `No .docx files found in ...` (safe, not an error)
  - If DOCX files are present, summary of extraction and output JSON files in `output/`

## 2. Remedy Extraction Parsing
- **Command:**
  ```sh
  python scripts/parse_remedy.py output/HN-REMEDY-2.json
  ```
- **Expected Output:**
  - Structured JSON summary of the parsed Remedy plan (see sample output in `output/`)

## 3. Network Query (CLI)
- **Command:**
  ```sh
  PYTHONPATH=. python scripts/ask_network.py "Is Accuracy Plus Medical Laboratory in the network?"
  ```
- **Note:**
  - `PYTHONPATH=.` is required for the script to find the `src` package.
  - If successful, prints the answer to the query.

## 4. Test Suite (Optional)
- **Command:**
  ```sh
  pytest
  ```
- **Expected Output:**
  - All tests should pass (or known failures documented in test logs).

---

**Evidence:**
- `parse_remedy.py` produces structured output from sample data.
- Ingestion pipeline handles missing DOCX files gracefully.
- Network query script requires `PYTHONPATH=.` to run successfully.

**For demo stability:**
- Do not add new features or expand scope.
- Use only the above commands for the demo.
- If any command fails, check environment and paths.
