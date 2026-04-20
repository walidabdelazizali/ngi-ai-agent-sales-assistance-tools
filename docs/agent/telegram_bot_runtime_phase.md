# Telegram Bot Runtime Phase Documentation

## Overview
This document describes the minimal, deterministic Telegram bot runtime for the agent system. The runtime exposes a single entrypoint for processing Telegram updates, delegating all logic to the validated transport and planner layers.

## Features
- Exposes `process_update(update_dict: dict) -> str | None`
- Extracts incoming Telegram text safely
- Passes only the text to `handle_telegram_message()`
- Returns the resulting text response
- Ignores unsupported/malformed update shapes safely
- No business logic duplication
- No live network or Telegram API calls in tests
- Main guard isolates any future network/bootstrap code

## Usage
```
from src.telegram_bot_runtime import process_update

update = {'message': {'text': 'What is the annual limit for Remedy 04?'}}
print(process_update(update))
```

## Output
- Clean, readable, stable text for Telegram
- Unsupported/empty/bad input returns a safe, user-friendly message or None

## Testing
- See `tests/test_telegram_bot_runtime.py` for full coverage
- All regression and contract tests must pass

## Limitations
- No scope expansion, no AI, no API, no live bot integration in this phase
- Only deterministic, validated logic is used

## Next Steps
- Future phases may add live Telegram bot wiring, always preserving deterministic contract and regression safety
