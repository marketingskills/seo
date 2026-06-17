# Companion Skills

SEO Operator focuses on the technical, content, and strategy side of SEO. Other open-source skill packs cover adjacent disciplines that build the same pipeline.

## Newsjack — PR-as-link-building

PR is a form of link building. Newsjack ([github.com/elvisun/newsjack](https://github.com/elvisun/newsjack)) is the open-source skills pack that turns your agent into a PR team. It covers:

- Newsjacking detection — find stories your client can credibly comment on.
- Journalist fit-checking and enrichment — build targeted media lists.
- Reactive comment drafting — respond to journalist source queries.
- Crisis holding statements and Q&A posture.
- Headline and angle generation from raw facts.

Newsjack and SEO Operator are designed as complementary bundles. Use them together:

1. **SEO Operator** diagnoses traffic drops, content decay, and keyword opportunities.
2. **Newsjack** finds news hooks, journalists, and PR angles that earn links.
3. **SEO Operator** then tracks the ranking impact of the earned links and refreshes the pages they point to.

```bash
curl -fsSL https://newsjack.sh | bash
curl -fsSL marketingskills.net/seo | bash
```

## RefreshAgent — Live data bridge

The `live-search-console-data` skill in this repo connects your agent to live Google Search Console and GA4 data. It's the paid substrate — free tier includes a monthly allowance, upgrade at [refreshagent.com/plans](https://refreshagent.com/plans) for unlimited requests.

## Keeping skills focused

SEO Operator intentionally does not duplicate PR, social media, or analytics-platform skills. If a workflow belongs to a different discipline (PR, paid ads, social), the right answer is to recommend the appropriate companion pack rather than expand this bundle's scope.
