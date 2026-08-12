from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path

import keyring

from .config import build_domain_map, load_settings
from .imap_client import ReadOnlyMailbox
from .naming import artifact_stem
from .parser import extract_evidence, incident_fingerprint, matches_filter, message_body
from .state import StateStore

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "config.yaml"


def _settings(path: str | None):
    return load_settings(Path(path) if path else DEFAULT_CONFIG)


def _prune_logs(settings, now: datetime | None = None) -> None:
    current = now or datetime.now().astimezone()
    log_dir = settings.root / "var" / "logs"
    if not log_dir.is_dir():
        return
    cutoff = current.date() - timedelta(days=2)
    for path in log_dir.glob("watcher-*.log"):
        try:
            log_date = datetime.strptime(path.stem.removeprefix("watcher-"), "%Y-%m-%d").date()
            if log_date < cutoff:
                path.unlink()
        except (OSError, ValueError):
            continue
    legacy = log_dir / "watcher.log"
    try:
        legacy.unlink(missing_ok=True)
    except OSError:
        pass


def _log_error(settings, message: str) -> None:
    _log_line(settings, message)


def _log_line(settings, message: str) -> None:
    now = datetime.now().astimezone()
    _prune_logs(settings, now)
    path = settings.root / "var" / "logs" / f"watcher-{now:%Y-%m-%d}.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{now.isoformat(timespec='seconds')} {message}\n")


def _status_path(settings) -> Path:
    raw = getattr(settings, "raw", {})
    state = raw.get("state", {}) if isinstance(raw, dict) else {}
    configured = state.get("status_file", "var/status.json")
    resolver = getattr(settings, "path", None)
    return resolver(configured) if resolver else settings.root / configured


def _write_status(settings, phase: str, **details) -> None:
    payload = {
        "phase": phase,
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        **details,
    }
    path = _status_path(settings)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(path)
    except OSError:
        return


def _preview_since(raw: dict) -> datetime:
    value = raw["polling"].get("preview_since")
    if not value:
        raise RuntimeError("polling.preview_since is not configured")
    cutoff = datetime.fromisoformat(str(value))
    if cutoff.tzinfo is None:
        raise RuntimeError("polling.preview_since must include a timezone")
    return cutoff


def _mapped_projects(domains: list[str], domain_map: dict[str, str]) -> dict[str, str]:
    return {domain: domain_map[domain] for domain in domains if domain in domain_map}


def set_credentials(args) -> int:
    settings = _settings(args.config)
    imap = settings.raw["imap"]
    username = args.username or imap.get("username") or input("Enterprise email address: ").strip()
    if not username:
        raise SystemExit("Email username is required")
    password = getpass("IMAP client password: ")
    keyring.set_password(imap["credential_service"], username, password)
    print(f"Credential stored for {username}. Set imap.username in config.yaml to the same address.")
    return 0


