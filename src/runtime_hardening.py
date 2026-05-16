from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from src.agent_wrapper import normalize_query as canonical_normalize_query
from src.query.network_lookup import get_network_lookup


_REPO_ROOT = Path(__file__).resolve().parents[1]
_RUNTIME_EVENTS_PATH = _REPO_ROOT / "docs" / "operational_usage" / "runtime_events.jsonl"
_RUNTIME_SUMMARY_PATH = _REPO_ROOT / "docs" / "operational_usage" / "runtime_summary.json"

_REQUIRED_DIRS = (
    _REPO_ROOT / "docs" / "operational_usage",
    _REPO_ROOT / "data" / "local_usage",
    _REPO_ROOT / "data" / "logs",
    _REPO_ROOT / "runtime_data" / "networks",
)

_REQUIRED_FILES = (
    _REPO_ROOT / "runtime_data" / "networks" / "network_list_normalized.csv",
    _REPO_ROOT / "data" / "local_usage" / "recent_usage.json",
)

_ALLOWED_RESULT_STATUSES = {"SUCCESS", "PARTIAL", "REFUSED_OK", "AMBIGUOUS", "FAILED"}
_TOP_LIMIT = 20


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_query(text: str) -> str:
    return canonical_normalize_query(text)


def _safe_load_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _safe_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _increment(counter: dict[str, int], key: str) -> None:
    normalized_key = str(key or "").strip()
    if not normalized_key:
        return
    counter[normalized_key] = int(counter.get(normalized_key, 0)) + 1


def _sorted_counter_dict(counter: Any, *, limit: int | None = None) -> dict[str, int]:
    if not isinstance(counter, dict):
        return {}
    items: list[tuple[str, int]] = []
    for k, v in counter.items():
        key = str(k or "").strip()
        if not key:
            continue
        items.append((key, int(v or 0)))
    items.sort(key=lambda item: (-item[1], item[0]))
    if isinstance(limit, int) and limit > 0:
        items = items[:limit]
    return {k: v for k, v in items}


def classify_result_status(agent_result: dict[str, Any], error_text: str = "") -> str:
    result = agent_result or {}
    ok = bool(result.get("ok"))
    intent = str(result.get("intent") or "").strip().lower()
    message = str(result.get("message") or error_text or "").lower()

    if not ok:
        if intent == "unsupported" or "not supported" in message:
            return "REFUSED_OK"
        if any(token in message for token in ("ambiguous", "unclear", "clarify", "more details")):
            return "AMBIGUOUS"
        return "FAILED"

    if any(token in message for token in ("not specified in plan data", "partially available", "city-level providers instead")):
        return "PARTIAL"

    if intent in {"plan_network_city_type", "plan_network_provider"} and any(
        token in message for token in ("not found", "no exact", "could not find")
    ):
        return "PARTIAL"

    return "SUCCESS"


def _empty_summary() -> dict[str, Any]:
    return {
        "generated_at": "",
        "total_requests": 0,
        "result_status_counts": {status: 0 for status in sorted(_ALLOWED_RESULT_STATUSES)},
        "top_intents": {},
        "top_plans": {},
        "top_output_modes": {},
        "top_failures": {},
        "top_ambiguous_queries": {},
        "most_used_actions": {},
        "top_unsupported_requests": {},
        "top_retry_patterns": {},
        "routing_instability_count": 0,
        "query_occurrences": {},
    }


