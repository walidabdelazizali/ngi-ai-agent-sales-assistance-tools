import os
from docx import Document

# Map plan names to DOCX filenames (update with actual filenames/paths)

# V2: Only allow plan loading from input_docs/ with explicit mapping to actual filenames
PLAN_DOCX_MAP = {
    "Remedy 02": "input_docs/HN-REMEDY-2.docx",
    "Remedy 03": "input_docs/HN-REMEDY-3.docx",
    "Remedy 04": "input_docs/HN-REMEDY 4.docx",
    "Remedy 05": "input_docs/HN-REMEDY 5.docx",
    "Remedy 06": "input_docs/HN-REMEDY 6.docx",
}

def load_clean_plan(plan_name: str) -> dict:
    """
    Load and extract raw data from the original Remedy DOCX file for the given plan.
    Returns a dict with paragraphs, tables, and raw text.
    """
    if plan_name not in PLAN_DOCX_MAP:
        raise ValueError(f"Unsupported plan name: {plan_name}")
    docx_path = PLAN_DOCX_MAP[plan_name]
    # Enforce input_docs/ only
    if not docx_path.startswith("input_docs/"):
        raise ValueError(f"Plan source path must be under input_docs/: {docx_path}")
    if not os.path.isfile(docx_path):
        raise ValueError(f"DOCX file not found for {plan_name}: {docx_path}")
    doc = Document(docx_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)
        tables.append(table_data)
    raw_text = "\n".join(paragraphs + ["\n".join(["\t".join(row) for row in tbl]) for tbl in tables])
    return {
        "plan_name": plan_name,
        "source_path": docx_path,
        "paragraphs": paragraphs,
        "tables": tables,
        "raw_text": raw_text,
    }

if __name__ == "__main__":
    from src.v2_plan_normalizer import normalize_clean_plan
    import pprint
    for plan in PLAN_DOCX_MAP:
        try:
            raw = load_clean_plan(plan)
            print(f"Plan: {plan}\n  source_path: {raw['source_path']}")
            norm = normalize_clean_plan(raw)
            print(f"  paragraph count: {len(raw['paragraphs'])}")
            print(f"  table count: {len(raw['tables'])}")
            print("  normalized output:")
            pprint.pprint(norm)
        except Exception as e:
            print(f"Plan: {plan}\n  ERROR: {e}")
