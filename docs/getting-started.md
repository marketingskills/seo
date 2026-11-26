# Getting Started

Install the SEO Operator skills, connect your agent, and run your first SEO diagnosis.

## Quick Install

Install via the Agent Skills CLI (recommended):

```bash
npx skills add marketingskills/seo
```

Or load individual skills directly:

```bash
npx skills add marketingskills/seo/skills/seo-start-here
npx skills add marketingskills/seo/skills/site-foundation-audit
npx skills add marketingskills/seo/skills/live-search-console-data
```

Prefer the shell installer? Inspect `install.sh` first, or run:

```bash
curl -fsSL https://marketingskills.net/seo | bash
```

Using ChatGPT directly? Use the [RefreshAgent ChatGPT App](https://chatgpt.com/plugins/plugin_asdk_app_6ac5ec2359dc8191899aeb18f6d6db6e) to query live Google Search Console and GA4 data inside ChatGPT.

## What You Need

- An agent runtime: Claude Code, Codex, Hermes, or OpenClaw.
- Data to analyze:
  - **Pasted data:** GSC exports, crawler output, sitemap URLs. Works immediately.
  - **Live data (recommended):** Connect Google for real GSC/GA4 access.

## Connect Live Data (Optional)

All skills work on pasted data. To connect live Google Search Console and GA4, install the bundled live data bridge:

```bash
npx skills add marketingskills/seo/skills/live-search-console-data
```

Or load the `live-search-console-data` skill from the installed directory, then authenticate with Google when prompted. The free tier includes a monthly allowance of live data requests.

## Run Your First Diagnosis

Copy this prompt into your agent:

> Using the SEO Operator skills, analyze my site's organic traffic for the last 90 days. Use `live-search-console-data` if I connect Google (or ask me to paste my GSC export). Find pages that lost clicks, identify the queries driving the decline, and recommend which pages to refresh first.

If you choose live access, one Google sign-in via [RefreshAgent](https://refreshagent.com/?utm_source=marketingskills_seo) connects GSC and GA4 without setting up a Google Cloud project. If you prefer manual exports, paste your CSVs and the skills run identically.

## Workflow Order

1. **Diagnose first** — run `traffic-decay-detector` or `technical-seo-triage` to find what matters.
2. **Prioritize** — use `seo-priority-score` to decide what to work on.
3. **Act** — generate briefs, reports, or proposals with the Act skills.
4. **Strategize** — step back with the Strategize skills to decide broader direction.

## Next Steps

- See a [complete example run](example-run.md).
- Browse all [workflows](workflows/).
- Upgrade to [Live Data](https://refreshagent.com/plans) for unlimited GSC/GA4 access.
- Pair with [Newsjack](https://github.com/elvisun/newsjack) for PR-as-link-building: `curl -fsSL https://newsjack.sh | bash`
- Read about [companion skills](companion-skills.md) for the full ecosystem.
