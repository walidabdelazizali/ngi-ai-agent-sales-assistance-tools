# Telegram Transport Phase Documentation

## Overview
This document describes the minimal deterministic Telegram transport for the agent system. The transport exposes a single function for handling Telegram messages, delegating all planning and formatting to the validated constrained planner.

## Features
- Exposes `handle_telegram_message(user_text: str) -> str`
- Delegates all planning and formatting to `execute_planned_query(user_text, "text")`
- No business logic duplication
- No AI, LLM, RAG, API, or scope expansion
- No network or live bot token required in tests

## Usage
```
from src.telegram_transport import handle_telegram_message

print(handle_telegram_message('What is the annual limit for Remedy 04?'))
```

## Output
- Clean, readable, stable text for Telegram
- Unsupported/empty/bad input returns a safe, user-friendly message

## Testing
- See `tests/test_telegram_transport.py` for full coverage
- All regression and contract tests must pass

## Limitations
- No scope expansion, no AI, no API, no bot integration in this phase
- Only deterministic, validated logic is used

## Next Steps
- Future phases may add live Telegram bot wiring, always preserving deterministic contract and regression safety
