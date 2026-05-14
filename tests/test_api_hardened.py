import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_home_page_serves_ui():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
    assert "NGI AI Sales Assistant" in resp.text


def test_home_provider_city_dropdown_is_controlled():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert '<select id="providerCity">' in html
    assert 'id="providerCity" type="text"' not in html
    for city in [
        "Dubai",
        "Sharjah",
        "Abu Dhabi",
        "Ajman",
        "Al Ain",
        "Ras Al Khaimah",
        "Fujairah",
        "Umm Al Quwain",
    ]:
        assert f'<option value="{city}">{city}</option>' in html


def test_home_provider_area_dropdown_phase1_is_controlled():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert '<select id="providerArea" disabled>' in html
    assert '<option value="">Select Area (Optional)</option>' in html
    assert "const areaOptionsByCity = " in html
    # Cities must be present as keys
    assert '"Dubai"' in html
    assert '"Sharjah"' in html
    assert '"Abu Dhabi"' in html
    assert '"Ajman"' in html
    # Key operational Sharjah areas must appear in the dropdown (dynamic from CSV)
    assert "Rolla" in html
    assert "Muwaileh" in html
    # Key Dubai areas must appear
    assert "Al Barsha" in html
    assert "Business Bay" in html


def test_home_provider_query_templates_are_deterministic_with_optional_area():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "let query = 'List ' + type + ' providers in ' + city + ' for ' + plan;" in html
    assert "query = 'List ' + type + ' providers in ' + area + ' ' + city + ' for ' + plan;" in html
    assert "providerCityEl.addEventListener('change', refreshAreaOptions);" in html


def test_home_productivity_polish_controls_present():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert 'class="panel sticky-search"' in html
    assert 'Usage Intelligence' in html
    assert 'Pinned Searches' in html
    assert 'Top Repeated Searches' in html
    assert 'Query Categories' in html
    assert 'id="clearRecentBtn"' in html
    assert 'id="clearPinnedBtn"' in html
    assert 'Clear Recent Searches' in html
    assert 'id="copyResponseBtn"' in html
    assert 'id="copyFeedback"' in html
    assert 'id="providerTypeChips"' in html
    assert 'data-provider-type="hospital"' in html
    assert 'data-provider-type="clinic"' in html
    assert 'data-provider-type="pharmacy"' in html
    assert 'data-provider-type="lab"' in html


def test_home_plan_dropdowns_are_controlled_with_required_plans():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert '<select id="planName">' in html
    assert '<select id="providerPlan">' in html
    assert '<select id="planA">' in html
    assert '<select id="planB">' in html

    assert 'id="planName" type="text"' not in html
    assert 'id="providerPlan" type="text"' not in html
    assert 'id="planA" type="text"' not in html
    assert 'id="planB" type="text"' not in html

    for plan in [
        "Classic 1",
        "Classic 1R",
        "Classic 2",
        "Classic 2R",
        "Classic 3",
        "Classic 4",
        "Prime 1",
        "Prime 2",
        "Remedy 2",
        "Remedy 3",
        "Remedy 4",
        "Remedy 5",
        "Remedy 6",
    ]:
        assert f'<option value="{plan}">{plan}</option>' in html


def test_home_plan_query_templates_are_unchanged():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "const query = 'Summarize ' + planName;" in html
    assert "const query = 'Compare ' + planA + ' vs ' + planB;" in html

def test_ask_smoke():
    resp = client.post("/ask", json={"question": "Hello"})
    assert resp.status_code == 200
    data = resp.json()
    expected_keys = {"status", "question", "answer", "error", "display_answer", "recent_searches", "usage_state"}
    assert set(data.keys()).issubset(expected_keys)
    # Accept status == "error" for unsupported queries, but require valid structure
    assert data["question"] == "Hello"
    assert data["status"] in ("ok", "error")
    # If error, must have a safe message and answer/display_answer present
    if data["status"] == "error":
        assert ("answer" in data or "display_answer" in data)
        # Accept answer can be None for unsupported
        assert isinstance(data.get("error"), str) or data["error"] is None
    else:
        assert data["answer"] is not None
        assert data["error"] is None

def test_ask_supported():
    # Use a known supported question (Remedy 03 summary)
    q = "اعطني ملخص لخطة ريميدي 03"
    resp = client.post("/ask", json={"question": q})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["question"] == q
    assert data["answer"] is not None
    assert data["answer"]["intent"] == "plan_summary"
    assert data["answer"]["plan_name"] == "Remedy 03"
    assert data["error"] is None

def test_ask_empty():
    resp = client.post("/ask", json={"question": "   "})
    assert resp.status_code == 400
    data = resp.json()
    assert data["status"] == "error"
    assert data["answer"] is None
    assert data["error"]

def test_ask_unsupported():
    # Query that is guaranteed to be unsupported
    q = "unsupported gibberish"
    resp = client.post("/ask", json={"question": q})
    assert resp.status_code == 200
    data = resp.json()
    expected_keys = {"status", "question", "answer", "error", "display_answer", "recent_searches", "usage_state"}
    assert set(data.keys()).issubset(expected_keys)
    assert data["status"] in ("error", "not_found")
    # answer can be None or a safe fallback
    assert "answer" in data or "display_answer" in data
    assert data["error"] or data.get("error") is None

