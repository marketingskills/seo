# Content Decay Demo Run

**GSC property:** demo-site.com (anonymized)  
**Date range:** 2026-03-18 to 2026-06-16 (90 days)  
**Comparison:** 2025-12-18 to 2026-03-17 (prior 90 days)  
**Pages analyzed:** 47  
**Queries analyzed:** 312  
**Skills used:** traffic-decay-detector, serp-authority-mark, content-refresh-brief

## Pipeline

### 1. Data Collection

Connected to GSC via RefreshAgent live data bridge. Pulled:
- 90-day page + query performance (clicks, impressions, CTR, avg position)
- Same for comparison period

### 2. Candidate Identification

Filtered to pages with:
- Organic clicks > 0 in current period
- Click decline > 15% vs prior period
- Impression decline or CTR decline as secondary signal

**Candidates emitted:** 12 pages

### 3. Drops & Reasons

| Page | Clicks (curr) | Clicks (prev) | Change | Drops Reason |
|---|---|---|---|---|
| /guides/seo-checklist | 1,784 | 3,024 | -1,240 (-41%) | Passes all filters |
| /blog/schema-markup | 1,726 | 2,616 | -890 (-34%) | Passes all filters |
| /blog/core-web-vitals | 2,164 | 2,774 | -610 (-22%) | Passes all filters |
| /tools/keyword-planner | 1,851 | 2,571 | -720 (-28%) | Passes all filters |
| /blog/link-building | 2,380 | 2,800 | -420 (-15%) | Passes all filters |
| /guides/technical-seo | 2,477 | 3,057 | -580 (-19%) | Passes all filters |
| /tools/serp-checker | 2,276 | 2,586 | -310 (-12%) | Passes all filters |
| /blog/onpage-seo | 1,540 | 1,690 | -150 (-9%) | Below threshold, rejected |
| /blog/voice-search | 890 | 970 | -80 (-8%) | Below threshold, rejected |
| /guides/local-seo | 650 | 710 | -60 (-8%) | Below threshold, rejected |
| /blog/amp-guide | 340 | 310 | +30 (+10%) | No decline, rejected |
| /tools/keyword-generator | 2,100 | 2,010 | +90 (+4%) | No decline, rejected |

**Drops:** 5 candidates removed (3 below threshold, 2 no decline)

### 4. Authority Check

Ran serp-authority-mark on primary query for each remaining candidate:

| Page | Primary Query | User DR | Top-10 Min DR | Authority Mark |
|---|---|---|---|---|
| /guides/seo-checklist | "seo checklist" | 54 | 42 (pos 7) | Opening |
| /blog/schema-markup | "schema markup guide" | 54 | 48 (pos 5) | Opening |
| /blog/core-web-vitals | "core web vitals" | 54 | 38 (pos 9) | Opening |
| /tools/keyword-planner | "free keyword planner" | 54 | 65 (pos 3) | No opening |
| /blog/link-building | "link building 2025" | 54 | 51 (pos 6) | Marginal |
| /guides/technical-seo | "technical seo audit" | 54 | 44 (pos 8) | Opening |
| /tools/serp-checker | "serp checker" | 54 | 60 (pos 2) | No opening |

**Drops:** 2 candidates removed (keyword-planner, serp-checker — no authority opening)

### 5. Priority Scoring

| Page | Impact | Confidence | Effort | Priority |
|---|---|---|---|---|
| /guides/seo-checklist | high | high | medium | 1 |
| /blog/schema-markup | high | medium | low | 2 |
| /blog/core-web-vitals | medium | high | low | 3 |
| /blog/link-building | medium | medium | high | 4 |
| /guides/technical-seo | medium | medium | high | 5 |

**Drops:** 2 candidates deprioritized (link-building — effort high, marginal authority; technical-seo — better as full rewrite)

### 6. Brief Generation

Generated refresh briefs for top 3 priorities. See:
- `refresh_briefs/seo-checklist-refresh-brief.md`
- `refresh_briefs/schema-markup-refresh-brief.md`
- `refresh_briefs/core-web-vitals-refresh-brief.md`

## Final Report

See `final_report.md` for the client-ready version.

## Caveats

- DR values from Ahrefs public API — may lag by days or weeks.
- Authority Mark is a domain-level signal, not page-level.
- Content quality, topical authority, and page links can override domain DR.
- Seasonal effects not fully isolated — "core web vitals" may have search volume seasonality.
