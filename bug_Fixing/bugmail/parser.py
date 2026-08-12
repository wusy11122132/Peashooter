from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from email.header import decode_header, make_header
from email.message import Message
from html import unescape
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urlparse


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.parts.append(value)


def _decode_header(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except (LookupError, UnicodeDecodeError):
        return value


def _payload_text(part: Message) -> str:
    data = part.get_payload(decode=True)
    if data is None:
        value = part.get_payload()
        return value if isinstance(value, str) else ""
    if not isinstance(data, bytes):
        return str(data)
    charset = part.get_content_charset() or "utf-8"
    try:
        return data.decode(charset, errors="replace")
    except LookupError:
        return data.decode("utf-8", errors="replace")


def message_body(message: Message) -> str:
    plain: list[str] = []
    html_parts: list[str] = []
    parts = message.walk() if message.is_multipart() else [message]
    for part in parts:
        if part.get_content_disposition() == "attachment":
            continue
        kind = part.get_content_type()
        if kind == "text/plain":
            plain.append(_payload_text(part))
        elif kind == "text/html":
            html_parts.append(_payload_text(part))
    plain_text = unescape("\n".join(plain))
    parser = _TextExtractor()
    parser.feed(unescape("\n".join(html_parts)))
    html_text = unescape("\n".join(parser.parts))
    # Some enterprise mail messages use a tiny plain-text placeholder while the
    # complete diagnostic is only present in the HTML alternative.
    return html_text if len(html_text.strip()) > len(plain_text.strip()) else plain_text


@dataclass(frozen=True)
class Evidence:
    subject: str
    sender: str
    date: str
    body: str
    urls: list[str]
    domains: list[str]
    query: dict[str, list[str]]
    sql_error_codes: list[str]
    tables: list[str]
    columns: list[str]
    last_included_files: list[str]

    def as_dict(self) -> dict:
        return asdict(self)


URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
SQL_CODE_PATTERNS = (
    re.compile(
        r"(?mi)^(?:\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\t)?(\d{3,5})(?=\s+(?:Unknown|Table|You have an error|Duplicate|Incorrect|Cannot|Data too long|Column|Deadlock|Lock wait|Access denied|No database selected))"
    ),
    re.compile(r"(?i)\b(?:SQL|MySQL|DB)\s*(?:error|errno|code)\D{0,8}(\d{3,5})(?!\d)"),
    re.compile(r"(?i)SQLSTATE\[[A-Z0-9]+\](?:\s*\[\d+\])?\D{0,8}(\d{3,5})(?!\d)"),
)
TABLE_RE = re.compile(
    r"(?:Table\s+['`]?[^.'`\s]+\.([A-Za-z0-9_]+)|(?:FROM|INTO|UPDATE|JOIN)\s+`?([A-Za-z0-9_]+)`?)",
    re.IGNORECASE,
)
COLUMN_RE = re.compile(r"Unknown\s+column\s+['`]([^'`]+)['`]", re.IGNORECASE)
LAST_FILE_RE = re.compile(r"LastIncludedFile\s*[:=]\s*([^\s,;]+)", re.IGNORECASE)
LOG_PATH_DOMAIN_RE = re.compile(r"/data/www/([A-Za-z0-9.-]+)/", re.IGNORECASE)
QUERY_FRAGMENT_RE = re.compile(
    r"(?:^|[\s:])/?\??((?:[A-Za-z][A-Za-z0-9_]*=[^&\s\r\n]+)(?:&[A-Za-z][A-Za-z0-9_]*=[^&\s\r\n]+)+)",
    re.IGNORECASE,
)
def _as_terms(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    return [item for item in value if isinstance(item, str) and item.strip()]


def _extract_sql_error_codes(text: str) -> list[str]:
    codes: list[str] = []
    for pattern in SQL_CODE_PATTERNS:
        for code in pattern.findall(text):
            if code not in codes:
                codes.append(code)
    return codes


def matches_filter(message: Message, body: str, subject_contains: str | list[str], keyword: str | list[str]) -> bool:
    subject = _decode_header(message.get("Subject"))
    headers = "\n".join(
        _decode_header(message.get(name))
        for name in ("From", "Sender", "Reply-To", "Resent-From", "X-Forwarded-For")
    )
    subject_terms = _as_terms(subject_contains)
    keyword_terms = _as_terms(keyword)
    haystack = (headers + "\n" + subject + "\n" + body).casefold()
    return any(term.casefold() in subject.casefold() for term in subject_terms) and any(
        term.casefold() in haystack for term in keyword_terms
    )


def extract_evidence(message: Message, body: str) -> Evidence:
    cleaned = unescape(body).replace("\u200b", "")
    urls = [unquote(match.group(0)).rstrip(".,);]") for match in URL_RE.finditer(cleaned)]
    domains: list[str] = []
    query: dict[str, list[str]] = {}
    for url in urls:
        parsed = urlparse(url)
        if parsed.hostname:
            domain = parsed.hostname.rstrip(".").lower()
            if domain not in domains:
                domains.append(domain)
        for key, values in parse_qs(parsed.query, keep_blank_values=True).items():
            query.setdefault(key, []).extend(values)
    for match in LOG_PATH_DOMAIN_RE.finditer(cleaned):
        domain = match.group(1).rstrip(".").lower()
        if domain not in domains:
            domains.append(domain)
    for match in QUERY_FRAGMENT_RE.finditer(cleaned):
        for key, values in parse_qs(match.group(1), keep_blank_values=True).items():
            query.setdefault(key, []).extend(values)
    tables = []
    for match in TABLE_RE.finditer(cleaned):
        table = match.group(1) or match.group(2)
        if table and table not in tables:
            tables.append(table)
    return Evidence(
        subject=_decode_header(message.get("Subject")),
        sender=_decode_header(message.get("From")),
        date=_decode_header(message.get("Date")),
        body=cleaned,
        urls=urls,
        domains=domains,
        query=query,
        sql_error_codes=_extract_sql_error_codes(cleaned),
        tables=tables,
        columns=list(dict.fromkeys(COLUMN_RE.findall(cleaned))),
        last_included_files=list(dict.fromkeys(LAST_FILE_RE.findall(cleaned))),
    )


def incident_fingerprint(evidence: Evidence) -> str:
    query = {
        key.casefold(): sorted(str(value).casefold() for value in values)
        for key, values in evidence.query.items()
        if key.casefold() in {"ch", "opt"}
    }
    identity = {
        "domains": sorted(domain.casefold() for domain in evidence.domains),
        "query": query,
        "codes": sorted(evidence.sql_error_codes),
        "tables": sorted(table.casefold() for table in evidence.tables),
        "columns": sorted(column.casefold() for column in evidence.columns),
    }
    encoded = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:24]
