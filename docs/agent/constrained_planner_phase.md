# Constrained Planner Phase Documentation

## Overview
This document describes the deterministic constrained planner for the agent system. The planner classifies user queries into supported intents and plans, and delegates execution to the validated adapter.

## Features
- Exposes `plan_user_query(user_query: str) -> dict`
- Planner output includes:
  - ok: True/False
  - intent: plan_core, reimbursement_rules, plan_summary, or unsupported
  - plan_name: Remedy 04, Remedy 05, or None
  - reason: explanation string
  - normalized_query: original query string
- Exposes `execute_planned_query(user_query: str, output_mode: str = "dict") -> dict | str`
- Execution always flows through the validated adapter
- No business logic duplication
- No AI, LLM, RAG, API, or scope expansion

## Usage
```
from src.constrained_planner import plan_user_query, execute_planned_query

print(plan_user_query('Tell me the annual limit for Remedy 04'))
print(execute_planned_query('Tell me the annual limit for Remedy 04', 'dict'))
```

## Output
- Planner: returns a small structured object with intent, plan, reason, and normalized query
- Executor: returns the validated adapter output or a safe unsupported envelope

## Testing
- See `tests/test_constrained_planner.py` for full coverage
- All regression and contract tests must pass

## Limitations
- No scope expansion, no AI, no API, no bot integration in this phase
- Only deterministic, validated logic is used

## Next Steps
- Future phases may add optional LLM or API front-ends, always preserving deterministic contract and regression safety
