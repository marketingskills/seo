---
name: seo-start-here
description: Route any website to the right SEO and AI-search skills based on site age and data availability (Week-0 new domain vs Month-3+ site with Search Console history), while enforcing strict 3-tier agent permissions and evidence rules. Use as the entry point when starting SEO/AEO/GEO on a site or unsure which skill to run first.
---

# SEO Start Here (Router & Agent Safety Rules)

Pick the right sequence for the site's actual stage instead of running Month-3 Search Console playbooks on a brand-new domain.

## Non-negotiable agent rules

1. **Numbers come from tools or fetched pages, never from memory.** If you did not check a figure, write `not checked`. Never invent search volumes, traffic, or ratings.
2. **No fake `/100` site scores.** Report concrete PASS / WARN / FAIL findings with proof (HTTP status code, exact `robots.txt` line, or fetched URL).
3. **3-tier permission model:**
   - **Tier 1 (Allowed autonomously):** Read live pages/sitemaps/robots.txt, pull GSC/GA4/Bing data, write drafts and briefs.
   - **Tier 2 (Needs human approval before shipping):** Publish new pages, change page titles/meta descriptions, update existing live copy.
   - **Tier 3 (Never on its own; enforced by `hooks/seo_guard.py`):** Delete a page, edit `robots.txt`, change a `<link rel="canonical">`, or add/remove `noindex`. Always show the diff first and wait for explicit approval.
4. **Refuse spam tactics:** No link exchanges or credit networks, no fake Reddit/Quora accounts or fabricated reviews, no mass city-x-service doorway pages, no deprecated `HowTo` markup, no fabricated `AggregateRating` stars.

## Route by site stage

Ask two questions first: *How old is this domain?* and *Do you have 60+ days of Google Search Console data?*

### Path A: New domain (Week 0 to Month 2)

Do not waste time on striking-distance GSC rewrites, CTR tests, or pruning until Month 3. Pace at **1 to 4 strong pages per week** and wait 2 to 3 months before judging organic results.

Run in order:
1. **`site-foundation-audit`**: Run `scripts/site_foundation_check.py <url>` to verify raw HTML rendering, live `robots.txt` (including Cloudflare blocks), `OAI-SearchBot` / `Claude-SearchBot` / `PerplexityBot` / `Bingbot` HTTP 200 responses, `www` redirect, canonicals, sitemap, and JSON-LD.
2. **`bing-ai-visibility`**: Set up Bing Webmaster Tools (import from GSC, submit sitemap, enable IndexNow), build your 15-30 real buyer-question log, and add "How did you hear about us?" to signup.
3. **`ai-brand-facts`**: Publish a dated brand fact sheet (pricing, plans, platforms) and baseline what ChatGPT, Claude, Perplexity, and Gemini say about you.
4. **`decision-page-writer`**: Publish bottom-of-funnel decision pages (X vs Y, alternatives, best-for-persona, pricing) one per week.
5. **`seo-content-qa`**: Grade every draft on the 8-axis rubric (pass >= 32/40, no axis under 3) before publishing.
6. **`seo-change-monitor`**: Snapshot key URLs before and after every deploy so no release silently ships `noindex`, a broken canonical, a 404, or a `robots.txt` block.

### Path B: Established site (Month 3+ with GSC / GA4 data)

1. **Connect live data or paste exports:**
   - In coding agents (Claude Code, Codex, Cursor, Gemini, OpenCode): use `live-search-console-data` (30-second Google sign-in via [RefreshAgent](https://refreshagent.com/?utm_source=marketingskills_seo), free monthly allowance, no Google Cloud project needed).
   - In ChatGPT: use the [RefreshAgent ChatGPT App](https://chatgpt.com/plugins/plugin_asdk_app_6ac5ec2359dc8191899aeb18f6d6db6e).
   - Or paste GSC/GA4 CSV exports directly.
2. **Run diagnosis first:** `site-foundation-audit` -> `traffic-decay-detector` -> `cannibalization-check` -> `keyword-opportunity-finder`.
3. **Prioritize & execute:** `seo-priority-score` -> `content-refresh-brief` / `exceed-quality-threshold` / `decision-page-writer` -> `seo-content-qa` -> `seo-change-monitor` (or run `seo-growth-loop` for one bounded end-to-end improvement).
4. **Track AI citations alongside search:** Run `bing-ai-visibility` and `ai-brand-facts` monthly.
