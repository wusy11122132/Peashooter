from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class ClickHouseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str
    secure: bool


@dataclass(frozen=True)
class MySQLConfig:
    host: str
    port: int
    username: str
    password: str
    database: str
    charset: str


def _required(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigurationError(f"Missing required environment variable: {name}")
    return value


def _port(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"Environment variable {name} must be an integer") from exc
    if not 1 <= value <= 65535:
        raise ConfigurationError(f"Environment variable {name} must be between 1 and 65535")
    return value


def _boolean(name: str, default: bool = False) -> bool:
    raw = os.getenv(name, str(default)).strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"Environment variable {name} must be true or false")


@lru_cache(maxsize=1)
def get_clickhouse_config() -> ClickHouseConfig:
    load_dotenv()
    return ClickHouseConfig(
        host=_required("CLICKHOUSE_HOST"),
        port=_port("CLICKHOUSE_PORT", 8123),
        username=_required("CLICKHOUSE_USER"),
        password=_required("CLICKHOUSE_PASSWORD"),
        database=_required("CLICKHOUSE_DATABASE"),
        secure=_boolean("CLICKHOUSE_SECURE"),
    )


@lru_cache(maxsize=1)
def get_mysql_config() -> MySQLConfig:
    load_dotenv()
    return MySQLConfig(
        host=_required("MYSQL_HOST"),
        port=_port("MYSQL_PORT", 3306),
        username=_required("MYSQL_USER"),
        password=_required("MYSQL_PASSWORD"),
        database=_required("MYSQL_DATABASE"),
        charset=os.getenv("MYSQL_CHARSET", "utf8"),
    )


@lru_cache(maxsize=1)
def get_external_mysql_config() -> MySQLConfig:
    load_dotenv()
    return MySQLConfig(
        host=_required("EXTERNAL_MYSQL_HOST"),
        port=_port("EXTERNAL_MYSQL_PORT", 3306),
        username=_required("EXTERNAL_MYSQL_USER"),
        password=_required("EXTERNAL_MYSQL_PASSWORD"),
        database=_required("EXTERNAL_MYSQL_DATABASE"),
        charset=os.getenv("EXTERNAL_MYSQL_CHARSET", "utf8"),
    )


def get_asset_root() -> Path:
    load_dotenv()
    configured = os.getenv("SLOTS_ASSET_ROOT")
    legacy = os.getenv("ASSET_CATALOG_PATH")
    if configured:
        path = Path(configured).expanduser()
    elif legacy:
        legacy_path = Path(legacy).expanduser()
        path = legacy_path.parent if legacy_path.name == "references" else legacy_path
    else:
        project_default = Path.cwd() / "slots-data-analysis"
        package_default = Path(__file__).resolve().parents[2] / "slots-data-analysis"
        path = project_default if project_default.is_dir() else package_default
    return path.resolve()


def get_personal_knowledge_path(asset_root: Path | None = None) -> Path:
    load_dotenv()
    configured = os.getenv("SLOTS_PERSONAL_KNOWLEDGE_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    root = asset_root or get_asset_root()
    return (root / "knowledge" / "personal").resolve()
