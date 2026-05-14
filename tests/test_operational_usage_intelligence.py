from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import src.api.app as api_app
from src.api.app import app
from src.operational_usage import OperationalUsageStore

client = TestClient(app)


@pytest.fixture()
def temp_usage_store(tmp_path, monkeypatch):
    store = OperationalUsageStore(
        recent_usage_path=tmp_path / "recent_usage.json",
        friction_log_path=tmp_path / "operator_friction.json",
        recent_limit=100,
    )
    monkeypatch.setattr(api_app, "_USAGE_STORE", store)
    api_app._RECENT_SUCCESSFUL_QUERIES.clear()
    return store


def test_recent_query_persistence(temp_usage_store):
    resp = client.post("/ask", json={"question": "Summarize Remedy 03"})
    assert resp.status_code == 200

    state = temp_usage_store.load_state()
    assert state["recent_queries"] == ["Summarize Remedy 03"]

    reloaded = OperationalUsageStore(
        recent_usage_path=temp_usage_store.recent_usage_path,
        friction_log_path=temp_usage_store.friction_log_path,
    )
    assert reloaded.load_state()["recent_queries"] == ["Summarize Remedy 03"]


def test_pinned_query_persistence(temp_usage_store):
    client.post("/ask", json={"question": "Summarize Remedy 03"})
    resp = client.post(
        "/ask",
        json={"question": "", "usage_action": "pin_query", "usage_query": "Summarize Remedy 03"},
    )
    assert resp.status_code == 200

    state = temp_usage_store.load_state()
    assert state["pinned_queries"] == ["Summarize Remedy 03"]

    reloaded = OperationalUsageStore(
        recent_usage_path=temp_usage_store.recent_usage_path,
        friction_log_path=temp_usage_store.friction_log_path,
    )
    assert reloaded.load_state()["pinned_queries"] == ["Summarize Remedy 03"]


def test_bounded_storage_truncation(temp_usage_store):
    for index in range(105):
        temp_usage_store.record_query(
            f"Summarize Plan {index}",
            {"ok": True, "intent": "plan_summary", "plan_name": f"Plan {index}", "city": "Dubai"},
        )

    state = temp_usage_store.load_state()
    assert len(state["recent_queries"]) == 100
    assert state["recent_queries"][0] == "Summarize Plan 104"
    assert state["recent_queries"][-1] == "Summarize Plan 5"


def test_query_category_tracking_and_context(temp_usage_store):
    temp_usage_store.record_query(
        "List hospital providers in Dubai for Remedy 03",
        {"ok": True, "intent": "plan_network_city_type", "plan_name": "Remedy 03", "city": "Dubai"},
    )

    state = temp_usage_store.load_state()
    assert state["last_city"] == "Dubai"
    assert state["last_plan"] == "Remedy 03"
    assert state["query_categories"]["plan_network_city_type"] == 1
    assert state["top_queries"]["List hospital providers in Dubai for Remedy 03"] == 1


def test_friction_logging_creation_and_append(temp_usage_store):
    first = client.post("/ask", json={"question": "unsupported gibberish"})
    second = client.post("/ask", json={"question": "another unsupported gibberish"})

    assert first.status_code == 200
    assert second.status_code == 200

    friction_path = temp_usage_store.friction_log_path
    assert friction_path.exists()

    entries = json.loads(friction_path.read_text(encoding="utf-8"))
    assert len(entries) >= 2
    assert entries[0]["classification"] in {"BLOCKED", "REVIEW", "GAP"}
    assert entries[0]["original_query"]
    assert entries[0]["normalized_query"]
    assert entries[0]["detected_intent"]
    assert entries[0]["result_type"]
    assert isinstance(entries[0]["retry_count"], int)


def test_safe_friction_logging_append_behavior(temp_usage_store):
    temp_usage_store.log_friction(
        "unsupported gibberish",
        {"ok": False, "intent": "unsupported", "message": "not supported", "status": "error"},
        retry_count=0,
    )
    temp_usage_store.log_friction(
        "unsupported gibberish",
        {"ok": False, "intent": "unsupported", "message": "not supported", "status": "error"},
        retry_count=1,
    )

    entries = json.loads(temp_usage_store.friction_log_path.read_text(encoding="utf-8"))
    assert len(entries) == 2
    assert entries[0]["classification"] == "BLOCKED"
    assert entries[1]["retry_count"] == 1


def test_deterministic_behavior_preservation(temp_usage_store):
    supported = client.post("/ask", json={"question": "What is the annual limit for Remedy 04?"})
    blocked = client.post("/ask", json={"question": "unsupported gibberish"})

    assert supported.status_code == 200
    assert blocked.status_code == 200

    supported_data = supported.json()
    blocked_data = blocked.json()

    assert supported_data["status"] == "ok"
    assert supported_data["answer"]["ok"] is True
    assert supported_data["answer"]["intent"] == "plan_core"
    assert blocked_data["answer"]["ok"] is False
    assert blocked_data["answer"]["intent"] == "unsupported"
