# Diagnose Workflow

Find what matters: technical issues, traffic decay, keyword gaps, cannibalization, authority ceilings, and competitor moves.

## Order of Operations

1. **Traffic decay detector** — find pages losing clicks, impressions, CTR.
2. **Technical SEO triage** — surface crawl, indexation, canonical, schema issues.
3. **Keyword opportunity finder** — find high-impression low-CTR terms and striking-distance keywords.
4. **Cannibalization check** — find query/page overlap.
5. **SERP authority mark** — check if you can realistically compete.
6. **Competitor SERP monitor** — track competitor new pages and ranking shifts.

## Data Sources

| Source | How to provide |
|---|---|
| GSC export | Paste query + page CSV or JSON from Search Console |
| GA4 export | Paste landing page + session data |
| Crawl output | Paste Screaming Frog, Sitebulb, or custom crawl JSON/CSV |
| Sitemap URLs | Paste XML sitemap URL or content |
| Live GSC/GA4 | Install `refreshagent/live-search-console-data` skill and authenticate |

## Output

A ranked list of diagnosed issues, each with:
- Metric change (clicks, impressions, CTR, ranking)
- Query-level breakdown
- Confidence level
- Recommended next step
