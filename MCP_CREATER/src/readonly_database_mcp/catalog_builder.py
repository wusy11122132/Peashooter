from __future__ import annotations

import hashlib
import json
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class CatalogBuildError(RuntimeError):
    """Raised when a catalog cannot be built safely."""


ASSET_MARKER = re.compile(
    r"<!--\s*asset\s*\n(?P<meta>.*?)\n-->[ \t]*\n(?P<header>#{2,6})[ \t]+(?P<title>[^\r\n]+)",
    re.DOTALL,
)
CORE_MARKER = re.compile(
    r"<!--\s*core-asset\s*\n(?P<meta>.*?)\n-->[ \t]*\n(?P<header>#{2,6})[ \t]+(?P<title>[^\r\n]+)",
    re.DOTALL,
)
LIST_FIELDS = {
    "products", "platforms", "types", "engines", "databases", "tables",
    "fields", "metrics", "templates", "conflicts",
}
SECRET_PATTERN = re.compile(
    r"(?:\b(?:password|passwd|pass)\b\s*[:=]|(?:mysql|clickhouse)://|(?:\d{1,3}\.){3}\d{1,3})",
    re.IGNORECASE,
)
CORE_ALLOWED_TYPES = {"database", "table", "field", "relationship", "engine", "partition", "technical"}
CORE_FORBIDDEN_TERMS = re.compile(r"(?:指标公式|必须过滤|历史结论|付费率|留存率|ROI\s*=|RTP\s*=)", re.IGNORECASE)
HEADING = re.compile(r"(?m)^##[ \t]+(?P<title>[^\r\n]+)")
KNOWN_CORE_TITLES = {
    "Classic / Golden数据库和核心表": "core-classic-golden-databases",
    "获客和广告成本数据": "core-acquisition-data",
    "广告收入数据": "core-ad-revenue-data",
    "每日快照和场景消耗表": "core-backup-activity-data",
    "活动排期和事件日志": "core-activity-log-data",
    "财务和机器 spin 表": "core-finance-spin-data",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_metadata(raw: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for line in raw.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key == "priority":
            metadata[key] = int(value)
        elif key in LIST_FIELDS:
            metadata[key] = [item.strip() for item in value.split(",") if item.strip()]
        elif key == "generated":
            metadata[key] = value.lower() == "true"
        else:
            metadata[key] = value
    return metadata


def _validate_id(asset_id: str, prefix: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,127}", asset_id) or not asset_id.startswith(prefix + "-"):
        raise CatalogBuildError(f"Invalid {prefix} asset id: {asset_id!r}")


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary.write_text(rendered, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def _file_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    excluded = exclude or set()
    return {
        path.relative_to(root).as_posix(): sha256(path.read_bytes())
        for path in sorted(root.rglob("*.md"))
        if path.name not in excluded
    }


@contextmanager
def _build_lock(root: Path, timeout: float = 15.0) -> Iterator[None]:
    lock = root / ".catalog-build.lock"
    deadline = time.monotonic() + timeout
    while True:
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(descriptor, str(os.getpid()).encode("ascii"))
            os.close(descriptor)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise CatalogBuildError("Timed out waiting for catalog build lock")
            time.sleep(0.05)
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def _sections(text: str, pattern: re.Pattern[str]) -> list[tuple[re.Match[str], str]]:
    matches = list(pattern.finditer(text))
    return [
        (match, text[match.start():(matches[index + 1].start() if index + 1 < len(matches) else len(text))].strip())
        for index, match in enumerate(matches)
    ]


def _plain_core_assets(path: Path, materials: Path, text: str) -> list[dict[str, Any]]:
    headings = list(HEADING.finditer(text))
    assets: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        title = heading.group("title").strip()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.start():end].strip()
        if not section:
            continue
        asset_id = KNOWN_CORE_TITLES.get(title, f"core-material-{sha256(title.encode('utf-8'))[:12]}")
        lowered = section.lower()
        products = []
        if "classic" in lowered or "casino" in lowered: products.append("classic")
        if "golden" in lowered: products.append("golden")
        if "fatcat" in lowered: products.append("fatcat")
        if "reels" in lowered: products.append("reels")
        if not products: products = ["classic", "golden", "fatcat", "reels"]
        engines = []
        if "mysql" in lowered: engines.append("mysql")
        if "clickhouse" in lowered: engines.append("clickhouse")
        identifiers = list(dict.fromkeys(re.findall(r"`([^`]+)`", section)))
        assets.append({
            "asset_id": asset_id,
            "title": title,
            "products": products,
            "platforms": ["ios", "android"],
            "types": ["database", "table", "field", "relationship"],
            "status": "documented",
            "priority": 90,
            "engines": engines,
            "tables": identifiers,
            "layer": "core",
            "authority": "material-derived",
            "generated": True,
            "supersedes": "",
            "conflicts": [],
            "material": path.relative_to(materials).as_posix(),
            "source": "primary:data-catalog.md",
            "content": section,
            "content_sha256": sha256(section.encode("utf-8")),
        })
    return assets


def build_core_catalog(asset_root: Path, *, force: bool = False) -> dict[str, Any]:
    asset_root = asset_root.resolve()
    materials = asset_root / "materials"
    output = asset_root / "core-catalog" / "catalog.json"
    if not materials.is_dir():
        raise CatalogBuildError("Materials directory is missing")
    hashes = _file_hashes(materials)
    if not force and output.is_file():
        try:
            existing = json.loads(output.read_text(encoding="utf-8"))
            if existing.get("version") == 2 and existing.get("material_hashes") == hashes:
                return existing
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass
    with _build_lock(asset_root):
        if not force and output.is_file():
            try:
                existing = json.loads(output.read_text(encoding="utf-8"))
                if existing.get("version") == 2 and existing.get("material_hashes") == hashes:
                    return existing
            except (OSError, UnicodeError, json.JSONDecodeError):
                pass
        assets: list[dict[str, Any]] = []
        seen: set[str] = set()
        for path in sorted(materials.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            marked_sections = _sections(text, CORE_MARKER)
            for match, section in marked_sections:
                metadata = parse_metadata(match.group("meta"))
                asset_id = str(metadata.pop("id", ""))
                _validate_id(asset_id, "core")
                if asset_id in seen:
                    raise CatalogBuildError(f"Duplicate core asset id: {asset_id}")
                seen.add(asset_id)
                types = set(metadata.get("types", []))
                if not types or not types.issubset(CORE_ALLOWED_TYPES):
                    raise CatalogBuildError(f"Core asset has non-technical types: {asset_id}")
                if SECRET_PATTERN.search(section) or CORE_FORBIDDEN_TERMS.search(section):
                    raise CatalogBuildError(f"Core asset contains forbidden content: {asset_id}")
                metadata.update({
                    "asset_id": asset_id,
                    "title": match.group("title").strip(),
                    "layer": "core",
                    "authority": "material-derived",
                    "generated": True,
                    "supersedes": metadata.get("supersedes", ""),
                    "conflicts": metadata.get("conflicts", []),
                    "material": path.relative_to(materials).as_posix(),
                    "content": section,
                    "content_sha256": sha256(section.encode("utf-8")),
                })
                assets.append(metadata)
            if path.name == "data-catalog.md" and not marked_sections:
                for metadata in _plain_core_assets(path, materials, text):
                    asset_id = metadata["asset_id"]
                    if asset_id in seen:
                        raise CatalogBuildError(f"Duplicate core asset id: {asset_id}")
                    if SECRET_PATTERN.search(metadata["content"]) or CORE_FORBIDDEN_TERMS.search(metadata["content"]):
                        raise CatalogBuildError(f"Core asset contains forbidden content: {asset_id}")
                    seen.add(asset_id)
                    assets.append(metadata)
        if not assets:
            raise CatalogBuildError("No core assets were found in materials")
        bundle = {"version": 2, "layer": "core", "material_hashes": hashes, "asset_count": len(assets), "assets": assets}
        _atomic_json(output, bundle)
        return bundle


def core_catalog_is_current(asset_root: Path) -> bool:
    asset_root = asset_root.resolve()
    materials = asset_root / "materials"
    output = asset_root / "core-catalog" / "catalog.json"
    if not materials.is_dir() or not output.is_file():
        return False
    try:
        bundle = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    return bundle.get("version") == 2 and bundle.get("material_hashes") == _file_hashes(materials)


def build_knowledge_index(directory: Path, layer: str) -> dict[str, Any]:
    if layer not in {"shared", "personal"}:
        raise ValueError("Knowledge layer must be shared or personal")
    directory = directory.resolve()
    if not directory.is_dir():
        return {"version": 2, "layer": layer, "files": {}, "asset_count": 0, "assets": []}
    files = _file_hashes(directory, exclude={"template.md"})
    assets: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(directory.rglob("*.md")):
        if path.name == "template.md":
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(directory).as_posix()
        for match, section in _sections(text, ASSET_MARKER):
            metadata = parse_metadata(match.group("meta"))
            asset_id = str(metadata.pop("id", ""))
            _validate_id(asset_id, layer)
            if asset_id in seen:
                raise CatalogBuildError(f"Duplicate {layer} asset id: {asset_id}")
            seen.add(asset_id)
            if metadata.get("layer") != layer:
                raise CatalogBuildError(f"Asset layer mismatch: {asset_id}")
            if SECRET_PATTERN.search(section):
                raise CatalogBuildError(f"Potential secret in {layer} asset: {asset_id}")
            metadata.update({
                "asset_id": asset_id,
                "title": match.group("title").strip(),
                "file": relative,
                "start": match.start(),
                "end": match.start() + len(section),
                "content_sha256": sha256(section.encode("utf-8")),
            })
            assets.append(metadata)
    index = {"version": 2, "layer": layer, "files": files, "asset_count": len(assets), "assets": assets}
    _atomic_json(directory / "asset-index.json", index)
    return index


def knowledge_index_is_current(directory: Path, layer: str) -> bool:
    index_path = directory / "asset-index.json"
    if not index_path.is_file():
        return False
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    return (
        index.get("version") == 2
        and index.get("layer") == layer
        and index.get("files") == _file_hashes(directory, exclude={"template.md"})
    )
