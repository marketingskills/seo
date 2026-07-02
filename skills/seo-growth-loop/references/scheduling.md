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

## Scheduled Runner Contract

Every scheduled job should be a bounded foreground process:

- run a noninteractive agent command (`codex exec` or `opencode run`)
- do exactly one SEO cycle, then stop
- use a lock so overlapping runs skip instead of stacking up
- use a wall-clock timeout and short kill-after window
- write stdout/stderr to a dated log file
- default to report-only mode unless publishing is explicitly approved
- avoid `resume`, `continue`, background jobs, app servers, web servers, or daemon commands

The bundled `scripts/run_seo_growth_loop.sh` wrapper implements this shape for Linux cron/systemd hosts with `bash`, `flock`, and GNU `timeout`.

## Cron Pattern

Use cron when the project runs on a server where cron is appropriate.

Recommended shape:

```cron
15 7 * * 1 /usr/bin/env bash /path/to/run_seo_growth_loop.sh >> /path/to/logs/seo-growth.log 2>&1
```

Recommended wrapper invocation:

```cron
15 7 * * 1 SEO_LOOP_PROJECT_DIR=/srv/example-site SEO_LOOP_RUNTIME=codex /path/to/skills/seo-growth-loop/scripts/run_seo_growth_loop.sh
```

Useful environment variables:

- `SEO_LOOP_PROJECT_DIR`: required project/site repo path
- `SEO_LOOP_RUNTIME`: `codex` or `opencode`; defaults to `codex`
- `SEO_LOOP_MODE`: `report-only` or `publish`; defaults to `report-only`
- `SEO_LOOP_LOG_DIR`: log directory; defaults to `$SEO_LOOP_PROJECT_DIR/seo-growth-logs`
- `SEO_LOOP_LOCK_FILE`: lock path; defaults to a `/tmp` lock derived from the project path
- `SEO_LOOP_TIMEOUT`: wall-clock limit; defaults to `3h`
- `SEO_LOOP_KILL_AFTER`: grace period before force kill; defaults to `5m`

Cron should normally run the wrapper directly, not wrap the agent command itself. Keep secrets in the user's shell profile, a root-readable environment file, or the scheduler's secret store; do not put secrets in crontab lines.

## Codex Cron Example

```cron
15 7 * * 1 SEO_LOOP_PROJECT_DIR=/srv/example-site SEO_LOOP_RUNTIME=codex /path/to/skills/seo-growth-loop/scripts/run_seo_growth_loop.sh
```

The wrapper runs:

```bash
codex exec --ephemeral --cd "$SEO_LOOP_PROJECT_DIR" --ask-for-approval never "$PROMPT"
```

`--ephemeral` avoids accumulating session files. `--ask-for-approval never` prevents unattended approval prompts from hanging the job.

## OpenCode Cron Example

```cron
15 7 * * 1 SEO_LOOP_PROJECT_DIR=/srv/example-site SEO_LOOP_RUNTIME=opencode /path/to/skills/seo-growth-loop/scripts/run_seo_growth_loop.sh
```

The wrapper runs:

```bash
opencode run --dir "$SEO_LOOP_PROJECT_DIR" "$PROMPT"
```

Use `opencode run` only. Avoid `opencode serve`, `opencode web`, `attach`, and continued sessions in scheduled jobs.

## Overlap And Cleanup

Use `flock -n` so a new run exits when the previous run is still active. Treat a skipped run as acceptable; the next scheduled window can try again.

Use `timeout --kill-after=5m 3h ...` or equivalent. Choose a timeout longer than a normal run but shorter than the cadence. For example, a weekly job can use `3h`; an hourly job should use a much smaller limit.

If the host does not provide `flock` or GNU `timeout`, use systemd timers with `LockFile`/single service semantics and `TimeoutStopSec`, or install the equivalent utilities before enabling cron.

## Systemd Timer Pattern

Use systemd timers when the server already uses systemd for scheduled jobs.

Create a service and timer pair only after permission. Include `WorkingDirectory`, `EnvironmentFile` when needed, `ExecStart` pointing at the wrapper script, `TimeoutStartSec`, and logs through journald or a project log path.

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

For Actions, use `concurrency` to prevent overlap:

```yaml
concurrency:
  group: seo-growth-loop-${{ github.ref }}
  cancel-in-progress: false
```

## Hosted Scheduler Pattern

Use a hosted scheduler when the site is CMS/API-only and has no suitable repo/server runtime. Prefer a small endpoint or serverless function that runs report-only unless explicitly approved.

## Disable Instructions

Every schedule install should include a disable path:

- cron: remove or comment the crontab line
- systemd: `systemctl disable --now <timer>`
- GitHub Actions: disable workflow or remove schedule
- hosted scheduler: disable the job in provider UI/API
