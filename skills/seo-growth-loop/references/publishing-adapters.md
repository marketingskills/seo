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
