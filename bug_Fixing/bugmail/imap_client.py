from __future__ import annotations

import imaplib
import re
from datetime import datetime, timedelta, timezone
from email import policy
from email.parser import BytesParser


class ReadOnlyMailbox:
    def __init__(self, host: str, port: int, username: str, password: str, mailbox: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.mailbox = mailbox
        self.connection: imaplib.IMAP4_SSL | None = None
        self.uidvalidity = "unknown"

    def __enter__(self) -> "ReadOnlyMailbox":
        connection = imaplib.IMAP4_SSL(self.host, self.port)
        connection.login(self.username, self.password)
        status, data = connection.select(self.mailbox, readonly=True)
        if status != "OK":
            connection.logout()
            raise RuntimeError(f"Cannot select mailbox {self.mailbox!r}")
        response = connection.response("UIDVALIDITY")[1]
        if response and response[0]:
            self.uidvalidity = response[0].decode("ascii", errors="replace")
        self.connection = connection
        return self

    def __exit__(self, *_args) -> None:
        if self.connection:
            try:
                self.connection.close()
            finally:
                self.connection.logout()

    def all_uids(self) -> list[str]:
        assert self.connection is not None
        status, data = self.connection.uid("search", None, "ALL")  # type: ignore[arg-type]
        if status != "OK":
            raise RuntimeError("IMAP UID search failed")
        return [item.decode("ascii") for item in data[0].split()]

    def uids_since(self, moment: datetime) -> list[str]:
        assert self.connection is not None
        months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
        criterion = f"{moment.day:02d}-{months[moment.month - 1]}-{moment.year:04d}"
        status, data = self.connection.uid("search", None, "SINCE", criterion)  # type: ignore[arg-type]
        if status != "OK":
            raise RuntimeError("IMAP date search failed")
        return [item.decode("ascii") for item in data[0].split()]

    def internal_date(self, uid: str) -> datetime:
        assert self.connection is not None
        status, data = self.connection.uid("fetch", uid, "(INTERNALDATE)")
        if status != "OK":
            raise RuntimeError(f"IMAP INTERNALDATE fetch failed for UID {uid}")
        raw = b" ".join(item[0] if isinstance(item, tuple) else item for item in data if item)
        match = re.search(
            rb'INTERNALDATE\s+"(\d{1,2})-([A-Za-z]{3})-(\d{4})\s+(\d{2}):(\d{2}):(\d{2})\s+([+-])(\d{2})(\d{2})"',
            raw,
        )
        if not match:
            raise RuntimeError(f"IMAP INTERNALDATE missing for UID {uid}")
        month_names = {name: index for index, name in enumerate(
            (b"Jan", b"Feb", b"Mar", b"Apr", b"May", b"Jun", b"Jul", b"Aug", b"Sep", b"Oct", b"Nov", b"Dec"), 1
        )}
        sign = 1 if match.group(7) == b"+" else -1
        offset = timedelta(hours=int(match.group(8)), minutes=int(match.group(9))) * sign
        return datetime(
            int(match.group(3)), month_names[match.group(2).title()], int(match.group(1)),
            int(match.group(4)), int(match.group(5)), int(match.group(6)), tzinfo=timezone(offset),
        )

    def fetch(self, uid: str):
        assert self.connection is not None
        status, data = self.connection.uid("fetch", uid, "(BODY.PEEK[])")
        if status != "OK" or not data or not isinstance(data[0], tuple):
            raise RuntimeError(f"IMAP fetch failed for UID {uid}")
        return BytesParser(policy=policy.default).parsebytes(data[0][1])
