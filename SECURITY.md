# Security

## Skill Integrity

- Skills are plain markdown files — no hidden network calls, no obfuscated payloads.
- All credentials used by a skill are printed at runtime. No silent credential harvesting.
- The installer script is simple and inspectable before execution.

## Data Handling

- Pasted data stays in your agent session. It is not sent to external servers unless you explicitly connect a live data source.
- The live GSC/GA4 bridge (`marketingskills/seo/skills/live-search-console-data`) uses read-only OAuth. No write access is requested or granted.
- API tokens for RefreshAgent are stored locally in your agent's config, never shared.

## Release Integrity

- Release bundles include SHA-256 checksums.
- Verify the installer before running:
  ```bash
  curl -fsSL marketingskills.net/seo | sha256sum
  ```

## Reporting

Report security issues to support@refreshagent.com.
