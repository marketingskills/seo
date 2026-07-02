#!/usr/bin/env python3
"""Infer SEO growth-loop project surfaces from local files.

This script is intentionally heuristic. It helps an agent start the preflight,
but project docs and live verification should override its guesses.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "dist",
    "build",
    "__pycache__",
    "staticfiles",
    ".next",
    ".cache",
    ".agents",
    ".codex",
    ".claude",
    ".gemini",
    ".taskmaster",
    "packaged-skills",
}

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".rs",
    ".rb",
    ".php",
    ".go",
    ".java",
    ".html",
    ".xml",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".env",
    ".example",
}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_files(root: Path, limit: int = 6000):
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            yield path
            count += 1
            if count >= limit:
                return


def read_small(path: Path, max_bytes: int = 200_000) -> str:
    try:
        if path.stat().st_size > max_bytes:
            return ""
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def add_hit(hits: dict[str, list[str]], key: str, path: Path, root: Path, limit: int = 12) -> None:
    bucket = hits.setdefault(key, [])
    value = rel(path, root)
    if len(bucket) < limit and value not in bucket:
        bucket.append(value)


def infer_framework(files: list[Path], root: Path) -> list[str]:
    names = {rel(path, root) for path in files}
    frameworks: list[str] = []
    markers = [
        ("django", ["manage.py", "settings.py", "urls.py"]),
        ("rails", ["Gemfile", "config/routes.rb"]),
        ("laravel", ["artisan", "composer.json"]),
        ("next", ["next.config.js", "next.config.mjs", "next.config.ts"]),
        ("astro", ["astro.config.mjs", "astro.config.ts"]),
        ("hugo", ["hugo.toml"]),
        ("jekyll", ["_config.yml"]),
        ("eleventy", [".eleventy.js", "eleventy.config.js"]),
        ("rust", ["Cargo.toml"]),
        ("wordpress", ["wp-config.php"]),
    ]
    for framework, required in markers:
        if any(name.endswith(marker) or name == marker for name in names for marker in required):
            frameworks.append(framework)
    if "package.json" in names:
        package_text = read_small(root / "package.json")
        for framework, pattern in [
            ("gatsby", r'"gatsby"'),
            ("docusaurus", r'"@docusaurus/'),
            ("nuxt", r'"nuxt"'),
            ("sveltekit", r'"@sveltejs/kit"'),
        ]:
            if re.search(pattern, package_text):
                frameworks.append(framework)
    return sorted(set(frameworks)) or ["unknown"]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 66

    files = list(iter_files(root))
    hits: dict[str, list[str]] = {}

    text_cache: dict[Path, str] = {}
    for path in files:
        name = path.name.lower()
        parts = {part.lower() for part in path.parts}
        suffix = path.suffix.lower()
        relative = rel(path, root).lower()

        if name in {"seo-growth-loop.yaml", ".seo-growth-loop.yaml", "seo_improvements_log.md"}:
            add_hit(hits, "seo_config_or_log", path, root)
        if re.search(r"(daily[_-]?growth|seo[_-]?agent|growth[_-]?workflow|run_.*growth)", name):
            add_hit(hits, "existing_growth_automation", path, root)
        if "growth_queues" in parts or ".repo-growth" in parts:
            add_hit(hits, "existing_growth_queue", path, root)
        if name in {"sitemap.xml", "sitemaps.py", "robots.txt"} or "sitemap" in relative:
            add_hit(hits, "indexing_surface", path, root)
        if any(part in parts for part in {"content", "posts", "blog", "src", "pages", "app"}) and suffix in {".md", ".mdx", ".html"}:
            add_hit(hits, "git_content_candidates", path, root)
        if any(part in parts for part in {"templates", "components", "layouts", "theme", "themes"}) and suffix in {".html", ".jsx", ".tsx", ".vue", ".svelte"}:
            add_hit(hits, "template_candidates", path, root)
        if (
            suffix in {".sql"}
            or "migrations" in parts
            or "migration" in parts
            or "entities" in parts
            or name in {"models.py", "schema.prisma", "models.rs"}
        ):
            add_hit(hits, "database_model_candidates", path, root)

        if suffix in TEXT_EXTENSIONS or name in {".env", ".env.example"}:
            text = text_cache.setdefault(path, read_small(path))
            lowered = text.lower()
            if any(token in lowered for token in ["wp-json", "wordpress", "contentful", "sanity", "webflow", "shopify", "strapi", "ghost"]):
                add_hit(hits, "cms_api_candidates", path, root)
            if any(token in lowered for token in ["refreshagent", "search console", "gsc_property", "indexnow", "authority mark"]):
                add_hit(hits, "seo_data_or_indexing_docs", path, root)
            if any(token in lowered for token in ["x-api-key", "api_key", "prod_api_key", "/api/"]):
                add_hit(hits, "custom_api_candidates", path, root)
            if any(token in lowered for token in ["django admin", "admin surface", "/admin/"]):
                add_hit(hits, "admin_surface_candidates", path, root)

    frameworks = infer_framework(files, root)
    has_git_content = bool(hits.get("git_content_candidates"))
    has_templates = bool(hits.get("template_candidates"))
    has_database = bool(hits.get("database_model_candidates"))
    has_cms_api = bool(hits.get("cms_api_candidates") or hits.get("custom_api_candidates"))
    has_existing_growth = bool(hits.get("existing_growth_automation") or hits.get("existing_growth_queue"))

    if has_cms_api and (has_templates or has_database):
        publishing_mode = "hybrid"
        source_of_truth = "hybrid"
    elif has_database and has_templates:
        publishing_mode = "hybrid"
        source_of_truth = "database"
    elif has_cms_api:
        publishing_mode = "cms_api"
        source_of_truth = "cms_api"
    elif has_git_content:
        publishing_mode = "local_repo"
        source_of_truth = "git"
    elif has_templates:
        publishing_mode = "local_repo"
        source_of_truth = "unknown"
    else:
        publishing_mode = "advisory"
        source_of_truth = "unknown"

    result = {
        "project_dir": str(root),
        "frameworks": frameworks,
        "publishing_mode_guess": publishing_mode,
        "content_source_of_truth_guess": source_of_truth,
        "has_existing_growth_workflow": has_existing_growth,
        "safe_default_mode": "report-only",
        "signals": hits,
        "notes": [
            "Heuristic output only; confirm against project docs, deploy scripts, and live URLs.",
            "If source of truth is unknown, stay report-only or advisory.",
            "If existing growth automation is present, use it as input before creating a new queue.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
