"""
Agent Adapter: Minimal deterministic integration surface for agent system.
"""
from typing import Any, Dict, Union
from src.agent_wrapper import run_agent_wrapper

# Human-readable formatting logic (aligns with entrypoint)
def _format_human_readable(result: dict) -> str:
    lines = [f"Intent: {result.get('intent')}"]
    if result.get('plan_name'):
        lines.append(f"Plan: {result.get('plan_name')}")
    if result.get('tool_name'):
        lines.append(f"Tool: {result.get('tool_name')}")
    lines.append(f"Message: {result.get('message')}")
    data = result.get('data')
    if data and isinstance(data, dict):
        for k in sorted(data.keys()):
            lines.append(f"{k}: {data[k]}")
    elif data:
        lines.append(f"Data: {data}")
    return "\n".join(lines)

def handle_user_query(user_query: str, output_mode: str = "dict") -> Union[Dict[str, Any], str]:
    result = run_agent_wrapper(user_query)
    if output_mode == "dict":
        return result
    elif output_mode == "text":
        return _format_human_readable(result)
    else:
        return {
            "ok": False,
            "intent": "unsupported",
            "plan_name": None,
            "tool_name": None,
            "data": None,
            "message": f"Invalid output_mode: {output_mode}. Supported: 'dict', 'text'."
        }