def _normalize_summary(summary: Any) -> dict[str, Any]:
    base = _empty_summary()
    if isinstance(summary, dict):
        for key in base:
            if key in summary:
                base[key] = summary[key]

        # Legacy compatibility: migrate old key if present.
        legacy_failures = summary.get("top_failed_queries")
        if isinstance(legacy_failures, dict):
            merged = dict(base.get("top_failures") or {})
            for key, count in legacy_failures.items():
                key_text = str(key or "").strip()
                if not key_text:
                    continue
                merged[key_text] = int(merged.get(key_text, 0)) + int(count or 0)
            base["top_failures"] = merged

    base["result_status_counts"] = _sorted_counter_dict(base.get("result_status_counts"))
    for status in sorted(_ALLOWED_RESULT_STATUSES):
        if status not in base["result_status_counts"]:
            base["result_status_counts"][status] = 0

    base["top_intents"] = _sorted_counter_dict(base.get("top_intents"), limit=_TOP_LIMIT)
    base["top_plans"] = _sorted_counter_dict(base.get("top_plans"), limit=_TOP_LIMIT)
    base["top_output_modes"] = _sorted_counter_dict(base.get("top_output_modes"), limit=_TOP_LIMIT)
    base["top_failures"] = _sorted_counter_dict(base.get("top_failures"), limit=_TOP_LIMIT)
    base["top_ambiguous_queries"] = _sorted_counter_dict(base.get("top_ambiguous_queries"), limit=_TOP_LIMIT)
    base["most_used_actions"] = _sorted_counter_dict(base.get("most_used_actions"), limit=_TOP_LIMIT)
    base["top_unsupported_requests"] = _sorted_counter_dict(base.get("top_unsupported_requests"), limit=_TOP_LIMIT)
    base["top_retry_patterns"] = _sorted_counter_dict(base.get("top_retry_patterns"), limit=_TOP_LIMIT)
    base["query_occurrences"] = _sorted_counter_dict(base.get("query_occurrences"), limit=200)
    base["total_requests"] = int(base.get("total_requests") or 0)
    base["routing_instability_count"] = int(base.get("routing_instability_count") or 0)
    base["generated_at"] = str(base.get("generated_at") or "")
    return base


class RuntimeHardeningStore:
    def __init__(self, events_path: Path | None = None, summary_path: Path | None = None) -> None:
        self.events_path = events_path or _RUNTIME_EVENTS_PATH
        self.summary_path = summary_path or _RUNTIME_SUMMARY_PATH
        self._lock = Lock()

    def record_runtime_event(self, event: dict[str, Any]) -> bool:
        """Best-effort telemetry recording that never raises into the response path."""
        try:
            payload = dict(event)
            payload["timestamp"] = str(payload.get("timestamp") or _now_iso())
            payload["normalized_query"] = normalize_query(str(payload.get("query") or payload.get("normalized_query") or ""))

            status = str(payload.get("result_status") or "FAILED").upper()
            if status not in _ALLOWED_RESULT_STATUSES:
                status = "FAILED"
                payload["result_status"] = status

            with self._lock:
                self.events_path.parent.mkdir(parents=True, exist_ok=True)
                with self.events_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

                summary = _normalize_summary(_safe_load_json(self.summary_path, _empty_summary()))

                summary["generated_at"] = _now_iso()
                summary["total_requests"] = int(summary.get("total_requests") or 0) + 1
                summary["result_status_counts"][status] = int(summary["result_status_counts"].get(status) or 0) + 1

                _increment(summary["top_intents"], str(payload.get("intent") or "unknown"))
                _increment(summary["top_plans"], str(payload.get("resolved_plan") or "unknown"))
                _increment(summary["top_output_modes"], str(payload.get("output_mode") or "detailed"))
                _increment(summary["most_used_actions"], str(payload.get("action") or "ask"))

                normalized_query = str(payload.get("normalized_query") or "")
                if normalized_query:
                    _increment(summary["query_occurrences"], normalized_query)
                    if int(summary["query_occurrences"].get(normalized_query) or 0) > 1:
                        _increment(summary["top_retry_patterns"], normalized_query)

                if status == "FAILED":
                    _increment(summary["top_failures"], normalized_query or str(payload.get("query") or "unknown"))
                if status == "AMBIGUOUS":
                    _increment(summary["top_ambiguous_queries"], normalized_query or str(payload.get("query") or "unknown"))
                    summary["routing_instability_count"] = int(summary.get("routing_instability_count") or 0) + 1
                if status == "REFUSED_OK":
                    _increment(summary["top_unsupported_requests"], normalized_query or str(payload.get("query") or "unknown"))

                _safe_write_json(self.summary_path, _normalize_summary(summary))
            return True
        except Exception:
            # Telemetry is best-effort; never break response handling.
            return False

    def diagnostics_snapshot(self) -> dict[str, Any]:
        return _normalize_summary(_safe_load_json(self.summary_path, _empty_summary()))


