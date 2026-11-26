#!/usr/bin/env python3
"""Zero-dependency technical SEO & AI-search foundation checker.

Checks raw HTML (no JS), live robots.txt (including Cloudflare-managed blocks),
live AI search crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot)
vs. training bots (GPTBot, ClaudeBot, Google-Extended), www redirect, canonicals,
sitemap availability, and JSON-LD (flagging deprecated HowTo or unverified ratings).

Outputs concrete PASS / WARN / FAIL checks with evidence, never an arbitrary /100 score.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any


SEARCH_BOTS = ("OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Bingbot", "Googlebot")
TRAINING_BOTS = ("GPTBot", "ClaudeBot", "Google-Extended")
DEFAULT_UA = "Mozilla/5.0 (compatible; MarketingSkillsSEOAudit/1.0; +https://marketingskills.net)"


class PageSignalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.in_h1 = False
        self.in_jsonld = False
        self.skip_depth = 0
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.text_parts: list[str] = []
        self.canonicals: list[str] = []
        self.meta_robots: list[str] = []
        self.jsonld_blocks: list[str] = []
        self._jsonld_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if t in ("script", "style", "noscript"):
            self.skip_depth += 1
            if t == "script" and "ld+json" in attr_map.get("type", "").lower():
                self.in_jsonld = True
                self._jsonld_buf = []
        elif t == "title":
            self.in_title = True
        elif t == "h1":
            self.in_h1 = True
        elif t == "link":
            rels = {r.strip().lower() for r in attr_map.get("rel", "").split()}
            if "canonical" in rels and attr_map.get("href"):
                self.canonicals.append(attr_map["href"].strip())
        elif t == "meta":
            name = attr_map.get("name", "").strip().lower()
            if name in ("robots", "googlebot", "bingbot") and attr_map.get("content"):
                self.meta_robots.append(f"{name}={attr_map['content'].strip()}")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t in ("script", "style", "noscript"):
            if self.in_jsonld and t == "script":
                self.jsonld_blocks.append("".join(self._jsonld_buf).strip())
                self.in_jsonld = False
                self._jsonld_buf = []
            if self.skip_depth > 0:
                self.skip_depth -= 1
        elif t == "title":
            self.in_title = False
        elif t == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h1:
            self.h1_parts.append(data)
        if self.skip_depth == 0:
            cleaned = " ".join(data.split())
            if cleaned:
                self.text_parts.append(cleaned)


def parse_html_signals(html: str) -> dict[str, Any]:
    parser = PageSignalParser()
    parser.feed(html)
    title = " ".join("".join(parser.title_parts).split())
    h1 = " ".join("".join(parser.h1_parts).split())
    body_text = " ".join(parser.text_parts)
    word_count = len(re.findall(r"[A-Za-z0-9']+", body_text))

    schema_types: list[str] = []
    schema_errors: list[str] = []
    for raw in parser.jsonld_blocks:
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            schema_errors.append(f"invalid JSON-LD: {exc.msg}")
            continue
        _collect_types(obj, schema_types)

    noindex = any("noindex" in entry.lower() for entry in parser.meta_robots)
    return {
        "title": title,
        "h1": h1,
        "raw_word_count": word_count,
        "canonicals": parser.canonicals,
        "meta_robots": parser.meta_robots,
        "noindex": noindex,
        "schema_types": sorted(set(schema_types)),
        "schema_errors": schema_errors,
    }


def _collect_types(node: Any, out: list[str]) -> None:
    if isinstance(node, list):
        for item in node:
            _collect_types(item, out)
    elif isinstance(node, dict):
        t = node.get("@type")
        if isinstance(t, str):
            out.append(t)
        elif isinstance(t, list):
            for entry in t:
                if isinstance(entry, str):
                    out.append(entry)
        for value in node.values():
            if isinstance(value, (dict, list)):
                _collect_types(value, out)


def parse_robots_txt(robots_text: str) -> dict[str, Any]:
    """Parse robots.txt rules for live AI search bots vs training bots + Cloudflare blocks."""
    groups: dict[str, list[tuple[str, str]]] = {}
    current_agents: list[str] = []
    sitemaps: list[str] = []
    cloudflare_managed = "cloudflare managed content" in robots_text.lower()

    for raw_line in robots_text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, value = line.split(":", 1)
        key = field.strip().lower()
        val = value.strip()
        if key == "user-agent":
            if current_agents and any(groups.get(a) for a in current_agents):
                current_agents = []
            agent = val.lower()
            current_agents.append(agent)
            groups.setdefault(agent, [])
        elif key in ("disallow", "allow"):
            for agent in current_agents:
                groups.setdefault(agent, []).append((key, val))
        elif key == "sitemap" and val:
            sitemaps.append(val)

    def bot_blocked_root(bot_name: str) -> tuple[bool, str]:
        specific = groups.get(bot_name.lower())
        rules = specific if specific is not None else groups.get("*", [])
        source = bot_name if specific is not None else "*"
        # Evaluate longest-match rule for root path "/"
        best_len = -1
        blocked = False
        matched_rule = "none (allowed by default)"
        for directive, path in rules:
            if path == "":
                continue
            if path == "/" or "/".startswith(path):
                if len(path) > best_len or (len(path) == best_len and directive == "allow"):
                    best_len = len(path)
                    blocked = directive == "disallow"
                    matched_rule = f"User-agent: {source} -> {directive.title()}: {path}"
        return blocked, matched_rule

    search_status = {}
    for bot in SEARCH_BOTS:
        blocked, rule = bot_blocked_root(bot)
        search_status[bot] = {"blocked": blocked, "rule": rule}

    training_status = {}
    for bot in TRAINING_BOTS:
        blocked, rule = bot_blocked_root(bot)
        training_status[bot] = {"blocked": blocked, "rule": rule}

    return {
        "cloudflare_managed_block": cloudflare_managed,
        "sitemaps": sitemaps,
        "search_bots": search_status,
        "training_bots": training_status,
    }


def audit_schema_types(schema_types: list[str], schema_errors: list[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if schema_errors:
        findings.append({"check": "jsonld_syntax", "status": "FAIL", "evidence": "; ".join(schema_errors)})
    if not schema_types:
        findings.append(
            {
                "check": "jsonld_presence",
                "status": "WARN",
                "evidence": "No JSON-LD structured data found (consider Organization, WebSite, Product/SoftwareApplication).",
            }
        )
    else:
        findings.append(
            {
                "check": "jsonld_presence",
                "status": "PASS",
                "evidence": f"Detected JSON-LD types: {', '.join(schema_types)}",
            }
        )
    if "HowTo" in schema_types:
        findings.append(
            {
                "check": "deprecated_howto",
                "status": "FAIL",
                "evidence": "Found deprecated HowTo schema (Google discontinued HowTo rich results in 2023).",
            }
        )
    if "FAQPage" in schema_types:
        findings.append(
            {
                "check": "faqpage_warning",
                "status": "WARN",
                "evidence": "Found FAQPage schema; Google restricts FAQ rich results mainly to gov/health sites.",
            }
        )
    if "AggregateRating" in schema_types or "Review" in schema_types:
        findings.append(
            {
                "check": "review_stars_verify",
                "status": "WARN",
                "evidence": "Found AggregateRating/Review schema; verify real, visible customer reviews exist on the page.",
            }
        )
    return findings


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


def fetch_url(url: str, *, user_agent: str = DEFAULT_UA, timeout: int = 12, follow_redirects: bool = True) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,text/plain,*/*"})
    opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirectHandler())
    try:
        with opener.open(req, timeout=timeout) as resp:
            body = resp.read(500_000).decode("utf-8", errors="replace")
            return {
                "status": resp.status,
                "final_url": resp.geturl(),
                "headers": {k.lower(): v for k, v in resp.headers.items()},
                "body": body,
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(100_000).decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "status": exc.code,
            "final_url": exc.headers.get("Location", url) if exc.headers else url,
            "headers": {k.lower(): v for k, v in (exc.headers.items() if exc.headers else [])},
            "body": body,
            "error": str(exc),
        }
    except Exception as exc:
        return {"status": 0, "final_url": url, "headers": {}, "body": "", "error": str(exc)}


def run_audit(url: str, *, timeout: int = 12) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url if "://" in url else f"https://{url}")
    origin = f"{parsed.scheme}://{parsed.netloc}"
    target_url = f"{origin}{parsed.path or '/'}"

    checks: list[dict[str, str]] = []

    # 1. Raw HTML fetch (no JavaScript)
    page = fetch_url(target_url, timeout=timeout)
    if page["status"] != 200:
        checks.append({"check": "homepage_status", "status": "FAIL", "evidence": f"HTTP {page['status']} ({page['error'] or 'non-200'})"})
        signals: dict[str, Any] = {}
    else:
        checks.append({"check": "homepage_status", "status": "PASS", "evidence": f"HTTP 200 at {page['final_url']}"})
        signals = parse_html_signals(page["body"])
        x_robots = page["headers"].get("x-robots-tag", "")
        if signals["noindex"] or "noindex" in x_robots.lower():
            checks.append({"check": "indexability", "status": "FAIL", "evidence": f"noindex detected (meta={signals['meta_robots']}, header={x_robots})"})
        else:
            checks.append({"check": "indexability", "status": "PASS", "evidence": "No noindex directive in meta robots or X-Robots-Tag"})

        if signals["h1"] and signals["raw_word_count"] >= 50:
            checks.append({"check": "raw_html_content", "status": "PASS", "evidence": f"H1='{signals['h1'][:70]}', {signals['raw_word_count']} words in raw HTML"})
        else:
            checks.append({"check": "raw_html_content", "status": "FAIL", "evidence": f"Weak/empty raw HTML (H1='{signals['h1']}', words={signals['raw_word_count']}); JS-only rendering hides content from AI crawlers"})

        if len(signals["canonicals"]) == 1:
            checks.append({"check": "canonical", "status": "PASS", "evidence": f"Canonical: {signals['canonicals'][0]}"})
        elif len(signals["canonicals"]) == 0:
            checks.append({"check": "canonical", "status": "FAIL", "evidence": "Missing <link rel='canonical'> tag"})
        else:
            checks.append({"check": "canonical", "status": "FAIL", "evidence": f"Multiple canonicals found: {signals['canonicals']}"})

        checks.extend(audit_schema_types(signals["schema_types"], signals["schema_errors"]))

    # 2. www <-> apex redirect check
    host = parsed.netloc
    alt_host = host[4:] if host.startswith("www.") else f"www.{host}"
    alt_url = f"{parsed.scheme}://{alt_host}/"
    alt_resp = fetch_url(alt_url, timeout=timeout, follow_redirects=False)
    if alt_resp["status"] in (301, 302, 307, 308):
        checks.append({"check": "www_redirect", "status": "PASS", "evidence": f"{alt_url} -> HTTP {alt_resp['status']} to {alt_resp['headers'].get('location', '')}"})
    elif alt_resp["status"] == 200:
        checks.append({"check": "www_redirect", "status": "WARN", "evidence": f"{alt_url} serves HTTP 200 directly instead of redirecting to canonical host"})
    else:
        checks.append({"check": "www_redirect", "status": "WARN", "evidence": f"{alt_url} returned HTTP {alt_resp['status']} ({alt_resp['error'] or 'no redirect'})"})

    # 3. Live robots.txt check
    robots_url = f"{origin}/robots.txt"
    robots_resp = fetch_url(robots_url, timeout=timeout)
    robots_parsed: dict[str, Any] = {}
    if robots_resp["status"] == 200:
        robots_parsed = parse_robots_txt(robots_resp["body"])
        if robots_parsed["cloudflare_managed_block"]:
            checks.append({"check": "cloudflare_robots_block", "status": "WARN", "evidence": "Live robots.txt contains a Cloudflare Managed Content block; verify search bots are not disallowed."})
        else:
            checks.append({"check": "cloudflare_robots_block", "status": "PASS", "evidence": "No Cloudflare-injected robots.txt block detected."})

        blocked_search = [b for b, info in robots_parsed["search_bots"].items() if info["blocked"]]
        if blocked_search:
            rules = "; ".join(f"{b} ({robots_parsed['search_bots'][b]['rule']})" for b in blocked_search)
            checks.append({"check": "robots_ai_search_bots", "status": "FAIL", "evidence": f"Live robots.txt blocks live search bots: {rules}"})
        else:
            checks.append({"check": "robots_ai_search_bots", "status": "PASS", "evidence": f"Live robots.txt allows all live search bots ({', '.join(SEARCH_BOTS)})"})

        blocked_train = [b for b, info in robots_parsed["training_bots"].items() if info["blocked"]]
        checks.append({
            "check": "robots_training_bots",
            "status": "PASS",
            "evidence": f"Training bots blocked: {', '.join(blocked_train) if blocked_train else 'none'} (separate from live search bots).",
        })
    else:
        checks.append({"check": "robots_txt", "status": "WARN", "evidence": f"{robots_url} returned HTTP {robots_resp['status']}"})

    # 4. Active live AI-search crawler probe (catches Cloudflare Bot Fight Mode 403s)
    bot_probes: dict[str, int] = {}
    failed_probes: list[str] = []
    for bot in ("OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Bingbot"):
        probe = fetch_url(target_url, user_agent=bot, timeout=timeout)
        bot_probes[bot] = probe["status"]
        if probe["status"] != 200:
            failed_probes.append(f"{bot}=HTTP {probe['status']}")
    if failed_probes:
        checks.append({"check": "live_crawler_http_probe", "status": "FAIL", "evidence": f"Non-200 response for live AI search crawlers: {', '.join(failed_probes)}"})
    else:
        checks.append({"check": "live_crawler_http_probe", "status": "PASS", "evidence": "All live AI search crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot) received HTTP 200"})

    # 5. Sitemap check
    sitemap_urls = robots_parsed.get("sitemaps") or [f"{origin}/sitemap.xml"]
    sm_url = sitemap_urls[0]
    sm_resp = fetch_url(sm_url, timeout=timeout)
    if sm_resp["status"] == 200 and ("<urlset" in sm_resp["body"] or "<sitemapindex" in sm_resp["body"]):
        loc_count = len(re.findall(r"<loc>", sm_resp["body"]))
        checks.append({"check": "sitemap", "status": "PASS", "evidence": f"{sm_url} returned HTTP 200 with {loc_count} <loc> entries"})
    else:
        checks.append({"check": "sitemap", "status": "FAIL", "evidence": f"{sm_url} returned HTTP {sm_resp['status']} or invalid XML"})

    return {
        "target_url": target_url,
        "summary": {
            "pass": sum(1 for c in checks if c["status"] == "PASS"),
            "warn": sum(1 for c in checks if c["status"] == "WARN"),
            "fail": sum(1 for c in checks if c["status"] == "FAIL"),
        },
        "bot_probes": bot_probes,
        "checks": checks,
    }


def render_markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        f"# Site Foundation & AI Crawler Audit: {report['target_url']}",
        "",
        f"**Results:** {s['pass']} PASS · {s['warn']} WARN · {s['fail']} FAIL *(findings only; no arbitrary /100 score)*",
        "",
        "| Check | Status | Proof |",
        "|---|---|---|",
    ]
    for item in report["checks"]:
        ev = item["evidence"].replace("|", "\\|")
        lines.append(f"| `{item['check']}` | **{item['status']}** | {ev} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Live site URL to audit (e.g. https://example.com)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    parser.add_argument("--timeout", type=int, default=12)
    args = parser.parse_args(argv)

    report = run_audit(args.url, timeout=args.timeout)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report), end="")
    return 1 if report["summary"]["fail"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