def test_ask_internal_error(monkeypatch):
    # Patch handle_user_query to raise
    def boom(*a, **kw):
        raise RuntimeError("fail!")
    import src.api.app
    monkeypatch.setattr(src.api.app, "handle_user_query", boom)
    resp = client.post("/ask", json={"question": "Hello"})
    assert resp.status_code == 500
    data = resp.json()
    assert data["status"] == "error"
    assert data["answer"] is None
    assert "fail!" in data["error"]


def test_ask_formatted_output_mode_preserves_raw_answer():
    q = "What is the annual limit for Remedy 04?"
    raw_resp = client.post("/ask", json={"question": q})
    fmt_resp = client.post("/ask", json={"question": q, "output_mode": "whatsapp_summary"})

    assert raw_resp.status_code == 200
    assert fmt_resp.status_code == 200

    raw_data = raw_resp.json()
    fmt_data = fmt_resp.json()

    assert raw_data["answer"] == fmt_data["answer"]
    assert raw_data["answer"]["ok"] is True
    assert raw_data["answer"]["intent"] == "plan_core"
    assert fmt_data["display_answer"]
    assert "Remedy 04" in fmt_data["display_answer"]
    assert fmt_data["display_answer"] != raw_data["display_answer"]


def test_ask_invalid_output_mode_blocked():
    resp = client.post("/ask", json={"question": "What is the annual limit for Remedy 04?", "output_mode": "json_export"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error"
    assert data["display_answer"] is None
    assert "invalid output_mode" in data["error"].lower()


def test_ask_unsupported_intent_not_formatted():
    resp = client.post("/ask", json={"question": "Provider 24HOUR PHARMACY in Remedy 6 network?", "output_mode": "whatsapp_summary"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error"
    assert data["display_answer"] is None
    assert data["answer"]["ok"] is False or data["answer"]["intent"] not in {"plan_core", "plan_summary", "plan_field", "plan_comparison"}


def test_ask_approval_gate_skips_formatter(monkeypatch):
    import src.api.app as api_app

    def fake_handle_user_query(*args, **kwargs):
        return {
            "ok": False,
            "intent": "unsupported",
            "plan_name": None,
            "tool_name": None,
            "data": None,
            "message": "blocked",
            "normalized": {"status": "not_found", "tool": None, "answer": None, "errors": ["blocked"]},
        }

    def boom(*args, **kwargs):
        raise AssertionError("formatter should not be called when approval gate fails")

    monkeypatch.setattr(api_app, "handle_user_query", fake_handle_user_query)
    monkeypatch.setattr(api_app, "format_output", boom)

    resp = client.post("/ask", json={"question": "What is the annual limit for Remedy 04?", "output_mode": "whatsapp_summary"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error"
    assert data["display_answer"] is None
    assert data["error"] == "blocked"


def test_recent_searches_tracks_only_successful_queries(monkeypatch):
    import src.api.app as api_app

    api_app._RECENT_SUCCESSFUL_QUERIES.clear()

    def fake_handle_user_query(q, output_mode="dict"):
        if q == "unsupported gibberish":
            return {
                "ok": False,
                "intent": "unsupported",
                "plan_name": None,
                "tool_name": None,
                "data": None,
                "message": "not supported",
                "normalized": {"status": "not_found", "tool": None, "answer": None, "errors": ["not supported"]},
            }
        return {
            "ok": True,
            "intent": "plan_summary",
            "plan_name": "Remedy 03",
            "tool_name": "plan_summary",
            "data": {},
            "message": "ok",
            "normalized": {"status": "ok", "tool": "plan_summary", "answer": "ok", "errors": []},
        }

    monkeypatch.setattr(api_app, "handle_user_query", fake_handle_user_query)

    first = client.post("/ask", json={"question": "Summarize Remedy 03"})
    second = client.post("/ask", json={"question": "Compare Classic 1 vs Prime 1"})
    third = client.post("/ask", json={"question": "unsupported gibberish"})

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 200

    second_recent = second.json()["recent_searches"]
    assert second_recent == ["Compare Classic 1 vs Prime 1", "Summarize Remedy 03"]

    third_recent = third.json()["recent_searches"]
    assert third_recent == second_recent


def test_recent_searches_keeps_last_ten(monkeypatch):
    import src.api.app as api_app

    api_app._RECENT_SUCCESSFUL_QUERIES.clear()

    def fake_success(*args, **kwargs):
        return {
            "ok": True,
            "intent": "plan_summary",
            "plan_name": "Remedy 03",
            "tool_name": "plan_summary",
            "data": {},
            "message": "ok",
            "normalized": {"status": "ok", "tool": "plan_summary", "answer": "ok", "errors": []},
        }

    monkeypatch.setattr(api_app, "handle_user_query", fake_success)

    latest = None
    for i in range(12):
        latest = client.post("/ask", json={"question": f"Summarize Plan {i}"})

    assert latest is not None
    payload = latest.json()
    recent = payload["recent_searches"]
    assert len(recent) == 10
    assert recent[0] == "Summarize Plan 11"
    assert recent[-1] == "Summarize Plan 2"
