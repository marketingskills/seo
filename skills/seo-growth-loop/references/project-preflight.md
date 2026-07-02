# Project Preflight

Run this before choosing SEO work. The goal is to classify the project by evidence, not by guesswork.

## Quick Probe

When local repository access exists, optionally run:

```bash
python3 /path/to/seo-growth-loop/scripts/probe_project.py /path/to/project
```

Use the output as hints, not as authority. Confirm important claims against project docs, deploy scripts, routes, models, templates, and live URLs when available.

## Required Preflight Summary

Record these fields in the run log or work log:

- site URL and primary domain
- framework/runtime
- content source of truth: Git, CMS/API, database, generated data, hybrid, or unknown
- publishing mode: local repo, CMS/API, hybrid, or advisory
- editable surfaces: files, admin, API, management command, seed/import file, database, or none
- existing SEO/growth commands and queues
- performance data source and freshness
- verification path
- indexing path
- safe default mode: report-only or publish-approved

## Classification Rules

Classify as **Git-backed** when the page body itself lives in versioned files and production deploys from those files.

Classify as **database-backed** when routes/templates render records from models, migrations, ORM schemas, SQL tables, fixtures, or management commands.

Classify as **CMS/API-backed** when docs, environment names, SDK packages, or admin/API routes point to WordPress, Webflow, Contentful, Sanity, Shopify, Strapi, Ghost, HubSpot, or a custom content API.

Classify as **generated-data-backed** when pages are produced from structured datasets, feeds, CSVs, JSON, crawlers, external APIs, or scheduled imports.

Classify as **hybrid** when templates/routes/schema/sitemaps live in code while entity/page records live in a database, CMS, API, or generated dataset.

Classify as **advisory** when the write path is unclear, credentials are unavailable, production state cannot be verified, or the requested mode is report-only.

## Existing Workflow Rule

If the project already has recurring SEO or growth automation, do not bypass it. Read its docs and outputs first. Use it to form the opportunity queue, then choose one bounded action.

Useful signals include:

- growth commands, management commands, or shell runners
- `growth_queues/`, `.repo-growth/`, `seo/`, `reports/`, or `logs/`
- `seo_improvements_log.md` or similar work logs
- docs mentioning Search Console, RefreshAgent, IndexNow, keyword research, Authority Mark, or sitemap submission

## Write-Safety Rule

Choose the lowest-risk write path that can produce the SEO improvement:

1. report-only when the source of truth or credentials are unclear
2. API/admin/database update when existing records drive the page
3. code change when reusable rendering, metadata, schema, sitemap, route, or internal-link logic is the bottleneck
4. hybrid change only when both record data and reusable code need to change

Never edit local seed/import files as a production change unless project docs or deploy scripts prove those files are the live source of truth.
