"""
Minimal FastAPI app exposing the insurance assistant for local integration (e.g., n8n).
"""

import json
from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from src.agent_adapter import handle_user_query
from src.operational_usage import get_operational_usage_store
from src.output_packaging import format_output
from src.query.network_lookup import get_network_lookup

app = FastAPI(title="Insurance Assistant API", version="1.0.0")

_USAGE_STORE = get_operational_usage_store()


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
            margin: 24px auto;
            padding: 0 16px;
        }
        .panel {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: 0 10px 24px rgba(19, 34, 53, 0.08);
            padding: 20px;
            margin-bottom: 16px;
        }
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
        .recent-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
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
            min-height: 34px;
            padding: 0 12px;
            border-radius: 8px;
            font-size: 0.88rem;
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
@@
         @media (max-width: 700px) {
             .row { grid-template-columns: 1fr; }
             .grid-2 { grid-template-columns: 1fr; }
             .grid-3 { grid-template-columns: 1fr; }
             .grid-4 { grid-template-columns: 1fr; }
            .usage-grid { grid-template-columns: 1fr; }
            .usage-meta { grid-template-columns: 1fr; }
             button { width: 100%; }
             .recent-header {
                 align-items: stretch;
                 flex-direction: column;
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
            line-height: 1.55;
        }
        #answerVal {
            padding: 4px 0;
        }
        .field + .field {
            margin-top: 10px;
        }
        .response-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0 0 12px;
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
        @media (max-width: 700px) {
            .row { grid-template-columns: 1fr; }
            .grid-2 { grid-template-columns: 1fr; }
            .grid-3 { grid-template-columns: 1fr; }
            .grid-4 { grid-template-columns: 1fr; }
            button { width: 100%; }
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
        </div>

        <div class=\"panel\">
            <div class="recent-header">
                <h2>Usage Intelligence</h2>
                <div class="header-actions">
                    <button id="clearRecentBtn" class="ghost-btn small-btn" type="button">Clear Recent Searches</button>
                    <button id="clearPinnedBtn" class="ghost-btn small-btn" type="button">Clear Pinned</button>
                </div>
            </div>
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

        <div class=\"panel\">
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

        <div class=\"panel\">
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

        <div class=\"panel\">
            <h2>Comparison Search</h2>
            <form id=\"compareForm\">
                <div class="response-actions">
                    <button id="copyResponseBtn" class="ghost-btn small-btn" type="button">Copy Response</button>
                    <span id="copyFeedback" class="copy-feedback">Copied</span>
                </div>
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

        <div class=\"panel\">
            <h2>Response</h2>
            <div id=\"result\" style=\"display:none\">
                <div id=\"statusTag\" class=\"status\"></div>
                <div class=\"field\"><span class=\"label\">Intent</span><div id=\"intentVal\">-</div></div>
                <div class=\"field\"><span class=\"label\">Plan</span><div id=\"planVal\">-</div></div>
                <div class=\"field\"><span class=\"label\">Answer / Message</span><pre id=\"answerVal\"></pre></div>
            </div>
        </div>
    </div>

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
        const intentVal = document.getElementById('intentVal');
        const planVal = document.getElementById('planVal');
        const answerVal = document.getElementById('answerVal');
        const copyResponseBtn = document.getElementById('copyResponseBtn');
        const copyFeedback = document.getElementById('copyFeedback');
        const providerTypeChipsEl = document.getElementById('providerTypeChips');
        const cityFilterChipsEl = document.getElementById('cityFilterChips');
        const planFilterChipsEl = document.getElementById('planFilterChips');
        const contextChipsEl = document.getElementById('contextChips');
        let recentSearches = Array.isArray(initialRecent) ? initialRecent : [];
        let usageState = initialUsage && typeof initialUsage === 'object' ? initialUsage : { recent_queries: [], pinned_queries: [], top_queries: [], last_city: '', last_plan: '', query_categories: [] };
        let _lastCity = (usageState.last_city || '').trim();
        let _lastProviderType = '';
        let _lastPlan = (usageState.last_plan || '').trim();
        const areaOptionsByCity = __AREA_OPTIONS_BY_CITY__;

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

        function showCopiedFeedback() {
            copyFeedback.classList.add('show');
            window.setTimeout(function () {
                copyFeedback.classList.remove('show');
            }, 900);
        }

        async function submitUsageAction(action, query) {
            try {
                const resp = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: query || '', usage_action: action, usage_query: query || '' })
                });
                const payload = await resp.json();
                syncUsageState(payload.usage_state || usageState);
            } catch (_err) {
                // Passive state update only; keep failures silent.
            }
        }

        async function submitQuery(question) {
            const trimmed = (question || '').trim();
            if (!trimmed) {
                resultEl.style.display = 'block';
                paintStatus('REVIEW');
                intentVal.textContent = 'unsupported';
                planVal.textContent = '-';
                answerVal.textContent = 'Question must not be empty.';
                return;
            }

            askBtn.disabled = true;
            askBtn.textContent = 'Searching...';

            try {
                const resp = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: trimmed })
                });
                const payload = await resp.json();
                const answer = payload.answer || {};
                const intent = answer.intent || 'unsupported';
                const plan = answer.plan_name || '-';
                const message = payload.display_answer || answer.message || payload.error || '';
                const opStatus = classifyStatus(trimmed, payload);

                if (answer.ok) {
                    rememberSuccessfulQuery(trimmed);
                }

                syncUsageState(payload.usage_state || usageState);
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
                askBtn.textContent = 'Search';
            }
        }

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
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
            await submitQuery(query);
        });

        providerCityEl.addEventListener('change', refreshAreaOptions);
        providerTypeEl.addEventListener('change', setActiveProviderTypeChip);

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

        copyResponseBtn.addEventListener('click', async function () {
            const text = answerVal.textContent || '';
            try {
                await navigator.clipboard.writeText(text);
                showCopiedFeedback();
            } catch (_err) {
                // Keep UX lightweight; clipboard failure remains silent.
            }
        });

        refreshAreaOptions();
        setActiveProviderTypeChip();
        setActiveCityChip();
        setActivePlanFilterChip();
        renderUsageState();
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
    q = request.question.strip() if isinstance(request.question, str) else ""
    usage_action = (request.usage_action or "").strip().lower()
    usage_query = (request.usage_query or q).strip()

    if usage_action in {"clear_recent", "clear_pinned"}:
        if usage_action == "clear_recent":
            usage_state = _USAGE_STORE.clear_recent()
        else:
            usage_state = _USAGE_STORE.ui_snapshot()
            with _USAGE_STORE._lock:
                state = _USAGE_STORE.load_state()
                state["pinned_queries"] = []
                _USAGE_STORE.save_state(state)
                usage_state = _USAGE_STORE.ui_snapshot()
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
        if usage_action == "pin_query":
            usage_state = _USAGE_STORE.pin_query(usage_query)
        else:
            usage_state = _USAGE_STORE.unpin_query(usage_query)
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
        requested_mode = (request.output_mode or "").strip().lower()
        supported_modes = {"whatsapp_summary", "email_summary", "benefit_explanation"}

        if requested_mode and requested_mode not in supported_modes:
            _USAGE_STORE.log_friction(q, {"ok": False, "intent": "unsupported", "status": "error", "message": f"Invalid output_mode: {request.output_mode}"}, retry_count=int(_USAGE_STORE.load_state().get("top_queries", {}).get(q, 0)))
            usage_state = _USAGE_STORE.ui_snapshot()
            return {
                "status": "error",
                "question": q,
                "display_answer": None,
                "answer": agent_result,
                "recent_searches": _recent_searches_snapshot(),
                "usage_state": usage_state,
                "error": f"Invalid output_mode: {request.output_mode}. Supported: 'whatsapp_summary', 'email_summary', 'benefit_explanation'.",
            }

        # Always return status_code=200 and valid structure, even for blocked plans
        # display_answer is ONLY populated when an explicit supported output_mode is requested
        # AND the intent is in the approved formatter set. All other cases return null.
        if agent_result.get("ok"):
            _remember_successful_query(q)
            intent = agent_result.get("intent")
            if requested_mode in supported_modes and intent in {"plan_core", "plan_summary", "plan_field", "plan_comparison"}:
                display_answer = format_output(agent_result, requested_mode)
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
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "question": q,
                "answer": None,
                "error": f"Internal error: {str(e)}"
            }
        )
