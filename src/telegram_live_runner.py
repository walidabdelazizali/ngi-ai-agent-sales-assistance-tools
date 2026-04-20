
"""
Minimal live Telegram activation runner for agent system.
"""
import os

def validate_startup() -> str:
    if "TELEGRAM_BOT_TOKEN" not in os.environ:
        return "ERROR: TELEGRAM_BOT_TOKEN not set in environment."
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token or not token.strip():
        return "ERROR: TELEGRAM_BOT_TOKEN is empty."
    try:
        import telegram.ext  # type: ignore
    except ImportError:
        return "ERROR: python-telegram-bot package not installed. Run 'pip install python-telegram-bot'."
    return "OK: TELEGRAM_BOT_TOKEN and python-telegram-bot present."

def start_bot() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token or not token.strip():
        print("ERROR: TELEGRAM_BOT_TOKEN not set in environment.")
        return
    try:
        import telegram.ext  # type: ignore
    except ImportError:
        print("ERROR: python-telegram-bot package not installed. Run 'pip install python-telegram-bot'.")
        return
    try:
        from telegram.ext import ApplicationBuilder, MessageHandler, filters
        # Import runtime only when actually starting the bot
        try:
            from src.telegram_bot_runtime import process_update
        except Exception as e:
            print(f"ERROR: Telegram runtime startup failed: {e}")
            return

        async def handle_message(update, context):
            if not update or not getattr(update, 'message', None):
                return
            text = getattr(update.message, 'text', None)
            if not isinstance(text, str):
                return
            update_dict = {'message': {'text': text}}
            response = process_update(update_dict)
            if isinstance(response, str) and response.strip():
                await update.message.reply_text(response)

        app = ApplicationBuilder().token(token).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("Bot started. Press Ctrl+C to stop.")
        app.run_polling()
    except Exception as e:
        print(f"ERROR: Telegram runtime startup failed: {e}")
        return

if __name__ == "__main__":
    start_bot()
