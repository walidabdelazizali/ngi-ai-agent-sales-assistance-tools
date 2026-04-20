# Known Limitations (Internal Beta)

- **No Remedy 03 support:** Queries about Remedy 03 will return an explicit unsupported response.
- **No compare_plans intent:** Comparison queries are not supported and will return an explicit unsupported response.
- **No broad product/data expansion:** Only Remedy 04 and Remedy 05 are supported in this baseline. No additional plans or data are available.
- **Internal beta only:** This release is for internal validation and feedback. Not for production or external rollout.
- **Telegram runtime:** Requires valid `TELEGRAM_BOT_TOKEN` and `python-telegram-bot` installed. Startup validation is strict and deterministic.
- **Unsupported queries:** Any unsupported plan or intent will return a safe, explicit unsupported envelope.
