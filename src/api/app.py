"""
Minimal FastAPI app exposing the insurance assistant for local integration (e.g., n8n).
"""

import json
import time
from typing import Any, Optional

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from src.agent_adapter import handle_user_query
from src.operational_usage import get_operational_usage_store
from src.output import format_output
from src.query.network_lookup import get_network_lookup
from src.runtime_hardening import (
    RuntimeHardeningStore,
    build_health_payload,
    classify_result_status,
    normalize_query,
    run_startup_validation,
)

app = FastAPI(title="Insurance Assistant API", version="1.0.0")

_USAGE_STORE = get_operational_usage_store()
_RUNTIME_STORE = RuntimeHardeningStore()
_STARTUP_VALIDATION = run_startup_validation()


_RECENT_SUCCESSFUL_QUERIES: list[str] = []


def _remember_successful_query(question: str) -> None:
    q = question.strip()
    if not q:
        return
    if q in _RECENT_SUCCESSFUL_QUERIES:
        _RECENT_SUCCESSFUL_QUERIES.remove(q)
    _RECENT_SUCCESSFUL_QUERIES.insert(0, q)
    del _RECENT_SUCCESSFUL_QUERIES[10:]


def _recent_searches_snapshot() -> list[str]:
    return list(_RECENT_SUCCESSFUL_QUERIES)


class AskRequest(BaseModel):
    question: str
    output_mode: Optional[str] = None
    usage_action: Optional[str] = None
    usage_query: Optional[str] = None
    usage_value: Optional[str] = None
    friction_tag: Optional[str] = None
    usage_context: Optional[str] = None
    duration_ms: Optional[int] = None


def _intent_hint_from_query(query: str) -> str:
    normalized = normalize_query(query)
    if not normalized:
        return "unknown"
    if any(token in normalized for token in ("compare", "comparison", "قارن", "مقارنة")):
        return "plan_comparison"
    if any(token in normalized for token in ("provider", "providers", "network", "hospital", "clinic", "pharmacy", "lab", "مزود", "مستشفى", "شبكة")):
        return "provider_lookup"
    if any(token in normalized for token in ("summary", "summarize", "plan", "ملخص", "خطة")):
        return "plan_summary"
    return "unknown"


def _record_runtime_observability_event(
    query: str,
    normalized_query: str,
    intent: str,
    resolved_plan: str,
    output_mode: str,
    response_time_ms: int,
    routing_time_ms: int,
    retrieval_time_ms: int,
    formatting_time_ms: int,
    result_status: str,
    fallback_used: bool,
    refusal_reason: str,
    provider_lookup_used: bool,
    comparison_used: bool,
    action: str = "ask",
) -> None:
    try:
        _RUNTIME_STORE.record_runtime_event(
            {
                "query": query,
                "normalized_query": normalized_query,
                "intent": intent,
                "resolved_plan": resolved_plan,
                "output_mode": output_mode,
                "response_time_ms": int(max(0, response_time_ms)),
                "routing_time_ms": int(max(0, routing_time_ms)),
                "retrieval_time_ms": int(max(0, retrieval_time_ms)),
                "formatting_time_ms": int(max(0, formatting_time_ms)),
                "result_status": result_status,
                "fallback_used": bool(fallback_used),
                "refusal_reason": refusal_reason,
                "provider_lookup_used": bool(provider_lookup_used),
                "comparison_used": bool(comparison_used),
                "action": action,
            }
        )
    except Exception:
        # Telemetry must never break operator responses.
        return


@app.get("/system/health")
def system_health() -> dict:
    return build_health_payload(_STARTUP_VALIDATION)


