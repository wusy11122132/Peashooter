from __future__ import annotations

import re

from sqlglot import exp, parse
from sqlglot.errors import ParseError


class UnsafeQueryError(ValueError):
    """Raised when SQL is not a single, side-effect-free query."""


_FORBIDDEN_NODE_NAMES = {
    "Alter", "Analyze", "Attach", "Command", "Copy", "Create", "Delete",
    "Detach", "Drop", "Execute", "Grant", "Insert", "Into", "LoadData",
    "Lock", "Merge", "Optimize", "Pragma", "Replace", "Revoke", "Set",
    "TruncateTable", "Unlock", "Update", "Use",
}

_FORBIDDEN_TEXT = re.compile(
    r"(?:\b(?:INTO\s+(?:OUTFILE|DUMPFILE)|FOR\s+(?:UPDATE|SHARE)|LOCK\s+IN\s+SHARE\s+MODE)\b|@[A-Za-z0-9_.$]+\s*:=)",
    re.IGNORECASE,
)


def validate_readonly_sql(sql: str, dialect: str) -> str:
    """Return normalized input after proving it is one read-only query."""
    if not isinstance(sql, str) or not sql.strip():
        raise UnsafeQueryError("SQL must be a non-empty string")

    candidate = sql.strip()
    if _FORBIDDEN_TEXT.search(candidate):
        raise UnsafeQueryError("Only side-effect-free SELECT queries are allowed")

    try:
        statements = [statement for statement in parse(candidate, read=dialect) if statement is not None]
    except ParseError as exc:
        raise UnsafeQueryError("SQL could not be parsed") from exc

    if len(statements) != 1:
        raise UnsafeQueryError("Exactly one SQL statement is allowed")

    statement = statements[0]
    if not isinstance(statement, exp.Query):
        raise UnsafeQueryError("Only SELECT or WITH ... SELECT queries are allowed")
    if not statement.find(exp.Select):
        raise UnsafeQueryError("The statement must contain a SELECT query")

    for node in statement.walk():
        if type(node).__name__ in _FORBIDDEN_NODE_NAMES:
            raise UnsafeQueryError("Only side-effect-free SELECT queries are allowed")

    return candidate