def _check_json_files_parse() -> tuple[bool, list[str]]:
    errors: list[str] = []
    json_candidates = [
        _REPO_ROOT / "data" / "local_usage" / "recent_usage.json",
        _REPO_ROOT / "data" / "logs" / "operator_friction.json",
        _REPO_ROOT / "docs" / "operational_usage" / "runtime_summary.json",
        *_REPO_ROOT.joinpath("output").glob("*.json"),
        *_REPO_ROOT.joinpath("runtime_data").glob("*.json"),
    ]
    for path in json_candidates:
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"malformed_json:{path.relative_to(_REPO_ROOT)}:{exc}")
    return (len(errors) == 0, errors)


def run_startup_validation() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []

    required_dirs_ok = True
    for directory in _REQUIRED_DIRS:
        exists = directory.exists() and directory.is_dir()
        checks.append({"check": f"dir:{directory.relative_to(_REPO_ROOT)}", "ok": exists})
        if not exists:
            required_dirs_ok = False
            errors.append(f"missing_directory:{directory.relative_to(_REPO_ROOT)}")

    required_files_ok = True
    for file_path in _REQUIRED_FILES:
        exists = file_path.exists() and file_path.is_file()
        non_empty = exists and file_path.stat().st_size > 0
        checks.append({"check": f"file:{file_path.relative_to(_REPO_ROOT)}", "ok": bool(exists and non_empty)})
        if not exists or not non_empty:
            required_files_ok = False
            errors.append(f"missing_or_empty_file:{file_path.relative_to(_REPO_ROOT)}")

    provider_ok = False
    try:
        lookup = get_network_lookup()
        provider_ok = hasattr(lookup, "df") and bool(getattr(lookup, "df", None) is not None and len(lookup.df) > 0)
        if provider_ok:
            required_columns = {"provider_name", "city", "type"}
            missing = [column for column in required_columns if column not in set(lookup.df.columns)]
            if missing:
                provider_ok = False
                errors.append(f"provider_dataset_missing_fields:{','.join(sorted(missing))}")
    except Exception as exc:
        errors.append(f"provider_dataset_load_failed:{exc}")

    checks.append({"check": "provider_dataset_load", "ok": provider_ok})

    json_ok, json_errors = _check_json_files_parse()
    checks.append({"check": "json_parse", "ok": json_ok})
    errors.extend(json_errors)

    telemetry_ok = True
    try:
        _RUNTIME_EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _RUNTIME_EVENTS_PATH.open("a", encoding="utf-8"):
            pass
        if not _RUNTIME_SUMMARY_PATH.exists():
            _safe_write_json(_RUNTIME_SUMMARY_PATH, _empty_summary())
        else:
            _safe_load_json(_RUNTIME_SUMMARY_PATH, _empty_summary())
    except Exception as exc:
        telemetry_ok = False
        errors.append(f"telemetry_not_writable:{exc}")

    checks.append({"check": "telemetry_writable", "ok": telemetry_ok})

    passed = required_dirs_ok and required_files_ok and provider_ok and json_ok and telemetry_ok
    return {
        "passed": passed,
        "checks": checks,
        "errors": errors,
        "timestamp": _now_iso(),
    }


def build_health_payload(startup_validation: dict[str, Any]) -> dict[str, str]:
    validation_passed = bool(startup_validation.get("passed"))

    provider_ok = any(item.get("check") == "provider_dataset_load" and item.get("ok") for item in startup_validation.get("checks", []))
    telemetry_ok = any(item.get("check") == "telemetry_writable" and item.get("ok") for item in startup_validation.get("checks", []))

    return {
        "api": "ok",
        "plan_loader": "ok" if validation_passed else "degraded",
        "provider_index": "ok" if provider_ok else "degraded",
        "telemetry": "ok" if telemetry_ok else "degraded",
        "startup_validation": "passed" if validation_passed else "failed",
    }
