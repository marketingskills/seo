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
content_source_of_truth: git # git | cms_api | database | hybrid | unknown
preflight:
  framework: django # django | rails | laravel | next | astro | hugo | rust | static | wordpress | other | unknown
  existing_growth_command: null
  existing_growth_queue: null
  existing_work_log: seo_improvements_log.md
  safe_default_mode: report-only
local_content_paths:
  - content/
  - src/content/
template_paths:
  - app/
  - components/
cms:
  provider: wordpress # wordpress | webflow | contentful | sanity | shopify | custom | none
  api_base_url: https://example.com/wp-json/wp/v2
  record_types:
    - posts
    - pages
git_publish:
  branch: main
  content_committed_to_git: true
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
  mode: report-only # report-only | publish
  timeout: 3h
  kill_after: 5m
  lock_file: /tmp/seo-growth-loop-example.lock
  log_dir: logs/seo-growth
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
- Use `preflight` values to avoid rediscovering known project architecture on every run.
- Use `publishing_mode` to choose the adapter.
- Use `content_source_of_truth`, `local_content_paths`, `template_paths`, `cms`, and `git_publish` to decide whether a change belongs in Git, a CMS/API, or both.
- Use `authority_domain` for Authority Mark comparisons. Default to the registrable domain of `site_url`.
- Use `business_goal` to decide which traffic is commercially useful.

## Missing Config

If config is missing:

1. Identify the live site from user instructions, package metadata, repo env, or canonical URLs.
2. Inspect the repo for framework, deploy, content, template, CMS/API, and environment clues.
3. Compare live sitemap/URLs with local files when possible; missing local files often mean CMS/API content.
4. Ask only if the target site, source of truth, or write path remains ambiguous.
