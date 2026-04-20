"""
Minimal Telegram bot runtime for agent system.
"""
from src.telegram_transport import handle_telegram_message

def process_update(update_dict: dict) -> str | None:
    """
    Extracts text from Telegram update dict, passes to transport, returns response.
    Returns None if no valid text is found.
    """
    if not isinstance(update_dict, dict):
        return None
    msg = update_dict.get("message")
    if not isinstance(msg, dict):
        return None
    text = msg.get("text")
    if not isinstance(text, str) or not text.strip():
        # Optionally, return a safe message for empty input
        return handle_telegram_message("")
    return handle_telegram_message(text)

if __name__ == "__main__":
    import os
    import sys
    print("This is a minimal Telegram bot runtime stub. To enable live bot, add token/network code here.")
    sys.exit(0)
