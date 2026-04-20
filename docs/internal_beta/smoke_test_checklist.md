# Internal Beta Smoke Test Checklist

## 1. Local Startup
- Ensure Python 3.12+ and `python-telegram-bot` are installed
- Copy `.env.example` to `.env` and set your real `TELEGRAM_BOT_TOKEN`
- Activate your virtual environment

## 2. TELEGRAM_BOT_TOKEN Loading
- Confirm `.env` is loaded and `TELEGRAM_BOT_TOKEN` is available in the environment

## 3. Startup Validation
- Run:
  ```
  .venv/Scripts/python.exe -c "from src.telegram_live_runner import validate_startup; print(validate_startup())"
  ```
- Expected: `OK: TELEGRAM_BOT_TOKEN and python-telegram-bot present.`

## 4. Telegram Live Run
- Start the bot using your preferred entrypoint (see README)
- Send test queries to your Telegram bot

## 5. Sample Queries & Expected Behavior

### Supported English Query
- **Query:** `What is the annual limit for Remedy 04?`
- **Expected:** Deterministic answer with plan_core fields for Remedy 04

### Supported Arabic Query
- **Query:** `ما هو الحد السنوي للريميدي 5؟`
- **Expected:** Deterministic answer with plan_core fields for Remedy 05

### Unsupported Remedy 03 Query
- **Query:** `ما الفرق بين الريميدي 3 والريميدي 4؟`
- **Expected:** Explicit unsupported response: only Remedy 04 and 05 are supported

### Unsupported Comparison Query
- **Query:** `Compare Remedy 04 and Remedy 05`
- **Expected:** Explicit unsupported response: compare_plans intent not supported

### Supported Reimbursement Rules Query
- **Query:** `What are the reimbursement rules for Remedy 05?`
- **Expected:** Deterministic answer with reimbursement_rules fields for Remedy 05

### Supported Plan Summary Query
- **Query:** `Summarize Remedy 04`
- **Expected:** Deterministic answer with plan_summary fields for Remedy 04

