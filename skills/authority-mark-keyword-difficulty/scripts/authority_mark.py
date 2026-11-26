#!/usr/bin/env python3
"""Fetch Ahrefs Domain Rating (free public APIv3) and compute an Authority Mark."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


API_URL = "https://api.ahrefs.com/v3/public/domain-rating-free"
VALID_VERSIONS = ("dr3", "dr4")
DEFAULT_ENV_FILES = (
    Path.home() / ".config" / "ahrefs" / ".env",
    Path.home() / ".env",
)


@dataclass
class DomainRating:
    domain: str
    dr: float | None
    error: str | None = None


def normalize_domain(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    if "://" not in value:
        value = "https://" + value
    parsed = urllib.parse.urlparse(value)
    host = parsed.netloc or parsed.path
    host = host.split("@")[-1].split(":")[0].lower().strip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def resolve_api_key(explicit_key: str | None = None) -> str | None:
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()
    env_key = os.environ.get("AHREFS_API_KEY", "").strip()
    if env_key:
        return env_key
    for env_path in DEFAULT_ENV_FILES:
        if not env_path.is_file():
            continue
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                k, v = stripped.split("=", 1)
                if k.strip() == "AHREFS_API_KEY":
                    val = v.strip().strip('"').strip("'")
                    if val:
                        return val
        except OSError:
            continue
    return None


def find_dr(payload: Any) -> float | None:
    if isinstance(payload, dict):
        for key in ("domain_rating", "domainRating", "dr", "rating"):
            value = payload.get(key)
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                try:
                    return float(value)
                except ValueError:
                    pass
        for value in payload.values():
            found = find_dr(value)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = find_dr(item)
            if found is not None:
                return found
    return None


def find_license(payload: Any) -> str | None:
    if isinstance(payload, dict):
        if isinstance(payload.get("license"), str):
            return payload["license"]
        for value in payload.values():
            found = find_license(value)
            if found:
                return found
    return None


def parse_batch_response(payload: Any) -> tuple[dict[str, DomainRating], str | None]:
    """Parse POST /v3/public/domain-rating-free response into normalized domain map."""
    results: dict[str, DomainRating] = {}
    license_url = find_license(payload)

    container = payload.get("domain_rating") if isinstance(payload, dict) else None
    targets = None
    if isinstance(container, dict) and isinstance(container.get("targets"), list):
        targets = container["targets"]
    elif isinstance(payload, dict) and isinstance(payload.get("targets"), list):
        targets = payload["targets"]
    elif isinstance(payload, list):
        targets = payload

    if not isinstance(targets, list):
        return results, license_url

    for item in targets:
        if not isinstance(item, dict):
            continue
        raw_target = item.get("target") or item.get("domain")
        if not isinstance(raw_target, str) or not raw_target.strip():
            continue
        dom = normalize_domain(raw_target)
        dr = find_dr(item)
        if dr is None:
            results[dom] = DomainRating(domain=dom, dr=None, error="DR field not found")
        else:
            results[dom] = DomainRating(domain=dom, dr=dr)
    return results, license_url


def _auth_headers(api_key: str, *, json_body: bool = False) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "authority-mark-skill/1.1",
    }
    if json_body:
        headers["Content-Type"] = "application/json"
    return headers


def fetch_dr_single(domain: str, api_key: str, version: str, timeout: float) -> tuple[DomainRating, str | None]:
    query = urllib.parse.urlencode({"target": domain, "version": version})
    request = urllib.request.Request(f"{API_URL}?{query}", headers=_auth_headers(api_key))
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return DomainRating(domain=domain, dr=None, error=f"HTTP {exc.code}"), None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return DomainRating(domain=domain, dr=None, error=str(exc)), None

    dr = find_dr(payload)
    license_url = find_license(payload)
    if dr is None:
        return DomainRating(domain=domain, dr=None, error="DR field not found"), license_url
    return DomainRating(domain=domain, dr=dr), license_url


def fetch_dr_batch(
    domains: list[str], api_key: str, version: str, timeout: float
) -> tuple[dict[str, DomainRating], str | None, str | None]:
    unique_domains = list(dict.fromkeys(domains))
    body = json.dumps({"targets": unique_domains, "version": version}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers=_auth_headers(api_key, json_body=True),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {}, None, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {}, None, str(exc)

    parsed, license_url = parse_batch_response(payload)
    if not parsed:
        return {}, license_url, "unexpected batch response shape"
    return parsed, license_url, None


def compare(user_dr: float | None, result_dr: float | None) -> str:
    if user_dr is None or result_dr is None:
        return "unavailable"
    if result_dr < user_dr:
        return "lower"
    if result_dr == user_dr:
        return "equal"
    return "higher"


def build_report(
    user_domain: str,
    serp_domains: list[str],
    ratings: dict[str, DomainRating],
    *,
    version: str,
    license_url: str | None = None,
) -> dict[str, Any]:
    user_rating = ratings.get(user_domain, DomainRating(domain=user_domain, dr=None, error="not returned"))
    rows: list[dict[str, Any]] = []
    authority_mark: dict[str, Any] | None = None

    for idx, domain in enumerate(serp_domains[:10], start=1):
        rating = ratings.get(domain, DomainRating(domain=domain, dr=None, error="not returned"))
        comparison = compare(user_rating.dr, rating.dr)
        row = {
            "rank": idx,
            "domain": domain,
            "dr": rating.dr,
            "error": rating.error,
            "comparison": comparison,
        }
        rows.append(row)
        if authority_mark is None and comparison == "lower":
            authority_mark = row

    return {
        "user_domain": user_domain,
        "user_dr": user_rating.dr,
        "user_error": user_rating.error,
        "dr_version": version,
        "license": license_url or "https://ahrefs.com/legal/domain-rating-license",
        "authority_mark": authority_mark,
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user-domain", required=True, help="Domain being evaluated")
    parser.add_argument(
        "--serp-domain",
        action="append",
        required=True,
        help="Organic SERP domain in rank order. Repeat for each top-10 result.",
    )
    parser.add_argument("--api-key", help="Ahrefs APIv3 Bearer token (or set AHREFS_API_KEY env var)")
    parser.add_argument("--version", choices=VALID_VERSIONS, default="dr3", help="Ahrefs DR version (dr3 or dr4)")
    parser.add_argument("--no-batch", action="store_true", help="Use per-domain GET requests instead of POST batch")
    parser.add_argument("--timeout", type=float, default=15.0, help="HTTP timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args(argv)

    api_key = resolve_api_key(args.api_key)
    if not api_key:
        print(
            "error: missing AHREFS_API_KEY. Ahrefs' /v3/public/domain-rating-free endpoint consumes 0 paid API units "
            "but requires a free Ahrefs APIv3 Bearer token.\n"
            "Generate a token in Ahrefs Account Settings -> API keys, then run:\n"
            "  export AHREFS_API_KEY='your_token_here'\n"
            "Docs: https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free",
            file=sys.stderr,
        )
        return 2

    user_domain = normalize_domain(args.user_domain)
    serp_domains = [normalize_domain(domain) for domain in args.serp_domain]
    all_domains = list(dict.fromkeys([user_domain, *serp_domains[:10]]))

    ratings: dict[str, DomainRating] = {}
    license_url: str | None = None

    if not args.no_batch:
        batch_ratings, batch_license, batch_err = fetch_dr_batch(all_domains, api_key, args.version, args.timeout)
        license_url = batch_license
        if batch_err in ("HTTP 401", "HTTP 403"):
            print(f"error: Ahrefs API rejected AHREFS_API_KEY ({batch_err}). Check your APIv3 token.", file=sys.stderr)
            return 2
        if batch_ratings:
            ratings.update(batch_ratings)

    # Fetch any missing domains individually (or all domains when --no-batch is set)
    for domain in all_domains:
        if domain not in ratings:
            single_rating, single_license = fetch_dr_single(domain, api_key, args.version, args.timeout)
            ratings[domain] = single_rating
            if not license_url and single_license:
                license_url = single_license

    result = build_report(user_domain, serp_domains, ratings, version=args.version, license_url=license_url)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"User domain: {user_domain}")
    print(f"User DR ({args.version}): {result['user_dr'] if result['user_dr'] is not None else 'unavailable'}")
    if result["user_error"]:
        print(f"User DR error: {result['user_error']}")
    print()
    if result["authority_mark"]:
        am = result["authority_mark"]
        print(f"Authority Mark: position {am['rank']} ({am['domain']}, DR {am['dr']})")
    else:
        print("Authority Mark: none in the provided top-10 domains")
    print()
    print("| Rank | Domain | DR | Comparison |")
    print("|---:|---|---:|---|")
    for row in result["rows"]:
        dr = "n/a" if row["dr"] is None else row["dr"]
        detail = row["comparison"] if not row["error"] else f"{row['comparison']} ({row['error']})"
        print(f"| {row['rank']} | {row['domain']} | {dr} | {detail} |")
    print()
    print("Source: Domain Rating by Ahrefs (https://ahrefs.com/)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