@app.on_event("startup")
def validate_runtime_startup() -> None:
    global _STARTUP_VALIDATION
    _STARTUP_VALIDATION = run_startup_validation()


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    _lookup = get_network_lookup()
    _usage_snapshot = _USAGE_STORE.ui_snapshot()
    _area_opts: dict[str, list[str]] = {
        city: _lookup.get_distinct_area_options(city)
        for city in ["Dubai", "Sharjah", "Abu Dhabi", "Ajman"]
    }
    import json as _json
    _area_opts_js = _json.dumps(_area_opts, ensure_ascii=False)
    _usage_state_js = _json.dumps(_usage_snapshot, ensure_ascii=False)
    page = """
<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>NGI AI Sales Assistant</title>
    <style>
        :root {
            --bg: #f4f7fb;
            --panel: #ffffff;
            --text: #132235;
            --muted: #516173;
            --accent: #0a6a4b;
            --accent-2: #134fa3;
            --border: #d4deea;
            --good: #0d8a47;
            --review: #8a5b00;
            --blocked: #1e4ca3;
            --gap: #b3261e;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Segoe UI, Tahoma, sans-serif;
            color: var(--text);
            background: radial-gradient(circle at top right, #dce9fb, transparent 42%),
                        radial-gradient(circle at top left, #d9f2ea, transparent 33%),
                        var(--bg);
            min-height: 100vh;
        }
        .wrap {
            max-width: 980px;
            margin: 20px auto;
            padding: 0 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .panel {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(19, 34, 53, 0.07);
            padding: 16px 20px;
            margin-bottom: 0;
        }
        .workflow-search { order: 1; }
        .workflow-quick { order: 2; }
        .workflow-results { order: 4; }
        .workflow-copy { order: 5; }
        .workflow-usage { order: 6; }
        .workflow-builders { order: 3; }
        .workflow-debug { order: 7; opacity: 0.9; }
        .sticky-search {
            position: sticky;
            top: 8px;
            z-index: 10;
        }
        h1 {
            margin: 0;
            font-size: 1.65rem;
        }
        h2 {
            margin: 0 0 10px;
            font-size: 1.05rem;
        }
        .subtitle {
            margin: 4px 0 0;
            color: var(--muted);
        }
        .row {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 10px;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
        }
        .grid-4 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 10px;
        }
        input[type=\"text\"],
        select {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 10px;
            font-size: 1rem;
            color: var(--text);
            background: #ffffff;
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
        .ghost-btn {
            background: var(--accent-2);
        }
        .section-actions {
            margin-top: 10px;
        }
        .mode-row {
            margin-top: 10px;
            display: grid;
            grid-template-columns: 170px 1fr;
            gap: 10px;
            align-items: center;
        }
        .mode-label {
            color: var(--muted);
            font-size: 0.9rem;
            font-weight: 600;
        }
        .mode-help {
            margin-top: 6px;
            color: var(--muted);
            font-size: 0.82rem;
        }
        .quick-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
        }
        .copy-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 10px;
        }
        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 8px;
        }
        .result-type {
            font-size: 0.82rem;
            text-transform: uppercase;
            color: var(--accent-2);
            font-weight: 700;
            letter-spacing: 0.03em;
        }
        .recent-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .recent-header h2 {
            margin: 0;
        }
        .header-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .small-btn {
            min-height: 32px;
            padding: 0 12px;
            border-radius: 8px;
            font-size: 0.88rem;
        }
        .small-btn:hover {
            filter: brightness(0.97);
        }
        .usage-grid {
            display: grid;
            grid-template-columns: 1.2fr 1.2fr 1fr;
            gap: 14px;
        }
        .usage-section {
            border: 1px solid var(--border);
            border-radius: 12px;
            background: #fbfdff;
            padding: 12px;
        }
        .usage-section h3 {
            margin: 0 0 10px;
            font-size: 0.98rem;
        }
        .usage-subsection + .usage-subsection {
            margin-top: 12px;
        }
        .usage-subsection h4 {
            margin: 0 0 8px;
            font-size: 0.88rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .usage-meta {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
        }
        .usage-kv {
            padding: 8px 10px;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: #fff;
        }
        .usage-kv .label {
            margin-bottom: 2px;
        }
        .recent-list {
            margin: 0;
            padding-left: 18px;
        }
        .recent-list li {
            margin: 6px 0;
        }
        .replay-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        .pin-btn {
            min-height: 28px;
            padding: 0 10px;
            border-radius: 8px;
            background: #edf4ff;
            color: var(--accent-2);
            border: 1px solid color-mix(in srgb, var(--accent-2), white 70%);
            font-size: 0.82rem;
        }
        .top-item,
        .category-item {
            margin: 6px 0;
        }
        .meta-count {
            color: var(--muted);
            font-size: 0.86rem;
        }
        .recent-btn {
            background: transparent;
            color: var(--accent-2);
            border: 0;
            cursor: pointer;
            font: inherit;
            padding: 0;
            min-height: 0;
            text-align: left;
            text-decoration: underline;
        }
        .chip-row {
            margin-top: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .chip-btn {
            min-height: 32px;
            padding: 0 12px;
            border: 1px solid var(--border);
            background: #f8fbff;
            color: var(--accent-2);
            font-size: 0.9rem;
            border-radius: 999px;
        }
        .chip-btn.active {
            border-color: var(--accent-2);
            background: #e8f1ff;
        }
        .chip-label {
            font-size: 0.82rem;
            color: var(--muted);
            padding: 0 4px;
            align-self: center;
            white-space: nowrap;
        }
        .context-chips-row {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid var(--border);
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        .empty-note {
            margin: 0;
            color: var(--muted);
        }
        .status {
            display: inline-block;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid transparent;
            margin-bottom: 8px;
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
        .field.meta-field {
            background: #f9fbff;
            opacity: 0.88;
        }
        .field.answer-field {
            border-color: #8db5f2;
            background: #f0f7ff;
            box-shadow: 0 0 0 2px #daeaff;
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
            line-height: 1.55;
        }
        #answerVal {
            padding: 4px 0;
        }
        .field + .field {
            margin-top: 10px;
        }
        .facts-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin: 4px 0 10px;
        }
        .fact-chip {
            padding: 2px 8px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #f4f8ff;
            font-size: 0.78rem;
            color: var(--muted);
            line-height: 1.35;
            white-space: nowrap;
        }
        .provider-summary {
            border: 1px solid var(--border);
            background: #f7fbff;
            border-radius: 10px;
            padding: 8px 10px;
            margin-top: 6px;
            font-size: 0.86rem;
            color: #1e2b45;
        }
        .provider-summary-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }
        .provider-count-badge {
            border: 1px solid var(--border);
            background: #e8f1ff;
            border-radius: 999px;
            padding: 2px 8px;
            font-size: 0.78rem;
            color: var(--accent-2);
            white-space: nowrap;
        }
        .provider-summary .label {
            margin-bottom: 2px;
        }
        .provider-points {
            margin: 4px 0 0;
            padding-left: 16px;
            max-height: 170px;
            overflow-y: auto;
            overscroll-behavior: contain;
            -webkit-overflow-scrolling: touch;
        }
        .provider-points li {
            margin: 2px 0;
        }
        .provider-toggle-btn {
            margin-top: 8px;
            min-height: 30px;
            padding: 0 10px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #f8fbff;
            color: var(--accent-2);
            font-size: 0.82rem;
        }
        .response-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0 0 12px;
        }
        .fast-repeat-actions {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 12px;
            padding: 10px;
            background: #f0f9ff;
            border: 1px solid var(--border);
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #e0e7ff;
            background: #fafbfe;
            margin: 12px 0;
            padding: 10px;
        #qaArabicBtn {
            background: #0f766e;
            font-weight: 700;
        }

        #qaArabicBtn:hover {
            background: #115b51;
        }
            background: #f8faff;
            border: 1px solid var(--border);
            border-radius: 10px;
        }
        .fast-repeat-actions button {
            min-height: 36px;
            padding: 0 10px;
            font-size: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.15s ease;
        }
        .fast-repeat-actions button:hover {
            filter: brightness(0.95);
            transform: translateY(-1px);
        }
        .response-chunks {
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .response-chunk {
            border: 1px solid var(--border);
            background: #fbfdff;
            border-radius: 10px;
            overflow: hidden;
        }
        .response-chunk summary {
            padding: 8px 10px;
            font-weight: 600;
            font-size: 0.86rem;
            color: #1b3555;
            cursor: pointer;
            list-style: none;
        }
        .response-chunk summary::-webkit-details-marker {
            display: none;
        }
        .response-chunk pre {
            padding: 0 10px 10px;
            font-size: 0.84rem;
            max-height: 220px;
            overflow-y: auto;
            overscroll-behavior: contain;
            -webkit-overflow-scrolling: touch;
        }
        .provider-cards {
            margin-top: 8px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        .provider-card {
            border: 1px solid var(--border);
            border-radius: 10px;
            background: #ffffff;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .provider-card-name {
            font-size: 0.86rem;
            font-weight: 700;
            color: #1a3354;
            line-height: 1.35;
        }
        .provider-card-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }
        .provider-card-chip {
            font-size: 0.74rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #f4f8ff;
            color: #415975;
            padding: 2px 7px;
        }
        .provider-card-actions {
            display: flex;
            gap: 6px;
        }
        .provider-card-actions button {
            min-height: 28px;
            width: auto;
            padding: 0 10px;
            font-size: 0.76rem;
            border-radius: 7px;
        }
        .mobile-action-bar {
            display: none;
        }
        .history-strip {
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid var(--border);
        }
        .history-strip .chip-label {
            margin-right: 4px;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .copy-preview {
            margin-top: 10px;
            border: 1px dashed var(--border);
            background: #fbfcff;
            border-radius: 10px;
            padding: 8px 10px;
        }
        .export-help {
                margin-top: 8px;
                margin-bottom: 6px;
                color: var(--muted);
                font-size: 0.78rem;
                line-height: 1.4;
            }
        .copy-preview pre {
            font-size: 0.83rem;
            line-height: 1.4;
            max-height: 132px;
            overflow-y: auto;
        }
        .copy-feedback {
            font-size: 0.88rem;
            color: var(--good);
            min-height: 1em;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        .copy-feedback.show {
            opacity: 1;
        }
        .copy-toast {
            position: fixed;
            right: 16px;
            bottom: 16px;
            background: #0e7490;
            color: #ffffff;
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 0.82rem;
            opacity: 0;
            transform: translateY(6px);
            pointer-events: none;
            transition: opacity 0.18s ease, transform 0.18s ease;
            z-index: 120;
        }
        .copy-toast.show {
            opacity: 1;
            transform: translateY(0);
        }
        .diagnostics-body[hidden] {
            display: none;
        }
        .collapsible-body[hidden] {
            display: none;
        }
        .collapsible-toggle {
            min-height: 28px;
            padding: 0 12px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 500;
            background: #f4f7fb;
            color: var(--muted);
            border: 1px solid var(--border);
        }
        .section-workspace-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            color: var(--muted);
            padding: 0 4px;
            opacity: 0.7;
        }
        @media (max-width: 700px) {
            .row { grid-template-columns: 1fr; }
            .grid-2 { grid-template-columns: 1fr; }
            .grid-3 { grid-template-columns: 1fr; }
            .grid-4 { grid-template-columns: 1fr; }
            .usage-grid { grid-template-columns: 1fr; }
            .usage-meta { grid-template-columns: 1fr; }
            .quick-grid { grid-template-columns: 1fr 1fr; }
            .copy-grid { grid-template-columns: 1fr; gap: 6px; padding: 8px; }
            .mode-row { grid-template-columns: 1fr; }
            .fast-repeat-actions { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; padding: 8px; }
            .fast-repeat-actions button { min-height: 32px; font-size: 0.70rem; padding: 0 6px; }
            #mobileArabicBtn { background: #0f766e; font-weight: 700; }
            button { width: 100%; }
            .panel { padding: 14px; }
            .field { padding: 9px 10px; }
            #answerVal { max-height: 280px; overflow-y: auto; }
            .recent-header {
                align-items: stretch;
                flex-direction: column;
            }
            .chip-row {
                gap: 6px;
            }
            .chip-btn {
                width: auto;
            }
            .copy-toast {
                left: 12px;
                right: 12px;
                bottom: 12px;
                text-align: center;
            }
            .provider-summary { font-size: 0.84rem; }
            .provider-points { max-height: 220px; }
            .provider-cards { grid-template-columns: 1fr; }
            .fast-repeat-actions { grid-template-columns: 1fr 1fr; }
            .mobile-action-bar {
                display: grid;
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: 6px;
                position: fixed;
                left: 10px;
                right: 10px;
                bottom: calc(12px + env(safe-area-inset-bottom, 0px));
                z-index: 110;
                padding: 7px;
                border-radius: 12px;
                border: 1px solid var(--border);
                background: rgba(255, 255, 255, 0.96);
                backdrop-filter: blur(3px);
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.14);
            }
            .mobile-action-bar button {
                min-height: 34px;
                padding: 0 4px;
                font-size: 0.74rem;
                border-radius: 8px;
                white-space: nowrap;
                line-height: 1.2;
            }
            body {
                padding-bottom: calc(112px + env(safe-area-inset-bottom, 0px));
                overscroll-behavior-y: contain;
            }
        }
    </style>
</head>
<body>
    <div class=\"wrap\">
        <div class="panel sticky-search">
            <h1>NGI AI Sales Assistant</h1>
            <p class=\"subtitle\">Operational command center for deterministic plan and provider queries.</p>
            <form id=\"askForm\" class=\"row\">
                <input id=\"question\" type=\"text\" placeholder=\"Ask about plans, providers, comparisons...\" />
                <button id=\"askBtn\" type=\"submit\">Search</button>
            </form>
            <div class="mode-row">
                <span class="mode-label">Viewing Mode</span>
                <select id="responseMode" aria-label="Response mode">
                    <option value="detailed">Detailed</option>
                    <option value="whatsapp">WhatsApp</option>
                    <option value="arabic">Arabic</option>
                    <option value="compact">Compact</option>
                </select>
            </div>
            <p class="mode-help">Viewing mode controls on-screen rendering only. Export buttons apply separate format transforms.</p>
        </div>

        <div class=\"panel workflow-quick\">
            <h2>Quick Actions</h2>
            <div class=\"quick-grid\">
                <button id=\"qaSummarize\" class=\"ghost-btn\" type=\"button\">Summarize Plan</button>
                <button id=\"qaCompare\" class=\"ghost-btn\" type=\"button\">Compare Plans</button>
                <button id=\"qaProvider\" class=\"ghost-btn\" type=\"button\">Provider Search</button>
                <button id=\"qaWhatsapp\" class=\"ghost-btn\" type=\"button\">WhatsApp Summary</button>
                <button id=\"qaArabic\" class=\"ghost-btn\" type=\"button\">Arabic Summary</button>
                <button id=\"qaNetwork\" class=\"ghost-btn\" type=\"button\">Network Lookup</button>
            </div>
            <div class=\"history-strip\">
                <span class=\"chip-label\">Recent Comparisons:</span>
                <span id=\"comparisonHistoryChips\" class=\"chip-row\"></span>
                </div>
                <div class=\"history-strip\">
                    <span class=\"chip-label\">Recent Plans:</span>
                    <span id=\"plansHistoryChips\" class=\"chip-row\"></span>
                </div>
        </div>

        <div class=\"panel workflow-usage\">
            <div class="recent-header">
                <h2>Usage Intelligence</h2>
                <div class="header-actions">
                    <button id="usageToggleBtn" class="collapsible-toggle" type="button">Show</button>
                    <button id="clearRecentBtn" class="ghost-btn small-btn" type="button">Clear Recent Searches</button>
                    <button id="clearPinnedBtn" class="ghost-btn small-btn" type="button">Clear Pinned</button>
                </div>
            </div>
            <div id="usageBody" class="collapsible-body" hidden>
            <div class="usage-grid">
                <div class="usage-section">
                    <h3>Recent Searches</h3>
                    <ul id="recentList" class="recent-list"></ul>
                    <p id="recentEmpty" class="empty-note">No successful searches yet.</p>
                </div>
                <div class="usage-section">
                    <h3>Pinned Searches</h3>
                    <ul id="pinnedList" class="recent-list"></ul>
                    <p id="pinnedEmpty" class="empty-note">No pinned searches yet.</p>
                </div>
                <div class="usage-section usage-summary">
                    <h3>Operational Context</h3>
                    <div class="usage-meta">
                        <div class="usage-kv"><span class="label">Last City</span><div id="lastCityVal">-</div></div>
                        <div class="usage-kv"><span class="label">Last Plan</span><div id="lastPlanVal">-</div></div>
                    </div>
                    <div class="usage-subsection">
                        <h4>Top Repeated Searches</h4>
                        <ul id="topList" class="recent-list"></ul>
                        <p id="topEmpty" class="empty-note">No repeated searches yet.</p>
                    </div>
                    <div class="usage-subsection">
                        <h4>Query Categories</h4>
                        <ul id="categoryList" class="recent-list"></ul>
                        <p id="categoryEmpty" class="empty-note">No category data yet.</p>
                    </div>
                </div>
            </div>
            </div>
        </div>

        <div class=\"panel workflow-builders\">
            <h2>Plan Quick Search</h2>
            <form id=\"planForm\">
                <div class=\"row\">
                    <select id=\"planName\">
                        <option value=\"Classic 1\">Classic 1</option>
                        <option value=\"Classic 1R\">Classic 1R</option>
                        <option value=\"Classic 2\">Classic 2</option>
                        <option value=\"Classic 2R\">Classic 2R</option>
                        <option value=\"Classic 3\">Classic 3</option>
                        <option value=\"Classic 4\">Classic 4</option>
                        <option value=\"Prime 1\">Prime 1</option>
                        <option value=\"Prime 2\">Prime 2</option>
                        <option value=\"Remedy 2\">Remedy 2</option>
                        <option value=\"Remedy 3\">Remedy 3</option>
                        <option value=\"Remedy 4\">Remedy 4</option>
                        <option value=\"Remedy 5\">Remedy 5</option>
                        <option value=\"Remedy 6\">Remedy 6</option>
                    </select>
                    <button class=\"ghost-btn\" type=\"submit\">Summarize Plan</button>
                </div>
            </form>
        </div>

        <div class=\"panel workflow-builders\">
            <h2>Provider Search</h2>
            <form id=\"providerForm\">
                <div class=\"grid-4\">
                    <select id=\"providerPlan\">
                        <option value=\"Classic 1\">Classic 1</option>
                        <option value=\"Classic 1R\">Classic 1R</option>
                        <option value=\"Classic 2\">Classic 2</option>
                        <option value=\"Classic 2R\">Classic 2R</option>
                        <option value=\"Classic 3\">Classic 3</option>
                        <option value=\"Classic 4\">Classic 4</option>
                        <option value=\"Prime 1\">Prime 1</option>
                        <option value=\"Prime 2\">Prime 2</option>
                        <option value=\"Remedy 2\">Remedy 2</option>
                        <option value=\"Remedy 3\">Remedy 3</option>
                        <option value=\"Remedy 4\">Remedy 4</option>
                        <option value=\"Remedy 5\">Remedy 5</option>
                        <option value=\"Remedy 6\">Remedy 6</option>
                    </select>
                    <select id=\"providerCity\">
                        <option value=\"\">Select City</option>
                        <option value=\"Dubai\">Dubai</option>
                        <option value=\"Sharjah\">Sharjah</option>
                        <option value=\"Abu Dhabi\">Abu Dhabi</option>
                        <option value=\"Ajman\">Ajman</option>
                        <option value=\"Al Ain\">Al Ain</option>
                        <option value=\"Ras Al Khaimah\">Ras Al Khaimah</option>
                        <option value=\"Fujairah\">Fujairah</option>
                        <option value=\"Umm Al Quwain\">Umm Al Quwain</option>
                    </select>
                    <select id=\"providerArea\" disabled>
                        <option value=\"\">Select Area (Optional)</option>
                    </select>
                    <select id=\"providerType\">
                        <option value=\"hospital\">Hospital</option>
                        <option value=\"clinic\">Clinic</option>
                        <option value=\"pharmacy\">Pharmacy</option>
                        <option value=\"lab\">Lab</option>
                    </select>
                </div>
                <div class="chip-row" id="providerTypeChips">
                    <span class="chip-label">Type:</span>
                    <button type="button" class="chip-btn" data-provider-type="hospital">Hospital</button>
                    <button type="button" class="chip-btn" data-provider-type="clinic">Clinic</button>
                    <button type="button" class="chip-btn" data-provider-type="pharmacy">Pharmacy</button>
                    <button type="button" class="chip-btn" data-provider-type="lab">Lab</button>
                </div>
                <div class="chip-row" id="cityFilterChips">
                    <span class="chip-label">City:</span>
                    <button type="button" class="chip-btn" data-city="Dubai">Dubai</button>
                    <button type="button" class="chip-btn" data-city="Sharjah">Sharjah</button>
                    <button type="button" class="chip-btn" data-city="Abu Dhabi">Abu Dhabi</button>
                </div>
                <div class="chip-row" id="planFilterChips">
                    <span class="chip-label">Plan:</span>
                    <button type="button" class="chip-btn" data-plan="Remedy 5">Remedy 5</button>
                    <button type="button" class="chip-btn" data-plan="Remedy 6">Remedy 6</button>
                    <button type="button" class="chip-btn" data-plan="Classic 1">Classic 1</button>
                    <button type="button" class="chip-btn" data-plan="Prime 1">Prime 1</button>
                </div>
                <div class="context-chips-row" id="contextChips" style="display:none"></div>
                <div class=\"section-actions\">
                    <button class=\"ghost-btn\" type=\"submit\">Search Providers</button>
                </div>
            </form>
        </div>

        <div class=\"panel workflow-builders\">
            <h2>Comparison Search</h2>
            <form id=\"compareForm\">
                <div class=\"grid-2\">
                    <select id=\"planA\">
                        <option value=\"Classic 1\">Classic 1</option>
                        <option value=\"Classic 1R\">Classic 1R</option>
                        <option value=\"Classic 2\">Classic 2</option>
                        <option value=\"Classic 2R\">Classic 2R</option>
                        <option value=\"Classic 3\">Classic 3</option>
                        <option value=\"Classic 4\">Classic 4</option>
                        <option value=\"Prime 1\">Prime 1</option>
                        <option value=\"Prime 2\">Prime 2</option>
                        <option value=\"Remedy 2\">Remedy 2</option>
                        <option value=\"Remedy 3\">Remedy 3</option>
                        <option value=\"Remedy 4\">Remedy 4</option>
                        <option value=\"Remedy 5\">Remedy 5</option>
                        <option value=\"Remedy 6\">Remedy 6</option>
                    </select>
                    <select id=\"planB\">
                        <option value=\"Classic 1\">Classic 1</option>
                        <option value=\"Classic 1R\">Classic 1R</option>
                        <option value=\"Classic 2\">Classic 2</option>
                        <option value=\"Classic 2R\">Classic 2R</option>
                        <option value=\"Classic 3\">Classic 3</option>
                        <option value=\"Classic 4\">Classic 4</option>
                        <option value=\"Prime 1\">Prime 1</option>
                        <option value=\"Prime 2\">Prime 2</option>
                        <option value=\"Remedy 2\">Remedy 2</option>
                        <option value=\"Remedy 3\">Remedy 3</option>
                        <option value=\"Remedy 4\">Remedy 4</option>
                        <option value=\"Remedy 5\">Remedy 5</option>
                        <option value=\"Remedy 6\">Remedy 6</option>
                    </select>
                </div>
                <div class=\"section-actions\">
                    <button class=\"ghost-btn\" type=\"submit\">Compare</button>
                </div>
            </form>
        </div>

        <div class=\"panel workflow-results\">
            <h2>Results Area</h2>
            <div id=\"result\" style=\"display:none\">
                <div class=\"result-header\">
                    <div id=\"statusTag\" class=\"status\"></div>
                    <div id=\"resultCardType\" class=\"result-type\">Result</div>
                </div>
                <div id=\"resultFacts\" class=\"facts-row\"></div>
                <div class=\"field meta-field\"><span class=\"label\">Section</span><div id=\"resultTitleVal\">Operational Result</div></div>
                <div class=\"field meta-field\"><span class=\"label\">Result Type</span><div id=\"intentVal\">-</div></div>
                <div class=\"field\"><span class=\"label\">Plan / Scope</span><div id=\"planVal\">-</div></div>
                <div id=\"providerSummary\" class=\"provider-summary\" style=\"display:none\"></div>
                <div id=\"providerCards\" class=\"provider-cards\" style=\"display:none\"></div>
                <div id=\"responseChunks\" class=\"response-chunks\" style=\"display:none\"></div>
                <div class=\"field answer-field\"><span class=\"label\">Final Answer</span><pre id=\"answerVal\"></pre></div>
                <div class=\"fast-repeat-actions\">
                    <button id=\"fastCopyBtn\" type=\"button\" class=\"ghost-btn\">Copy</button>
                    <button id=\"fastWhatsappBtn\" type=\"button\" class=\"ghost-btn\">WhatsApp</button>
                    <button id=\"fastArabicBtn\" type=\"button\" class=\"ghost-btn\">Arabic</button>
                    <button id=\"fastCompactBtn\" type=\"button\" class=\"ghost-btn\">Compact</button>
                        <button id=\"fastCompareThisBtn\" type=\"button\" class=\"ghost-btn\" style=\"display:none\">Compare This</button>
                        <button id=\"fastCompareAgainBtn\" type=\"button\" class=\"ghost-btn\">Compare Again</button>
                </div>
            </div>
        </div>

        <div class=\"panel workflow-copy\">
            <h2>Export / Copy Formats</h2>
            <div class=\"copy-grid\">
                <button id=\"copyResponseBtn\" class=\"ghost-btn\" type=\"button\">Copy Response</button>
                <button id=\"copyWhatsappBtn\" class=\"ghost-btn\" type=\"button\">Copy as WhatsApp</button>
                <button id=\"copyArabicBtn\" class=\"ghost-btn\" type=\"button\">Copy as Arabic</button>
                <button id=\"copyCompactBtn\" class=\"ghost-btn\" type=\"button\">Copy as Compact</button>
            </div>
            <div class=\"export-help\">Export actions transform the latest answer into the selected target format.</div>
            <span id=\"copyFeedback\" class=\"copy-feedback\">Copied</span>
            <div id=\"exportPreviewBody\" class=\"collapsible-body\" hidden>
            <div class=\"copy-preview\">
                <span id=\"copyPreviewLabel\" class=\"label\">Export Preview</span>
                <pre id=\"copyPreviewVal\">-</pre>
            </div>
            </div>
        </div>

        <div class=\"panel workflow-debug\">
            <h2>Debug / Telemetry</h2>
            <button id=\"toggleDiagnosticsBtn\" class=\"ghost-btn small-btn\" type=\"button\">Show Diagnostics</button>
            <div id=\"diagnosticsBody\" class=\"diagnostics-body\" hidden>
            <div class=\"usage-meta\">
                <div class=\"usage-kv\"><span class=\"label\">Last Query</span><div id=\"dbgQuery\">-</div></div>
                <div class=\"usage-kv\"><span class=\"label\">Mode</span><div id=\"dbgMode\">Detailed</div></div>
                <div class=\"usage-kv\"><span class=\"label\">Formatter</span><div id=\"dbgFormatter\">None</div></div>
                <div class=\"usage-kv\"><span class=\"label\">Status</span><div id=\"dbgStatus\">-</div></div>
            </div>
            <div class=\"usage-meta\">
                <div class=\"usage-kv\"><span class=\"label\">Top Quick Action</span><div id=\"dbgQuickTop\">-</div></div>
                <div class=\"usage-kv\"><span class=\"label\">Top Response Mode</span><div id=\"dbgModeTop\">-</div></div>
                <div class=\"usage-kv\"><span class=\"label\">Top Copy Action</span><div id=\"dbgCopyTop\">-</div></div>
                <div class=\"usage-kv\"><span class=\"label\">Provider / Compare</span><div id=\"dbgFlowTop\">0 / 0</div></div>
            </div>
            <div class=\"chip-row\" id=\"frictionTagRow\">
                <span class=\"chip-label\">Tag Friction:</span>
                <button type=\"button\" class=\"chip-btn\" data-friction-tag=\"GOOD\">GOOD</button>
                <button type=\"button\" class=\"chip-btn\" data-friction-tag=\"REVIEW\">REVIEW</button>
                <button type=\"button\" class=\"chip-btn\" data-friction-tag=\"SLOW\">SLOW</button>
                <button type=\"button\" class=\"chip-btn\" data-friction-tag=\"CONFUSING\">CONFUSING</button>
                <button type=\"button\" class=\"chip-btn\" data-friction-tag=\"REPEATED\">REPEATED</button>
                <button type=\"button\" class=\"chip-btn\" data-friction-tag=\"BLOCKED_OK\">BLOCKED_OK</button>
            </div>
            </div>
        </div>
    </div>
    <div class=\"mobile-action-bar\" id=\"mobileActionBar\">
        <button id=\"mobileAskBtn\" type=\"button\">Ask</button>
        <button id=\"mobileCompareBtn\" type=\"button\">Compare</button>
        <button id=\"mobileProvidersBtn\" type=\"button\">Providers</button>
        <button id=\"mobileWhatsappBtn\" type=\"button\">WhatsApp</button>
        <button id=\"mobileArabicBtn\" type=\"button\">Arabic</button>
    </div>
    <div id=\"copyToast\" class=\"copy-toast\" aria-live=\"polite\">Copied</div>

    <script>
        const initialRecent = __INITIAL_RECENT_SEARCHES__;
        const initialUsage = __INITIAL_USAGE_STATE__;
        const form = document.getElementById('askForm');
        const planForm = document.getElementById('planForm');
        const providerForm = document.getElementById('providerForm');
        const compareForm = document.getElementById('compareForm');
        const questionEl = document.getElementById('question');
        const planNameEl = document.getElementById('planName');
        const providerPlanEl = document.getElementById('providerPlan');
        const providerCityEl = document.getElementById('providerCity');
        const providerAreaEl = document.getElementById('providerArea');
        const providerTypeEl = document.getElementById('providerType');
        const planAEl = document.getElementById('planA');
        const planBEl = document.getElementById('planB');
        const responseModeEl = document.getElementById('responseMode');
        const askBtn = document.getElementById('askBtn');
        const recentListEl = document.getElementById('recentList');
        const recentEmptyEl = document.getElementById('recentEmpty');
        const pinnedListEl = document.getElementById('pinnedList');
        const pinnedEmptyEl = document.getElementById('pinnedEmpty');
        const topListEl = document.getElementById('topList');
        const topEmptyEl = document.getElementById('topEmpty');
        const categoryListEl = document.getElementById('categoryList');
        const categoryEmptyEl = document.getElementById('categoryEmpty');
        const clearRecentBtn = document.getElementById('clearRecentBtn');
        const clearPinnedBtn = document.getElementById('clearPinnedBtn');
        const resultEl = document.getElementById('result');
        const statusTag = document.getElementById('statusTag');
        const resultCardTypeEl = document.getElementById('resultCardType');
        const resultFactsEl = document.getElementById('resultFacts');
        const resultTitleVal = document.getElementById('resultTitleVal');
        const intentVal = document.getElementById('intentVal');
        const planVal = document.getElementById('planVal');
        const providerSummaryEl = document.getElementById('providerSummary');
        const providerCardsEl = document.getElementById('providerCards');
        const responseChunksEl = document.getElementById('responseChunks');
        const answerVal = document.getElementById('answerVal');
        const copyResponseBtn = document.getElementById('copyResponseBtn');
        const copyWhatsappBtn = document.getElementById('copyWhatsappBtn');
        const copyArabicBtn = document.getElementById('copyArabicBtn');
        const copyCompactBtn = document.getElementById('copyCompactBtn');
        const copyFeedback = document.getElementById('copyFeedback');
        const copyPreviewLabelEl = document.getElementById('copyPreviewLabel');
        const copyPreviewVal = document.getElementById('copyPreviewVal');
        const copyToast = document.getElementById('copyToast');
        const qaSummarizeBtn = document.getElementById('qaSummarize');
        const qaCompareBtn = document.getElementById('qaCompare');
        const qaProviderBtn = document.getElementById('qaProvider');
        const qaWhatsappBtn = document.getElementById('qaWhatsapp');
        const qaArabicBtn = document.getElementById('qaArabic');
        const qaNetworkBtn = document.getElementById('qaNetwork');
        const comparisonHistoryChipsEl = document.getElementById('comparisonHistoryChips');
        const fastCopyBtn = document.getElementById('fastCopyBtn');
        const fastWhatsappBtn = document.getElementById('fastWhatsappBtn');
        const fastArabicBtn = document.getElementById('fastArabicBtn');
        const fastCompactBtn = document.getElementById('fastCompactBtn');
        const fastCompareAgainBtn = document.getElementById('fastCompareAgainBtn');
        const mobileAskBtn = document.getElementById('mobileAskBtn');
        const mobileCompareBtn = document.getElementById('mobileCompareBtn');
        const mobileProvidersBtn = document.getElementById('mobileProvidersBtn');
        const mobileWhatsappBtn = document.getElementById('mobileWhatsappBtn');
        const mobileArabicBtn = document.getElementById('mobileArabicBtn');
        const mobileActionBar = document.getElementById('mobileActionBar');
        const dbgQueryEl = document.getElementById('dbgQuery');
        const dbgModeEl = document.getElementById('dbgMode');
        const dbgFormatterEl = document.getElementById('dbgFormatter');
        const dbgStatusEl = document.getElementById('dbgStatus');
        const dbgQuickTopEl = document.getElementById('dbgQuickTop');
        const dbgModeTopEl = document.getElementById('dbgModeTop');
        const dbgCopyTopEl = document.getElementById('dbgCopyTop');
        const dbgFlowTopEl = document.getElementById('dbgFlowTop');
        const frictionTagRowEl = document.getElementById('frictionTagRow');
        const toggleDiagnosticsBtn = document.getElementById('toggleDiagnosticsBtn');
        const diagnosticsBodyEl = document.getElementById('diagnosticsBody');
        const usageToggleBtnEl = document.getElementById('usageToggleBtn');
        const usageBodyEl = document.getElementById('usageBody');
        const exportPreviewBodyEl = document.getElementById('exportPreviewBody');
        const lastCityVal = document.getElementById('lastCityVal');
        const lastPlanVal = document.getElementById('lastPlanVal');
        const providerTypeChipsEl = document.getElementById('providerTypeChips');
        const cityFilterChipsEl = document.getElementById('cityFilterChips');
        const planFilterChipsEl = document.getElementById('planFilterChips');
        const contextChipsEl = document.getElementById('contextChips');
        const fastCompareThisBtn = document.getElementById('fastCompareThisBtn');
        const plansHistoryChipsEl = document.getElementById('plansHistoryChips');
        const LS_KEY = 'ngi_operator_ui_state_v2';
        const SS_LAST_SEARCH = 'ngi_operator_last_search_v2';
        const LS_RECENT_COMPARISONS = 'ngi_recent_comparisons_v1';
        const LS_RECENT_PLANS = 'ngi_recent_plans_v1';
        let recentSearches = Array.isArray(initialRecent) ? initialRecent : [];
        let usageState = initialUsage && typeof initialUsage === 'object' ? initialUsage : {
            recent_queries: [],
            pinned_queries: [],
            top_queries: [],
            last_city: '',
            last_plan: '',
            query_categories: [],
            operator_metrics: {
                quick_actions: [],
                response_modes: [],
                copy_actions: [],
                workflow_actions: [],
                friction_tags: [],
                comparison_queries: 0,
                provider_lookup_queries: 0,
                repeated_queries: 0,
            },
        };
        let _lastCity = (usageState.last_city || '').trim();
        let _lastProviderType = '';
        let _lastPlan = (usageState.last_plan || '').trim();
        let _lastPayload = null;
        let _lastQuestion = '';
        let _lastRenderedText = '';
        let _lastResultContext = {
            type: 'unsupported',
            intent: 'unsupported',
            ok: false,
            planName: '',
            providerLines: [],
            isProviderResult: false,
            isComparison: false,
            isNetworkLookup: false,
        };
        let _recentComparisons = [];
        let _lastDurationMs = 0;
        let _diagnosticsOpen = false;
        const areaOptionsByCityRaw = __AREA_OPTIONS_BY_CITY__;
        const areaOptionsByCity = (areaOptionsByCityRaw && typeof areaOptionsByCityRaw === 'object') ? areaOptionsByCityRaw : {};

        function refreshAreaOptions() {
            const city = providerCityEl.value.trim();
            providerAreaEl.innerHTML = '';

            const placeholder = document.createElement('option');
            placeholder.value = '';
            placeholder.textContent = 'Select Area (Optional)';
            providerAreaEl.appendChild(placeholder);

            if (!city) {
                providerAreaEl.disabled = true;
                providerAreaEl.value = '';
                return;
            }

            const areas = areaOptionsByCity[city] || [];
            for (const area of areas) {
                const option = document.createElement('option');
                option.value = area;
                option.textContent = area;
                providerAreaEl.appendChild(option);
            }

            providerAreaEl.disabled = false;
            providerAreaEl.value = '';
        }

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

        function hasArabic(text) {
            return /[\u0600-\u06FF]/.test(text || '');
        }

        function activeMode() {
            return responseModeEl ? responseModeEl.value : 'detailed';
        }

        function outputModeForUiMode(mode) {
            // Keep detailed mode on raw deterministic answer path (no formatter call).
            if (mode === 'detailed') return null;
            if (mode === 'whatsapp') return 'whatsapp_summary';
            // Arabic/compact are local presentation transforms, not backend formatter modes.
            if (mode === 'arabic') return null;
            if (mode === 'compact') return null;
            return null;
        }

        function classifyCardType(intent, question) {
            const i = (intent || '').toLowerCase();
            const q = (question || '').toLowerCase();
            if (i.includes('comparison') || q.includes('compare')) return { label: 'Comparison Result Card', section: 'Comparison Result' };
            if (i.includes('network') || q.includes('provider') || q.includes('network')) return { label: 'Provider Result Card', section: 'Provider Result' };
            if (i.includes('plan') || q.includes('summarize')) return { label: 'Plan Summary Card', section: 'Plan Summary' };
            return { label: 'Result Card', section: 'Operational Result' };
        }

        function chooseRenderedText(mode, payload) {
            const answer = payload && payload.answer ? payload.answer : {};
            const intent = String(answer.intent || '').toLowerCase();
            const raw = String(answer.message || payload.error || '');
            const formatted = String(payload.display_answer || '');
            // Preserve full deterministic comparison body; never collapse it via formatter output.
            if (intent === 'plan_comparison') {
                if (mode === 'compact') return compactText(raw);
                if (mode === 'arabic') {
                    if (hasArabic(raw)) return normalizeArabicSpacing(raw);
                    return raw;
                }
                return raw;
            }
            if (mode === 'detailed') return formatted || raw;
            if (mode === 'whatsapp') return formatted || raw;
            if (mode === 'compact') return formatted || compactText(raw);
            if (mode === 'arabic') {
                if (hasArabic(formatted)) return formatted;
                if (hasArabic(raw)) return raw;
                return 'هذه المعلومات غير متاحة حالياً أو أن الاستعلام غير مدعوم.';
            }
            return raw || formatted;
        }

        function isComparisonFlow(intent, question) {
            const i = String(intent || '').toLowerCase();
            const q = String(question || '').toLowerCase();
            return i === 'plan_comparison' || q.includes('compare') || q.includes('comparison') || q.includes('قارن');
        }

        function isPlanFlow(intent) {
            const i = String(intent || '').toLowerCase();
            return i === 'plan_core' || i === 'plan_summary' || i === 'plan_field';
        }

        function isProviderListFlow(intent, question, extracted) {
            const i = String(intent || '').toLowerCase();
            const q = String(question || '').toLowerCase();
            const hasProviders = Array.isArray(extracted && extracted.providerLines) && extracted.providerLines.length > 0;
            return hasProviders && (Boolean(extracted && extracted.isProviderResult) || i.includes('network_city_type') || (q.includes('list ') && q.includes('providers in')));
        }

        function isNetworkLookupFlow(intent, question, extracted) {
            const i = String(intent || '').toLowerCase();
            const q = String(question || '').toLowerCase();
            const providerListFlow = isProviderListFlow(intent, question, extracted);
            if (providerListFlow) {
                return false;
            }
            return i.includes('network') || q.includes('network lookup') || (q.includes('network') && !q.includes('providers in'));
        }

        function buildResultContext(question, payload, extracted) {
            const answer = payload && payload.answer ? payload.answer : {};
            const intent = String(answer.intent || 'unsupported');
            const ok = Boolean(answer.ok);
            const planName = String(answer.plan_name || '').trim();
            const comparison = isComparisonFlow(intent, question);
            const providerList = isProviderListFlow(intent, question, extracted);
            const networkLookup = isNetworkLookupFlow(intent, question, extracted);
            let type = 'unsupported';
            if (!ok) {
                type = 'unsupported';
            } else if (comparison) {
                type = 'comparison';
            } else if (providerList) {
                type = 'provider_list';
            } else if (networkLookup) {
                type = 'network_lookup';
            } else if (isPlanFlow(intent)) {
                type = 'plan';
            } else {
                type = 'generic';
            }

            return {
                type: type,
                intent: intent,
                ok: ok,
                planName: planName,
                providerLines: Array.isArray(extracted && extracted.providerLines) ? extracted.providerLines.slice() : [],
                isProviderResult: Boolean(extracted && extracted.isProviderResult),
                isComparison: comparison,
                isNetworkLookup: networkLookup,
            };
        }

        function actionRulesForContext(ctx) {
            const t = String(ctx && ctx.type || 'unsupported');
            if (t === 'plan') {
                return { response: true, whatsapp: true, arabic: true, compact: true, compare: true, compareAgain: true };
            }
            if (t === 'comparison') {
                return { response: true, whatsapp: true, arabic: true, compact: true, compare: false, compareAgain: true };
            }
            if (t === 'provider_list') {
                return { response: true, whatsapp: true, arabic: false, compact: true, compare: false, compareAgain: false };
            }
            if (t === 'network_lookup') {
                return { response: true, whatsapp: true, arabic: false, compact: true, compare: false, compareAgain: false };
            }
            if (t === 'generic') {
                return { response: true, whatsapp: false, arabic: false, compact: false, compare: false, compareAgain: false };
            }
            return { response: true, whatsapp: false, arabic: false, compact: false, compare: false, compareAgain: false };
        }

        function _setActionVisible(el, visible) {
            if (!el) {
                return;
            }
            el.style.display = visible ? '' : 'none';
        }

        function _setActionLabel(el, text) {
            if (!el) {
                return;
            }
            el.textContent = text;
        }

        function applyActionVisibility(ctx) {
            const rules = actionRulesForContext(ctx);
            _setActionVisible(copyResponseBtn, rules.response);
            _setActionVisible(copyWhatsappBtn, rules.whatsapp);
            _setActionVisible(copyArabicBtn, rules.arabic);
            _setActionVisible(copyCompactBtn, rules.compact);

            _setActionVisible(fastCopyBtn, rules.response);
            _setActionVisible(fastWhatsappBtn, rules.whatsapp);
            _setActionVisible(fastArabicBtn, rules.arabic);
            _setActionVisible(fastCompactBtn, rules.compact);
            _setActionVisible(fastCompareThisBtn, rules.compare);
            _setActionVisible(fastCompareAgainBtn, rules.compareAgain);

            _setActionVisible(mobileWhatsappBtn, rules.whatsapp);
            _setActionVisible(mobileArabicBtn, rules.arabic);

            const type = String(ctx && ctx.type || 'unsupported');
            if (type === 'provider_list') {
                _setActionLabel(copyResponseBtn, 'Copy Providers');
                _setActionLabel(copyWhatsappBtn, 'Copy Providers as WhatsApp');
                _setActionLabel(copyCompactBtn, 'Copy as Compact Provider List');
                _setActionLabel(fastCopyBtn, 'Copy Providers');
            } else if (type === 'comparison') {
                _setActionLabel(copyResponseBtn, 'Copy Comparison');
                _setActionLabel(copyWhatsappBtn, 'Copy Comparison as WhatsApp');
                _setActionLabel(copyCompactBtn, 'Copy as Compact Comparison');
                _setActionLabel(fastCopyBtn, 'Copy Comparison');
            } else if (type === 'network_lookup') {
                _setActionLabel(copyResponseBtn, 'Copy Network');
                _setActionLabel(copyWhatsappBtn, 'Copy Network as WhatsApp');
                _setActionLabel(copyCompactBtn, 'Copy as Compact Network');
                _setActionLabel(fastCopyBtn, 'Copy Network');
            } else {
                _setActionLabel(copyResponseBtn, 'Copy Response');
                _setActionLabel(copyWhatsappBtn, 'Copy as WhatsApp');
                _setActionLabel(copyCompactBtn, 'Copy as Compact');
                _setActionLabel(fastCopyBtn, 'Copy');
            }
        }

        function refreshMobileActionVisibility() {
            const isMobile = window.innerWidth <= 700;
            _setActionVisible(mobileActionBar, isMobile);
            if (!isMobile) {
                return;
            }
            const rules = actionRulesForContext(_lastResultContext || { type: 'unsupported' });
            _setActionVisible(mobileWhatsappBtn, rules.whatsapp);
            _setActionVisible(mobileArabicBtn, rules.arabic);
        }

        function compactText(text) {
            const lines = String(text || '').split(/\\r?\\n/).map(function (line) { return line.trim(); }).filter(Boolean);
            return lines.slice(0, 5).join('\\n');
        }

        function normalizeArabicSpacing(text) {
            return String(text || '')
                .replace(/\s+/g, ' ')
                .replace(/\s+([،؛:!?\.])/g, '$1')
                .trim();
        }

        function safeSetStorage(storage, key, value) {
            try {
                storage.setItem(key, value);
            } catch (_err) {
                // Local persistence is optional and should not block operator flow.
            }
        }

        function safeGetStorage(storage, key) {
            try {
                return storage.getItem(key);
            } catch (_err) {
                return null;
            }
        }

        function persistUiState(lastQuickAction) {
            let quickAction = '';
            if (typeof lastQuickAction === 'string') {
                quickAction = lastQuickAction;
            } else {
                const previous = safeGetStorage(window.localStorage, LS_KEY);
                if (previous) {
                    try {
                        const parsed = JSON.parse(previous);
                        quickAction = String(parsed.lastQuickAction || '');
                    } catch (_err) {
                        quickAction = '';
                    }
                }
            }
            const state = {
                responseMode: responseModeEl.value,
                question: questionEl.value,
                planName: planNameEl.value,
                planA: planAEl.value,
                planB: planBEl.value,
                providerPlan: providerPlanEl.value,
                providerCity: providerCityEl.value,
                providerArea: providerAreaEl.value,
                providerType: providerTypeEl.value,
                lastQuickAction: quickAction
            };
            safeSetStorage(window.localStorage, LS_KEY, JSON.stringify(state));
        }

        function restoreUiState() {
            const raw = safeGetStorage(window.localStorage, LS_KEY);
            if (!raw) {
                const sessionLast = safeGetStorage(window.sessionStorage, SS_LAST_SEARCH);
                if (sessionLast) {
                    questionEl.value = sessionLast;
                }
                return;
            }

            try {
                const state = JSON.parse(raw);
                responseModeEl.value = state.responseMode || responseModeEl.value;
                questionEl.value = state.question || questionEl.value;
                planNameEl.value = state.planName || planNameEl.value;
                planAEl.value = state.planA || planAEl.value;
                planBEl.value = state.planB || planBEl.value;
                providerPlanEl.value = state.providerPlan || providerPlanEl.value;
                providerCityEl.value = state.providerCity || providerCityEl.value;
                providerTypeEl.value = state.providerType || providerTypeEl.value;
                refreshAreaOptions();
                providerAreaEl.value = state.providerArea || providerAreaEl.value;
            } catch (_err) {
                // Ignore stale local state and continue with defaults.
            }
        }

        function _splitProviderMessage(message) {
            const lines = String(message || '').split(/\\r?\\n/).map(function (line) { return line.trim(); }).filter(Boolean);
            const providerLines = [];
            const nonProviderLines = [];

            function isProviderDiagnosticLine(line) {
                const lowered = String(line || '').toLowerCase();
                if (!lowered) {
                    return false;
                }
                return (
                    lowered === '[provider list]' ||
                    lowered === '[area debug]' ||
                    lowered === 'providers:' ||
                    lowered === 'provider area checks:' ||
                    lowered.startsWith('resolved network:') ||
                    lowered.startsWith('area match mode:') ||
                    lowered.startsWith('matched providers count:') ||
                    lowered.startsWith('raw area query:') ||
                    lowered.startsWith('normalized area query:') ||
                    lowered.startsWith('expanded alias terms:') ||
                    lowered.startsWith('showing first 25 providers only') ||
                    lowered.startsWith('provider:') ||
                    lowered.startsWith('- provider:')
                );
            }

            for (const line of lines) {
                if (isProviderDiagnosticLine(line)) {
                    continue;
                }
                if (/^[-*•]/.test(line) || /^\d+[\.)]/.test(line)) {
                    const normalizedProvider = line
                        .replace(/^[-*•]\s*/, '')
                        .replace(/^\d+[\.)]\s*/, '')
                        .trim();
                    if (normalizedProvider && !providerLines.includes(normalizedProvider)) {
                        providerLines.push(normalizedProvider);
                    }
                } else {
                    nonProviderLines.push(line);
                }
            }
            return { providerLines, nonProviderLines };
        }

        function _providerRowParts(line) {
            const parts = String(line || '').split('-').map(function (part) { return part.trim(); }).filter(Boolean);
            return {
                name: parts[0] || String(line || '').trim(),
                city: parts[1] || '',
                type: parts[2] || '',
                network: parts[3] || '',
            };
        }

        function _chunkLabelForLine(line, intent, isProviderResult) {
            const lowered = String(line || '').toLowerCase();
            if (!line) return '';
            if (isProviderResult || lowered.includes('provider')) return 'Providers';
            if (lowered.includes('network') || lowered.includes('الشبكة')) return 'Network';
            if (lowered.includes('coverage') || lowered.includes('التغطية') || lowered.includes('area of coverage')) return 'Coverage';
            if (lowered.includes('comparison') || lowered.includes('compare') || intent === 'plan_comparison') return 'Comparison';
            if (lowered.includes('note') || lowered.includes('please') || lowered.includes('ملاحظة')) return 'Notes';
            return 'Core Info';
        }

        function renderResponseChunks(message, intent, isProviderResult) {
            responseChunksEl.innerHTML = '';
            const lines = String(message || '').split(/\\r?\\n/).map(function (line) { return line.trim(); }).filter(Boolean);
            if (!lines.length) {
                responseChunksEl.style.display = 'none';
                return;
            }

            const order = ['Core Info', 'Network', 'Coverage', 'Providers', 'Comparison', 'Notes'];
            const chunks = {
                'Core Info': [],
                'Network': [],
                'Coverage': [],
                'Providers': [],
                'Comparison': [],
                'Notes': [],
            };

            for (const line of lines) {
                if (isProviderResult && (/^[-*•]/.test(line) || /^\d+[\.)]/.test(line))) {
                    continue;
                }
                if (isProviderResult && /^(\[provider list\]|resolved network:|providers:|area match mode:|matched providers count:|showing first 25 providers only)/i.test(line)) {
                    continue;
                }
                const label = _chunkLabelForLine(line, intent, isProviderResult);
                if (label && chunks[label]) {
                    chunks[label].push(line);
                }
            }

            let hasChunk = false;
            for (const label of order) {
                if (!chunks[label].length) {
                    continue;
                }
                hasChunk = true;
                const details = document.createElement('details');
                details.className = 'response-chunk';
                details.open = label === 'Core Info' || label === 'Comparison' || label === 'Providers';
                const summary = document.createElement('summary');
                summary.textContent = label;
                const pre = document.createElement('pre');
                pre.textContent = chunks[label].join('\\n');
                details.appendChild(summary);
                details.appendChild(pre);
                responseChunksEl.appendChild(details);
            }

            responseChunksEl.style.display = hasChunk ? 'flex' : 'none';
        }

        function _copyProviderCardLine(parts) {
            const payload = buildProviderExportText('response');
            copyText(payload, 'providers');
        }

        function _copyProviderCardWhatsapp(parts) {
            const payload = buildProviderExportText('whatsapp');
            copyText(payload, 'providers whatsapp');
        }

        function renderProviderCards(providerLines) {
            providerCardsEl.innerHTML = '';
            if (!Array.isArray(providerLines) || !providerLines.length) {
                providerCardsEl.style.display = 'none';
                return;
            }

            for (const line of providerLines.slice(0, 12)) {
                const parts = _providerRowParts(line);
                const card = document.createElement('div');
                card.className = 'provider-card';

                const nameEl = document.createElement('div');
                nameEl.className = 'provider-card-name';
                nameEl.textContent = parts.name;

                const meta = document.createElement('div');
                meta.className = 'provider-card-meta';
                for (const value of [parts.city, parts.type, parts.network]) {
                    if (!value) continue;
                    const chip = document.createElement('span');
                    chip.className = 'provider-card-chip';
                    chip.textContent = value;
                    meta.appendChild(chip);
                }

                const actions = document.createElement('div');
                actions.className = 'provider-card-actions';
                const copyBtn = document.createElement('button');
                copyBtn.type = 'button';
                copyBtn.className = 'ghost-btn';
                copyBtn.textContent = 'Copy';
                copyBtn.addEventListener('click', function () {
                    _copyProviderCardLine(parts);
                });

                const waBtn = document.createElement('button');
                waBtn.type = 'button';
                waBtn.className = 'ghost-btn';
                waBtn.textContent = 'WhatsApp';
                waBtn.addEventListener('click', function () {
                    _copyProviderCardWhatsapp(parts);
                });

                actions.appendChild(copyBtn);
                actions.appendChild(waBtn);
                card.appendChild(nameEl);
                card.appendChild(meta);
                card.appendChild(actions);
                providerCardsEl.appendChild(card);
            }

            providerCardsEl.style.display = 'grid';
        }

        function loadRecentComparisons() {
            const raw = safeGetStorage(window.localStorage, LS_RECENT_COMPARISONS);
            if (!raw) {
                _recentComparisons = [];
                return;
            }
            try {
                const parsed = JSON.parse(raw);
                _recentComparisons = Array.isArray(parsed) ? parsed.filter(Boolean).slice(0, 6) : [];
            } catch (_err) {
                _recentComparisons = [];
            }
        }

        function pushRecentComparison(query) {
            const q = String(query || '').trim();
            if (!q.toLowerCase().includes('compare') || !q) {
                return;
            }
            _recentComparisons = _recentComparisons.filter(function (item) { return item !== q; });
            _recentComparisons.unshift(q);
            _recentComparisons = _recentComparisons.slice(0, 6);
            safeSetStorage(window.localStorage, LS_RECENT_COMPARISONS, JSON.stringify(_recentComparisons));
            renderComparisonHistory();
        }

        function renderComparisonHistory() {
            comparisonHistoryChipsEl.innerHTML = '';
            if (!_recentComparisons.length) {
                comparisonHistoryChipsEl.textContent = '-';
                return;
            }
            for (const query of _recentComparisons) {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'chip-btn';
                btn.textContent = query.replace(/^compare\s+/i, '');
                btn.addEventListener('click', function () {
                    questionEl.value = query;
                    submitQuery(query);
                });
                comparisonHistoryChipsEl.appendChild(btn);
            }
        }

        let _recentPlans = [];

        function loadRecentPlans() {
            const raw = safeGetStorage(window.localStorage, LS_RECENT_PLANS);
            if (!raw) {
                _recentPlans = [];
                return;
            }
            try {
                const parsed = JSON.parse(raw);
                _recentPlans = Array.isArray(parsed) ? parsed.filter(Boolean).slice(0, 8) : [];
            } catch (_err) {
                _recentPlans = [];
            }
        }

        function pushRecentPlan(planName) {
            const p = String(planName || '').trim();
            if (!p || p === '-' || p.length > 50) {
                return;
            }
            _recentPlans = _recentPlans.filter(function (item) { return item !== p; });
            _recentPlans.unshift(p);
            _recentPlans = _recentPlans.slice(0, 8);
            safeSetStorage(window.localStorage, LS_RECENT_PLANS, JSON.stringify(_recentPlans));
            renderPlansHistory();
        }

        function renderPlansHistory() {
            plansHistoryChipsEl.innerHTML = '';
            if (!_recentPlans.length) {
                plansHistoryChipsEl.textContent = '-';
                return;
            }
            for (const planName of _recentPlans) {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'chip-btn';
                btn.textContent = planName;
                btn.addEventListener('click', function () {
                    const query = 'Summarize ' + planName;
                    questionEl.value = query;
                    submitQuery(query);
                });
                plansHistoryChipsEl.appendChild(btn);
            }
        }

        function extractResultFacts(question, payload, message) {
            const answer = payload && payload.answer ? payload.answer : {};
            const facts = [];
            const lowerIntent = String(answer.intent || '').toLowerCase();
            const lowerQuestion = String(question || '').toLowerCase();
            const isProviderResult = lowerIntent.includes('provider') || lowerIntent.includes('network_city_type') || lowerQuestion.includes('list ') && lowerQuestion.includes('providers in');
            const split = _splitProviderMessage(message);
            const providerRows = split.providerLines;
            const countMatch = String(message || '').match(/(?:count|total)\s*[:=]\s*(\d{1,4})/i);
            const providersCount = countMatch ? Number(countMatch[1]) : providerRows.length;
            if (answer.plan_name) {
                facts.push('Plan: ' + answer.plan_name);
            }
            if (providersCount > 0 && isProviderResult) {
                facts.push('Providers: ' + providersCount);
            }
            return {
                facts: facts.slice(0, 4),
                isProviderResult,
                providerLines: providerRows,
                providerCount: providersCount,
                nonProviderLines: split.nonProviderLines,
            };
        }

        function renderResultFacts(question, payload, message) {
            resultFactsEl.innerHTML = '';
            providerSummaryEl.style.display = 'none';
            providerSummaryEl.innerHTML = '';
            const extracted = extractResultFacts(question, payload, message);
            for (const fact of extracted.facts) {
                const chip = document.createElement('span');
                chip.className = 'fact-chip';
                chip.textContent = fact;
                resultFactsEl.appendChild(chip);
            }
            if (extracted.isProviderResult && Array.isArray(extracted.providerLines) && extracted.providerLines.length > 0) {
                const head = document.createElement('div');
                head.className = 'provider-summary-head';

                const label = document.createElement('span');
                label.className = 'label';
                label.textContent = 'Provider Snapshot';

                const badge = document.createElement('span');
                badge.className = 'provider-count-badge';
                badge.textContent = String(extracted.providerCount || extracted.providerLines.length) + ' providers';

                head.appendChild(label);
                head.appendChild(badge);

                const ul = document.createElement('ul');
                ul.className = 'provider-points';
                for (const line of extracted.providerLines.slice(0, 5)) {
                    const li = document.createElement('li');
                    li.textContent = line;
                    ul.appendChild(li);
                }

                providerSummaryEl.appendChild(head);
                providerSummaryEl.appendChild(ul);

                if (extracted.providerLines.length > 5) {
                    const toggleBtn = document.createElement('button');
                    toggleBtn.type = 'button';
                    toggleBtn.className = 'provider-toggle-btn';
                    toggleBtn.textContent = 'Show All Providers';
                    let showAll = false;
                    toggleBtn.addEventListener('click', function () {
                        showAll = !showAll;
                        ul.innerHTML = '';
                        const rows = showAll ? extracted.providerLines : extracted.providerLines.slice(0, 5);
                        for (const row of rows) {
                            const li = document.createElement('li');
                            li.textContent = row;
                            ul.appendChild(li);
                        }
                        toggleBtn.textContent = showAll ? 'Show First 5' : 'Show All Providers';
                    });
                    providerSummaryEl.appendChild(toggleBtn);
                }

                const condensed = (extracted.nonProviderLines || []).join('\\n');
                if (condensed) {
                    answerVal.textContent = condensed;
                }
                providerSummaryEl.style.display = 'block';
            }
        }

        function resetCopyPreview() {
            if (copyPreviewLabelEl) copyPreviewLabelEl.textContent = 'Export Preview';
            copyPreviewVal.textContent = '-';
        }

        function setCopyPreview(exportPayload) {
            if (copyPreviewLabelEl) {
                copyPreviewLabelEl.textContent = 'Export Preview (' + String(exportPayload.label || 'Response') + ')';
            }
            copyPreviewVal.textContent = exportPayload.text || '-';
        }

        function updateTelemetry(question, mode, formatter, statusText) {
            dbgQueryEl.textContent = question || '-';
            dbgModeEl.textContent = mode || 'detailed';
            dbgFormatterEl.textContent = formatter || 'None';
            dbgStatusEl.textContent = statusText || '-';
        }

        function setDiagnosticsVisibility(isOpen) {
            _diagnosticsOpen = Boolean(isOpen);
            diagnosticsBodyEl.hidden = !_diagnosticsOpen;
            toggleDiagnosticsBtn.textContent = _diagnosticsOpen ? 'Hide Diagnostics' : 'Show Diagnostics';
        }

        function setUsageVisibility(open) {
            usageBodyEl.hidden = !open;
            usageToggleBtnEl.textContent = open ? 'Hide' : 'Show';
        }

        function showExportPreview() {
            if (exportPreviewBodyEl) exportPreviewBodyEl.hidden = false;
        }

        function topMetricLabel(items) {
            if (!Array.isArray(items) || !items.length) {
                return '-';
            }
            const top = items[0] || {};
            if (!top.query) {
                return '-';
            }
            return top.query + ' (' + String(top.count || 0) + 'x)';
        }

        function renderOperatorMetrics() {
            const metrics = usageState && usageState.operator_metrics ? usageState.operator_metrics : {};
            dbgQuickTopEl.textContent = topMetricLabel(metrics.quick_actions);
            dbgModeTopEl.textContent = topMetricLabel(metrics.response_modes);
            dbgCopyTopEl.textContent = topMetricLabel(metrics.copy_actions);
            const providerCount = Number(metrics.provider_lookup_queries || 0);
            const compareCount = Number(metrics.comparison_queries || 0);
            dbgFlowTopEl.textContent = String(providerCount) + ' / ' + String(compareCount);
        }

        async function fetchFormattedText(question, formatterMode) {
            const resp = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question, output_mode: formatterMode })
            });
            const payload = await resp.json();
            const answer = payload && payload.answer ? payload.answer : {};
            return String(payload.display_answer || answer.message || payload.error || '');
        }

        async function resolveExportPayload(exportKind) {
            const labels = {
                response: 'Response',
                whatsapp: 'WhatsApp',
                arabic: 'Arabic',
                compact: 'Compact',
            };
            const currentText = String(_lastRenderedText || answerVal.textContent || '').trim();
            const context = _lastResultContext || { type: 'unsupported' };
            const rules = actionRulesForContext(context);

            if (exportKind === 'whatsapp' && !rules.whatsapp) {
                return { label: labels.whatsapp, text: '' };
            }
            if (exportKind === 'arabic' && !rules.arabic) {
                return { label: labels.arabic, text: '' };
            }
            if (exportKind === 'compact' && !rules.compact) {
                return { label: labels.compact, text: '' };
            }

            if (exportKind === 'response') {
                return { label: labels.response, text: currentText };
            }

            if (context.type === 'provider_list' || context.type === 'network_lookup') {
                return {
                    label: labels[exportKind] || 'Response',
                    text: buildProviderExportText(exportKind),
                };
            }

            if (context.type === 'comparison') {
                return {
                    label: labels[exportKind] || 'Response',
                    text: buildComparisonExportText(exportKind),
                };
            }

            if (context.type !== 'plan') {
                return { label: labels[exportKind] || 'Response', text: currentText };
            }

            const formatterByKind = {
                whatsapp: 'whatsapp_summary',
            };
            const question = String(_lastQuestion || questionEl.value || '').trim();
            if (!question) {
                return { label: labels[exportKind] || 'Response', text: currentText };
            }

            if (exportKind === 'arabic') {
                return {
                    label: labels.arabic,
                    text: hasArabic(currentText) ? normalizeArabicSpacing(currentText) : currentText,
                };
            }

            if (exportKind === 'compact') {
                return {
                    label: labels.compact,
                    text: compactText(currentText),
                };
            }

            const rendered = await fetchFormattedText(question, formatterByKind[exportKind]);
            return {
                label: labels[exportKind] || 'Response',
                text: String(rendered || '').trim(),
            };
        }

        async function copyFromExportPayload(actionValue, exportKind) {
            const rules = actionRulesForContext(_lastResultContext || { type: 'unsupported' });
            if ((exportKind === 'whatsapp' && !rules.whatsapp) || (exportKind === 'arabic' && !rules.arabic) || (exportKind === 'compact' && !rules.compact)) {
                return;
            }
            await submitUsageAction('track_copy_action', _lastQuestion || questionEl.value, { usage_value: actionValue });
            showExportPreview();
            const exportPayload = await resolveExportPayload(exportKind);
            if (!String(exportPayload.text || '').trim()) {
                return;
            }
            setCopyPreview(exportPayload);
            await copyText(exportPayload.text, exportPayload.label.toLowerCase());
        }

        function _providerContextFromQuestion() {
            const q = String(_lastQuestion || questionEl.value || '').trim();
            const fallbackType = providerTypeEl.value || '';
            const fallbackPlan = (planVal.textContent && planVal.textContent !== '-') ? planVal.textContent : providerPlanEl.value;
            const fallbackLocation = providerAreaEl.value ? (providerAreaEl.value + ' ' + providerCityEl.value) : providerCityEl.value;
            const match = q.match(/^list\s+(.+?)\s+providers\s+in\s+(.+?)\s+for\s+(.+)$/i);
            if (!match) {
                return {
                    providerType: fallbackType,
                    location: fallbackLocation,
                    planName: fallbackPlan,
                };
            }
            return {
                providerType: String(match[1] || fallbackType).trim(),
                location: String(match[2] || fallbackLocation).trim(),
                planName: String(match[3] || fallbackPlan).trim(),
            };
        }

        function _providerLinesForExport() {
            const lines = Array.isArray(_lastResultContext.providerLines) ? _lastResultContext.providerLines : [];
            if (lines.length) {
                return lines.slice(0, 30).map(function (line) {
                    const parts = _providerRowParts(line);
                    return parts.name || String(line || '').trim();
                }).filter(Boolean);
            }
            return [];
        }

        function buildProviderExportText(exportKind) {
            const info = _providerContextFromQuestion();
            const lines = _providerLinesForExport();
            const title = exportKind === 'compact' ? 'Providers' : 'Providers:';
            const header = [
                info.planName ? ('Plan: ' + info.planName) : '',
                info.location ? ('City: ' + info.location) : '',
                info.providerType ? ('Provider Type: ' + info.providerType) : '',
            ].filter(Boolean);

            const providersBlock = lines.length
                ? lines.map(function (name) { return '* ' + name; }).join('\\n')
                : (String(_lastRenderedText || answerVal.textContent || '').trim() || 'No providers available.');

            if (exportKind === 'compact') {
                const compactParts = header.concat([title, providersBlock]);
                return compactText(compactParts.join('\\n'));
            }

            return header.concat(['', title, '', providersBlock]).join('\\n').trim();
        }

        function buildComparisonExportText(exportKind) {
            const text = String(_lastRenderedText || answerVal.textContent || '').trim();
            if (exportKind === 'compact') {
                return compactText(text);
            }
            if (exportKind === 'arabic') {
                return hasArabic(text) ? normalizeArabicSpacing(text) : text;
            }
            return text;
        }

        function renderRecentSearches() {
            recentListEl.innerHTML = '';
            const items = Array.isArray(usageState.recent_queries) ? usageState.recent_queries : recentSearches;
            if (!Array.isArray(items) || items.length === 0) {
                recentEmptyEl.style.display = 'block';
                return;
            }

            recentEmptyEl.style.display = 'none';
            for (const query of items) {
                const li = document.createElement('li');
                const row = document.createElement('div');
                row.className = 'replay-row';

                const replayBtn = document.createElement('button');
                replayBtn.type = 'button';
                replayBtn.className = 'recent-btn';
                replayBtn.textContent = query;
                replayBtn.addEventListener('click', function () {
                    questionEl.value = query;
                    submitQuery(query);
                });

                const pinBtn = document.createElement('button');
                pinBtn.type = 'button';
                pinBtn.className = 'pin-btn';
                pinBtn.textContent = 'Pin';
                pinBtn.addEventListener('click', function () {
                    submitUsageAction('pin_query', query);
                });

                row.appendChild(replayBtn);
                row.appendChild(pinBtn);
                li.appendChild(row);
                recentListEl.appendChild(li);
            }
        }

        function renderPinnedSearches() {
            pinnedListEl.innerHTML = '';
            const items = Array.isArray(usageState.pinned_queries) ? usageState.pinned_queries : [];
            if (!items.length) {
                pinnedEmptyEl.style.display = 'block';
                return;
            }

            pinnedEmptyEl.style.display = 'none';
            for (const query of items) {
                const li = document.createElement('li');
                const row = document.createElement('div');
                row.className = 'replay-row';

                const replayBtn = document.createElement('button');
                replayBtn.type = 'button';
                replayBtn.className = 'recent-btn';
                replayBtn.textContent = query;
                replayBtn.addEventListener('click', function () {
                    questionEl.value = query;
                    submitQuery(query);
                });

                const unpinBtn = document.createElement('button');
                unpinBtn.type = 'button';
                unpinBtn.className = 'pin-btn';
                unpinBtn.textContent = 'Unpin';
                unpinBtn.addEventListener('click', function () {
                    submitUsageAction('unpin_query', query);
                });

                row.appendChild(replayBtn);
                row.appendChild(unpinBtn);
                li.appendChild(row);
                pinnedListEl.appendChild(li);
            }
        }

        function renderTopQueries() {
            topListEl.innerHTML = '';
            const items = Array.isArray(usageState.top_queries) ? usageState.top_queries : [];
            if (!items.length) {
                topEmptyEl.style.display = 'block';
                return;
            }

            topEmptyEl.style.display = 'none';
            for (const item of items.slice(0, 5)) {
                const li = document.createElement('li');
                li.className = 'top-item';

                const row = document.createElement('div');
                row.className = 'replay-row';

                const replayBtn = document.createElement('button');
                replayBtn.type = 'button';
                replayBtn.className = 'recent-btn';
                replayBtn.textContent = item.query;
                replayBtn.addEventListener('click', function () {
                    questionEl.value = item.query;
                    submitQuery(item.query);
                });

                const countEl = document.createElement('span');
                countEl.className = 'meta-count';
                countEl.textContent = item.count + 'x';

                row.appendChild(replayBtn);
                row.appendChild(countEl);
                li.appendChild(row);
                topListEl.appendChild(li);
            }
        }

        function renderCategories() {
            categoryListEl.innerHTML = '';
            const items = Array.isArray(usageState.query_categories) ? usageState.query_categories : [];
            if (!items.length) {
                categoryEmptyEl.style.display = 'block';
                return;
            }

            categoryEmptyEl.style.display = 'none';
            for (const item of items.slice(0, 8)) {
                const li = document.createElement('li');
                li.className = 'category-item';
                li.textContent = item.category + ' - ' + item.count;
                categoryListEl.appendChild(li);
            }
        }

        function renderUsageState() {
            recentSearches = Array.isArray(usageState.recent_queries) ? usageState.recent_queries : recentSearches;
            lastCityVal.textContent = usageState.last_city || '-';
            lastPlanVal.textContent = usageState.last_plan || '-';
            renderRecentSearches();
            renderPinnedSearches();
            renderTopQueries();
            renderCategories();
            renderContextChips();
            renderOperatorMetrics();
        }

        function syncUsageState(nextState) {
            if (nextState && typeof nextState === 'object') {
                usageState = nextState;
                recentSearches = Array.isArray(nextState.recent_queries) ? nextState.recent_queries : recentSearches;
                if (nextState.last_city) { _lastCity = nextState.last_city; }
                if (nextState.last_plan) { _lastPlan = nextState.last_plan; }
            }
            renderUsageState();
        }

        function rememberSuccessfulQuery(query) {
            const q = (query || '').trim();
            if (!q) {
                return;
            }
            const existingIndex = recentSearches.indexOf(q);
            if (existingIndex >= 0) {
                recentSearches.splice(existingIndex, 1);
            }
            recentSearches.unshift(q);
            recentSearches = recentSearches.slice(0, 10);
        }

        function setActiveProviderTypeChip() {
            const selected = providerTypeEl.value.trim().toLowerCase();
            const chips = providerTypeChipsEl.querySelectorAll('.chip-btn');
            for (const chip of chips) {
                const chipType = String(chip.dataset.providerType || '').toLowerCase();
                chip.classList.toggle('active', chipType === selected);
            }
        }

        function setActiveCityChip() {
            const city = providerCityEl.value.trim();
            const chips = cityFilterChipsEl.querySelectorAll('.chip-btn');
            for (const chip of chips) {
                chip.classList.toggle('active', chip.dataset.city === city);
            }
        }

        function setActivePlanFilterChip() {
            const plan = providerPlanEl.value.trim();
            const chips = planFilterChipsEl.querySelectorAll('.chip-btn');
            for (const chip of chips) {
                chip.classList.toggle('active', chip.dataset.plan === plan);
            }
        }

        function _capitalize(s) {
            return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
        }

        function _tryAutoSubmitProviderQuery() {
            const city = providerCityEl.value.trim();
            const type = providerTypeEl.value.trim().toLowerCase();
            const plan = providerPlanEl.value.trim();
            const area = providerAreaEl.value.trim();
            if (!city || !type || !plan) { return; }
            let query = 'List ' + type + ' providers in ' + city + ' for ' + plan;
            if (area) { query = 'List ' + type + ' providers in ' + area + ' ' + city + ' for ' + plan; }
            questionEl.value = query;
            submitQuery(query);
        }

        function renderContextChips() {
            if (!contextChipsEl) { return; }
            contextChipsEl.innerHTML = '';
            const chips = [];
            if (_lastCity) { chips.push({ label: _lastCity, kind: 'city', value: _lastCity }); }
            if (_lastProviderType) { chips.push({ label: _capitalize(_lastProviderType) + 's', kind: 'ptype', value: _lastProviderType }); }
            if (_lastPlan) { chips.push({ label: _lastPlan, kind: 'plan', value: _lastPlan }); }
            if (!chips.length) { contextChipsEl.style.display = 'none'; return; }
            contextChipsEl.style.display = 'flex';
            const lbl = document.createElement('span');
            lbl.className = 'chip-label';
            lbl.textContent = 'Last used:';
            contextChipsEl.appendChild(lbl);
            for (const item of chips) {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'chip-btn active';
                btn.textContent = item.label;
                btn.addEventListener('click', function () {
                    if (item.kind === 'city') {
                        providerCityEl.value = item.value;
                        refreshAreaOptions();
                        setActiveCityChip();
                        _tryAutoSubmitProviderQuery();
                    } else if (item.kind === 'ptype') {
                        providerTypeEl.value = item.value;
                        setActiveProviderTypeChip();
                        _tryAutoSubmitProviderQuery();
                    } else if (item.kind === 'plan') {
                        providerPlanEl.value = item.value;
                        setActivePlanFilterChip();
                        _tryAutoSubmitProviderQuery();
                    }
                });
                contextChipsEl.appendChild(btn);
            }
        }

        function showCopiedFeedback(label) {
            const text = label ? ('Copied ' + label) : 'Copied';
            copyFeedback.textContent = text;
            copyFeedback.classList.add('show');
            if (copyToast) {
                copyToast.textContent = text;
                copyToast.classList.add('show');
            }
            window.setTimeout(function () {
                copyFeedback.classList.remove('show');
                if (copyToast) {
                    copyToast.classList.remove('show');
                }
            }, 900);
        }

        async function submitUsageAction(action, query, extras) {
            const payloadBody = {
                question: query || '',
                usage_action: action,
                usage_query: query || ''
            };
            if (extras && typeof extras === 'object') {
                Object.assign(payloadBody, extras);
            }
            try {
                const resp = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payloadBody)
                });
                const payload = await resp.json();
                syncUsageState(payload.usage_state || usageState);
            } catch (_err) {
                // Passive state update only; keep failures silent.
            }
        }

        function deriveWorkflowAction(query) {
            const q = String(query || '').toLowerCase();
            if (q.includes('compare') || q.includes('comparison') || q.includes('قارن')) {
                return 'compare_summarize';
            }
            if (q.includes('provider') || q.includes('providers') || q.includes('network') || q.includes('مستشفى') || q.includes('مزود') || q.includes('شبكة')) {
                return 'provider_lookup';
            }
            return 'search_copy_send';
        }

        function deriveFrictionTag(statusText, durationMs, query) {
            const q = String(query || '').trim();
            if (!q) {
                return 'REVIEW';
            }
            if (Number(durationMs || 0) >= 3500) {
                return 'SLOW';
            }
            const top = Array.isArray(usageState.top_queries) ? usageState.top_queries : [];
            const existing = top.find(function (item) { return item.query === q; });
            if (existing && Number(existing.count || 0) >= 2) {
                return 'REPEATED';
            }
            if (statusText === 'BLOCKED_OK') {
                return 'BLOCKED_OK';
            }
            if (statusText === 'GOOD') {
                return 'GOOD';
            }
            return 'REVIEW';
        }

        async function submitQuery(question) {
            const trimmed = (question || '').trim();
            const uiMode = activeMode();
            const outputMode = outputModeForUiMode(uiMode);
            const startedAtMs = Date.now();
            if (!trimmed) {
                resultEl.style.display = 'block';
                paintStatus('REVIEW');
                resultCardTypeEl.textContent = 'Result Card';
                resultTitleVal.textContent = 'Operational Result';
                intentVal.textContent = 'unsupported';
                planVal.textContent = '-';
                answerVal.textContent = 'Question must not be empty.';
                resultFactsEl.innerHTML = '';
                providerSummaryEl.style.display = 'none';
                providerSummaryEl.innerHTML = '';
                providerCardsEl.style.display = 'none';
                providerCardsEl.innerHTML = '';
                responseChunksEl.style.display = 'none';
                responseChunksEl.innerHTML = '';
                _lastPayload = null;
                _lastQuestion = '';
                _lastRenderedText = answerVal.textContent;
                _lastResultContext = buildResultContext('', { answer: { ok: false, intent: 'unsupported' } }, { providerLines: [], isProviderResult: false });
                applyActionVisibility(_lastResultContext);
                refreshMobileActionVisibility();
                _lastDurationMs = 0;
                resetCopyPreview();
                updateTelemetry('', uiMode, outputMode || 'None', 'REVIEW');
                return;
            }

            // Clear stale action state while new result is loading.
            _lastResultContext = buildResultContext('', { answer: { ok: false, intent: 'unsupported' } }, { providerLines: [], isProviderResult: false });
            applyActionVisibility(_lastResultContext);
            refreshMobileActionVisibility();

            askBtn.disabled = true;
            askBtn.textContent = 'Searching...';

            try {
                const resp = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: trimmed, output_mode: outputMode || null })
                });
                const payload = await resp.json();
                const answer = payload.answer || {};
                const intent = answer.intent || 'unsupported';
                const plan = answer.plan_name || '-';
                const message = chooseRenderedText(uiMode, payload);
                const opStatus = classifyStatus(trimmed, payload);
                const card = classifyCardType(intent, trimmed);

                if (answer.ok) {
                    rememberSuccessfulQuery(trimmed);
                }

                syncUsageState(payload.usage_state || usageState);
                resultEl.style.display = 'block';
                paintStatus(opStatus);
                resultCardTypeEl.textContent = card.label;
                resultTitleVal.textContent = card.section;
                intentVal.textContent = intent;
                planVal.textContent = plan;
                if (plan && plan !== '-' && plan.length > 0) {
                    pushRecentPlan(plan);
                    fastCompareThisBtn.style.display = 'inline-block';
                } else {
                    fastCompareThisBtn.style.display = 'none';
                }
                answerVal.textContent = message;
                renderResultFacts(trimmed, payload, message);
                pushRecentComparison(trimmed);
                const extracted = extractResultFacts(trimmed, payload, message);
                _lastResultContext = buildResultContext(trimmed, payload, extracted);
                applyActionVisibility(_lastResultContext);
                refreshMobileActionVisibility();
                renderProviderCards(extracted.providerLines);
                renderResponseChunks(message, intent, extracted.isProviderResult);
                _lastPayload = payload;
                _lastQuestion = trimmed;
                _lastRenderedText = message;
                _lastDurationMs = Date.now() - startedAtMs;
                resetCopyPreview();
                safeSetStorage(window.sessionStorage, SS_LAST_SEARCH, trimmed);
                persistUiState();
                updateTelemetry(trimmed, uiMode, outputMode || 'None', opStatus);
                const workflowAction = deriveWorkflowAction(trimmed);
                const frictionTag = deriveFrictionTag(opStatus, _lastDurationMs, trimmed);
                await submitUsageAction('track_response_mode', trimmed, { usage_value: uiMode });
                await submitUsageAction('track_workflow_action', trimmed, { usage_value: workflowAction });
                await submitUsageAction('tag_friction', trimmed, {
                    friction_tag: frictionTag,
                    usage_context: workflowAction,
                    duration_ms: _lastDurationMs,
                    usage_value: frictionTag,
                });
            } catch (err) {
                resultEl.style.display = 'block';
                paintStatus('REVIEW');
                resultCardTypeEl.textContent = 'Result Card';
                resultTitleVal.textContent = 'Operational Result';
                intentVal.textContent = 'unsupported';
                planVal.textContent = '-';
                answerVal.textContent = 'Request failed: ' + err;
                resultFactsEl.innerHTML = '';
                providerSummaryEl.style.display = 'none';
                providerSummaryEl.innerHTML = '';
                providerCardsEl.style.display = 'none';
                providerCardsEl.innerHTML = '';
                responseChunksEl.style.display = 'none';
                responseChunksEl.innerHTML = '';
                _lastPayload = null;
                _lastQuestion = trimmed;
                _lastRenderedText = answerVal.textContent;
                _lastResultContext = buildResultContext(trimmed, { answer: { ok: false, intent: 'unsupported' } }, { providerLines: [], isProviderResult: false });
                applyActionVisibility(_lastResultContext);
                refreshMobileActionVisibility();
                _lastDurationMs = Date.now() - startedAtMs;
                resetCopyPreview();
                updateTelemetry(trimmed, uiMode, outputMode || 'None', 'REVIEW');
                await submitUsageAction('track_response_mode', trimmed, { usage_value: uiMode });
                await submitUsageAction('track_workflow_action', trimmed, { usage_value: deriveWorkflowAction(trimmed) });
                await submitUsageAction('tag_friction', trimmed, {
                    friction_tag: deriveFrictionTag('REVIEW', _lastDurationMs, trimmed),
                    usage_context: 'search_copy_send',
                    duration_ms: _lastDurationMs,
                });
            } finally {
                askBtn.disabled = false;
                askBtn.textContent = 'Search';
            }
        }

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            persistUiState();
            await submitQuery(questionEl.value);
        });

        planForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const planName = planNameEl.value.trim();
            if (!planName) {
                await submitQuery('');
                return;
            }
            const query = 'Summarize ' + planName;
            questionEl.value = query;
            persistUiState('summarize');
            await submitQuery(query);
        });

        providerForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const plan = providerPlanEl.value.trim();
            const city = providerCityEl.value.trim();
            const area = providerAreaEl.value.trim();
            const type = providerTypeEl.value.trim().toLowerCase();
            if (!plan || !city || !type) {
                await submitQuery('');
                return;
            }
            // Track explicit persistence state (Part D).
            _lastCity = city;
            _lastProviderType = type;
            _lastPlan = plan;
            renderContextChips();
            let query = 'List ' + type + ' providers in ' + city + ' for ' + plan;
            if (area) {
                query = 'List ' + type + ' providers in ' + area + ' ' + city + ' for ' + plan;
            }
            questionEl.value = query;
            persistUiState('provider');
            await submitQuery(query);
        });

        providerCityEl.addEventListener('change', refreshAreaOptions);
        providerCityEl.addEventListener('input', refreshAreaOptions);
        providerCityEl.addEventListener('change', function () {
            setActiveCityChip();
            persistUiState();
        });
        providerTypeEl.addEventListener('change', function () {
            setActiveProviderTypeChip();
            persistUiState();
        });
        providerPlanEl.addEventListener('change', function () {
            setActivePlanFilterChip();
            persistUiState();
        });
        providerAreaEl.addEventListener('change', function () {
            persistUiState();
        });
        responseModeEl.addEventListener('change', function () {
            updateTelemetry(_lastQuestion || '', activeMode(), outputModeForUiMode(activeMode()) || 'None', dbgStatusEl.textContent || '-');
            persistUiState();
            submitUsageAction('track_response_mode', _lastQuestion || questionEl.value, { usage_value: responseModeEl.value });
        });
        window.addEventListener('resize', refreshMobileActionVisibility);
        planNameEl.addEventListener('change', function () { persistUiState(); });
        planAEl.addEventListener('change', function () { persistUiState(); });
        planBEl.addEventListener('change', function () { persistUiState(); });
        questionEl.addEventListener('change', function () { persistUiState(); });

        providerTypeChipsEl.addEventListener('click', function (e) {
            const target = e.target;
            if (!(target instanceof HTMLElement)) {
                return;
            }
            const chip = target.closest('.chip-btn');
            if (!chip) {
                return;
            }
            const selectedType = String(chip.dataset.providerType || '').trim().toLowerCase();
            if (!selectedType) {
                return;
            }
            providerTypeEl.value = selectedType;
            setActiveProviderTypeChip();
            _tryAutoSubmitProviderQuery();
        });

        cityFilterChipsEl.addEventListener('click', function (e) {
            const chip = e.target.closest('.chip-btn');
            if (!chip) { return; }
            const city = String(chip.dataset.city || '').trim();
            if (!city) { return; }
            providerCityEl.value = city;
            refreshAreaOptions();
            setActiveCityChip();
            _tryAutoSubmitProviderQuery();
        });

        planFilterChipsEl.addEventListener('click', function (e) {
            const chip = e.target.closest('.chip-btn');
            if (!chip) { return; }
            const plan = String(chip.dataset.plan || '').trim();
            if (!plan) { return; }
            providerPlanEl.value = plan;
            setActivePlanFilterChip();
            _tryAutoSubmitProviderQuery();
        });

        clearRecentBtn.addEventListener('click', function () {
            submitUsageAction('clear_recent', '');
        });

        clearPinnedBtn.addEventListener('click', function () {
            submitUsageAction('clear_pinned', '');
        });

        usageToggleBtnEl.addEventListener('click', function () {
            setUsageVisibility(usageBodyEl.hidden);
        });

        async function copyText(text, label) {
            try {
                await navigator.clipboard.writeText(String(text || ''));
                showCopiedFeedback(label || 'response');
            } catch (_err) {
                // Keep UX lightweight; clipboard failure remains silent.
            }
        }

        copyResponseBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_response', 'response');
        });

        copyWhatsappBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_whatsapp', 'whatsapp');
        });

        copyArabicBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_arabic', 'arabic');
        });

        copyCompactBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_compact', 'compact');
        });

        fastCopyBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_response', 'response');
        });

        fastWhatsappBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_whatsapp', 'whatsapp');
        });

        fastArabicBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_arabic', 'arabic');
        });

        fastCompactBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_compact', 'compact');
        });

        fastCompareAgainBtn.addEventListener('click', async function () {
            const rules = actionRulesForContext(_lastResultContext || { type: 'unsupported' });
            if (!rules.compareAgain) {
                return;
            }
            const lower = String(_lastQuestion || '').toLowerCase();
            if (lower.includes('compare')) {
                await submitQuery(_lastQuestion);
                return;
            }
            const fallbackQuery = 'Compare ' + planAEl.value.trim() + ' vs ' + planBEl.value.trim();
            questionEl.value = fallbackQuery;
            await submitQuery(fallbackQuery);
        });

        fastCompareThisBtn.addEventListener('click', async function () {
            const rules = actionRulesForContext(_lastResultContext || { type: 'unsupported' });
            if (!rules.compare) {
                return;
            }
            const currentPlan = planVal.textContent || '';
            if (!currentPlan || currentPlan === '-') {
                return;
            }
            const otherPlan = planBEl.value.trim();
            if (!otherPlan) {
                return;
            }
            const query = 'Compare ' + currentPlan + ' vs ' + otherPlan;
            questionEl.value = query;
            await submitUsageAction('track_quick_action', query, { usage_value: 'compare_this' });
            await submitQuery(query);
        });

        mobileAskBtn.addEventListener('click', async function () {
            await submitQuery(questionEl.value || _lastQuestion);
        });

        mobileCompareBtn.addEventListener('click', async function () {
            const query = 'Compare ' + planAEl.value.trim() + ' vs ' + planBEl.value.trim();
            questionEl.value = query;
            await submitQuery(query);
        });

        mobileProvidersBtn.addEventListener('click', async function () {
            const plan = providerPlanEl.value.trim();
            const city = providerCityEl.value.trim();
            const type = providerTypeEl.value.trim().toLowerCase();
            const area = providerAreaEl.value.trim();
            if (!plan || !city || !type) {
                await submitQuery('');
                return;
            }
            let query = 'List ' + type + ' providers in ' + city + ' for ' + plan;
            if (area) {
                query = 'List ' + type + ' providers in ' + area + ' ' + city + ' for ' + plan;
            }
            questionEl.value = query;
            await submitQuery(query);
        });

        mobileWhatsappBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_whatsapp', 'whatsapp');
        });

        mobileArabicBtn.addEventListener('click', async function () {
            await copyFromExportPayload('copy_arabic', 'arabic');
        });

        qaSummarizeBtn.addEventListener('click', async function () {
            await submitUsageAction('track_quick_action', questionEl.value, { usage_value: 'summarize' });
            const planName = planNameEl.value.trim();
            const query = 'Summarize ' + planName;
            questionEl.value = query;
            persistUiState('summarize');
            await submitQuery(query);
        });

        qaCompareBtn.addEventListener('click', async function () {
            await submitUsageAction('track_quick_action', questionEl.value, { usage_value: 'compare' });
            const planA = planAEl.value.trim();
            const planB = planBEl.value.trim();
            const query = 'Compare ' + planA + ' vs ' + planB;
            questionEl.value = query;
            persistUiState('compare');
            await submitQuery(query);
        });

        qaProviderBtn.addEventListener('click', async function () {
            await submitUsageAction('track_quick_action', questionEl.value, { usage_value: 'provider_search' });
            const plan = providerPlanEl.value.trim();
            const city = providerCityEl.value.trim();
            const area = providerAreaEl.value.trim();
            const type = providerTypeEl.value.trim().toLowerCase();
            if (!plan || !city || !type) {
                await submitQuery('');
                return;
            }
            let query = 'List ' + type + ' providers in ' + city + ' for ' + plan;
            if (area) {
                query = 'List ' + type + ' providers in ' + area + ' ' + city + ' for ' + plan;
            }
            questionEl.value = query;
            persistUiState('provider');
            await submitQuery(query);
        });

        qaWhatsappBtn.addEventListener('click', async function () {
            await submitUsageAction('track_quick_action', questionEl.value, { usage_value: 'whatsapp_summary' });
            responseModeEl.value = 'whatsapp';
            const planName = planNameEl.value.trim();
            const query = 'Summarize ' + planName;
            questionEl.value = query;
            persistUiState('whatsapp_summary');
            await submitQuery(query);
        });

        qaArabicBtn.addEventListener('click', async function () {
            await submitUsageAction('track_quick_action', questionEl.value, { usage_value: 'arabic_summary' });
            responseModeEl.value = 'arabic';
            const planName = planNameEl.value.trim();
            const query = 'اعطني ملخص ' + planName;
            questionEl.value = query;
            persistUiState('arabic_summary');
            await submitQuery(query);
        });

        qaNetworkBtn.addEventListener('click', async function () {
            await submitUsageAction('track_quick_action', questionEl.value, { usage_value: 'network_lookup' });
            const plan = providerPlanEl.value.trim();
            const query = 'What is the network for ' + plan + '?';
            questionEl.value = query;
            persistUiState('network_lookup');
            await submitQuery(query);
        });

        frictionTagRowEl.addEventListener('click', async function (e) {
            const chip = e.target.closest('.chip-btn');
            if (!chip) {
                return;
            }
            const tag = String(chip.dataset.frictionTag || '').trim().toUpperCase();
            if (!tag) {
                return;
            }
            const query = _lastQuestion || questionEl.value || '';
            await submitUsageAction('tag_friction', query, {
                friction_tag: tag,
                usage_value: tag,
                usage_context: deriveWorkflowAction(query),
                duration_ms: _lastDurationMs,
            });
            showCopiedFeedback('tag ' + tag);
        });

        toggleDiagnosticsBtn.addEventListener('click', function () {
            setDiagnosticsVisibility(!_diagnosticsOpen);
        });

        restoreUiState();
        loadRecentComparisons();
        renderComparisonHistory();
        loadRecentPlans();
        renderPlansHistory();
        refreshAreaOptions();
        setActiveProviderTypeChip();
        setActiveCityChip();
        setActivePlanFilterChip();
        renderUsageState();
        setDiagnosticsVisibility(false);
        setUsageVisibility(false);
        applyActionVisibility(_lastResultContext);
        refreshMobileActionVisibility();
        resetCopyPreview();
        updateTelemetry('', activeMode(), outputModeForUiMode(activeMode()) || 'None', '-');
        compareForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const planA = planAEl.value.trim();
            const planB = planBEl.value.trim();
            if (!planA || !planB) {
                await submitQuery('');
                return;
            }
            const query = 'Compare ' + planA + ' vs ' + planB;
            questionEl.value = query;
            persistUiState('compare');
            await submitQuery(query);
        });
    </script>
</body>
</html>
"""
    return HTMLResponse(
        content=page
        .replace("__AREA_OPTIONS_BY_CITY__", _area_opts_js)
        .replace("__INITIAL_RECENT_SEARCHES__", json.dumps(_usage_snapshot.get("recent_queries", _recent_searches_snapshot())))
        .replace("__INITIAL_USAGE_STATE__", _usage_state_js)
    )


