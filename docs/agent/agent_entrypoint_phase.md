# Agent Entrypoint Phase Documentation

## Overview
This document describes the minimal deterministic CLI entrypoint for the agent wrapper. The entrypoint allows users to submit a plain-language query and receive a structured or human-readable answer, using only validated deterministic logic.

## Features
- Accepts a single user query from the command line
- Calls `run_agent_wrapper(user_query)`
- Prints a clean, deterministic output for humans by default
- Supports a `--json` flag for machine-readable output
- No business logic duplication; all routing is delegated to the agent wrapper
- No AI, LLM, RAG, API, or scope expansion

## Usage
```
.venv/Scripts/python.exe -m src.agent_entrypoint "What is the annual limit for Remedy 04?"
.venv/Scripts/python.exe -m src.agent_entrypoint --json "What are the reimbursement rules for Remedy 05?"
```

## Output
### Human-readable (default)
- Intent
- Plan name (if available)
- Tool name (if available)
- Message
- Structured fields from data in a readable order

### JSON mode
- Full structured envelope as returned by `run_agent_wrapper`

## Example
```
Intent: plan_core
Plan: Remedy 04
Tool: get_plan_core
Message: Plan core fields returned.
annual_limit: 500,000
...
```

## Testing
- See `tests/test_agent_entrypoint.py` for full coverage
- All regression and contract tests must pass

## Limitations
- No scope expansion, no AI, no API, no bot integration in this phase
- Only deterministic, validated logic is used

## Next Steps
- Future phases may add API, bot, or integration layers, always preserving deterministic contract and regression safety
