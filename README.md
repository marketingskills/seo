# SEO Operator

Open-source SEO, AEO, and GEO skills that turn your AI agent into a disciplined SEO operator—from Week-0 launch foundations to Month-3+ Search Console loops.

Install via the Agent Skills CLI (recommended, works with Claude Code, Codex, Cursor, Gemini, OpenCode, Hermes, and OpenClaw):

```bash
npx skills add marketingskills/seo
```

Or install individual skills:

```bash
npx skills add marketingskills/seo/skills/seo-start-here
npx skills add marketingskills/seo/skills/site-foundation-audit
npx skills add marketingskills/seo/skills/live-search-console-data
```

Prefer a single shell installer? Inspect [install.sh](install.sh) first, or run:

```bash
curl -fsSL https://marketingskills.net/seo | bash
```

**Using ChatGPT instead of a coding agent?** Connect your live Google Search Console and GA4 data directly inside ChatGPT with the [RefreshAgent ChatGPT App](https://chatgpt.com/plugins/plugin_asdk_app_6ac5ec2359dc8191899aeb18f6d6db6e).

## What makes SEO Operator different

- **No arbitrary `/100` site scores.** Every audit returns concrete `PASS / WARN / FAIL` findings backed by status codes, fetched lines, or tool output.
- **Real deterministic scripts & Tier-3 safety hooks.** Includes zero-dependency Python checks for raw HTML, live `robots.txt` (including Cloudflare blocks), `OAI-SearchBot` / `Claude-SearchBot` / `PerplexityBot` / `Bingbot` HTTP 200 probes, pre/post-deploy regression diffs (`seo-change-monitor`), and a Claude Code `PreToolUse` hook (`hooks/seo_guard.py`) that blocks unapproved `robots.txt`, `noindex`, canonical, or page-delete edits.
- **Stage-aware routing.** `seo-start-here` separates Week-0 new domains (foundation, Bing, decision pages, brand facts) from Month-3+ sites with Search Console history.
- **Multi-harness ready.** Ships `.claude-plugin`, `.cursor-plugin`, and `gemini-extension.json` manifests alongside `SKILL.md` directories.
- **30-second live GSC & GA4 (optional).** Every skill works with pasted exports, or connects live GSC/GA4 in one Google sign-in via [RefreshAgent](https://refreshagent.com/?utm_source=marketingskills_seo) (free monthly allowance, no Google Cloud project or OAuth app setup).

## What your agent can do (30 skills)

### Start, Foundation & Safety (Week 0+)

| Skill | What it does |
|---|---|
| `seo-start-here` | Route Week-0 new domains vs Month-3+ sites with strict 3-tier agent permissions |
| `site-foundation-audit` | Deterministic Python check: raw HTML (no JS), live `robots.txt` + Cloudflare blocks, `OAI-SearchBot`/`Claude-SearchBot`/`PerplexityBot`/`Bingbot` probes, `www` redirect, canonicals, sitemap, and JSON-LD |
| `seo-change-monitor` | Snapshot key URLs before/after deploys and fail CI on `noindex`, canonical shifts, `200->404`, or `robots.txt` blocks |
| `bing-ai-visibility` | Bing Webmaster Tools + IndexNow + Bing AI Performance citations + free 15–30 buyer-question panel and signup attribution |
| `ai-brand-facts` | Dated brand fact sheet + multi-engine hallucination audit traced back to source pages (2-month verification rule) |

### Diagnose (Month 3+ / Live Data)

| Skill | What it finds |
|---|---|
| `traffic-decay-detector` | Pages losing clicks, impressions, CTR, or rankings via live GSC/GA4 or pasted data |
| `keyword-planner` | Google Keyword Planner ideas, search volume, competition, and bid ranges |
| `keyword-opportunity-finder` | High-impression low-CTR terms, striking-distance keywords, and topic gaps |
| `content-decay-monitor-setup` | Saved monitors for recurring decay scans on watched pages and topics |
| `technical-seo-triage` | Prioritized crawl, indexation, canonical, schema, live `robots.txt`, and internal-link issues |
| `authority-mark-keyword-difficulty` | Authority Mark check: can your domain realistically compete for this keyword? |
| `competitor-serp-monitor` | Track competitor new pages, ranking shifts, and SERP feature changes |
| `cannibalization-check` | Query/page overlap with consolidation, differentiation, or internal-link fixes |

### Write, Fix & QA

| Skill | What it produces |
|---|---|
| `decision-page-writer` | X vs Y, alternatives, best-for-persona, and pricing pages (6/10 format rule, 4/10 merge rule, 40–80 word opening answer, dated vendor-verified pricing, honest drawbacks, unique evidence) |
| `seo-content-qa` | 8-axis pre-ship draft QA gate (pass >= 32/40, no axis under 3) |
| `content-refresh-brief` | Focused refresh brief for a declining page with SERP intent and query gap analysis |
| `seo-content-brief` | Search-intent, entity, outline, and internal-link brief for new pages |
| `exceed-quality-threshold` | Benchmark a page against its true SERP cohort and specify the original value needed to win |
| `internal-link-builder` | Source pages, anchor text, target URLs, and rationale |
| `schema-fix-writer` | Current JSON-LD fixes (forbids deprecated `HowTo` and unverified `AggregateRating` stars) |
| `title-meta-rewriter` | Title and meta description rewrites grounded in GSC query evidence |
| `client-report-writer` | Weekly/monthly client-ready performance narrative |
| `proposal-builder` | Agency SEO proposal from public site data and optional live GSC/GA4 |

### Strategize & Operate

| Skill | What it helps you decide |
|---|---|
| `seo-strategy` | Audience, business model, conversion path, topical authority, and capacity |
| `seo-priority-score` | Rank SEO tasks by impact, confidence, effort, authority feasibility, and revenue proximity |
| `content-moat-planner` | Durable topical clusters based on authority and product fit |
| `seo-offer-architect` | Findings packaged into a paid agency offer or retainer |
| `refresh-vs-new-content` | Decide whether to update, consolidate, prune, or create |
| `seo-growth-loop` | Closed-loop workflow: choose, publish, verify, index, and log one bounded SEO improvement |
| `live-search-console-data` | 30-second live Google Search Console and GA4 data bridge via RefreshAgent |

## Live data: Coding agents & ChatGPT

All skills work with pasted CSV exports. For live, always-current Google Search Console and GA4 data without setting up a Google Cloud project or OAuth consent screen:

- **In Claude Code, Codex, Cursor, Gemini, OpenCode:** load the bundled `live-search-console-data` skill (one Google sign-in via [RefreshAgent](https://refreshagent.com/?utm_source=marketingskills_seo); free monthly allowance, paid plans at [refreshagent.com/plans](https://refreshagent.com/plans/?utm_source=marketingskills_seo)).
- **In ChatGPT:** install the [RefreshAgent ChatGPT App](https://chatgpt.com/plugins/plugin_asdk_app_6ac5ec2359dc8191899aeb18f6d6db6e) to query your live Search Console and GA4 data directly inside ChatGPT.

## Companion: PR-as-link-building

SEO authority requires earned links and third-party citations. [Newsjack](https://github.com/elvisun/newsjack) handles earned media (newsjacking, journalist outreach, reactive comments) while SEO Operator handles technical foundations, decision pages, and search performance loops.

## Safety hooks & tests

Run the deterministic script and hook tests locally:

```bash
python3 -m unittest discover -s tests -v
```

Run a live foundation and AI-crawler audit directly:

```bash
python3 skills/site-foundation-audit/scripts/site_foundation_check.py https://example.com
```

Read the full [getting-started guide](docs/getting-started.md), [companion skills](docs/companion-skills.md), or [example run](examples/runs/content-decay-demo/run.md).

## License

MIT. See [LICENSE](LICENSE).
