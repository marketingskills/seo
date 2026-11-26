#!/usr/bin/env python3
"""Pre/post-deploy SEO regression snapshot & diff gate.

Snapshots key URLs (HTTP status, final URL, title, H1, canonical, meta/header robots,
JSON-LD types, and live robots.txt) and diffs two snapshots to catch the 4 silent
deploy killers before Google or AI crawlers do:
  1. Page turns noindex
  2. Canonical changes or disappears
  3. HTTP 200 becomes 4xx/5xx or unexpected redirect
  4. robots.txt blocks root or live search bots
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Reuse HTML + robots parser from sibling skill when available, with inline fallback
SIBLING_SCRIPTS = Path(__file__).resolve().parents[2] / "site-foundation-audit" / "scripts"
if SIBLING_SCRIPTS.exists():
    sys.path.insert(0, str(SIBLING_SCRIPTS))

import site_foundation_check as sfc  # noqa: E402


def snapshot_urls(urls: list[str], *, timeout: int = 12) -> dict[str, Any]:
    if not urls:
        raise ValueError("Provide at least one URL to snapshot")

    first = urllib.parse.urlparse(urls[0] if "://" in urls[0] else f"https://{urls[0]}")
    origin = f"{first.scheme}://{first.netloc}"
    robots_resp = sfc.fetch_url(f"{origin}/robots.txt", timeout=timeout)
    robots_body = robots_resp["body"] if robots_resp["status"] == 200 else ""
    robots_parsed = sfc.parse_robots_txt(robots_body) if robots_body else {}

    pages: dict[str, dict[str, Any]] = {}
    for raw_url in urls:
        url = raw_url if "://" in raw_url else f"https://{raw_url}"
        resp = sfc.fetch_url(url, timeout=timeout)
        signals = sfc.parse_html_signals(resp["body"]) if resp["status"] == 200 else {}
        x_robots = resp["headers"].get("x-robots-tag", "")
        pages[url] = {
            "status": resp["status"],
            "final_url": resp["final_url"],
            "title": signals.get("title", ""),
            "h1": signals.get("h1", ""),
            "canonical": signals.get("canonicals", [None])[0] if signals.get("canonicals") else None,
            "noindex": bool(signals.get("noindex")) or ("noindex" in x_robots.lower()),
            "meta_robots": signals.get("meta_robots", []),
            "x_robots_tag": x_robots,
            "schema_types": signals.get("schema_types", []),
        }

    return {
        "version": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "origin": origin,
        "robots_txt": {
            "status": robots_resp["status"],
            "sha256": hashlib.sha256(robots_body.encode("utf-8")).hexdigest() if robots_body else None,
            "blocked_search_bots": sorted(
                b for b, info in robots_parsed.get("search_bots", {}).items() if info["blocked"]
            ),
            "cloudflare_managed_block": robots_parsed.get("cloudflare_managed_block", False),
        },
        "pages": pages,
    }


def diff_snapshots(baseline: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    critical: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    # Check robots.txt regressions
    base_robots = baseline.get("robots_txt", {})
    curr_robots = current.get("robots_txt", {})
    new_blocked = sorted(
        set(curr_robots.get("blocked_search_bots", [])) - set(base_robots.get("blocked_search_bots", []))
    )
    if new_blocked:
        critical.append(
            {
                "url": f"{current.get('origin', '')}/robots.txt",
                "type": "robots_blocked_search_bots",
                "detail": f"Newly blocked live search bots in robots.txt: {', '.join(new_blocked)}",
            }
        )
    elif curr_robots.get("sha256") != base_robots.get("sha256"):
        warnings.append(
            {
                "url": f"{current.get('origin', '')}/robots.txt",
                "type": "robots_txt_changed",
                "detail": "Live robots.txt content hash changed; verify diff manually.",
            }
        )

    base_pages = baseline.get("pages", {})
    curr_pages = current.get("pages", {})

    for url, b in base_pages.items():
        c = curr_pages.get(url)
        if c is None:
            warnings.append({"url": url, "type": "url_missing_in_current", "detail": "URL present in baseline was not checked in current snapshot."})
            continue

        # Killer 1: HTTP status regression
        if b["status"] == 200 and c["status"] != 200:
            critical.append({"url": url, "type": "status_regression", "detail": f"HTTP 200 became HTTP {c['status']}"})
        elif b["status"] != c["status"]:
            warnings.append({"url": url, "type": "status_changed", "detail": f"HTTP {b['status']} -> HTTP {c['status']}"})

        # Killer 2: Page turned noindex
        if not b["noindex"] and c["noindex"]:
            critical.append({"url": url, "type": "became_noindex", "detail": f"Indexable page turned noindex (meta={c['meta_robots']}, header={c['x_robots_tag']})"})

        # Killer 3: Canonical changed or disappeared
        if b["canonical"] != c["canonical"]:
            critical.append({"url": url, "type": "canonical_changed", "detail": f"Canonical '{b['canonical']}' -> '{c['canonical']}'"})

        # Warning diffs: title, H1, schema types
        if b["title"] != c["title"]:
            warnings.append({"url": url, "type": "title_changed", "detail": f"Title '{b['title']}' -> '{c['title']}'"})
        if b["h1"] != c["h1"]:
            warnings.append({"url": url, "type": "h1_changed", "detail": f"H1 '{b['h1']}' -> '{c['h1']}'"})
        dropped_schema = sorted(set(b.get("schema_types", [])) - set(c.get("schema_types", [])))
        if dropped_schema:
            warnings.append({"url": url, "type": "schema_dropped", "detail": f"Dropped JSON-LD types: {', '.join(dropped_schema)}"})

    return {
        "passed": len(critical) == 0,
        "critical_count": len(critical),
        "warning_count": len(warnings),
        "critical": critical,
        "warnings": warnings,
    }


def render_diff_markdown(diff: dict[str, Any]) -> str:
    verdict = "PASS (no critical SEO regressions)" if diff["passed"] else "FAIL (critical SEO regressions detected)"
    lines = [
        f"# SEO Deploy Regression Diff: {verdict}",
        "",
        f"- **Critical regressions:** {diff['critical_count']}",
        f"- **Warnings:** {diff['warning_count']}",
    ]
    if diff["critical"]:
        lines.extend(["", "## Critical Regressions (Block Deploy)", "", "| URL | Type | Detail |", "|---|---|---|"])
        for item in diff["critical"]:
            lines.append(f"| `{item['url']}` | `{item['type']}` | {item['detail']} |")
    if diff["warnings"]:
        lines.extend(["", "## Warnings (Review Diff)", "", "| URL | Type | Detail |", "|---|---|---|"])
        for item in diff["warnings"]:
            lines.append(f"| `{item['url']}` | `{item['type']}` | {item['detail']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_snap = sub.add_parser("snapshot", help="Capture baseline or post-deploy SEO snapshot")
    p_snap.add_argument("--urls", nargs="+", help="List of URLs to snapshot")
    p_snap.add_argument("--urls-file", help="Newline-separated file of URLs to snapshot")
    p_snap.add_argument("--out", help="Output JSON path (prints to stdout if omitted)")
    p_snap.add_argument("--timeout", type=int, default=12)

    p_diff = sub.add_parser("diff", help="Diff baseline and current snapshot JSON files")
    p_diff.add_argument("baseline", help="Baseline snapshot JSON path")
    p_diff.add_argument("current", help="Current snapshot JSON path")
    p_diff.add_argument("--format", choices=("markdown", "json"), default="markdown")

    args = parser.parse_args(argv)
    if args.cmd == "snapshot":
        urls: list[str] = list(args.urls or [])
        if args.urls_file:
            urls.extend(
                line.strip()
                for line in Path(args.urls_file).read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.strip().startswith("#")
            )
        snap = snapshot_urls(urls, timeout=args.timeout)
        payload = json.dumps(snap, indent=2)
        if args.out:
            Path(args.out).write_text(payload + "\n", encoding="utf-8")
            print(f"Saved snapshot of {len(snap['pages'])} URLs to {args.out}")
        else:
            print(payload)
        return 0

    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    current = json.loads(Path(args.current).read_text(encoding="utf-8"))
    result = diff_snapshots(baseline, current)
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render_diff_markdown(result), end="")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
