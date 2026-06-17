# SEO Operator

The open-source skills that turn your agent into an SEO operator.

Install once. Claude Code, Codex, Hermes, or OpenClaw can diagnose traffic drops,
write refresh briefs, build SEO proposals, and generate client-ready reports.

```bash
curl -fsSL marketingskills.net/seo | bash
```

Are you a human? Copy this prompt to any AI:

> help me setup https://github.com/marketingskills/seo and find SEO growth opportunities for my site

## What your agent can do

### Diagnose

Surface what matters — technical issues, traffic decay, keyword gaps, cannibalization, authority ceilings, and competitor moves.

| Skill | What it finds |
|---|---|
| `traffic-decay-detector` | Pages losing clicks, impressions, CTR, or rankings using GSC/GA4 or pasted data |
| `keyword-opportunity-finder` | High-impression low-CTR terms, striking-distance keywords, topic gaps |
| `content-decay-monitor-setup` | Saved monitors for recurring decay scans on watched pages/topics |
| `technical-seo-triage` | Prioritized crawl, indexation, canonical, schema, and internal-link issues |
| `serp-authority-mark` | Authority Mark method — can your site realistically compete for this keyword? |
| `competitor-serp-monitor` | Track competitor new pages, ranking shifts, SERP feature changes |
| `cannibalization-check` | Query/page overlap with consolidation or differentiation recommendations |

### Act

Turn diagnosis into output — refresh briefs, content briefs, internal link maps, schema fixes, title rewrites, client reports, and proposals.

| Skill | What it produces |
|---|---|
| `content-refresh-brief` | Focused refresh brief for a declining page with SERP intent analysis |
| `seo-content-brief` | Search-intent, entity, outline, and internal-link brief for new pages |
| `internal-link-builder` | Source pages, anchor text, target URLs, and rationale |
| `schema-fix-writer` | Schema change proposals from page type and SERP context |
| `title-meta-rewriter` | Title/meta descriptions from GSC query evidence and SERP intent |
| `client-report-writer` | Weekly/monthly client-ready performance narrative |
| `proposal-builder` | Agency proposal from public site data and optional GSC/GA4 |

### Strategize

Decide what not to do — priority scoring, content moat planning, offer architecture, and refresh-vs-new decisions.

| Skill | What it helps you decide |
|---|---|
| `seo-strategy` | Audience, business model, conversion path, topical authority, capacity |
| `seo-priority-score` | Rank tasks by impact, confidence, effort, authority feasibility, revenue proximity |
| `content-moat-planner` | Durable topical clusters based on authority and product fit |
| `seo-offer-architect` | Findings into a paid agency package or retainer |
| `refresh-vs-new-content` | Update, consolidate, prune, or create |

## Companion: PR-as-link-building

SEO authority requires backlinks. Newsjack is the open-source PR skills pack that turns your agent into a PR team — newsjacking, journalist outreach, reactive comments, crisis holding statements, and media monitoring. Together, the two bundles cover the full SEO + PR lifecycle:

| SEO Operator (this repo) | Newsjack |
|---|---|
| Diagnose traffic and ranking issues | Detect newsjack opportunities |
| Write content refresh briefs | Draft journalist pitches |
| Generate client reports | Write reactive comments |
| Build SEO proposals | Run PR campaigns |
| Authority-mark keyword difficulty | Find relevant journalists |

```bash
# Install both bundles
curl -fsSL marketingskills.net/seo | bash
curl -fsSL https://newsjack.sh | bash
```

PR is a form of link building. Newsjack handles the earned-media side while SEO Operator handles the technical and content side.

## Repository structure

```
skills/                     # Individual skill directories
  traffic-decay-detector/
  keyword-opportunity-finder/
  content-decay-monitor-setup/
  technical-seo-triage/
  serp-authority-mark/
  competitor-serp-monitor/
  cannibalization-check/
  content-refresh-brief/
  seo-content-brief/
  internal-link-builder/
  schema-fix-writer/
  title-meta-rewriter/
  client-report-writer/
  proposal-builder/
  seo-strategy/
  seo-priority-score/
  content-moat-planner/
  seo-offer-architect/
  refresh-vs-new-content/
  live-search-console-data/  # Live GSC/GA4 data bridge — 30s setup
docs/                       # Getting started, example run, workflows
examples/                   # Anonymized real run artifacts
```

Each skill is a directory with a `SKILL.md` file that an agent can load directly.

## Works with pasted data, gets better with live GSC/GA4

All skills work with data you paste in: GSC exports, crawler output, sitemap URLs, public SERPs. For repeatable, always-current analysis, install the live data bridge skill:

```bash
curl -fsSL marketingskills.net/seo | bash
```

Or add individual skills from the bundle:

```bash
npx skills add marketingskills/seo/skills/traffic-decay-detector
```

The `live-search-console-data` skill connects your agent to live Google Search Console and GA4 data through RefreshAgent. The free tier includes a monthly allowance. Upgrade at [refreshagent.com/plans](https://refreshagent.com/plans).

## Example run

```
examples/runs/content-decay-demo/run.md
```

Shows a complete run: 7 pages responsible for 62% of organic decline identified, 3 refreshes chosen, briefs written, client-ready action plan produced.

Read the full [getting-started guide](docs/getting-started.md) or [skip to the example run](docs/example-run.md).

## License

MIT
