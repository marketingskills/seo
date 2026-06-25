# Scheduling Reference

Use scheduling only when the user explicitly asks for recurring SEO work or approves a proposed schedule. Do not install or modify scheduled jobs silently.

## Permission Gate

Before installing a schedule, present:

- what command or workflow will run
- cadence and timezone
- where logs/reports will be written
- whether it can write production content or only produce reports
- required secrets and where they must be configured
- how to disable the schedule

Ask for explicit permission before writing cron entries, systemd timers, GitHub Actions workflows, hosted scheduler configs, or CMS automation rules.

## Safe Defaults

Default recurring mode should be report-only:

- gather performance data
- produce an opportunity queue
- write a log/report
- avoid production writes
- avoid auto-publishing
- avoid indexing submissions unless URLs were actually changed

Make auto-publishing a separate opt-in flag or job.

## Cron Pattern

Use cron when the project runs on a server where cron is appropriate.

Recommended shape:

```cron
15 7 * * 1 /usr/bin/env bash /path/to/run_seo_growth_loop.sh >> /path/to/logs/seo-growth.log 2>&1
```

Wrapper script expectations:

- set working directory
- load environment or document required env vars
- run report-only by default
- write dated output
- exit nonzero on hard failures
- avoid printing secrets

## Systemd Timer Pattern

Use systemd timers when the server already uses systemd for scheduled jobs.

Create a service and timer pair only after permission. Include `WorkingDirectory`, `EnvironmentFile` when needed, and logs through journald or a project log path.

## GitHub Actions Pattern

Use GitHub Actions when the workflow is repo-centered and secrets can be safely stored in GitHub.

Use scheduled workflows for report generation, not direct production writes, unless the user explicitly approves:

```yaml
on:
  schedule:
    - cron: "15 7 * * 1"
  workflow_dispatch:
```

Store API keys as repository or organization secrets. Do not commit secrets.

## Hosted Scheduler Pattern

Use a hosted scheduler when the site is CMS/API-only and has no suitable repo/server runtime. Prefer a small endpoint or serverless function that runs report-only unless explicitly approved.

## Disable Instructions

Every schedule install should include a disable path:

- cron: remove or comment the crontab line
- systemd: `systemctl disable --now <timer>`
- GitHub Actions: disable workflow or remove schedule
- hosted scheduler: disable the job in provider UI/API
