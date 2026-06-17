#!/usr/bin/env python3
"""Fetch Ahrefs DR values and compute an Authority Mark from SERP domains."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


API_URL = "https://api.ahrefs.com/v3/public/domain-rating-free"


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


def fetch_dr(domain: str, timeout: float) -> DomainRating:
    query = urllib.parse.urlencode({"target": domain})
    request = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={"Accept": "application/json", "User-Agent": "authority-mark-skill/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return DomainRating(domain=domain, dr=None, error=f"HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return DomainRating(domain=domain, dr=None, error=str(exc))

    dr = find_dr(payload)
    if dr is None:
        return DomainRating(domain=domain, dr=None, error="DR field not found")
    return DomainRating(domain=domain, dr=dr)


def compare(user_dr: float | None, result_dr: float | None) -> str:
    if user_dr is None or result_dr is None:
        return "unavailable"
    if result_dr < user_dr:
        return "lower"
    if result_dr == user_dr:
        return "equal"
    return "higher"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user-domain", required=True, help="Domain being evaluated")
    parser.add_argument(
        "--serp-domain",
        action="append",
        required=True,
        help="Organic SERP domain in rank order. Repeat for each top-10 result.",
    )
    parser.add_argument("--timeout", type=float, default=15.0, help="HTTP timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    user_domain = normalize_domain(args.user_domain)
    serp_domains = [normalize_domain(domain) for domain in args.serp_domain]

    user_rating = fetch_dr(user_domain, args.timeout)
    rows: list[dict[str, Any]] = []
    authority_mark: dict[str, Any] | None = None

    for idx, domain in enumerate(serp_domains[:10], start=1):
        rating = fetch_dr(domain, args.timeout)
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

    result = {
        "user_domain": user_domain,
        "user_dr": user_rating.dr,
        "user_error": user_rating.error,
        "authority_mark": authority_mark,
        "rows": rows,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"User domain: {user_domain}")
    print(f"User DR: {user_rating.dr if user_rating.dr is not None else 'unavailable'}")
    if user_rating.error:
        print(f"User DR error: {user_rating.error}")
    print()
    if authority_mark:
        print(
            "Authority Mark: "
            f"position {authority_mark['rank']} ({authority_mark['domain']}, DR {authority_mark['dr']})"
        )
    else:
        print("Authority Mark: none in the provided top-10 domains")
    print()
    print("| Rank | Domain | DR | Comparison |")
    print("|---:|---|---:|---|")
    for row in rows:
        dr = "n/a" if row["dr"] is None else row["dr"]
        detail = row["comparison"] if not row["error"] else f"{row['comparison']} ({row['error']})"
        print(f"| {row['rank']} | {row['domain']} | {dr} | {detail} |")

    return 0


if __name__ == "__main__":
    sys.exit(main())
