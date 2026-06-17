# Example Run: Content Decay Detection & Refresh Briefs

**Data window:** Last 90 days vs previous 90 days  
**GSC property:** demo-site.com (anonymized)  
**Pages considered:** 47 pages with organic clicks > 0  
**Queries considered:** 312 queries with impressions > 0  
**Analysis date:** 2026-06-16

## What Happened

The agent analyzed 90 days of GSC data, compared it to the prior 90 days, and identified 7 pages responsible for 62% of the total organic click decline.

## Drop & Reason

| Page | Click Change | Query Impact | Primary Cause |
|---|---|---|---|
| /guides/seo-checklist | -1,240 clicks (-41%) | "seo checklist" dropped from pos 3 to pos 8 | SERP drift — new competitor guide |
| /blog/schema-markup | -890 clicks (-34%) | "schema markup guide" CTR fell 60% | Featured snippet lost |
| /tools/keyword-planner | -720 clicks (-28%) | "free keyword planner" impressions halved | Query seasonality + new entrant |
| /blog/core-web-vitals | -610 clicks (-22%) | "core web vitals" CTR down 35% | Old publish date, competitors updated |
| /guides/technical-seo | -580 clicks (-19%) | "technical seo audit" pos 5 to pos 9 | Content depth gap |
| /blog/link-building | -420 clicks (-15%) | "link building 2025" pos 4 to pos 7 | Outdated examples |
| /tools/serp-checker | -310 clicks (-12%) | "serp checker" declining impressions | Tool page without updates |

## Priority Scoring

| Page | Impact | Confidence | Effort | Authority Feasibility | Priority |
|---|---|---|---|---|---|
| /guides/seo-checklist | high | high | medium | achievable | 1 |
| /blog/schema-markup | high | medium | low | achievable | 2 |
| /blog/core-web-vitals | medium | high | low | achievable | 3 |
| /tools/keyword-planner | medium | medium | high | needs research | 4 |

## Drops & Reasons

The remaining 3 pages were deprioritized because:
- `/blog/link-building` — effort high, seasonal boost unlikely, better to merge into the main link-building hub.
- `/tools/serp-checker` — tool pages require product updates, outside content refresh scope.
- `/guides/technical-seo` — better handled as a full rewrite under the technical SEO cluster, not a refresh.

## Recommended Actions

1. Refresh `/guides/seo-checklist` — update content, improve SERP intent match, add recent data.
2. Refresh `/blog/schema-markup` — target the featured snippet, update examples and schema types.
3. Refresh `/blog/core-web-vitals` — add 2026 data, link to new tools/sources, improve freshness signal.

## What Needs a Human Decision

- Whether to expand `/guides/seo-checklist` into a full hub page or keep it as a single guide.
- Whether `/tools/keyword-planner` needs a product investment or should be redirected.
- Budget for the full /guides/technical-seo rewrite (out of scope for quick wins).

## Artifacts

Machine-readable outputs from this run:

```
candidates.json
gsc_query_rollup.json
page_decay_findings.json
serp_authority_checks.json
priority_scores.json
refresh_briefs/
  seo-checklist-refresh-brief.md
  schema-markup-refresh-brief.md
  core-web-vitals-refresh-brief.md
final_report.md
```
