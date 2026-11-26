---
name: decision-page-writer
description: Research and write high-converting bottom-of-funnel SEO and AI-search decision pages (X vs Y, X alternatives, best X for a specific persona, X pricing) using strict SERP format checks, keyword merge rules, 40-80 word opening answers, dated vendor-verified pricing, honest drawbacks, and original evidence. Use when building commercial pages designed to rank, convert, and get cited by AI answer engines.
---

# Decision Page Writer

Build the pages buyers read right before choosing: **X vs Y**, **X alternatives**, **best X for [one specific persona]**, and **X pricing**. These pages convert directly and get lifted by AI search engines.

## Hard rules (do not break)

1. **SERP format check (6/10 rule):** Inspect the live top 10 organic results for the query first. If 6 or more of the top 10 are the same page type, build that page type. If all 10 are editorial blog posts and you sell a product that cannot credibly win that format, skip the query.
2. **Keyword merge check (4/10 rule):** Two queries belong on the **same page** when they share 4 or more URLs in their top 10 results. Do not create separate cannibalizing pages.
3. **Direct opening answer (40–80 words):** Answer the buyer's exact decision in the first 40 to 80 words and name the product clearly. AI engines lift passages, not whole pages.
4. **List size discipline:** A "best of" or "alternatives" page lists **5 to 8 real options**. Three reads like an advert; 25 reads like a thin directory.
5. **Dated, vendor-verified pricing:** Every price must be checked on the vendor's own live pricing page and marked `Checked on YYYY-MM-DD`. Never quote prices from memory.
6. **Honest drawbacks for every option:** State at least one concrete drawback for every tool listed, **including your own product**.
7. **Do not rank yourself #1 on your own list** unless you state an explicit, transparent criterion (and even then, placing a strong category leader first or grouping by best-fit use case builds far more trust and citations).
8. **Mandatory unique evidence (information gain):** Add at least one thing none of the top 10 results have—your own benchmark, side-by-side test, real screenshot, workflow walkthrough, or measured dataset—and state the exact method.
9. **Check mobile video SERPs:** If searching the "best X" query on mobile shows a video carousel, plan a companion long-form video with chapters from `00:00` and hand-corrected captions.

## Workflow

1. **Validate the query on live SERPs:** Record the top 10 URLs, dominant page type (check 6/10 rule), and overlap with adjacent queries (check 4/10 rule).
2. **Inspect AI query fan-out:** Note the 5–10 sub-questions a buyer (or ChatGPT/Claude searching step) asks when evaluating this choice (pricing, limits, integrations, migration effort, hidden drawbacks, best-fit team size).
3. **Gather verified facts first:** Fetch every listed competitor's pricing/features page live and record the check date. Ask the user for their own real test, screenshot, or benchmark data rather than inventing one.
4. **Draft the page structure:**
   - **Direct answer block (40–80 words)** answering who should pick what.
   - **Quick comparison table** (Option, Best for, Pricing checked on YYYY-MM-DD, Key drawback).
   - **Original test / method block** showing what you actually measured or ran.
   - **Per-option breakdown (5–8 options)** with concrete strengths, one honest drawback, and fit criteria.
   - **Clear decision summary** ("Choose A if..., Choose B if...").
5. **Gate before shipping:** Run `seo-content-qa` (must score >= 32/40 with no axis below 3) before publishing.
