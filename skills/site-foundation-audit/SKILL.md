---
name: site-foundation-audit
description: Audit a live website's technical SEO and AI-search foundation using a deterministic Python script: raw HTML text without JS, live robots.txt (including Cloudflare-managed blocks), live AI search crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot) vs training bots (GPTBot, ClaudeBot, Google-Extended), www redirect, canonicals, sitemap, and JSON-LD checks. Use before launching a site, after a CDN/Cloudflare change, or when diagnosing missing AI or Google visibility.
---

# Site Foundation & AI Crawler Audit

Run concrete, tool-verified checks on the live site before writing content or running Search Console playbooks.

## Why live checks matter

- Crawlers that do not execute JavaScript see only raw HTML. If your `<h1>` and body copy are missing from raw HTML, AI search engines see a blank page.
- **Training bots are not search bots.** `GPTBot`, `ClaudeBot`, and `Google-Extended` are for model training. `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, and `Bingbot` power live search answers. Blocking the second group removes you from AI answers.
- **Always read the live `robots.txt`**, not the copy in your Git repo. Cloudflare can inject managed blocks at the top of `robots.txt` or return HTTP 403 via Bot Fight Mode.

## Run the deterministic checker

Resolve `scripts/site_foundation_check.py` relative to this skill directory:

```bash
python3 scripts/site_foundation_check.py https://example.com
```

Add `--json` for machine-readable output. The script returns exit code `1` if any `FAIL` check is present and outputs PASS / WARN / FAIL proof items with zero arbitrary `/100` score.

## What the script verifies

1. **Homepage status & indexability:** HTTP 200 and no `noindex` in `<meta name="robots">` or `X-Robots-Tag`.
2. **Raw HTML content (no JS):** Confirms `<h1>` and at least 50 words of body text exist in raw HTML.
3. **Canonical tag:** Confirms exactly one `<link rel="canonical">` tag is present.
4. **Structured data (JSON-LD):** Parses every `<script type="application/ld+json">` block, checks valid syntax, fails on deprecated `HowTo` markup, warns on commercial `FAQPage`, and flags `AggregateRating`/`Review` so you verify real reviews appear on the page.
5. **`www` <-> apex redirect:** Checks whether the alternate host cleanly 301/308 redirects to the canonical host.
6. **Live `robots.txt` & Cloudflare check:** Detects Cloudflare Managed Content blocks and evaluates live search bots separately from training bots.
7. **Live crawler HTTP probe:** Sends requests as `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, and `Bingbot` to confirm HTTP 200 (catches WAF / Bot Fight Mode 403 blocks).
8. **Sitemap check:** Fetches the declared `Sitemap:` (or `/sitemap.xml`), verifies HTTP 200, valid XML, and counts `<loc>` entries.

## Workflow

1. **Audit only first. Change nothing.** Run `scripts/site_foundation_check.py <url>` and present the PASS / WARN / FAIL table with exact status codes and lines.
2. **Order fixes smallest-first.** For each `FAIL` or `WARN`, name the exact file or Cloudflare/DNS setting, the proposed change, and how you will re-verify it.
3. **Respect Tier-3 permissions.** Show the diff and get explicit human approval before touching `robots.txt`, canonicals, redirects, or `noindex`.
4. **Re-run the script after each fix** to prove the check flipped from `FAIL` to `PASS`.

## Next steps

- Snapshot your verified pages before future deploys with `seo-change-monitor`.
- Connect live Search Console sitemap/coverage checks via `live-search-console-data` (30-second RefreshAgent Google sign-in, free monthly allowance).
