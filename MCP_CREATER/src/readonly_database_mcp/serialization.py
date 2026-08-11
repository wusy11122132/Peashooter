from __future__ import annotations

import base64
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID


def json_value(value: object) -> object:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (UUID, IPv4Address, IPv6Address)):
        return str(value)
    if isinstance(value, (bytes, bytearray, memoryview)):
        encoded = base64.b64encode(bytes(value)).decode("ascii")
        return {"base64": encoded}
    if isinstance(value, Enum):
        return json_value(value.value)
    if isinstance(value, tuple):
        return [json_value(item) for item in value]
    if isinstance(value, list):
        return [json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    return str(value)


def serialize_rows(rows: list[tuple[object, ...]] | tuple[tuple[object, ...], ...]) -> list[list[object]]:
    return [[json_value(value) for value in row] for row in rows]

