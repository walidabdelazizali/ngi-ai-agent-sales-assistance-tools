# Telegram Live Activation Phase Documentation

## Overview
This document describes the minimal, deterministic live Telegram activation runner for the agent system. The runner provides a safe, owner-controlled path for local bot startup, with all business logic isolated in validated layers.

## Features
- Exposes `start_bot()` for local activation
- Reads `TELEGRAM_BOT_TOKEN` from environment only
- Fails safely and clearly if token is missing
- Imports Telegram SDK only inside runner
- Routes all incoming text updates to `process_update(update_dict)`
- Replies only with non-empty string responses
- Ignores malformed updates safely
- No business logic duplication
- No production deployment or cloud wiring

## Usage
1. Install requirements: `pip install python-telegram-bot`
2. Set your bot token in the environment:
   - On Windows: `set TELEGRAM_BOT_TOKEN=your_token_here`
   - On Unix: `export TELEGRAM_BOT_TOKEN=your_token_here`
3. Run: `python -m src.telegram_live_runner`

## Output
- Clean, readable, stable text for Telegram
- Safe error if token is missing

## Testing
- See `tests/test_telegram_live_runner.py` for full coverage
- All regression and contract tests must pass

## Limitations
- No scope expansion, no AI, no API, no production deployment in this phase
- Only deterministic, validated logic is used

## Next Steps
- Future phases may add production deployment, always preserving deterministic contract and regression safety
