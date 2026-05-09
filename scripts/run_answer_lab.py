from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "operational_usage" / "answer_lab_results.md"
QUERIES = [
    "classic3 limit",
    "classic2 cashless?",
    "شبكة كلاسيك 3",
    "What is the area of coverage for Classic 2?",
    "Compare Classic 3 and Remedy 04",
    "Summarize Classic 3",
    "Summarize Classic 2",
    "Summarize Classic 2R",
    "classic2r limit",
    "شبكة كلاسيك 2R",
    "هل كلاسيك 3 يحتاج referral؟",
    "هل كلاسيك 3 فيه direct billing؟",
    "pharmacy Classic 3",
    "maternity Classic 3",
]
SEPARATOR = "=" * 50


def run_query(query: str) -> dict:
    cmd = [sys.executable, "-m", "src.agent_entrypoint", "--json", query]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip() or "Entrypoint execution failed."
        return {
            "ok": False,
            "intent": "error",
            "plan_name": None,
            "message": message,
        }
    return json.loads(result.stdout)


def classify_status(result: dict) -> str:
    intent = result.get("intent")
    ok = bool(result.get("ok"))
    plan_name = result.get("plan_name")

    if ok and intent in ("plan_core", "plan_summary"):
        return "GOOD"
    if intent == "plan_comparison" and not ok:
        return "BLOCKED_OK"
    if intent == "unsupported":
        return "REVIEW" if plan_name else "GAP"
    return "REVIEW"


def render_block(query: str, result: dict) -> str:
    lines = [
        SEPARATOR,
        "QUERY:",
        query,
        "",
        "INTENT:",
        str(result.get("intent")),
        "",
        "PLAN:",
        str(result.get("plan_name") or "-"),
        "",
        "ANSWER:",
        str(result.get("message") or ""),
        "",
        "STATUS:",
        classify_status(result),
        "",
        "NOTES:",
        "",
        SEPARATOR,
    ]
    return "\n".join(lines)


def main() -> int:
    blocks = []
    for query in QUERIES:
        result = run_query(query)
        blocks.append(render_block(query, result))

    output = "\n\n".join(blocks) + "\n"
    print(output, end="")
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())