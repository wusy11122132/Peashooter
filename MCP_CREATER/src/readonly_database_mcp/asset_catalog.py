from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_builder import (
    CatalogBuildError,
    build_core_catalog,
    build_knowledge_index,
    knowledge_index_is_current,
)


class AssetCatalogError(RuntimeError):
    """Safe catalog error suitable for returning over MCP."""


PRODUCT_ALIASES = {
    "classic": {"classic", "aaa", "casino", "经典"},
    "golden": {"golden", "黄金"},
    "fatcat": {"fatcat", "fat cat", "肥猫"},
    "reels": {"reels"},
}
PLATFORM_ALIASES = {"ios": {"ios", "iphone", "苹果"}, "android": {"android", "安卓"}}
KNOWLEDGE_LEVELS = {"core": 0, "shared": 1, "personal": 2}
QUERY_EXPANSIONS = {
    "留存": {"retention", "login", "login_diff", "cohort", "ltv"},
    "付费": {"payment", "charge", "revenue", "payer", "order"},
    "充值": {"payment", "charge", "revenue", "order"},
    "广告收入": {"ad-revenue", "ad_revenue", "monetize", "revenueintegration"},
    "买量": {"roi", "campaign", "install", "afcost", "ads"},
    "活跃": {"dau", "login", "spin", "active"},
    "活动": {"activity", "acti", "schedule", "event"},
    "生命周期": {"lifecycle", "retention", "ltv"},
    "字段": {"field", "schema", "column"},
    "过滤": {"filter", "exclude", "specialuser", "test"},
    "rtp": {"rtp", "totalwin", "totalbet", "payback"},
    "spin": {"spin", "slot_payback", "finance_logs", "betlogs"},
}
LIST_FIELDS = {
    "products", "platforms", "types", "engines", "databases", "tables",
    "fields", "metrics", "templates", "conflicts",
}


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: str | None, aliases: dict[str, set[str]], label: str) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    for canonical, names in aliases.items():
        if normalized == canonical or normalized in names:
            return canonical
    raise ValueError(f"Unsupported {label}: {value}")


