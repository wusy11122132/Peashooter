from __future__ import annotations

import os
import re
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml


class ConfigurationError(ValueError):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid configuration:\n- " + "\n- ".join(errors))


@dataclass(frozen=True)
class Settings:
    root: Path
    raw: dict

    def path(self, value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else self.root / path


def load_settings(path: Path) -> Settings:
    resolved = path.resolve()
    with resolved.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    if not isinstance(loaded, dict):
        raise ConfigurationError(["configuration root must be a mapping"])
    raw = deepcopy(loaded)
    raw.setdefault("imap", {})
    raw.setdefault("vhosts", {})
    if username := os.environ.get("BUGMAIL_IMAP_USERNAME"):
        raw["imap"]["username"] = username
    if directory := os.environ.get("BUGMAIL_VHOST_DIRECTORY"):
        raw["vhosts"]["directory"] = directory
    _validate(raw)
    return Settings(resolved.parent, raw)


def _validate(raw: dict) -> None:
    errors: list[str] = []
    required = {
        "imap": ("host", "port", "mailbox", "username", "credential_service"),
        "filters": ("subject_contains", "keyword"),
        "polling": ("max_messages", "lease_minutes", "preview_scan_limit", "preview_since"),
        "analysis": (
            "fingerprint_cooldown_hours", "max_evidence_chars", "timeout_seconds",
            "show_scheduled_approval", "actionable", "sql_output_file", "reports_directory",
        ),
        "vhosts": ("directory", "overrides"),
        "state": ("database", "evidence_directory", "status_file"),
    }
    for section, fields in required.items():
        value = raw.get(section)
        if not isinstance(value, dict):
            errors.append(f"{section} must be a mapping")
            continue
        for field in fields:
            if field not in value or value[field] is None or value[field] == "":
                errors.append(f"{section}.{field} is required")

    positive_fields = (
        ("imap", "port"), ("polling", "max_messages"), ("polling", "lease_minutes"),
        ("polling", "preview_scan_limit"), ("analysis", "max_evidence_chars"),
        ("analysis", "timeout_seconds"),
    )
    for section, field in positive_fields:
        value = raw.get(section, {}).get(field) if isinstance(raw.get(section), dict) else None
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value <= 0):
            errors.append(f"{section}.{field} must be a positive integer")

    preview = raw.get("polling", {}).get("preview_since") if isinstance(raw.get("polling"), dict) else None
    if preview:
        try:
            parsed = datetime.fromisoformat(str(preview))
            if parsed.tzinfo is None:
                raise ValueError
        except ValueError:
            errors.append("polling.preview_since must be an ISO timestamp with timezone")

    allowed_actions = {"code_change", "database_change", "config_change", "no_change", "need_info"}
    actions = raw.get("analysis", {}).get("actionable") if isinstance(raw.get("analysis"), dict) else None
    if actions is not None and (
        not isinstance(actions, list) or not actions or any(action not in allowed_actions for action in actions)
    ):
        errors.append("analysis.actionable must be a non-empty list of supported actions")
    for section, field in (("filters", "subject_contains"), ("filters", "keyword")):
        value = raw.get(section, {}).get(field) if isinstance(raw.get(section), dict) else None
        if value is not None and (not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value)):
            errors.append(f"{section}.{field} must be a non-empty list of strings")
    sql_output = raw.get("analysis", {}).get("sql_output_file") if isinstance(raw.get("analysis"), dict) else None
    if sql_output is not None:
        if not isinstance(sql_output, str) or not sql_output.strip():
            errors.append("analysis.sql_output_file must be a non-empty relative path")
        else:
            output_path = Path(sql_output)
            if output_path.is_absolute() or ".." in output_path.parts:
                errors.append("analysis.sql_output_file must stay inside the mapped project")
    if errors:
        raise ConfigurationError(errors)


def _directive(text: str, name: str) -> list[str]:
    pattern = re.compile(
        rf"^[^\S\r\n]*{re.escape(name)}[^\S\r\n]+([^\r\n]*?)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    values: list[str] = []
    for match in pattern.finditer(text):
        values.extend(part.strip('"\'') for part in match.group(1).split() if part.strip('"\''))
    return values


def build_domain_map(settings: Settings) -> dict[str, str]:
    vhost = settings.raw.get("vhosts", {})
    result: dict[str, str] = {}
    directory = Path(vhost.get("directory", ""))
    if directory.is_dir():
        for config_file in sorted(directory.glob("*.conf")):
            text = config_file.read_text(encoding="utf-8", errors="replace")
            roots = _directive(text, "DocumentRoot")
            if not roots:
                continue
            root = str(Path(roots[-1]).resolve())
            for domain in _directive(text, "ServerName") + _directive(text, "ServerAlias"):
                result[domain.rstrip(".").lower()] = root
    for domain, project in vhost.get("overrides", {}).items():
        result[str(domain).rstrip(".").lower()] = str(Path(project).resolve())
    return result
