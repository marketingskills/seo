#!/usr/bin/env python3
"""Tier-3 SEO safety hook for AI coding agents (Claude Code PreToolUse or standalone CLI).

"Put the 'never' in a hook, not in a prompt."

Blocks unapproved agent edits or shell commands that:
  1. Modify robots.txt
  2. Delete page/template/content files via rm or git rm
  3. Inject noindex directives or alter <link rel="canonical">
  4. Emit deprecated HowTo JSON-LD schema

Set SEO_ALLOW_CRITICAL_EDIT=1 after explicit human approval of the diff.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PROTECTED_FILES = ("robots.txt",)
CONTENT_EXTENSIONS = (".html", ".astro", ".tsx", ".jsx", ".md", ".mdx", ".njk", ".liquid", ".erb", ".php")
NOINDEX_RE = re.compile(r'content\s*=\s*["\'][^"\']*noindex|X-Robots-Tag["\']?\s*[:=]\s*["\']?[^"\']*noindex', re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link[^>]+rel\s*=\s*["\']canonical["\']', re.IGNORECASE)
HOWTO_RE = re.compile(r'"@type"\s*:\s*"HowTo"', re.IGNORECASE)
RM_PAGE_RE = re.compile(r"\b(?:git\s+)?rm\b.*\.(?:html|astro|tsx|jsx|md|mdx)\b", re.IGNORECASE)


def check_text_change(file_path: str, content: str) -> list[str]:
    reasons: list[str] = []
    name = Path(file_path).name.lower()
    if name in PROTECTED_FILES:
        reasons.append(f"Protected SEO file '{name}' requires explicit human approval before editing.")
    if NOINDEX_RE.search(content):
        reasons.append("Detected a 'noindex' directive in written content. Show the diff and get human approval first.")
    if CANONICAL_RE.search(content) and Path(file_path).suffix.lower() in CONTENT_EXTENSIONS:
        reasons.append("Detected a '<link rel=\"canonical\">' modification. Show the diff and get human approval first.")
    if HOWTO_RE.search(content):
        reasons.append("Detected deprecated HowTo JSON-LD schema (discontinued by Google in 2023).")
    return reasons


def check_bash_command(command: str) -> list[str]:
    reasons: list[str] = []
    if re.search(r"robots\.txt", command, re.IGNORECASE) and re.search(r"(>|tee|sed\s+-i|rm\b|mv\b|cp\b)", command):
        reasons.append("Shell command modifies or deletes robots.txt. Show the diff and get human approval first.")
    if RM_PAGE_RE.search(command):
        reasons.append("Shell command deletes a page/content file. Never delete indexable pages without explicit human approval.")
    return reasons


def evaluate_hook_payload(payload: dict[str, Any]) -> list[str]:
    tool = str(payload.get("tool_name", "")).lower()
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return []

    if tool in ("edit", "write", "multiedit"):
        file_path = str(tool_input.get("file_path") or tool_input.get("path") or "")
        content = str(
            tool_input.get("new_string")
            or tool_input.get("content")
            or tool_input.get("replacement")
            or ""
        )
        return check_text_change(file_path, content)
    if tool == "bash":
        return check_bash_command(str(tool_input.get("command") or ""))
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-file", help="Run static Tier-3 SEO guard checks on a file")
    args = parser.parse_args(argv)

    if os.environ.get("SEO_ALLOW_CRITICAL_EDIT") == "1":
        return 0

    if args.check_file:
        path = Path(args.check_file)
        text = path.read_text(encoding="utf-8", errors="replace")
        reasons = check_text_change(str(path), text)
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            return 0
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return 0
        reasons = evaluate_hook_payload(payload)

    if reasons:
        print("SEO GUARDRAIL BLOCKED (Tier 3 - requires human approval):", file=sys.stderr)
        for r in reasons:
            print(f"  - {r}", file=sys.stderr)
        print("Set SEO_ALLOW_CRITICAL_EDIT=1 after the user approves the exact diff.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
