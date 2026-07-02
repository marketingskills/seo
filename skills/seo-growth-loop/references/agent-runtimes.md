# Agent Runtime Reference

The SEO workflow is agent-agnostic. Runtime differences only affect how commands are run, files are edited, approvals are requested, and changes are handed off.

## Default: Claude Code

Assume Claude Code-style local project work when no runtime is specified:

- Read project instructions such as `CLAUDE.md`, `AGENTS.md`, or repo docs.
- Use local shell tools and file edits.
- Follow project-specific test/deploy instructions.
- Use the user's established approval model before live writes, cron installs, or pushes.

## Codex

Use Codex conventions when running inside Codex:

- Read `AGENTS.md` and applicable skills before acting.
- Use `apply_patch` for manual file edits when available.
- Respect filesystem/network sandboxing and request approval for external writes, network, production changes, or scheduling.
- Prefer deterministic local tests before finalizing.
- Keep user-facing final summaries concise and include verification status.

For scheduled runs, use the noninteractive CLI and avoid persistent sessions:

```bash
codex exec --ephemeral --cd /path/to/project --ask-for-approval never \
  "Use the seo-growth-loop skill. Run exactly one report-only cycle, write the log, and stop."
```

Use `--ask-for-approval never` in cron so the job fails cleanly instead of hanging on an approval prompt. Do not use interactive Codex, `resume`, app servers, or remote-control daemons for scheduled SEO loops.

## OpenCode

Use OpenCode or other coding-agent conventions when that is the active runtime:

- Read the project's agent instruction files and OpenCode config if present.
- Use the editing and command tools provided by that runtime.
- Preserve the same SEO decision loop; only the mechanics of file edits, command execution, and approval prompts change.
- If OpenCode lacks a needed integration, switch to advisory mode or provide exact commands for the user to run.

For scheduled runs, use `opencode run` as a foreground one-shot command:

```bash
opencode run --dir /path/to/project \
  "Use the seo-growth-loop skill. Run exactly one report-only cycle, write the log, and stop."
```

Do not use `opencode serve`, `opencode web`, `attach`, `--continue`, or long-lived shared sessions for cron jobs. If the runtime needs a persistent server for another reason, run the SEO loop through a separate locked wrapper and enforce a timeout around the foreground command.

## Advisory Or No Local Code

Use when there is no repo, no write access, or no deploy path:

- Do not claim implementation.
- Produce CMS-ready copy, metadata, schema suggestions, internal link targets, and verification steps.
- Include the baseline and Authority Mark evidence so a human or another system can implement.

## Runtime Selection

If multiple runtimes are possible, choose in this order:

1. User-specified runtime.
2. Runtime implied by the current environment.
3. Claude Code-style local workflow as default.
4. Advisory mode when no safe execution path exists.
