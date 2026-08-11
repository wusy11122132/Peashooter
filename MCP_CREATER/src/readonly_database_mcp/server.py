from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any

from mcp.server.fastmcp import FastMCP

from .asset_catalog import AssetCatalog
from .catalog_builder import build_core_catalog
from .config import (
    get_asset_root,
    get_clickhouse_config,
    get_external_mysql_config,
    get_mysql_config,
    get_personal_knowledge_path,
)
from .database import query_clickhouse as execute_clickhouse
from .database import query_mysql as execute_mysql

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)

mcp = FastMCP(
    "readonly-database",
    instructions=(
        "Call search_data_assets at the default core level to select databases, tables, and fields. "
        "For approved business metrics and filters request knowledge_level='shared'; request "
        "knowledge_level='personal' only when the user wants personal extensions. Query internal "
        "MySQL with query_mysql, external MySQL with query_external_mysql, and external ClickHouse "
        "with query_clickhouse. 777 is an internal environment alias, not a product: always query it "
        "with query_mysql, using aaa-ios for game data or 777_actilogs for activity logs. Reuse the "
        "applicable Classic/Golden external MySQL table and field definitions, but not external "
        "database names or ClickHouse tables. Never assume 777 data is synchronized with external data. "
        "Only read-only SELECT SQL is accepted."
    ),
)


@mcp.tool()
async def query_mysql(sql: str, max_rows: int = 100) -> dict[str, Any]:
    """Query internal MySQL, including 777 data in aaa-ios and logs in 777_actilogs."""
    return await asyncio.to_thread(execute_mysql, get_mysql_config(), sql, max_rows)


@mcp.tool()
async def query_external_mysql(sql: str, max_rows: int = 100) -> dict[str, Any]:
    """Run one read-only SELECT query against the external MySQL database."""
    return await asyncio.to_thread(
        execute_mysql,
        get_external_mysql_config(),
        sql,
        max_rows,
        connection_name="external_mysql",
    )


@mcp.tool()
async def query_clickhouse(sql: str, max_rows: int = 100) -> dict[str, Any]:
    """Run one read-only SELECT query against the external ClickHouse database."""
    return await asyncio.to_thread(execute_clickhouse, get_clickhouse_config(), sql, max_rows)


@mcp.tool()
async def search_data_assets(
    query: str,
    product: str | None = None,
    platform: str | None = None,
    asset_type: str | None = None,
    knowledge_level: str = "core",
    limit: int = 10,
) -> dict[str, Any]:
    """Find data assets; core is technical only, while shared/personal explicitly add business knowledge."""
    root = get_asset_root()
    catalog = await asyncio.to_thread(AssetCatalog.load, root, get_personal_knowledge_path(root), knowledge_level)
    return await asyncio.to_thread(catalog.search, query, product, platform, asset_type, limit)


@mcp.tool()
async def get_data_asset(asset_id: str) -> dict[str, Any]:
    """Load one complete core, shared, or personal asset with authority and conflict metadata."""
    root = get_asset_root()
    catalog = await asyncio.to_thread(AssetCatalog.load, root, get_personal_knowledge_path(root), "personal")
    return await asyncio.to_thread(catalog.get, asset_id)


def main() -> None:
    build_core_catalog(get_asset_root())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
