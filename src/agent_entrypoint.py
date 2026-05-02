"""
Agent Entrypoint: Minimal deterministic CLI for agent wrapper.
"""
import sys
import argparse
import json
from src.agent_wrapper import run_agent_wrapper

def print_human_readable(result: dict):
    print(f"Intent: {result.get('intent')}")
    if result.get('plan_name'):
        print(f"Plan: {result.get('plan_name')}")
    if result.get('tool_name'):
        print(f"Tool: {result.get('tool_name')}")
    print(f"Message: {result.get('message')}")

def main():
    parser = argparse.ArgumentParser(description="Deterministic Agent Entrypoint")
    parser.add_argument('--json', action='store_true', help='Output machine-readable JSON')
    parser.add_argument('query', nargs='+', help='User query string')
    args = parser.parse_args()
    user_query = ' '.join(args.query)
    result = run_agent_wrapper(user_query)
    # Always print valid structure, even for blocked plans
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result.get("ok"):
            print(f"Intent: {result.get('intent')}")
            if result.get('plan_name'):
                print(f"Plan: {result.get('plan_name')}")
            if result.get('tool_name'):
                print(f"Tool: {result.get('tool_name')}")
            print(f"Message: {result.get('message')}")
        else:
            print_human_readable(result)

if __name__ == "__main__":
    main()
