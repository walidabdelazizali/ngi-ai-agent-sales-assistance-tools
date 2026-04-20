"""
Telegram Transport: Minimal deterministic Telegram message handler for agent system.
"""
from src.constrained_planner import execute_planned_query

def handle_telegram_message(user_text: str) -> str:
    user_text = (user_text or '').strip()
    if not user_text:
        return "Sorry, I didn't receive a valid question. Please ask about Remedy 04 or Remedy 05."
    result = execute_planned_query(user_text, "text")
    return result if isinstance(result, str) else str(result)
