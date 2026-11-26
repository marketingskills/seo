---
name: seo-change-monitor
description: Catch silent SEO regressions before or after a deploy by snapshotting key URLs (HTTP status, redirects, canonical, noindex, title, H1, JSON-LD types, and live robots.txt) and diffing against a saved baseline. Exits non-zero on critical regressions so it works in CI/CD. Use before redesigns, migrations, framework upgrades, or any production release.
---

# SEO Change Monitor

Most sudden traffic drops after a release come from one boring line: a stray `noindex`, a staging canonical, a broken redirect turning 200 into 404, or a `robots.txt` block. Snapshot key pages before every deploy and diff immediately after.

## The 4 silent deploy killers (CI-blocking critical regressions)

1. An indexable page turns `noindex` (`<meta name="robots">` or `X-Robots-Tag`).
2. A `<link rel="canonical">` changes target or disappears.
3. An HTTP `200` page turns into `4xx`/`5xx` or an unexpected redirect.
4. Live `robots.txt` starts blocking `/` or live search bots (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Bingbot`, `Googlebot`).

## Run the deterministic snapshot & diff script

Resolve `scripts/seo_snapshot.py` relative to this skill directory.

### 1. Capture baseline before deploy (20 to 200 key URLs)

```bash
python3 scripts/seo_snapshot.py snapshot \
  --urls https://example.com/ https://example.com/pricing https://example.com/about \
  --out seo-baseline.json
```

Or pass a newline-separated file:

```bash
python3 scripts/seo_snapshot.py snapshot --urls-file key-urls.txt --out seo-baseline.json
```

### 2. Capture post-deploy snapshot and diff

```bash
python3 scripts/seo_snapshot.py snapshot --urls-file key-urls.txt --out seo-current.json
python3 scripts/seo_snapshot.py diff seo-baseline.json seo-current.json
```

- Exits `0` when zero critical regressions exist (warnings such as title, H1, or dropped JSON-LD types are still reported for human review).
- Exits `2` on any critical regression so CI/CD or a post-deploy check stops immediately.
- Add `--format json` for automated pipelines.

## Workflow

1. Pick the top 20–200 revenue, landing, and top-traffic URLs (pull top pages from `live-search-console-data` via `GET /api/v1/sc/pages` if connected, or from the live sitemap).
2. Save `seo-baseline.json` before shipping changes.
3. Run `snapshot` + `diff` right after deploy (or against a preview environment).
4. Block release or roll back immediately if any critical regression fires.
5. Once clean, promote `seo-current.json` to the new `seo-baseline.json` and log the release date so you can watch GSC impressions over the next 2–4 weeks.
