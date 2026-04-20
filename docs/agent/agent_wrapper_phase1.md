# Agent Wrapper Phase 1 Documentation

## Overview
This document describes Phase 1 of the deterministic agent-ready wrapper for the NGI AI Agent Sales Assistance Tools project. This wrapper enables agent/tool-calling integration by providing a stable, regression-safe, and deterministic interface for classifying user queries and routing them to validated tool contract functions.

## Design Principles
- **No AI, LLM, RAG, or fuzzy logic**: All routing and plan extraction is explicit and rule-based.
- **Regression-safe**: Wrapper uses only validated tool contract functions and does not duplicate business logic.
- **Deterministic**: No guessing, no fallback to defaults, no scope expansion.
- **Explicit intent and plan extraction**: Only supported intents and plans are recognized.

## Supported Intents
- `plan_core`: Queries for plan identity/core fields (plan name, code, network, annual limit, area of coverage, direct billing, referral)
- `reimbursement_rules`: Queries for reimbursement, outside network, outside UAE, reimbursement basis, reimbursement conditions, reimbursement documents
- `plan_summary`: Queries for summary, overview, or plan summary
- `unsupported`: All other queries

## Supported Plans
- Remedy 04
- Remedy 05

## Public API
```
def run_agent_wrapper(user_query: str) -> dict
```

### Response Envelope
```
{
  "ok": bool,
  "intent": str,
  "plan_name": str | None,
  "tool_name": str | None,
  "data": dict | None,
  "message": str
}
```

## Routing Logic
- If the query contains a supported plan and matches a supported intent, the wrapper calls the corresponding tool contract function and returns the result in the envelope.
- If the plan is missing or unsupported, returns an envelope with `ok: False` and a safe message.
- If the intent is unsupported, returns an envelope with `ok: False` and a safe message.

## Example Usage
```
from src.agent_wrapper import run_agent_wrapper

print(run_agent_wrapper('What is the annual limit for Remedy 04?'))
print(run_agent_wrapper('What are the reimbursement rules for Remedy 05?'))
print(run_agent_wrapper('Give me a summary of Remedy 04'))
print(run_agent_wrapper('Tell me about Remedy 99'))
```

## Testing
- See `tests/test_agent_wrapper.py` for comprehensive test coverage.
- All existing regression tests must pass.

## Limitations
- Only supports explicit, deterministic routing for the intents and plans listed above.
- No AI, LLM, RAG, API, or fuzzy expansion.
- No defaulting to a plan if not found.

## Next Steps
- Expand supported intents and plans in future phases as needed, maintaining regression safety and deterministic behavior.
