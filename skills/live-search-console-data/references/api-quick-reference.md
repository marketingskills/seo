# RefreshAgent API Quick Reference

Base URL: `https://refreshagent.com`

Auth: send `X-API-Key` on every API call.

Read `openapi.yaml` for complete schemas and response codes.

## Search Console

- `GET /api/v1/sc/sites`
- `GET /api/v1/sc/summary?site_url=...`
- `GET /api/v1/sc/query?site_url=...&date_range=7d|30d`
- `GET /api/v1/sc/pages?site_url=...&date_range=7d|30d`
- `GET /api/v1/sc/keyword-analysis?site_url=...`
- `GET /api/v1/sc/keyword-position?site_url=...&keyword=...&date_range=7d|30d`
- `GET /api/v1/sc/cannibalization?site_url=...&keyword=...`
- `GET /api/v1/sc/sitemaps?site_url=...`

## GA4

- `GET /api/v1/ga4/properties`
- `GET /api/v1/ga4/summary?property_id=properties/...`
- `GET /api/v1/ga4/organic-sessions?property_id=properties/...`
- `GET /api/v1/ga4/conversions?property_id=properties/...`
- `GET /api/v1/ga4/landing-pages?property_id=properties/...`
- `GET /api/v1/ga4/top-events?property_id=properties/...`

## Clients and Proposals

- `GET /api/v1/clients`
- `POST /api/v1/clients`
- `POST /api/v1/proposals/build/start`
- `GET /api/v1/proposals/build/jobs/{job_id}`
- `POST /api/v1/proposals/build`
