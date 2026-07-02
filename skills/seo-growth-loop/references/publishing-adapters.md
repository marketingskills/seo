# Publishing Adapters

Choose the safest adapter the project actually supports. Do not force a local-code workflow onto a CMS-only project, and do not fabricate production changes in advisory mode.

## Publishing Surface Detection

Before writing, classify the project by evidence. Prefer explicit project config or docs, then inspect the repo and environment.

Use **local repo mode** when content itself lives in versioned files:

- Markdown/MDX/content collections under paths such as `content/`, `posts/`, `blog/`, `src/content/`, `app/**/page.*`, or `pages/**`
- static-site generators such as Astro, Next static content, Hugo, Jekyll, Eleventy, Docusaurus, or Gatsby with file-backed posts
- docs or deploy notes saying content changes are committed, reviewed, and deployed from Git
- existing commits that add or update article/page files

Use **CMS/API mode** when content records live outside Git:

- WordPress, Webflow, Contentful, Sanity, Strapi, Shopify, Ghost, HubSpot, Notion-backed sites, Airtable-backed sites, or a custom content API
- environment variables or docs naming API endpoints, tokens, CMS spaces/datasets, WordPress REST credentials, or admin URLs
- repo contains only theme, frontend, templates, build code, or integration code while live posts/pages are absent from the repo
- sitemap/live URL inventory contains content that has no matching local source file

Use **hybrid mode** when code and content are split:

- templates, components, schema, routing, sitemap, or internal-link logic are in Git
- page/post/product/entity records are created or edited through a CMS/API/database
- examples: edit a WordPress theme or Next frontend in Git, then create/update the blog post via WordPress REST; add schema rendering in code, then enrich CMS fields; change a listing template in Git, then add entity records via API

Use **advisory mode** when the publishing surface cannot be verified, credentials are missing, writes are unsafe, or the user only wants recommendations.

If evidence conflicts, choose the lowest-risk mode that can complete the requested change and log the uncertainty. Ask only when the target site, source of truth, or production write path remains ambiguous after inspection.

## Source-Of-Truth Rule

Before changing a URL, answer: "Where does this page's rendered content actually come from?"

Common answers:

- **Git file**: edit the content file or route/template in Git, then test and follow the deploy workflow.
- **Database record**: update through the admin/API/management command that writes the live database; edit seed files only when the project says seed files are the production source.
- **CMS/API record**: read and patch the record through the official API/admin surface.
- **Generated from structured data**: change the generator, thresholds, query, template, or source dataset based on which part limits quality.
- **Template plus database/API**: use hybrid mode and separate data changes from reusable rendering changes.
- **Unknown**: stay report-only or advisory until the source of truth is clear.

Do not treat local repository access as proof that production content is Git-backed. Do not treat a seed/import file as production content unless project docs or deploy scripts confirm it.

## Adapter Priority Matrix

| Opportunity | Prefer code/Git when | Prefer API/admin/database when |
|---|---|---|
| Title/meta/schema | rendering logic lives in templates or components | editable SEO fields exist on records |
| One entity, location, product, or company | the entity is represented by a versioned file | the page type already exists and records drive pages |
| New page type or route | route/template/schema/sitemap behavior is missing | CMS already supports the page type cleanly |
| Internal links | navigation, related-link modules, or sitewide templates need changes | record-level relationships or tags drive links |
| Programmatic expansion | generator thresholds, templates, or sitemap logic need changes | adding records alone creates indexable pages |
| Content refresh | page body is file-backed | body/FAQ/fields are editable records |

When both columns apply, use hybrid mode and log the required order of operations.

## Existing Automation Handoff

If the project already has a growth workflow, queue, or SEO agent script, use it as the first diagnostic input:

- commands named like `daily_growth_*`, `run_*growth*.sh`, `seo_agent.*`, or management commands that write SEO queues
- output folders such as `growth_queues/`, `.repo-growth/`, or SEO reports
- logs such as `seo_improvements_log.md`, `seo_growth.log`, or dated growth reports
- docs mentioning Search Console, RefreshAgent, IndexNow, keyword queues, Authority Mark, or recurring SEO work

Do not create a second scheduler or duplicate opportunity queue unless the user explicitly wants a replacement. Prefer: run or read the existing workflow, choose one action from its output, implement/verify/log, then stop.

## CMS/API Mode

Use when the site content is managed through WordPress, Webflow, Contentful, Sanity, Shopify, a custom API, or an admin surface.

Process:

1. Confirm the endpoint/admin surface and authentication method without exposing secrets.
2. Read the current live record/page first.
3. Prepare a minimal content/data patch.
4. Write through the official API/admin path.
5. Verify the rendered live URL.
6. Log the exact record/page changed and verification result.

Avoid schema or layout assumptions unless the CMS exposes those fields.

## Local Repo Mode

Use when the project has local code/content and the user expects code changes.

Process:

1. Inspect framework, routes, templates, content folders, tests, and deploy notes.
2. Make narrow edits that match local conventions.
3. Run deterministic checks relevant to the touched surface.
4. Verify local render when possible.
5. Commit/PR/push only if the user requested or the project workflow says to do so.
6. Log touched files and affected production URLs.

## Hybrid Mode

Use when page types, schema, templates, or internal linking live in code while entity/content records live in a CMS/API/database.

Process:

1. Map each intended change to its source of truth: code/template, CMS/API record, database row, or both.
2. Decide whether the bottleneck is data coverage, page architecture, internal linking, metadata rendering, or schema.
3. Use API/CMS for entity/content enrichment, post/page creation, metadata fields, FAQs, media assignments, and category/tag changes.
4. Use code for reusable page templates, schema rendering, routing, sitemap generation, canonical logic, and internal-link modules.
5. Verify both the changed record and the rendered page.
6. Log files changed, API records changed, deploy/publish status, and any ordering dependency between code deploy and content publish.

## Advisory Mode

Use when the agent lacks write access, deploy access, or a local repo.

Deliver:

- target URL/query and baseline metrics
- rationale and Authority Mark if relevant
- CMS-ready title/meta/body/FAQ/internal-link recommendations
- schema suggestions
- implementation checklist
- verification checklist
- follow-up measurement date

Do not say the change was made.

## Indexing

Use the project's available indexing path:

- IndexNow for supported domains.
- Search Console URL inspection or sitemap resubmission when available.
- CMS-generated sitemap ping when that is the only path.
- No indexing action if none is available; log the limitation.

Submit only canonical, public, indexable production URLs that changed.
