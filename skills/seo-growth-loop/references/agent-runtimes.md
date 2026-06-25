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

## OpenCode

Use OpenCode or other coding-agent conventions when that is the active runtime:

- Read the project's agent instruction files and OpenCode config if present.
- Use the editing and command tools provided by that runtime.
- Preserve the same SEO decision loop; only the mechanics of file edits, command execution, and approval prompts change.
- If OpenCode lacks a needed integration, switch to advisory mode or provide exact commands for the user to run.

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
