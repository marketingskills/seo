---
name: ai-brand-facts
description: Audit what ChatGPT, Claude, Perplexity, Gemini, and Copilot say about your brand, trace wrong or outdated facts (pricing, plans, platforms, positioning, namesake confusion) back to the web pages causing them, produce a dated public brand fact sheet, and track verified fixes over two consecutive months. Use when AI engines get your pricing/features wrong, after a rebrand or pricing change, or when setting up an AEO/GEO entity baseline.
---

# AI Brand Facts & Hallucination Audit

AI engines rarely invent your old pricing out of thin air. They read stale pages, old directories, outdated pricing tables, or a namesake company you left lying around on the web. Tidy the source pages, publish a clear dated fact sheet, and re-test monthly.

## Workflow

### 1. Lock the canonical ground truth (Dated Brand Fact Sheet)
Gather verified, current facts from the user (never guess):
- Exact brand name, domain, category, and one-sentence description
- Current pricing, tiers, free trial / free tier status (`Verified YYYY-MM-DD`)
- Supported platforms, integrations, and deployment model (e.g. self-hosted vs hosted)
- Who it is built for and who it is *not* for
- Founder / company entity, headquarters, and canonical social/GitHub profiles
- Disambiguation note if a namesake company or product exists

Draft a clean, crawlable **`/facts` or `/about` dated fact sheet** formatted in plain subject-verb-object statements and tables so answer engines can extract exact claims cleanly.

### 2. Run the multi-engine brand audit
Test 8–12 brand-level queries logged out across **ChatGPT, Claude, Perplexity, and Gemini** (run each query at least twice, because source sets shift week to week):
- `"What is [Brand]?"`
- `"[Brand] pricing"`
- `"Does [Brand] have a free plan?"`
- `"[Brand] vs [Top Competitor]"`
- `"Who is [Brand] best for?"`
- `"[Brand] reviews and limitations"`

### 3. Classify every claim and trace its source
Log every surfaced claim in a structured claim ledger:

| Engine | Query | Claim returned | Verdict (`Correct` / `Outdated` / `Wrong` / `Missing` / `Namesake confusion`) | Cited or likely source URL | Fix owner & action |
|---|---|---|---|---|---|

### 4. Fix at the source (in priority order)
1. **Your own site:** Update stale blog posts, pricing pages, docs, FAQ snippets, and `Organization` / `SoftwareApplication` JSON-LD `sameAs` links. Publish the dated fact sheet.
2. **Controlled third-party profiles (20–30 key listings):** Sync identical brand name, one-line description, pricing summary, and logo across GitHub, LinkedIn, G2/Capterra, Product Hunt, YouTube, and key software directories.
3. **Uncontrolled third-party articles:** Send a short, factual 120–180 word correction note with a link to your dated fact sheet (one follow-up after 7 days, then stop).

### 5. Two-month confirmation rule
Because LLM search results fluctuate week to week, never mark a wrong claim "fixed" after a single clean check. Re-run the exact prompt log monthly and mark a claim **Resolved** only after it disappears for **two consecutive months**.
