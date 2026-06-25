# Publishing Adapters

Choose the safest adapter the project actually supports. Do not force a local-code workflow onto a CMS-only project, and do not fabricate production changes in advisory mode.

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

1. Decide whether the bottleneck is data coverage or page architecture.
2. Use API/CMS for entity/content enrichment.
3. Use code for reusable page templates, schema, routing, sitemap, and internal-link logic.
4. Verify both the data record and rendered page.

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
