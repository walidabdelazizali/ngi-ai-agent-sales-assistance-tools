import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_ask_smoke():
    resp = client.post("/ask", json={"question": "Hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"status", "question", "answer", "error"}
    assert data["status"] == "ok"
    assert data["question"] == "Hello"
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
    assert resp.status_code == 400
    data = resp.json()
    assert data["status"] == "error"
    assert data["answer"] is not None
    assert data["error"]

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
