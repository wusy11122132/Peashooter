from __future__ import annotations

import logging
import time
from typing import Any

import clickhouse_connect
import pymysql

from .config import ClickHouseConfig, MySQLConfig
from .serialization import serialize_rows
from .sql_security import validate_readonly_sql

LOGGER = logging.getLogger(__name__)
QUERY_TIMEOUT_SECONDS = 30
MAX_ROWS_LIMIT = 1000


class DatabaseQueryError(RuntimeError):
    """Safe database error suitable for returning over MCP."""


def validate_max_rows(max_rows: int) -> int:
    if isinstance(max_rows, bool) or not isinstance(max_rows, int):
        raise ValueError("max_rows must be an integer")
    if not 1 <= max_rows <= MAX_ROWS_LIMIT:
        raise ValueError(f"max_rows must be between 1 and {MAX_ROWS_LIMIT}")
    return max_rows


def _result(connection: str, database: str, columns: list[str], rows: list[tuple[Any, ...]], max_rows: int, started: float) -> dict[str, Any]:
    truncated = len(rows) > max_rows
    visible_rows = rows[:max_rows]
    return {
        "connection": connection,
        "database": database,
        "columns": columns,
        "rows": serialize_rows(visible_rows),
        "row_count": len(visible_rows),
        "truncated": truncated,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
    }


def _safe_failure(connection: str, exc: Exception) -> DatabaseQueryError:
    LOGGER.error("%s query failed (%s)", connection, type(exc).__name__)
    return DatabaseQueryError(f"{connection} query failed ({type(exc).__name__})")


def _close_mysql(connection: Any) -> None:
    try:
        connection.rollback()
    except Exception as exc:
        LOGGER.error("mysql rollback failed (%s)", type(exc).__name__)
    try:
        connection.close()
    except Exception as exc:
        LOGGER.error("mysql close failed (%s)", type(exc).__name__)


def query_mysql(
    config: MySQLConfig,
    sql: str,
    max_rows: int = 100,
    *,
    connection_name: str = "internal_mysql",
) -> dict[str, Any]:
    max_rows = validate_max_rows(max_rows)
    sql = validate_readonly_sql(sql, "mysql")
    started = time.perf_counter()
    db_connection = None
    try:
        db_connection = pymysql.connect(
            host=config.host,
            port=config.port,
            user=config.username,
            password=config.password,
            database=config.database,
            charset=config.charset,
            autocommit=False,
            connect_timeout=QUERY_TIMEOUT_SECONDS,
            read_timeout=QUERY_TIMEOUT_SECONDS,
            write_timeout=QUERY_TIMEOUT_SECONDS,
        )
        with db_connection.cursor() as cursor:
            cursor.execute(f"SET SESSION MAX_EXECUTION_TIME = {QUERY_TIMEOUT_SECONDS * 1000}")
            cursor.execute("START TRANSACTION READ ONLY")
            cursor.execute(sql)
            columns = [description[0] for description in (cursor.description or [])]
            rows = list(cursor.fetchmany(max_rows + 1))
        return _result(connection_name, config.database, columns, rows, max_rows, started)
    except Exception as exc:
        raise _safe_failure(connection_name, exc) from None
    finally:
        if db_connection is not None:
            _close_mysql(db_connection)


def query_clickhouse(
    config: ClickHouseConfig,
    sql: str,
    max_rows: int = 100,
    *,
    connection_name: str = "external_clickhouse",
) -> dict[str, Any]:
    max_rows = validate_max_rows(max_rows)
    sql = validate_readonly_sql(sql, "clickhouse")
    started = time.perf_counter()
    client = None
    try:
        client = clickhouse_connect.get_client(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
            database=config.database,
            secure=config.secure,
            connect_timeout=QUERY_TIMEOUT_SECONDS,
            send_receive_timeout=QUERY_TIMEOUT_SECONDS,
        )
        query_result = client.query(
            sql,
            settings={
                "readonly": 1,
                "max_execution_time": QUERY_TIMEOUT_SECONDS,
                "max_result_rows": max_rows + 1,
                "result_overflow_mode": "break",
            },
        )
        rows = list(query_result.result_rows)
        columns = list(query_result.column_names)
        return _result(connection_name, config.database, columns, rows, max_rows, started)
    except Exception as exc:
        raise _safe_failure(connection_name, exc) from None
    finally:
        if client is not None:
            try:
                client.close()
            except Exception as exc:
                LOGGER.error("clickhouse close failed (%s)", type(exc).__name__)
