"""
Minimal FastAPI app exposing the insurance assistant for local integration (e.g., n8n).
"""

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agent_adapter import handle_user_query

app = FastAPI(title="Insurance Assistant API", version="1.0.0")

class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: AskRequest):
    q = request.question.strip() if isinstance(request.question, str) else ""
    if not q:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "question": request.question,
                "answer": None,
                "error": "Question must not be empty."
            }
        )
    try:
        agent_result = handle_user_query(q, output_mode="dict")
        display_answer = None
        # Always return status_code=200 and valid structure, even for blocked plans
        if agent_result.get("ok"):
            intent = agent_result.get("intent")
            data = agent_result.get("data")
            if intent == "plan_summary" and data and isinstance(data, dict) and data.get("summary_text"):
                display_answer = data["summary_text"]
            elif agent_result.get("message"):
                display_answer = agent_result["message"]
        return {
            "status": "ok" if agent_result.get("ok") else "error",
            "question": q,
            "display_answer": display_answer if agent_result.get("ok") else None,
            "answer": agent_result,
            "error": None if agent_result.get("ok") else agent_result.get("message")
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "question": q,
                "answer": None,
                "error": f"Internal error: {str(e)}"
            }
        )