def list_domains(args) -> int:
    mapping = build_domain_map(_settings(args.config))
    print(json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def check_config(args) -> int:
    settings = _settings(args.config)
    print(json.dumps({"status": "ok", "config": str(settings.root)}, ensure_ascii=False, indent=2))
    return 0


def claim_messages(settings, cursor_cutoff: datetime | None = None) -> list[dict]:
    raw = settings.raw
    imap = raw["imap"]
    username = imap.get("username", "").strip()
    if not username:
        raise RuntimeError("imap.username is empty")
    password = keyring.get_password(imap["credential_service"], username)
    if not password:
        raise RuntimeError("credential not found")

    state = StateStore(settings.path(raw["state"]["database"]))
    evidence_dir = settings.path(raw["state"]["evidence_directory"])
    evidence_dir.mkdir(parents=True, exist_ok=True)
    domain_map = build_domain_map(settings)
    filters = raw["filters"]
    polling = raw["polling"]
    claimed: list[dict] = []

    mailbox_name = imap["mailbox"]
    with ReadOnlyMailbox(imap["host"], int(imap["port"]), username, password, mailbox_name) as mailbox:
        cursor = state.get_mailbox_cursor(mailbox_name)
        if cursor is None or cursor["uidvalidity"] != mailbox.uidvalidity:
            all_uids = mailbox.all_uids()
            latest_uid = max(all_uids, key=int) if all_uids else "0"
            latest_time = (
                mailbox.internal_date(latest_uid) if all_uids else (cursor_cutoff or datetime.now().astimezone())
            )
            state.reset_mailbox_cursor(
                mailbox_name, mailbox.uidvalidity, latest_uid, latest_time.isoformat()
            )
            return []

        retries = state.claim_retry(
            mailbox_name,
            cursor["initialized_at"],
            int(polling["lease_minutes"]),
            int(polling["max_messages"]),
        )
        for retry in retries:
            path = Path(retry["evidence_path"])
            if not path.is_file():
                state.complete(retry["message_key"])
                continue
            evidence = json.loads(path.read_text(encoding="utf-8"))
            claimed.append({**retry, "evidence": evidence})
        if claimed:
            return claimed

        cursor_time = datetime.fromisoformat(cursor["last_message_time"])
        candidates = []
        for uid in mailbox.uids_since(cursor_time):
            received_at = mailbox.internal_date(uid)
            if int(uid) > int(cursor["last_uid"]) and (cursor_cutoff is None or received_at <= cursor_cutoff):
                candidates.append((received_at, uid))
        for received_at, uid in sorted(candidates, key=lambda item: int(item[1])):
            message = mailbox.fetch(uid)
            body = message_body(message)
            if not matches_filter(message, body, filters["subject_contains"], filters["keyword"]):
                state.advance_mailbox_cursor(
                    mailbox_name, mailbox.uidvalidity, uid, received_at.isoformat()
                )
                continue
            extracted = extract_evidence(message, body)
            projects = _mapped_projects(extracted.domains, domain_map)
            if not projects:
                state.advance_mailbox_cursor(
                    mailbox_name, mailbox.uidvalidity, uid, received_at.isoformat()
                )
                continue
            key = hashlib.sha256(f"{mailbox_name}:{mailbox.uidvalidity}:{uid}".encode()).hexdigest()[:24]
            evidence = extracted.as_dict()
            evidence["projects"] = projects
            evidence["message_key"] = key
            evidence["received_at"] = received_at.isoformat()
            path = evidence_dir / f"{artifact_stem(evidence, key, received_at)}.json"
            path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
            if state.claim(key, mailbox_name, mailbox.uidvalidity, uid, str(path), int(polling["lease_minutes"])):
                item = {"message_key": key, "evidence_path": str(path), "evidence": evidence}
                if len(claimed) < int(polling["max_messages"]):
                    claimed.append(item)
                else:
                    state.release(key)
            state.advance_mailbox_cursor(
                mailbox_name, mailbox.uidvalidity, uid, received_at.isoformat()
            )
    return claimed


def poll(args) -> int:
    settings = _settings(args.config)
    try:
        claimed = claim_messages(settings)
    except RuntimeError as error:
        print(json.dumps({"status": "configuration_required", "reason": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "ok", "messages": claimed}, ensure_ascii=False, indent=2))
    return 0


def run_once(args) -> int:
    settings = _settings(args.config)
    _prune_logs(settings)
    run_started_at = datetime.now().astimezone()
    _write_status(settings, "starting", started_at=run_started_at.isoformat(timespec="seconds"))
    _log_line(settings, "run_started")
    _write_status(settings, "polling")
    try:
        messages = claim_messages(settings, cursor_cutoff=run_started_at)
    except Exception as error:
        _write_status(settings, "failed", error=str(error)[:2000])
        _log_error(settings, f"poll_failed {error}")
        if sys.stderr is not None:
            print(json.dumps({"status": "poll_failed", "reason": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if not messages:
        _write_status(settings, "idle")
        _log_line(settings, "poll_complete messages=0")
        return 0

    from .analyzer import analyze, launch_fix

    raw = settings.raw
    analysis_config = raw["analysis"]
    store = StateStore(settings.path(raw["state"]["database"]))
    failures = 0
    for message in messages:
        evidence = message["evidence"]
        message_key = message["message_key"]
        fingerprint = incident_fingerprint(extract_evidence_from_dict(evidence))
        should_analyze = store.claim_incident(
            fingerprint,
            message["evidence_path"],
            int(analysis_config["fingerprint_cooldown_hours"]),
            int(raw["polling"]["lease_minutes"]),
        )
        if not should_analyze:
            store.complete(message_key)
            _write_status(settings, "deduplicated", message_key=message_key, fingerprint=fingerprint)
            _log_line(settings, f"incident_skipped message_key={message_key} fingerprint={fingerprint}")
            continue
        try:
            _write_status(settings, "analyzing", message_key=message_key, fingerprint=fingerprint)
            _log_line(settings, f"analysis_started message_key={message_key} fingerprint={fingerprint}")
            result, analysis_path, report_path = analyze(settings, evidence, fingerprint)
            store.record_analysis(
                fingerprint,
                str(analysis_path),
                str(report_path),
                result["action"],
                float(result["confidence"]),
            )
            store.complete(message_key)
            _write_status(
                settings,
                "analysis_complete",
                message_key=message_key,
                fingerprint=fingerprint,
                action=result["action"],
                report_path=str(report_path),
            )
            _log_line(
                settings,
                f"analysis_complete message_key={message_key} fingerprint={fingerprint} action={result['action']}",
            )
            if result["action"] not in set(analysis_config["actionable"]):
                continue
            if not analysis_config.get("show_scheduled_approval", False):
                continue
            from .approval import request_approval

            _write_status(settings, "waiting_approval", message_key=message_key, fingerprint=fingerprint)
            _log_line(settings, f"approval_waiting message_key={message_key} fingerprint={fingerprint}")
            decision = request_approval(
                result["summary"],
                result["cause"],
                result["action"],
                float(result["confidence"]),
                report_path,
            )
            if decision == "approve":
                store.approve_incident(fingerprint)
                _write_status(settings, "approved", message_key=message_key, fingerprint=fingerprint)
                launch_fix(settings, evidence, result, report_path)
            elif decision == "ignore":
                store.ignore_incident(fingerprint)
                _write_status(settings, "ignored", message_key=message_key, fingerprint=fingerprint)
            else:
                _write_status(settings, "deferred", message_key=message_key, fingerprint=fingerprint)
        except Exception as error:
            failures += 1
            store.fail_incident(fingerprint, str(error))
            store.release(message_key)
            _write_status(settings, "failed", message_key=message_key, fingerprint=fingerprint, error=str(error)[:2000])
            _log_error(settings, f"analysis_failed fingerprint={fingerprint} error={error}")
            if sys.stderr is not None:
                print(
                    json.dumps(
                        {"status": "analysis_failed", "message_key": message_key, "reason": str(error)},
                        ensure_ascii=False,
                    ),
                    file=sys.stderr,
                )
    if not failures:
        _write_status(settings, "idle")
        _log_line(settings, f"run_complete messages={len(messages)}")
    return 1 if failures else 0


def preview_latest(args) -> int:
    settings = _settings(args.config)
    raw = settings.raw
    imap = raw["imap"]
    username = imap.get("username", "").strip()
    password = keyring.get_password(imap["credential_service"], username) if username else None
    if not username or not password:
        print("Enterprise email credential is not configured", file=sys.stderr)
        return 2

    domain_map = build_domain_map(settings)
    filters = raw["filters"]
    preview_since = _preview_since(raw)
    evidence = None
    with ReadOnlyMailbox(imap["host"], int(imap["port"]), username, password, imap["mailbox"]) as mailbox:
        # IMAP SINCE has day-level precision, so verify INTERNALDATE before fetching the body.
        uids = mailbox.uids_since(preview_since)[-int(raw["polling"].get("preview_scan_limit", 100)) :]
        for uid in reversed(uids):
            received_at = mailbox.internal_date(uid)
            if received_at <= preview_since:
                continue
            message = mailbox.fetch(uid)
            body = message_body(message)
            if not matches_filter(message, body, filters["subject_contains"], filters["keyword"]):
                continue
            extracted = extract_evidence(message, body)
            projects = _mapped_projects(extracted.domains, domain_map)
            if not projects:
                continue
            evidence = extracted.as_dict()
            evidence["projects"] = projects
            evidence["message_key"] = hashlib.sha256(
                f"{imap['mailbox']}:{mailbox.uidvalidity}:{uid}".encode()
            ).hexdigest()[:24]
            evidence["received_at"] = received_at.isoformat()
            break
    if evidence is None:
        print(f"No matching error email found after {preview_since.isoformat()}")
        return 0

    from .analyzer import _validate_result, analyze, launch_fix
    from .approval import request_approval

    store = StateStore(settings.path(raw["state"]["database"]))
    fingerprint = incident_fingerprint(extract_evidence_from_dict(evidence))
    incident = store.get_incident(fingerprint)
    result = None
    report_path = None
    if incident and incident["analysis_path"] and incident["report_path"]:
        analysis_path = Path(incident["analysis_path"])
        existing_report = Path(incident["report_path"])
        if analysis_path.is_file() and existing_report.is_file():
            try:
                result = _validate_result(json.loads(analysis_path.read_text(encoding="utf-8")))
                report_path = existing_report
            except (json.JSONDecodeError, RuntimeError):
                result = None
    if result is None or report_path is None:
        result, analysis_path, report_path = analyze(settings, evidence, fingerprint)
        if incident:
            store.record_analysis(
                fingerprint,
                str(analysis_path),
                str(report_path),
                result["action"],
                float(result["confidence"]),
            )

    decision = request_approval(
        result["summary"], result["cause"], result["action"], float(result["confidence"]), report_path
    )
    if decision == "approve":
        store.approve_incident(fingerprint)
        launch_fix(settings, evidence, result, report_path)
    elif decision == "ignore":
        store.ignore_incident(fingerprint)
    return 0


def extract_evidence_from_dict(data: dict):
    from .parser import Evidence

    fields = Evidence.__dataclass_fields__
    return Evidence(**{name: data[name] for name in fields})


def complete(args) -> int:
    settings = _settings(args.config)
    store = StateStore(settings.path(settings.raw["state"]["database"]))
    if not store.complete(args.message_key):
        print("Unknown message key", file=sys.stderr)
        return 1
    print(json.dumps({"status": "completed", "message_key": args.message_key}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only internal error mail intake")
    parser.add_argument("--config")
    sub = parser.add_subparsers(dest="command", required=True)
    credentials = sub.add_parser("set-credentials")
    credentials.add_argument("--username")
    credentials.set_defaults(func=set_credentials)
    domains = sub.add_parser("list-domains")
    domains.set_defaults(func=list_domains)
    checker = sub.add_parser("check-config")
    checker.set_defaults(func=check_config)
    poller = sub.add_parser("poll")
    poller.set_defaults(func=poll)
    runner = sub.add_parser("run-once")
    runner.set_defaults(func=run_once)
    preview = sub.add_parser("preview-latest")
    preview.set_defaults(func=preview_latest)
    done = sub.add_parser("complete")
    done.add_argument("message_key")
    done.set_defaults(func=complete)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
