"""Owner-facing CLI for querying Remedy plans.

Usage:
    python -m src.query field "Remedy 03" "annual limit"
    python -m src.query compare "Remedy 02" "Remedy 03"
    python -m src.query compare "Remedy 02" "Remedy 03" --field pharmacy
    python -m src.query compare "Remedy 02" "Remedy 03" --differences-only
    python -m src.query summary "Remedy 03"
    python -m src.query ask "What is the annual limit for Remedy 03?"
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from src.query.plan_query import (
    answer_owner_query,
    compare_plans,
    get_plan_field,
    summarize_plan,
)


def _print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _print_field(result: dict[str, Any]) -> None:
    code = result.get("plan_code", "?")
    label = result.get("label", result.get("field", "?"))
    formatted = result.get("formatted", "")
    print(f"[{code}] {label}:")
    print(f"  {formatted}")


def _print_summary(result: dict[str, Any]) -> None:
    code = result.get("plan_code", "?")
    print(f"=== {code} Summary ===")
    print(result.get("summary_text", ""))


def _print_compare(result: dict[str, Any]) -> None:
    a = result.get("plan_a_code", "?")
    b = result.get("plan_b_code", "?")

    # Single-field comparison
    if "field" in result and "match" in result:
        label = result.get("label", result["field"])
        print(f"=== {a} vs {b}: {label} ===")
        if result["match"]:
            print(f"  Same: {result['plan_a_formatted']}")
        else:
            print(f"  {a}: {result['plan_a_formatted']}")
            print(f"  {b}: {result['plan_b_formatted']}")
        return

    # Error case
    if "error" in result:
        print(result["error"])
        return

    print(f"=== {a} vs {b} ===")

    # Differences only
    if result.get("differences_only"):
        diff = result.get("differing", {})
        if not diff:
            print("  No differences found.")
        for f, d in diff.items():
            print(f"\n  {d['label']}:")
            print(f"    {a}: {d['plan_a']}")
            print(f"    {b}: {d['plan_b']}")
        return

    # Full comparison
    matched = result.get("matched", [])
    diff = result.get("differing", {})

    if diff:
        print("\n  --- Differences ---")
        for f, d in diff.items():
            print(f"  {d['label']}:")
            print(f"    {a}: {d['plan_a']}")
            print(f"    {b}: {d['plan_b']}")

    if matched:
        print("\n  --- Matching ---")
        for m in matched:
            print(f"  {m['label']}: {m['value']}")


def cmd_field(args: argparse.Namespace) -> int:
    result = get_plan_field(args.plan, args.field)
    if args.json:
        _print_json(result)
    else:
        _print_field(result)
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    result = compare_plans(
        args.plan_a, args.plan_b,
        field_name=args.field,
        differences_only=args.differences_only,
    )
    if args.json:
        _print_json(result)
    else:
        _print_compare(result)
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    result = summarize_plan(args.plan)
    if args.json:
        _print_json(result)
    else:
        _print_summary(result)
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    question = " ".join(args.question)
    result = answer_owner_query(question)
    if args.json:
        _print_json(result)
        return 0

    rtype = result.get("type")
    if rtype == "field":
        _print_field(result["result"])
    elif rtype == "compare":
        _print_compare(result["result"])
    elif rtype == "summary":
        _print_summary(result["result"])
    elif rtype == "network":
        print(result["result"])
    else:
        print(result.get("message", "Unsupported query."))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.query",
        description="Query Remedy insurance plans (deterministic, no AI).",
    )
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON instead of formatted text.")
    sub = parser.add_subparsers(dest="command", required=True)

    # field
    p_field = sub.add_parser("field", help="Get a specific field for a plan.")
    p_field.add_argument("plan", help="Plan name (e.g. 'Remedy 03').")
    p_field.add_argument("field", help="Field name (e.g. 'annual limit').")
    p_field.set_defaults(func=cmd_field)

    # compare
    p_cmp = sub.add_parser("compare", help="Compare two plans.")
    p_cmp.add_argument("plan_a", help="First plan name.")
    p_cmp.add_argument("plan_b", help="Second plan name.")
    p_cmp.add_argument("--field", default=None,
                       help="Compare a specific field only.")
    p_cmp.add_argument("--differences-only", action="store_true",
                       help="Show only fields that differ.")
    p_cmp.set_defaults(func=cmd_compare)

    # summary
    p_sum = sub.add_parser("summary", help="Show plan summary.")
    p_sum.add_argument("plan", help="Plan name.")
    p_sum.set_defaults(func=cmd_summary)

    # ask
    p_ask = sub.add_parser("ask",
                           help="Ask a question in plain text.")
    p_ask.add_argument("question", nargs="+",
                       help="The question to answer.")
    p_ask.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
