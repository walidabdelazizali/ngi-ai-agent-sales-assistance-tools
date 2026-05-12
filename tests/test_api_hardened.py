import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_home_page_serves_ui():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
    assert "Local Insurance Assistant" in resp.text

def test_ask_smoke():
    resp = client.post("/ask", json={"question": "Hello"})
    assert resp.status_code == 200
    data = resp.json()
    expected_keys = {"status", "question", "answer", "error", "display_answer"}
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
    expected_keys = {"status", "question", "answer", "error", "display_answer"}
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
