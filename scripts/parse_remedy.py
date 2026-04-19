"""Quick CLI helper: parse one extracted JSON and print structured output.

Usage::

    python scripts/parse_remedy.py output/HN-REMEDY-2.json
"""

import json
import sys
from pathlib import Path

# Ensure project root is on sys.path when run as a script.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.parsers.remedy_parser import parse_remedy_plan  # noqa: E402


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <extracted.json>", file=sys.stderr)
        return 1

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"File not found: {json_path}", file=sys.stderr)
        return 1

    extraction = json.loads(json_path.read_text(encoding="utf-8"))
    parsed = parse_remedy_plan(extraction)

    # Print without raw_section_map for readability (it can be large).
    display = {k: v for k, v in parsed.items() if k != "raw_section_map"}
    display["raw_section_map_keys"] = list(parsed.get("raw_section_map", {}).keys())

    print(json.dumps(display, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
