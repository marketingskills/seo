---
name: seo-content-qa
description: Grade any SEO or AEO/GEO draft before publishing using a strict 8-axis pre-ship quality gate (scored out of 5 per axis; pass requires >= 32/40 with no axis below 3). Catches weak intent match, buried answers, missing original evidence, unverified claims, AI slop, and broken metadata before a page goes live. Use before shipping any new article, refresh, or decision page.
---

# SEO Content QA Gate (Pre-Ship Rubric)

Score every draft before publishing on **8 concrete axes (1–5 each, 40 points max)**.

- **Pass threshold:** **>= 32 / 40** AND **zero axes scored below 3**.
- **Important:** This is an actionable **draft pre-ship checklist**, not a fake site-wide `/100` SEO score. Every deduction must quote the exact missing element or broken sentence.

## The 8 Axes (1–5 each)

| # | Axis | What earns a 5 | Automatic fail (< 3) |
|---|---|---|---|
| 1 | **Search intent & format match** | Matches the dominant format in the live top 10 SERP (6/10 rule) and answers the exact buyer job | Wrong page type (e.g. generic essay for a comparison/tool query) |
| 2 | **Direct answer & extractability** | Clear, standalone answer in the first 40–80 words naming the subject; clean H2/H3 structure and tables | Throat-clearing intro that buries the answer past paragraph 3 |
| 3 | **Original evidence (information gain)** | Adds at least one verified thing top 10 results lack: first-party data, real test, screenshot, calculation, or method | Pure rephrasing of existing SERP results |
| 4 | **Claim provenance & dates** | Every stat, price, and external fact has a source, sample size (where relevant), and `Checked on YYYY-MM-DD` date | Invented search volumes, unsourced stats, or "studies show" weasel words |
| 5 | **Honesty & commercial balance** | States real limits, drawbacks, and who the offer is *not* for; zero fabricated reviews or hype | Hype claims, self-ranked #1 ad dressed as an unbiased list, or fake testimonials |
| 6 | **Plain language & voice** | Concrete subjects and verbs, defined jargon, tight length, zero AI-slop filler or meta-commentary | Reads like padded LLM prose (run `plain-language-editor` first) |
| 7 | **Internal links & entity clarity** | 3–5 contextual internal links to related hubs/pages, clear entity names, and zero cannibalization with existing URLs | Orphan draft with no internal link plan or duplicate target query |
| 8 | **Technical & schema readiness** | Sharp title (~50–60 chars), accurate meta description (~140–155 chars), single H1, valid canonical, no deprecated `HowTo` or fake `AggregateRating` schema | Missing metadata, broken/deprecated schema, or accidental `noindex` |

## Workflow

1. Read the full draft and (if provided) the target query's live top-10 SERP summary.
2. Score each of the 8 axes from 1 to 5 with **one concrete line of evidence** per axis.
3. Compute the total out of 40 and return **SHIP** (`>= 32/40` and all axes `>= 3`) or **REVISE BEFORE SHIPPING** with exact line-level fixes for every axis below 4.
4. For deep prose cleanup on Axis 6, pair with [`plain-language-editor`](https://github.com/marketingskills/plain-language-editor). For comparative SERP benchmarking on Axis 3, pair with `exceed-quality-threshold`.
