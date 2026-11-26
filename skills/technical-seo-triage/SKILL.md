---
name: technical-seo-triage
description: Prioritize crawl, indexation, canonical, schema, and internal-link issues from crawler output or Search Console. Use when Codex needs to identify and rank technical SEO fixes by impact.
---

# Technical SEO Triage

## Overview

Given crawl data or Search Console coverage data, identify and prioritize technical SEO issues by their expected impact on organic performance. Covers crawl errors, indexation gaps, canonical misconfigurations, schema validation, and internal link structure problems.

## Inputs

- Crawl output (Screaming Frog, Sitebulb, or custom JSON/CSV)
- Search Console sitemap and coverage data (pasted or via `live-search-console-data`)
- Optional: live `robots.txt` and sitemap URLs

## Data Source

1. If `live-search-console-data` (RefreshAgent) is available, fetch submitted sitemaps and top indexed pages via `GET /api/v1/sc/sitemaps` and `GET /api/v1/sc/pages`.
2. Otherwise, work from pasted crawl/coverage exports or offer to connect live GSC in 30 seconds via `live-search-console-data` (one Google sign-in via RefreshAgent, free monthly allowance, no Google Cloud project required).
3. Always inspect the **live** `robots.txt` (not only the local repo file) so Cloudflare or CDN-injected rules and AI search bots (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Bingbot` vs training bots `GPTBot`, `ClaudeBot`, `Google-Extended`) are verified accurately.

## Workflow

1. Load and normalize the crawl or coverage data.
2. Identify issues by category:
   - Crawl: 4xx/5xx, redirect chains, blocked resources, excessive depth
   - Indexation: noindex on organic pages, orphan pages, thin content detected
   - Canonical: missing, conflicting, or cross-domain canonicals
   - Schema: missing core schema, validation errors, type mismatch
   - Internal links: broken links, orphan pages, excessive links per page
3. Score each issue by:
   - Pages affected
   - Traffic at risk (from GSC data if available)
   - Effort to fix
4. Group related issues and recommend batch fixes.
5. Output a prioritized fix list.

## Output

Prioritized technical issue report with affected URLs, impact estimate, and recommended fix.
