---
name: schema-fix-writer
description: Propose schema markup changes from page type and SERP context. Use when Codex needs to write or fix structured data for better SERP display and rich results eligibility.
---

# Schema Fix Writer

## Overview

Given a page URL and its content, analyze what schema types are genuinely supported and propose specific JSON-LD changes (`Organization`, `WebSite`, `Article`, `Product`, `SoftwareApplication`, `LocalBusiness`, `BreadcrumbList`, etc.).

## Current Eligibility Rules

- **Do not recommend deprecated `HowTo` markup** (Google stopped showing HowTo rich results in 2023).
- **Do not rate `FAQPage` markup as high-impact** for standard commercial sites (Google restricted FAQ rich results primarily to authoritative government and health sites).
- **Never add `AggregateRating` or review stars** unless real, verifiable customer reviews are visibly published on the page.

## Inputs

- Page URL and optionally its rendered content
- Current schema (if any) — paste from source or tool output
- Page type or topic

## Workflow

1. Determine the page type from content analysis.
2. Check the page's current schema markup for errors or missing fields.
3. Research the target SERP for rich result types present.
4. Propose schema changes:
   - Add missing schema type for the page type
   - Fix validation errors in existing schema
   - Add relevant verified properties (author, publisher, dates, pricing, availability, breadcrumbs, `sameAs` entities)
   - Remove deprecated, deceptive, or unverified markup (such as `HowTo` or fabricated review stars)
5. Write the JSON-LD or microdata snippet.
6. Include testing instructions (Schema.org validator, Rich Results Test).

## Output

Schema recommendation with proposed markup, validation notes, and SERP eligibility impact.
