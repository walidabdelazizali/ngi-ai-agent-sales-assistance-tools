# Agent Adapter Phase Documentation

## Overview
This document describes the minimal deterministic integration adapter for the agent system. The adapter exposes a single function for external systems to call, returning either a structured envelope or a human-readable string.

## Features
- Exposes `handle_user_query(user_query: str, output_mode: str = "dict")`
- Supports output modes:
  - "dict": returns the validated contract envelope
  - "text": returns a human-readable formatted string
- Delegates all routing and formatting to validated agent wrapper and entrypoint logic
- No business logic duplication
- No AI, LLM, RAG, API, or scope expansion

## Usage
```
from src.agent_adapter import handle_user_query

print(handle_user_query('What is the annual limit for Remedy 04?', 'dict'))
print(handle_user_query('What are the reimbursement rules for Remedy 05?', 'text'))
```

## Output
- "dict" mode: returns the full structured envelope
- "text" mode: returns a stable, readable string
- Invalid output_mode: returns a safe deterministic error envelope

## Testing
- See `tests/test_agent_adapter.py` for full coverage
- All regression and contract tests must pass

## Limitations
- No scope expansion, no AI, no API, no bot integration in this phase
- Only deterministic, validated logic is used

## Next Steps
- Future phases may add API, bot, or integration layers, always preserving deterministic contract and regression safety
