"""
Minimal FastAPI app exposing the insurance assistant for local integration (e.g., n8n).
"""

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from src.agent_adapter import handle_user_query

app = FastAPI(title="Insurance Assistant API", version="1.0.0")

class AskRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
        return HTMLResponse(
                content="""
<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Insurance Assistant Local UI</title>
    <style>
        :root {
            --bg: #f6f7fb;
            --panel: #ffffff;
            --text: #1f2937;
            --muted: #6b7280;
            --accent: #0b5fff;
            --border: #dbe1ea;
            --good: #0f8f4b;
            --review: #a16207;
            --blocked: #1d4ed8;
            --gap: #b91c1c;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Segoe UI, Tahoma, sans-serif;
            color: var(--text);
            background: radial-gradient(circle at top right, #dbeafe, transparent 45%),
                                    radial-gradient(circle at top left, #dcfce7, transparent 35%),
                                    var(--bg);
            min-height: 100vh;
        }
        .wrap {
            max-width: 900px;
            margin: 32px auto;
            padding: 0 16px;
        }
        .card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            padding: 20px;
        }
        h1 {
            margin: 0 0 6px;
            font-size: 1.45rem;
        }
        p {
            margin: 0 0 16px;
            color: var(--muted);
        }
        .row {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 10px;
            margin-bottom: 14px;
        }
        input[type=\"text\"] {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 10px;
            font-size: 1rem;
        }
        button {
            border: 0;
            border-radius: 10px;
            padding: 0 16px;
            background: var(--accent);
            color: white;
            font-weight: 600;
            cursor: pointer;
            min-height: 44px;
        }
        button:disabled {
            opacity: 0.7;
            cursor: default;
        }
        .status {
            display: inline-block;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid transparent;
            margin-bottom: 12px;
        }
        .good { color: var(--good); border-color: color-mix(in srgb, var(--good), white 70%); background: #f0fdf4; }
        .review { color: var(--review); border-color: color-mix(in srgb, var(--review), white 65%); background: #fffbeb; }
        .blocked { color: var(--blocked); border-color: color-mix(in srgb, var(--blocked), white 65%); background: #eff6ff; }
        .gap { color: var(--gap); border-color: color-mix(in srgb, var(--gap), white 65%); background: #fef2f2; }
        .field {
            margin: 8px 0;
            padding: 10px 12px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: #fcfdff;
        }
        .label {
            display: block;
            font-size: 0.8rem;
            color: var(--muted);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: Consolas, monospace;
            font-size: 0.92rem;
        }
        @media (max-width: 700px) {
            .row { grid-template-columns: 1fr; }
            button { width: 100%; }
        }
    </style>
</head>
<body>
    <div class=\"wrap\">
        <div class=\"card\">
            <h1>Local Insurance Assistant</h1>
            <p>Display-only UI using the existing deterministic backend and JSON API contract.</p>
            <form id=\"askForm\" class=\"row\">
                <input id=\"question\" type=\"text\" placeholder=\"e.g. classic3 limit\" />
                <button id=\"askBtn\" type=\"submit\">Ask</button>
            </form>

            <div id=\"result\" style=\"display:none\">
                <div id=\"statusTag\" class=\"status\"></div>
                <div class=\"field\"><span class=\"label\">Intent</span><div id=\"intentVal\">-</div></div>
                <div class=\"field\"><span class=\"label\">Plan</span><div id=\"planVal\">-</div></div>
                <div class=\"field\"><span class=\"label\">Answer / Message</span><pre id=\"answerVal\"></pre></div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('askForm');
        const questionEl = document.getElementById('question');
        const askBtn = document.getElementById('askBtn');
        const resultEl = document.getElementById('result');
        const statusTag = document.getElementById('statusTag');
        const intentVal = document.getElementById('intentVal');
        const planVal = document.getElementById('planVal');
        const answerVal = document.getElementById('answerVal');

        function classifyStatus(question, payload) {
            const q = (question || '').toLowerCase();
            const answer = payload && payload.answer ? payload.answer : {};
            const intent = (answer.intent || '').toLowerCase();
            const message = String(answer.message || payload.error || '').toLowerCase();

            if (answer.ok) return 'GOOD';

            const isComparison =
                intent === 'plan_comparison' ||
                q.includes('compare') ||
                q.includes('comparison') ||
                q.includes('best enhanced plan') ||
                q.includes('best plan overall');
            if (isComparison && message.includes('not supported')) return 'BLOCKED_OK';

            const isBenefitGap =
                q.includes('pharmacy') || q.includes('maternity') || q.includes('private room') || q.includes('الطوارئ');
            if (isBenefitGap && message.includes('not supported')) return 'GAP';

            return 'REVIEW';
        }

        function paintStatus(statusText) {
            statusTag.textContent = statusText;
            statusTag.className = 'status';
            if (statusText === 'GOOD') statusTag.classList.add('good');
            else if (statusText === 'BLOCKED_OK') statusTag.classList.add('blocked');
            else if (statusText === 'GAP') statusTag.classList.add('gap');
            else statusTag.classList.add('review');
        }

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const question = questionEl.value.trim();
            if (!question) {
                resultEl.style.display = 'block';
                paintStatus('REVIEW');
                intentVal.textContent = 'unsupported';
                planVal.textContent = '-';
                answerVal.textContent = 'Question must not be empty.';
                return;
            }

            askBtn.disabled = true;
            askBtn.textContent = 'Asking...';

            try {
                const resp = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                const payload = await resp.json();
                const answer = payload.answer || {};
                const intent = answer.intent || 'unsupported';
                const plan = answer.plan_name || '-';
                const message = payload.display_answer || answer.message || payload.error || '';
                const opStatus = classifyStatus(question, payload);

                resultEl.style.display = 'block';
                paintStatus(opStatus);
                intentVal.textContent = intent;
                planVal.textContent = plan;
                answerVal.textContent = message;
            } catch (err) {
                resultEl.style.display = 'block';
                paintStatus('REVIEW');
                intentVal.textContent = 'unsupported';
                planVal.textContent = '-';
                answerVal.textContent = 'Request failed: ' + err;
            } finally {
                askBtn.disabled = false;
                askBtn.textContent = 'Ask';
            }
        });
    </script>
</body>
</html>
"""
        )


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
