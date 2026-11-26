---
name: bing-ai-visibility
description: Set up and run a zero-cost AI search visibility workflow using Bing Webmaster Tools (GSC import, sitemap, IndexNow, Bing AI Performance citations), a 15-30 real buyer-question log tested logged-out across ChatGPT, Claude, Perplexity, and Gemini, and self-reported signup attribution. Use when measuring AEO/GEO visibility without paying for speculative visibility trackers.
---

# Bing & Free AI Visibility Measurement

Before paying for an AI visibility tracker, set up the free first-party stack and a disciplined buyer-question log.

## Part 1: Bing Webmaster Tools & IndexNow (10-minute setup)

Copilot runs on Bing, and ChatGPT relies heavily on Bing's index. Bing Webmaster Tools also provides an **AI Performance** report showing first-party AI citation counts and grounding queries—the closest free first-party citation data available.

1. Open **Bing Webmaster Tools** and import your verified property directly from Google Search Console.
2. Submit your canonical `sitemap.xml` (containing only indexable 200-status URLs).
3. Enable **IndexNow** (via Cloudflare Crawler Hints, plugin, or a post-deploy ping) so new and updated pages reach Bing within minutes.
4. Export Bing **AI Performance** monthly and track **both** total cited appearances and unique cited pages per day (rising citations across fewer pages means concentration, not broad coverage).

## Part 2: Free buyer-question tracking (15–30 real questions)

1. **Collect 15–30 real buyer questions** from sales calls, support inbox, customer reviews, and Search Console queries (never invent 30 generic prompts from imagination; mark any temporary guesses `[GUESSED - REPLACE]`).
2. **Inspect hidden search fan-out:** Open the "Searching..." step in ChatGPT or Claude on your top 5 buyer questions. Record the sub-queries the engine actually fires—each one maps to either a page you need on your site or a third-party list/platform you need to be included on.
3. **Test twice per engine, logged out:** Run each prompt at least twice across **ChatGPT, Claude, Perplexity, and Gemini** (single runs are noisy because answers swap sources weekly).
4. **Track two separate numbers:**
   - **Cited:** Your domain URL appears as a source citation.
   - **Recommended / Named:** Your brand is explicitly named in the answer (often via third-party "best of" lists, YouTube videos, or review sites—in large studies, most citations go to third-party pages, so track both your own URLs and third-party lists).

## Part 3: Low-volume reporting & real attribution

- **Under ~100 AI referral visits/month:** Report **raw counts**, never dramatic percentages (`+200%` from 1 to 3 visits is noise).
- **Add "How did you hear about us?" to signup / contact forms:** Referral analytics regularly misattribute dark-social and AI-assistant discovery to Google Search or Direct. Compare self-reported responses against GA4 referrals monthly.
- **Pair with live GA4/GSC data:** Use `live-search-console-data` (`GET /api/v1/ga4/summary`, `GET /api/v1/ga4/landing-pages`) via [RefreshAgent](https://refreshagent.com/?utm_source=marketingskills_seo) or the [RefreshAgent ChatGPT App](https://chatgpt.com/plugins/plugin_asdk_app_6ac5ec2359dc8191899aeb18f6d6db6e) to pull real referral and conversion baselines alongside your citation log.

## Output Template

```markdown
## Monthly AI Visibility Log (YYYY-MM)

### 1. Bing AI Performance (First-Party)
- Total cited appearances: N (prior: N)
- Avg cited pages/day: N (prior: N)
- Top grounding query themes: ...

### 2. Buyer-Question Panel (N questions x 2 runs x 4 engines)
| Question | Source (Inbox/Call/GSC) | ChatGPT (Named / Cited) | Claude (Named / Cited) | Perplexity (Named / Cited) | Gemini (Named / Cited) | Dominant 3rd-party URLs cited |
|---|---|---|---|---|---|---|

### 3. AI Referral Counts & Self-Reported Signups
- GA4 AI referral visits (raw count): N
- "How did you hear about us?" mentions of AI tools: N

### 4. Next 3 Actions (Own-site pages + 3rd-party list outreach)
```
