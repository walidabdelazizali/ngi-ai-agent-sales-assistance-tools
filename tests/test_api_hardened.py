import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

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
