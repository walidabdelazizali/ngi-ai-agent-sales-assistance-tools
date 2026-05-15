from pathlib import Path

from fastapi.testclient import TestClient

from src.api.app import app
from src.runtime_hardening import RuntimeHardeningStore, classify_result_status, run_startup_validation


client = TestClient(app)


def test_system_health_endpoint_shape():
    resp = client.get("/system/health")
    assert resp.status_code == 200
    payload = resp.json()
    assert set(payload.keys()) == {
        "api",
        "plan_loader",
        "provider_index",
        "telemetry",
        "startup_validation",
    }
    assert payload["api"] == "ok"


def test_runtime_store_writes_jsonl_and_summary(tmp_path: Path):
    events_path = tmp_path / "runtime_events.jsonl"
    summary_path = tmp_path / "runtime_summary.json"
    store = RuntimeHardeningStore(events_path=events_path, summary_path=summary_path)

    store.record_runtime_event(
        {
            "query": "Compare Classic 1 vs Prime 1",
            "intent": "plan_comparison",
            "resolved_plan": "Classic 1 vs Prime 1",
            "output_mode": "compact_summary",
            "response_time_ms": 210,
            "routing_time_ms": 5,
            "retrieval_time_ms": 180,
            "formatting_time_ms": 20,
            "result_status": "SUCCESS",
            "fallback_used": False,
            "refusal_reason": "",
            "provider_lookup_used": False,
            "comparison_used": True,
            "action": "ask",
        }
    )

    store.record_runtime_event(
        {
            "query": "best plan for me",
            "intent": "unsupported",
            "resolved_plan": "",
            "output_mode": "detailed",
            "response_time_ms": 80,
            "routing_time_ms": 2,
            "retrieval_time_ms": 40,
            "formatting_time_ms": 0,
            "result_status": "REFUSED_OK",
            "fallback_used": True,
            "refusal_reason": "not supported",
            "provider_lookup_used": False,
            "comparison_used": False,
            "action": "ask",
        }
    )

    assert events_path.exists()
    lines = events_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2

    summary = store.diagnostics_snapshot()
    assert int(summary["total_requests"]) == 2
    assert int(summary["result_status_counts"]["SUCCESS"]) == 1
    assert int(summary["result_status_counts"]["REFUSED_OK"]) == 1
    assert int(summary["top_intents"]["plan_comparison"]) == 1
    assert int(summary["most_used_actions"]["ask"]) == 2
    assert int(summary["top_failures"].get("best plan for me", 0)) == 0


def test_runtime_store_never_raises_on_write_failure(tmp_path: Path):
    events_path = tmp_path / "missing" / "runtime_events.jsonl"
    summary_path = tmp_path / "runtime_summary.json"
    store = RuntimeHardeningStore(events_path=events_path, summary_path=summary_path)

    # Simulate a write failure by replacing directory with a file.
    blocker = tmp_path / "missing"
    blocker.write_text("not a directory", encoding="utf-8")

    ok = store.record_runtime_event(
        {
            "query": "Summarize Classic 1",
            "intent": "plan_summary",
            "resolved_plan": "Classic 1",
            "output_mode": "detailed",
            "result_status": "SUCCESS",
        }
    )
    assert ok is False


def test_result_status_classification_is_deterministic():
    assert classify_result_status({"ok": True, "intent": "plan_summary", "message": "Plan: Classic 1"}) == "SUCCESS"
    assert classify_result_status({"ok": False, "intent": "unsupported", "message": "not supported"}) == "REFUSED_OK"
    assert classify_result_status({"ok": False, "intent": "plan_summary", "message": "ambiguous input"}) == "AMBIGUOUS"
    assert classify_result_status({"ok": False, "intent": "plan_summary", "message": "unexpected"}) == "FAILED"


def test_startup_validation_structure():
    report = run_startup_validation()
    assert isinstance(report, dict)
    assert {"passed", "checks", "errors", "timestamp"}.issubset(set(report.keys()))
    assert isinstance(report["checks"], list)
    assert isinstance(report["errors"], list)
