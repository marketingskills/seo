#!/usr/bin/env python3
"""Authenticated RefreshAgent REST helper."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

CONFIG_DIR = Path.home() / ".config" / "refreshagent"
CONFIG_FILE = CONFIG_DIR / ".env"
LOGIN_LOCK_DIR = CONFIG_DIR / ".login.lock"
LOGIN_WAIT_SECONDS = 600
LOGIN_LOCK_STALE_SECONDS = 900
LOGIN_WAIT_POLL_SECONDS = 1.0


def parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected KEY=VALUE")
    key, raw = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("parameter key cannot be empty")
    return key, raw


def build_url(base_url: str, path: str, params: list[tuple[str, str]]) -> str:
    base = base_url.rstrip("/") + "/"
    url = urljoin(base, path.lstrip("/"))
    if params:
        url = f"{url}?{urlencode(params)}"
    return url


def load_body(raw_json: str | None) -> bytes | None:
    if raw_json is None:
        return None
    try:
        parsed: Any = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON body: {exc}") from exc
    return json.dumps(parsed, separators=(",", ":")).encode("utf-8")


def load_config_api_key() -> str | None:
    if not CONFIG_FILE.exists():
        return None
    try:
        for line in CONFIG_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            if key.strip() == "REFRESHAGENT_API_KEY":
                return value.strip().strip('"').strip("'") or None
    except OSError:
        return None
    return None


def save_config_api_key(api_key: str, base_url: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        "\n".join(
            [
                f'REFRESHAGENT_API_KEY="{api_key}"',
                f'REFRESHAGENT_BASE_URL="{base_url.rstrip("/")}"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    try:
        CONFIG_FILE.chmod(0o600)
    except OSError:
        pass


def acquire_login_lock() -> bool:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            LOGIN_LOCK_DIR.mkdir()
            (LOGIN_LOCK_DIR / "pid").write_text(str(os.getpid()), encoding="utf-8")
            return True
        except FileExistsError:
            try:
                age = time.time() - LOGIN_LOCK_DIR.stat().st_mtime
            except OSError:
                age = 0
            if age > LOGIN_LOCK_STALE_SECONDS:
                release_login_lock()
                continue
            return False


def release_login_lock() -> None:
    try:
        (LOGIN_LOCK_DIR / "pid").unlink(missing_ok=True)
        LOGIN_LOCK_DIR.rmdir()
    except OSError:
        pass


def wait_for_login_owner() -> str | None:
    deadline = time.monotonic() + LOGIN_WAIT_SECONDS
    print(
        "Another RefreshAgent login is already in progress. Waiting for it to finish...",
        file=sys.stderr,
    )
    while time.monotonic() < deadline:
        api_key = load_config_api_key()
        if api_key:
            return api_key
        if not LOGIN_LOCK_DIR.exists():
            return load_config_api_key()
        time.sleep(LOGIN_WAIT_POLL_SECONDS)
    return None


class CliCallbackHandler(BaseHTTPRequestHandler):
    server_version = "RefreshAgentCliAuth/1.0"

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)
        expected_state = getattr(self.server, "expected_state", "")  # type: ignore[attr-defined]
        state = (params.get("state") or [""])[0]
        if expected_state and not secrets.compare_digest(state, expected_state):
            self.send_error(400, "Invalid login callback state")
            return

        api_key = (params.get("key") or [""])[0].strip()
        base_url = (params.get("base_url") or ["https://refreshagent.com"])[0]
        if not api_key:
            self.send_error(400, "Missing RefreshAgent key")
            return
        if any(char in api_key for char in "\r\n\t "):
            self.send_error(400, "Invalid RefreshAgent key")
            return

        self.server.api_key = api_key  # type: ignore[attr-defined]
        self.server.base_url = base_url  # type: ignore[attr-defined]
        body = (
            "<!doctype html><meta charset='utf-8'>"
            "<title>RefreshAgent connected</title>"
            "<style>body{font-family:system-ui,sans-serif;max-width:680px;margin:12vh auto;"
            "line-height:1.5;color:#17211c}code{background:#f3f4f6;padding:.2rem .4rem;"
            "border-radius:4px}</style>"
            "<h1>RefreshAgent is connected.</h1>"
            "<p>Your secure key was saved locally. You can close this tab and return to Claude Code.</p>"
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        threading.Thread(target=self.server.shutdown, daemon=True).start()


def run_cli_login(base_url: str) -> str:
    existing_key = load_config_api_key()
    if existing_key:
        return existing_key

    owns_login = acquire_login_lock()
    if not owns_login:
        api_key = wait_for_login_owner()
        if api_key:
            return api_key
        raise SystemExit(
            "Timed out waiting for the active RefreshAgent login. "
            "Close stale browser login tabs and rerun one RefreshAgent command."
        )

    try:
        existing_key = load_config_api_key()
        if existing_key:
            return existing_key

        try:
            server = ThreadingHTTPServer(("127.0.0.1", 0), CliCallbackHandler)
        except PermissionError as exc:
            raise SystemExit(
                "RefreshAgent login needs to listen on 127.0.0.1 for the OAuth callback, "
                "but this agent sandbox blocked local socket binding. Rerun the command with "
                "local network/socket permission approved, or run it once in a normal terminal "
                f"to create {CONFIG_FILE}."
            ) from exc

        server.api_key = ""  # type: ignore[attr-defined]
        server.base_url = base_url  # type: ignore[attr-defined]
        server.expected_state = secrets.token_urlsafe(24)  # type: ignore[attr-defined]
        callback_url = (
            f"http://127.0.0.1:{server.server_port}/callback"
            f"?state={server.expected_state}"  # type: ignore[attr-defined]
        )
        auth_url = build_url(base_url, "/auth/cli", [("callback", callback_url)])

        print("RefreshAgent needs Google access before it can query SEO data.", file=sys.stderr)
        print(f"Opening login page: {auth_url}", file=sys.stderr)
        print(
            "Only one login window is needed. After Google sign-in, this command will save "
            "the key and continue.",
            file=sys.stderr,
        )
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass

        deadline = time.monotonic() + LOGIN_WAIT_SECONDS
        while time.monotonic() < deadline and not getattr(server, "api_key", ""):
            server.timeout = min(10, max(1, int(deadline - time.monotonic())))
            server.handle_request()

        api_key = getattr(server, "api_key", "")
        returned_base_url = getattr(server, "base_url", base_url)
        server.server_close()

        if not api_key:
            raise SystemExit(
                "Login timed out before the localhost callback completed. "
                "Close stale RefreshAgent login tabs, rerun one command, and complete the "
                "new browser tab within 10 minutes."
            )

        save_config_api_key(api_key, returned_base_url)
        print(f"Saved RefreshAgent key to {CONFIG_FILE}", file=sys.stderr)
        return api_key
    finally:
        release_login_lock()


def main() -> int:
    parser = argparse.ArgumentParser(description="Call RefreshAgent API endpoints.")
    parser.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    parser.add_argument("path", help="API path, e.g. /api/v1/sc/sites")
    parser.add_argument("--param", action="append", default=[], type=parse_key_value, help="Query parameter as KEY=VALUE")
    parser.add_argument("--json", dest="json_body", help="JSON request body for POST/PUT/PATCH")
    parser.add_argument("--base-url", default=os.environ.get("REFRESHAGENT_BASE_URL", "https://refreshagent.com"))
    parser.add_argument("--api-key", default=os.environ.get("REFRESHAGENT_API_KEY") or load_config_api_key())
    parser.add_argument("--login", action="store_true", help="Start browser login and save the RefreshAgent key locally.")
    args = parser.parse_args()

    if args.login or not args.api_key:
        args.api_key = run_cli_login(args.base_url)

    body = load_body(args.json_body)
    url = build_url(args.base_url, args.path, args.param)
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 RefreshAgentSkill/1.0",
        "X-API-Key": args.api_key,
    }
    if body is not None:
        headers["Content-Type"] = "application/json"

    request = Request(url, data=body, headers=headers, method=args.method)

    try:
        with urlopen(request, timeout=60) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        error_payload = exc.read().decode("utf-8", errors="replace")
        if exc.code == 402:
            try:
                parsed_error = json.loads(error_payload)
            except json.JSONDecodeError:
                parsed_error = {}
            message = parsed_error.get("error") or "Free Google data request limit reached."
            upgrade_url = parsed_error.get("upgrade_url")
            print(message, file=sys.stderr)
            if upgrade_url:
                print(f"Upgrade to Live Data: {upgrade_url}", file=sys.stderr)
            return 1
        print(f"HTTP {exc.code} {exc.reason}: {error_payload}", file=sys.stderr)
        return 1
    except URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        return 1

    try:
        print(json.dumps(json.loads(payload), indent=2, sort_keys=True))
    except json.JSONDecodeError:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
