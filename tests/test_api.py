import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_ask_smoke():
    resp = client.post("/ask", json={"question": "Hello"})
    assert resp.status_code == 200
    assert "answer" in resp.json()
    assert "intent" in resp.json()["answer"]

def test_ask_supported():
    # Use a known supported question (Remedy 03 summary)
    q = "اعطني ملخص لخطة ريميدي 03"
    resp = client.post("/ask", json={"question": q})
    assert resp.status_code == 200
    data = resp.json()["answer"]
    assert data["intent"] == "plan_summary"
    assert data["plan_name"] == "Remedy 03"
    assert "message" in data

def test_ask_error():
    # Simulate error by passing a non-string (should be caught by pydantic)
    resp = client.post("/ask", json={"question": 123})
    assert resp.status_code == 422
