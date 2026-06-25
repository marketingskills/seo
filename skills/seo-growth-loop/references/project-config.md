# Project Config Reference

Use a project config when present. If none exists, infer these fields from the repo, CMS notes, environment, or user instructions.

```yaml
site_url: https://example.com
primary_domain: example.com
gsc_property: sc-domain:example.com
business_goal: qualified demos
target_audience: buyers researching vendors
publishing_mode: local_repo # local_repo | cms_api | hybrid | advisory
agent_runtime: claude_code # claude_code | codex | opencode | other | advisory
content_update_surface: WordPress REST API, Contentful, Django admin, Markdown files, etc.
production_verification: live_url # live_url | preview_url | local_server | advisory_only
indexing_method: indexnow # indexnow | search_console | sitemap_only | cms_auto | none
work_log_path: seo_improvements_log.md
keyword_source: keyword-planner, Ahrefs export, CSV path, GSC queries, etc.
authority_domain: example.com
scheduling:
  enabled: false
  method: cron # cron | systemd | github_actions | hosted | none
  cadence: weekly
  command: null
restricted_topics:
  - topics that should not be targeted
required_checks:
  - rendered page returns 200
  - indexable when intended
  - title/meta/canonical present
  - schema validates
  - internal links work
```

## Config Use

- Use `site_url` for live verification and canonical URLs.
- Use `gsc_property` for Search Console requests.
- Use `publishing_mode` to choose the adapter.
- Use `authority_domain` for Authority Mark comparisons. Default to the registrable domain of `site_url`.
- Use `business_goal` to decide which traffic is commercially useful.

## Missing Config

If config is missing:

1. Identify the live site from user instructions, package metadata, repo env, or canonical URLs.
2. Inspect the repo for framework, deploy, content, and API clues.
3. Ask only if the target site or write path remains ambiguous.
