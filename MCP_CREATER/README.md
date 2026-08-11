# Read-only Database MCP

本地 Python MCP Server，通过 stdio 为 MCP 客户端提供数据库资产检索和严格只读查询：

- `query_mysql`：查询内网 MySQL
- `query_external_mysql`：查询外网 MySQL
- `query_clickhouse`：查询外网 ClickHouse
- `search_data_assets`：按业务问题检索数据库、表、字段、指标、过滤规则和 SQL 模板
- `get_data_asset`：读取一个完整资产及其来源、状态和核验信息

每个工具接收 `sql` 和可选的 `max_rows`（默认 100，范围 1-1000）。仅允许一条 `SELECT` 或 `WITH ... SELECT`，超时为 30 秒。

## 安装

需要 Python 3.11 或更高版本。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[test]"
```

项目根目录的 `.env` 保存本机连接信息且不会被 Git 跟踪。部署到其他机器时，复制 `.env.example` 为 `.env` 并填写实际值。

默认从 `slots-data-analysis` 加载四层资产。目录位于其他位置时设置 `SLOTS_ASSET_ROOT`；个人知识可通过 `SLOTS_PERSONAL_KNOWLEDGE_PATH` 指向独立目录。

## 启动

```powershell
.\.venv\Scripts\python -m readonly_database_mcp
```

stdio 模式下终端不会出现普通交互提示，这是正常行为。日志只写入 stderr，不会破坏 MCP 消息。

## Codex 配置

将以下配置加入 Codex 的 `config.toml`，并把路径改为本机绝对路径：

```toml
[mcp_servers.readonly_database]
command = "E:\\work\\工作文档\\MCP_CREATER\\.venv\\Scripts\\python.exe"
args = ["-m", "readonly_database_mcp"]
cwd = "E:\\work\\工作文档\\MCP_CREATER"
startup_timeout_sec = 20
tool_timeout_sec = 40
```

重启 Codex 后应出现五个工具。`search_data_assets` 默认只返回 core 技术元数据；需要团队统计口径时传 `knowledge_level="shared"`，明确采用个人扩展时传 `knowledge_level="personal"`。

数据库工具映射：

- 内网 MySQL：`query_mysql`，读取 `MYSQL_*`。
- 外网 MySQL：`query_external_mysql`，读取 `EXTERNAL_MYSQL_*`。
- 外网 ClickHouse：`query_clickhouse`，读取 `CLICKHOUSE_*`。

777 是内网环境别名，不是新产品。用户明确指定 777 时必须使用 `query_mysql`：游戏数据使用 `aaa-ios`，活动日志使用 `777_actilogs`。其表名和字段可参考 Classic / Golden 外网 MySQL 结构，但不能照搬外网库名或 ClickHouse 表，也不能假定内外网数据同步。查询失败或缺表时直接报告，不自动回退到外网。

外网 MySQL 未配置时只会影响 `query_external_mysql`，不会阻止 MCP 启动或其他工具调用。

## Slots 数据分析 Skill

`slots-data-analysis/` 是可独立分发的 Skill，不依赖 `demo-test`。将该目录安装到使用者的 Codex Skills 目录后，Classic、Golden、FatCat、Reels 等业务问题会自动触发选库流程；其他 MCP 客户端也可直接调用资产检索工具。

资产结构如下：

- `materials/`：脱敏后的汇总材料，是 core 的输入。
- `core-catalog/`：MCP 从材料自动生成，不人工编辑，也不扫描数据库。
- `knowledge/shared/`：可选团队公共口径；目录不存在时为 0 项。
- `knowledge/personal/`：可选个人扩展；目录不存在时为 0 项，也可由环境变量指向外部目录。

材料发生变化或配置了知识目录后可运行：

```powershell
.\.venv\Scripts\python slots-data-analysis\scripts\build_core_catalog.py
.\.venv\Scripts\python slots-data-analysis\scripts\build_knowledge_index.py
.\.venv\Scripts\python slots-data-analysis\scripts\validate_catalog.py
```

## 返回格式

```json
{
  "connection": "internal_mysql",
  "database": "mysql",
  "columns": ["id", "name"],
  "rows": [[1, "example"]],
  "row_count": 1,
  "truncated": false,
  "elapsed_ms": 12.34
}
```

日期时间转为 ISO 8601 字符串，Decimal 和 UUID 转为字符串，二进制值转为 `{ "base64": "..." }`。

## 安全说明

服务在应用层解析 SQL，并在数据库层启用只读事务或只读设置。生产使用时仍必须为 MySQL 和 ClickHouse 账号只授予读取权限。不要把 `.env` 提交到版本库；已经通过聊天或其他渠道共享过的密码应当轮换。

## 测试

```powershell
.\.venv\Scripts\python -m pytest
```
