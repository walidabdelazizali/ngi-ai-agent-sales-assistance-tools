"""Passive local operational usage storage for recent searches and friction logs."""

from __future__ import annotations

import json
import os
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Optional


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_recent_usage_path() -> Path:
    return _repo_root() / "data" / "local_usage" / "recent_usage.json"


def _default_friction_log_path() -> Path:
    return _repo_root() / "data" / "logs" / "operator_friction.json"


def _normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKC", (value or "").strip().lower())
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _empty_state() -> dict[str, Any]:
    return {
        "recent_queries": [],
        "pinned_queries": [],
        "top_queries": {},
        "last_city": "",
        "last_plan": "",
        "query_categories": {},
    }


def _safe_json_load(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _safe_json_write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_path, path)


def _sorted_counter_items(counter_dict: dict[str, int]) -> list[dict[str, Any]]:
    items = sorted(
        ((str(key), int(value)) for key, value in counter_dict.items() if str(key).strip()),
        key=lambda item: (-item[1], item[0].lower(), item[0]),
    )
    return [{"query": query, "count": count} for query, count in items]


def _sorted_category_items(category_dict: dict[str, int]) -> list[dict[str, Any]]:
    items = sorted(
        ((str(key), int(value)) for key, value in category_dict.items() if str(key).strip()),
        key=lambda item: (-item[1], item[0].lower(), item[0]),
    )
    return [{"category": category, "count": count} for category, count in items]


def _category_from_intent(intent: str, query: str) -> str:
    normalized_intent = _normalize_text(intent)
    normalized_query = _normalize_text(query)

    if normalized_intent in {
        "plan_summary",
        "plan_core",
        "plan_field",
        "plan_comparison",
        "plan_network_provider",
        "plan_network_city_type",
        "unsupported",
    }:
        return normalized_intent

    if "compare" in normalized_query or "قارن" in normalized_query:
        return "plan_comparison"
    if any(token in normalized_query for token in ["providers", "provider", "hospital", "clinic", "pharmacy", "lab", "مزود", "مستشفى", "عيادة", "صيدلية", "مختبر"]):
        return "provider_search"
    if any(token in normalized_query for token in ["summary", "summarize", "ملخص", "overview", "details"]):
        return "plan_summary"
    return normalized_intent or "unknown"