def _knowledge_level(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in KNOWLEDGE_LEVELS:
        raise ValueError("knowledge_level must be core, shared, or personal")
    return normalized


def _terms(query: str) -> set[str]:
    lowered = query.lower().strip()
    terms = {lowered}
    terms.update(re.findall(r"[a-z0-9_*-]+", lowered))
    for phrase, expansions in QUERY_EXPANSIONS.items():
        if phrase in lowered:
            terms.add(phrase)
            terms.update(expansions)
    for canonical, aliases in PRODUCT_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            terms.add(canonical)
            terms.update(aliases)
    for canonical, aliases in PLATFORM_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            terms.add(canonical)
            terms.update(aliases)
    return {term for term in terms if term}


@dataclass
class AssetCatalog:
    asset_root: Path
    personal_path: Path
    assets: list[dict[str, Any]]
    contents: dict[str, str]
    layers: list[str]
    layer_counts: dict[str, int]

    @classmethod
    def load(cls, asset_root: Path, personal_path: Path, knowledge_level: str = "core") -> "AssetCatalog":
        level = _knowledge_level(knowledge_level)
        try:
            core = build_core_catalog(asset_root)
            layers = ["core"]
            assets = list(core["assets"])
            contents = {asset["asset_id"]: asset["content"] for asset in assets}
            layer_counts = {"core": len(assets), "shared": 0, "personal": 0}
            if KNOWLEDGE_LEVELS[level] >= KNOWLEDGE_LEVELS["shared"]:
                shared = asset_root / "knowledge" / "shared"
                if shared.is_dir():
                    if not knowledge_index_is_current(shared, "shared"):
                        build_knowledge_index(shared, "shared")
                    shared_assets, shared_contents = cls._load_knowledge(shared, "shared")
                    assets.extend(shared_assets)
                    contents.update(shared_contents)
                    layer_counts["shared"] = len(shared_assets)
                layers.append("shared")
            if KNOWLEDGE_LEVELS[level] >= KNOWLEDGE_LEVELS["personal"]:
                if personal_path.is_dir():
                    if not knowledge_index_is_current(personal_path, "personal"):
                        build_knowledge_index(personal_path, "personal")
                    personal_assets, personal_contents = cls._load_knowledge(personal_path, "personal")
                    assets.extend(personal_assets)
                    contents.update(personal_contents)
                    layer_counts["personal"] = len(personal_assets)
                layers.append("personal")
        except (OSError, UnicodeError, json.JSONDecodeError, CatalogBuildError) as exc:
            raise AssetCatalogError(f"Data asset catalog could not be prepared ({type(exc).__name__})") from None
        ids = [asset["asset_id"] for asset in assets]
        if len(ids) != len(set(ids)):
            raise AssetCatalogError("Data asset IDs conflict across layers")
        return cls(asset_root.resolve(), personal_path.resolve(), assets, contents, layers, layer_counts)

    @staticmethod
    def _load_knowledge(directory: Path, layer: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
        index = json.loads((directory / "asset-index.json").read_text(encoding="utf-8"))
        if index.get("version") != 2 or index.get("layer") != layer:
            raise AssetCatalogError(f"Unsupported {layer} knowledge index")
        contents: dict[str, str] = {}
        for asset in index["assets"]:
            text = (directory / asset["file"]).read_text(encoding="utf-8")
            content = text[int(asset["start"]):int(asset["end"])].strip()
            if _digest(content.encode("utf-8")) != asset.get("content_sha256"):
                raise AssetCatalogError(f"{layer} knowledge content changed during loading")
            contents[asset["asset_id"]] = content
        return index["assets"], contents

    def get(self, asset_id: str) -> dict[str, Any]:
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise ValueError("asset_id must be a non-empty string")
        for asset in self.assets:
            if asset.get("asset_id") == asset_id:
                return {**asset, "content": self.contents[asset_id]}
        raise AssetCatalogError(f"Data asset not found in loaded layers: {asset_id}")

    def search(
        self,
        query: str,
        product: str | None = None,
        platform: str | None = None,
        asset_type: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 25:
            raise ValueError("limit must be between 1 and 25")
        product = _canonical(product, PRODUCT_ALIASES, "product")
        platform = _canonical(platform, PLATFORM_ALIASES, "platform")
        requested_type = asset_type.strip().lower() if asset_type else None
        terms = _terms(query)
        scored: list[tuple[float, dict[str, Any], str]] = []
        layer_boost = {"core": 0.0, "shared": 1.0, "personal": 0.0}
        for asset in self.assets:
            products = {str(item).lower() for item in asset.get("products", [])}
            platforms = {str(item).lower() for item in asset.get("platforms", [])}
            types = {str(item).lower() for item in asset.get("types", [])}
            if product and product not in products and "shared" not in products:
                continue
            if platform and platform not in platforms and "all" not in platforms:
                continue
            if requested_type and requested_type not in types:
                continue
            content = self.contents[asset["asset_id"]]
            title = str(asset.get("title", "")).lower()
            metadata_text = " ".join(str(item).lower() for key in LIST_FIELDS for item in asset.get(key, []))
            body = content.lower()
            score = float(asset.get("priority", 0)) / 10.0 + layer_boost.get(asset.get("layer", ""), 0.0)
            matched = 0
            for term in terms:
                if term in title:
                    score += 12; matched += 1
                elif term in metadata_text:
                    score += 8; matched += 1
                elif term in body:
                    score += 2; matched += 1
            if product and product in products: score += 10
            if platform and platform in platforms: score += 4
            if requested_type: score += 4
            if matched: scored.append((score, asset, content))
        scored.sort(key=lambda item: (-item[0], -int(item[1].get("priority", 0)), item[1]["asset_id"]))
        results = []
        for score, asset, content in scored[:limit]:
            result = {key: value for key, value in asset.items() if key not in {"start", "end", "content_sha256", "content"}}
            result["score"] = round(score, 2)
            result["confidence"] = "high" if score >= 30 else "medium" if score >= 18 else "low"
            result["excerpt"] = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()[:1200]
            results.append(result)
        return {
            "query": query,
            "knowledge_level": self.layers[-1],
            "layers_searched": self.layers,
            "layer_counts": {layer: self.layer_counts[layer] for layer in self.layers},
            "filters": {"product": product, "platform": platform, "asset_type": requested_type},
            "result_count": len(results),
            "results": results,
        }
