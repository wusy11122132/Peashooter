from __future__ import annotations

import re
from datetime import datetime
from email.utils import parsedate_to_datetime

ACTIVITY_RE = re.compile(r"\bActivity[\s._-]*(\d+)\b", re.IGNORECASE)
UNSAFE_RE = re.compile(r"[^A-Za-z0-9]+")


def _evidence_time(evidence: dict, fallback: datetime | None) -> datetime:
    received_at = evidence.get("received_at")
    if received_at:
        try:
            return datetime.fromisoformat(str(received_at))
        except ValueError:
            pass
    message_date = evidence.get("date")
    if message_date:
        try:
            return parsedate_to_datetime(str(message_date))
        except (TypeError, ValueError):
            pass
    return fallback or datetime.now().astimezone()


def _query_values(evidence: dict, name: str) -> list[str]:
    query = evidence.get("query", {})
    if not isinstance(query, dict):
        return []
    for key, values in query.items():
        if str(key).casefold() != name.casefold():
            continue
        if isinstance(values, list):
            return [str(value) for value in values if str(value).strip()]
        if str(values).strip():
            return [str(values)]
    return []


def _safe_label(value: str) -> str:
    return UNSAFE_RE.sub("-", value).strip("-")


def _artifact_label(evidence: dict) -> str:
    route_values = _query_values(evidence, "CH") + _query_values(evidence, "Opt")
    for value in route_values + [str(evidence.get("body", ""))]:
        if match := ACTIVITY_RE.search(value):
            return f"Activity{match.group(1)}"

    route = "-".join(filter(None, (_safe_label(value) for value in route_values)))
    return route[:64].rstrip("-") or "general"


def artifact_stem(evidence: dict, unique_id: str, fallback_time: datetime | None = None) -> str:
    moment = _evidence_time(evidence, fallback_time)
    short_id = _safe_label(unique_id)[:8] or "item"
    return f"{moment:%Y%m%d-%H%M%S}-{_artifact_label(evidence)}-{short_id}"