def _last_city_from_result(result: dict[str, Any], query: str) -> str:
    value = str(result.get("city") or result.get("requested_city") or "").strip()
    if value:
        return value
    query_text = _normalize_text(query)
    for candidate in ["Dubai", "Sharjah", "Abu Dhabi", "Ajman", "Al Ain", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"]:
        if _normalize_text(candidate) in query_text:
            return candidate
    return ""


def _last_plan_from_result(result: dict[str, Any], query: str) -> str:
    value = str(result.get("plan_name") or "").strip()
    if value:
        return value
    query_text = _normalize_text(query)
    plan_tokens = [
        "remedy 2",
        "remedy 3",
        "remedy 4",
        "remedy 5",
        "remedy 6",
        "classic 1",
        "classic 1r",
        "classic 2",
        "classic 2r",
        "classic 3",
        "classic 4",
        "prime 1",
        "prime 2",
    ]
    for token in plan_tokens:
        if token in query_text:
            return token.title().replace("1R", "1R").replace("2R", "2R")
    return ""


def _classification_for_log(query: str, result: dict[str, Any], retry_count: int) -> Optional[str]:
    normalized_query = _normalize_text(query)
    message = str(result.get("message") or result.get("error") or "")
    intent = _normalize_text(str(result.get("intent") or ""))
    ok = bool(result.get("ok"))

    if not ok:
        if "not supported" in message.lower() or intent == "unsupported":
            return "BLOCKED"
        if "not found" in message.lower() or "ambiguous" in message.lower():
            return "REVIEW"
        return "GAP"

    if retry_count > 0 or len(normalized_query) > 120:
        return "REVIEW"

    return None


@dataclass
class OperationalUsageStore:
    recent_usage_path: Path = field(default_factory=_default_recent_usage_path)
    friction_log_path: Path = field(default_factory=_default_friction_log_path)
    recent_limit: int = 100
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def load_state(self) -> dict[str, Any]:
        state = _empty_state()
        loaded = _safe_json_load(self.recent_usage_path, state)
        if isinstance(loaded, dict):
            state.update({k: loaded.get(k, state[k]) for k in state})
        state["recent_queries"] = [str(item).strip() for item in state.get("recent_queries", []) if str(item).strip()]
        state["pinned_queries"] = [str(item).strip() for item in state.get("pinned_queries", []) if str(item).strip()]
        state["top_queries"] = {str(k).strip(): int(v) for k, v in dict(state.get("top_queries", {})).items() if str(k).strip()}
        state["query_categories"] = {str(k).strip(): int(v) for k, v in dict(state.get("query_categories", {})).items() if str(k).strip()}
        state["last_city"] = str(state.get("last_city") or "").strip()
        state["last_plan"] = str(state.get("last_plan") or "").strip()
        return state

    def save_state(self, state: dict[str, Any]) -> None:
        payload = {
            "recent_queries": list(state.get("recent_queries", []))[: self.recent_limit],
            "pinned_queries": list(dict.fromkeys(str(item).strip() for item in state.get("pinned_queries", []) if str(item).strip())),
            "top_queries": dict(state.get("top_queries", {})),
            "last_city": str(state.get("last_city") or "").strip(),
            "last_plan": str(state.get("last_plan") or "").strip(),
            "query_categories": dict(state.get("query_categories", {})),
        }
        _safe_json_write(self.recent_usage_path, payload)

    def ui_snapshot(self) -> dict[str, Any]:
        state = self.load_state()
        return {
            "recent_queries": list(state["recent_queries"]),
            "pinned_queries": list(state["pinned_queries"]),
            "top_queries": _sorted_counter_items(state["top_queries"]),
            "last_city": state["last_city"],
            "last_plan": state["last_plan"],
            "query_categories": _sorted_category_items(state["query_categories"]),
        }

    def clear_recent(self) -> dict[str, Any]:
        with self._lock:
            state = self.load_state()
            state["recent_queries"] = []
            self.save_state(state)
            return self.ui_snapshot()

    def pin_query(self, query: str) -> dict[str, Any]:
        normalized = str(query or "").strip()
        if not normalized:
            return self.ui_snapshot()
        with self._lock:
            state = self.load_state()
            pinned = [item for item in state["pinned_queries"] if item != normalized]
            pinned.insert(0, normalized)
            state["pinned_queries"] = pinned
            self.save_state(state)
            return self.ui_snapshot()

    def unpin_query(self, query: str) -> dict[str, Any]:
        normalized = str(query or "").strip()
        with self._lock:
            state = self.load_state()
            state["pinned_queries"] = [item for item in state["pinned_queries"] if item != normalized]
            self.save_state(state)
            return self.ui_snapshot()

    def record_query(self, query: str, result: dict[str, Any]) -> dict[str, Any]:
        normalized_query = str(query or "").strip()
        if not normalized_query:
            return self.ui_snapshot()

        result = result or {}
        category = _category_from_intent(str(result.get("intent") or ""), normalized_query)

        with self._lock:
            state = self.load_state()
            retry_count = int(state["top_queries"].get(normalized_query, 0))
            state["top_queries"][normalized_query] = retry_count + 1
            state["query_categories"][category] = int(state["query_categories"].get(category, 0)) + 1

            if bool(result.get("ok")):
                recent = [item for item in state["recent_queries"] if item != normalized_query]
                recent.insert(0, normalized_query)
                state["recent_queries"] = recent[: self.recent_limit]

            last_city = _last_city_from_result(result, normalized_query)
            if last_city:
                state["last_city"] = last_city

            last_plan = _last_plan_from_result(result, normalized_query)
            if last_plan:
                state["last_plan"] = last_plan

            self.save_state(state)

            classification = _classification_for_log(normalized_query, result, retry_count)
            if classification:
                self._append_friction_log(
                    {
                        "timestamp": _now_iso(),
                        "original_query": normalized_query,
                        "normalized_query": _normalize_text(normalized_query),
                        "detected_intent": str(result.get("intent") or "unsupported"),
                        "result_type": str(result.get("status") or result.get("intent") or "unknown"),
                        "retry_count": retry_count,
                        "classification": classification,
                    }
                )

            return self.ui_snapshot()

    def _append_friction_log(self, entry: dict[str, Any]) -> None:
        current = _safe_json_load(self.friction_log_path, [])
        if not isinstance(current, list):
            current = []
        current.append(entry)
        _safe_json_write(self.friction_log_path, current)

    def log_friction(self, query: str, result: dict[str, Any], retry_count: int = 0) -> Optional[dict[str, Any]]:
        classification = _classification_for_log(query, result, retry_count)
        if not classification:
            return None
        entry = {
            "timestamp": _now_iso(),
            "original_query": str(query or "").strip(),
            "normalized_query": _normalize_text(query),
            "detected_intent": str(result.get("intent") or "unsupported"),
            "result_type": str(result.get("status") or result.get("intent") or "unknown"),
            "retry_count": int(retry_count),
            "classification": classification,
        }
        with self._lock:
            self._append_friction_log(entry)
        return entry


_DEFAULT_USAGE_STORE = OperationalUsageStore()


def get_operational_usage_store() -> OperationalUsageStore:
    return _DEFAULT_USAGE_STORE