@app.post("/ask")
def ask(request: AskRequest):
    total_started = time.perf_counter()
    q = request.question.strip() if isinstance(request.question, str) else ""
    normalized_q = normalize_query(q)
    usage_action = (request.usage_action or "").strip().lower()
    usage_query = (request.usage_query or q).strip()
    usage_value = (request.usage_value or "").strip()
    friction_tag = (request.friction_tag or "").strip().upper()
    usage_context = (request.usage_context or "").strip()
    duration_ms = int(request.duration_ms or 0)

    def _safe_usage_state_snapshot() -> dict[str, Any]:
        try:
            return _USAGE_STORE.ui_snapshot()
        except Exception:
            # Telemetry state is non-critical; keep operator path uninterrupted.
            return {
                "recent_queries": [],
                "pinned_queries": [],
                "top_queries": [],
                "last_city": "",
                "last_plan": "",
                "query_categories": [],
            }

    if usage_action in {"clear_recent", "clear_pinned"}:
        try:
            if usage_action == "clear_recent":
                usage_state = _USAGE_STORE.clear_recent()
            else:
                usage_state = _safe_usage_state_snapshot()
                with _USAGE_STORE._lock:
                    state = _USAGE_STORE.load_state()
                    state["pinned_queries"] = []
                    _USAGE_STORE.save_state(state)
                    usage_state = _safe_usage_state_snapshot()
        except Exception as exc:
            print(f"[telemetry warning] usage_action={usage_action} failed: {exc}")
            usage_state = _safe_usage_state_snapshot()
        _record_runtime_observability_event(
            query=usage_query or q,
            normalized_query=normalize_query(usage_query or q),
            intent="operator_action",
            resolved_plan="",
            output_mode=(request.output_mode or "").strip().lower() or "none",
            response_time_ms=int((time.perf_counter() - total_started) * 1000),
            routing_time_ms=0,
            retrieval_time_ms=0,
            formatting_time_ms=0,
            result_status="SUCCESS",
            fallback_used=False,
            refusal_reason="",
            provider_lookup_used=False,
            comparison_used=False,
            action=usage_action,
        )
        return {
            "status": "ok",
            "question": q,
            "display_answer": None,
            "answer": None,
            "recent_searches": _recent_searches_snapshot(),
            "usage_state": usage_state,
            "error": None,
        }

    if usage_action in {"pin_query", "unpin_query"} and usage_query:
        try:
            if usage_action == "pin_query":
                usage_state = _USAGE_STORE.pin_query(usage_query)
            else:
                usage_state = _USAGE_STORE.unpin_query(usage_query)
        except Exception as exc:
            print(f"[telemetry warning] usage_action={usage_action} failed: {exc}")
            usage_state = _safe_usage_state_snapshot()
        _record_runtime_observability_event(
            query=usage_query,
            normalized_query=normalize_query(usage_query),
            intent="operator_action",
            resolved_plan="",
            output_mode=(request.output_mode or "").strip().lower() or "none",
            response_time_ms=int((time.perf_counter() - total_started) * 1000),
            routing_time_ms=0,
            retrieval_time_ms=0,
            formatting_time_ms=0,
            result_status="SUCCESS",
            fallback_used=False,
            refusal_reason="",
            provider_lookup_used=False,
            comparison_used=False,
            action=usage_action,
        )
        return {
            "status": "ok",
            "question": usage_query,
            "display_answer": None,
            "answer": None,
            "recent_searches": _recent_searches_snapshot(),
            "usage_state": usage_state,
            "error": None,
        }

    if usage_action in {"track_quick_action", "track_response_mode", "track_copy_action", "track_workflow_action", "tag_friction"}:
        event_map = {
            "track_quick_action": "quick_action",
            "track_response_mode": "response_mode",
            "track_copy_action": "copy_action",
            "track_workflow_action": "workflow_action",
            "tag_friction": "friction_tag",
        }
        event_type = event_map[usage_action]
        event_value = friction_tag if event_type == "friction_tag" else usage_value
        try:
            recorder = getattr(_USAGE_STORE, "record_operator_event", None)
            if callable(recorder):
                usage_state = recorder(
                    event_type,
                    event_value,
                    query=usage_query,
                    metadata={
                        "result_type": usage_context or "operator_ui",
                        "duration_ms": duration_ms,
                    },
                )
            else:
                usage_state = _safe_usage_state_snapshot()
        except Exception as exc:
            print(f"[telemetry warning] usage_action={usage_action} failed: {exc}")
            usage_state = _safe_usage_state_snapshot()
        _record_runtime_observability_event(
            query=usage_query,
            normalized_query=normalize_query(usage_query),
            intent="operator_action",
            resolved_plan="",
            output_mode=(request.output_mode or "").strip().lower() or "none",
            response_time_ms=int((time.perf_counter() - total_started) * 1000),
            routing_time_ms=0,
            retrieval_time_ms=0,
            formatting_time_ms=0,
            result_status="SUCCESS",
            fallback_used=False,
            refusal_reason="",
            provider_lookup_used=False,
            comparison_used=False,
            action=usage_action,
        )
        return {
            "status": "ok",
            "question": usage_query,
            "display_answer": None,
            "answer": None,
            "recent_searches": _recent_searches_snapshot(),
            "usage_state": usage_state,
            "error": None,
        }

    if not q:
        _record_runtime_observability_event(
            query=str(request.question or ""),
            normalized_query=normalize_query(str(request.question or "")),
            intent="unsupported",
            resolved_plan="",
            output_mode=(request.output_mode or "").strip().lower() or "none",
            response_time_ms=int((time.perf_counter() - total_started) * 1000),
            routing_time_ms=0,
            retrieval_time_ms=0,
            formatting_time_ms=0,
            result_status="FAILED",
            fallback_used=True,
            refusal_reason="Question must not be empty.",
            provider_lookup_used=False,
            comparison_used=False,
        )
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
        routing_started = time.perf_counter()
        hinted_intent = _intent_hint_from_query(q)
        routing_time_ms = int((time.perf_counter() - routing_started) * 1000)

        retrieval_started = time.perf_counter()
        agent_result = handle_user_query(q, output_mode="dict")
        retrieval_time_ms = int((time.perf_counter() - retrieval_started) * 1000)

        display_answer = None
        formatting_time_ms = 0
        requested_mode = (request.output_mode or "").strip().lower()
        accepted_modes = {
            "detailed",
            "whatsapp_summary",
            "arabic_summary",
            "compact_summary",
            "email_summary",
            "benefit_explanation",
        }
        formatter_modes = {
            "whatsapp_summary",
            "email_summary",
            "benefit_explanation",
        }

        if requested_mode and requested_mode not in accepted_modes:
            _USAGE_STORE.log_friction(q, {"ok": False, "intent": "unsupported", "status": "error", "message": f"Invalid output_mode: {request.output_mode}"}, retry_count=int(_USAGE_STORE.load_state().get("top_queries", {}).get(q, 0)))
            usage_state = _USAGE_STORE.ui_snapshot()
            _record_runtime_observability_event(
                query=q,
                normalized_query=normalized_q,
                intent=str(agent_result.get("intent") or hinted_intent or "unsupported"),
                resolved_plan=str(agent_result.get("plan_name") or ""),
                output_mode=requested_mode,
                response_time_ms=int((time.perf_counter() - total_started) * 1000),
                routing_time_ms=routing_time_ms,
                retrieval_time_ms=retrieval_time_ms,
                formatting_time_ms=formatting_time_ms,
                result_status="FAILED",
                fallback_used=True,
                refusal_reason=f"Invalid output_mode: {request.output_mode}",
                provider_lookup_used=False,
                comparison_used=False,
            )
            return {
                "status": "error",
                "question": q,
                "display_answer": None,
                "answer": agent_result,
                "recent_searches": _recent_searches_snapshot(),
                "usage_state": usage_state,
                "error": (
                    f"Invalid output_mode: {request.output_mode}. Supported: "
                    "'detailed', 'whatsapp_summary', 'arabic_summary', 'compact_summary', 'email_summary', 'benefit_explanation'."
                ),
            }

        # Always return status_code=200 and valid structure, even for blocked plans
        # display_answer is ONLY populated when an explicit supported output_mode is requested
        # AND the intent is in the approved formatter set. All other cases return null.
        if agent_result.get("ok"):
            _remember_successful_query(q)
            intent = agent_result.get("intent")
            # Comparison and local presentation modes (arabic/compact/detailed)
            # intentionally stay on deterministic raw rendering.
            if requested_mode in formatter_modes and intent in {"plan_core", "plan_summary", "plan_field"}:
                formatting_started = time.perf_counter()
                display_answer = format_output(agent_result, requested_mode)
                formatting_time_ms = int((time.perf_counter() - formatting_started) * 1000)

        intent_value = str(agent_result.get("intent") or hinted_intent or "unsupported")
        output_mode_value = requested_mode or "detailed"
        provider_lookup_used = intent_value in {"plan_network_city_type", "plan_network_provider"} or hinted_intent == "provider_lookup"
        comparison_used = intent_value == "plan_comparison"
        result_status = classify_result_status(agent_result)
        refusal_reason = "" if agent_result.get("ok") else str(agent_result.get("message") or "")
        fallback_used = bool(not agent_result.get("ok") or not display_answer)

        _record_runtime_observability_event(
            query=q,
            normalized_query=normalized_q,
            intent=intent_value,
            resolved_plan=str(agent_result.get("plan_name") or ""),
            output_mode=output_mode_value,
            response_time_ms=int((time.perf_counter() - total_started) * 1000),
            routing_time_ms=routing_time_ms,
            retrieval_time_ms=retrieval_time_ms,
            formatting_time_ms=formatting_time_ms,
            result_status=result_status,
            fallback_used=fallback_used,
            refusal_reason=refusal_reason,
            provider_lookup_used=provider_lookup_used,
            comparison_used=comparison_used,
        )

        usage_state = _USAGE_STORE.record_query(q, agent_result)
        return {
            "status": "ok" if agent_result.get("ok") else "error",
            "question": q,
            "display_answer": display_answer if agent_result.get("ok") else None,
            "answer": agent_result,
            "recent_searches": _recent_searches_snapshot(),
            "usage_state": usage_state,
            "error": None if agent_result.get("ok") else agent_result.get("message")
        }
    except Exception as e:
        _record_runtime_observability_event(
            query=q,
            normalized_query=normalized_q,
            intent="error",
            resolved_plan="",
            output_mode=(request.output_mode or "").strip().lower() or "none",
            response_time_ms=int((time.perf_counter() - total_started) * 1000),
            routing_time_ms=0,
            retrieval_time_ms=0,
            formatting_time_ms=0,
            result_status="FAILED",
            fallback_used=True,
            refusal_reason=str(e),
            provider_lookup_used=False,
            comparison_used=False,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "question": q,
                "answer": None,
                "error": f"Internal error: {str(e)}"
            }
        )
