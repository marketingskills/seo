# Authority Mark Keyword Difficulty

Codex skill for evaluating SEO keyword difficulty with a live SERP authority watermark instead of an opaque keyword difficulty score.

The skill searches the current SERP, collects Ahrefs DR for the top organic ranking domains and the user's domain, then identifies the first top-10 result whose DR is lower than the user's site.

## Install

```bash
npx skills add refreshagent/authority-mark-keyword-difficulty
```

## Companion Skill

For easier live Google Search Console and GA4 access through RefreshAgent, install:

```bash
npx skills add refreshagent/live-search-console-data
```

Use this skill for SERP authority analysis. Use `refreshagent/live-search-console-data` when answers should include real GSC queries, pages, rankings, clicks, impressions, CTR, GA4 sessions, or conversion data.
