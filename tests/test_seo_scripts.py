"""Unit tests for deterministic SEO foundation, snapshot diff, and hook guard scripts."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/site-foundation-audit/scripts"))
sys.path.insert(0, str(ROOT / "skills/seo-change-monitor/scripts"))
sys.path.insert(0, str(ROOT / "skills/authority-mark-keyword-difficulty/scripts"))
sys.path.insert(0, str(ROOT / "hooks"))

import site_foundation_check as sfc  # noqa: E402
import seo_snapshot as snap  # noqa: E402
import authority_mark as am  # noqa: E402
import seo_guard as guard  # noqa: E402


class SiteFoundationTests(unittest.TestCase):
    def test_robots_distinguishes_search_bots_from_training_bots(self) -> None:
        robots = """
# BEGIN Cloudflare Managed content
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: *
Allow: /
Sitemap: https://example.com/sitemap.xml
"""
        parsed = sfc.parse_robots_txt(robots)
        self.assertTrue(parsed["cloudflare_managed_block"])
        self.assertFalse(parsed["search_bots"]["OAI-SearchBot"]["blocked"])
        self.assertFalse(parsed["search_bots"]["Bingbot"]["blocked"])
        self.assertTrue(parsed["training_bots"]["GPTBot"]["blocked"])
        self.assertTrue(parsed["training_bots"]["ClaudeBot"]["blocked"])
        self.assertEqual(parsed["sitemaps"], ["https://example.com/sitemap.xml"])

    def test_robots_catches_blocked_oai_searchbot(self) -> None:
        robots = "User-agent: OAI-SearchBot\nDisallow: /\n"
        parsed = sfc.parse_robots_txt(robots)
        self.assertTrue(parsed["search_bots"]["OAI-SearchBot"]["blocked"])

    def test_html_parser_and_deprecated_schema_checks(self) -> None:
        html = """
        <html><head>
          <title>Example Product</title>
          <link rel="canonical" href="https://example.com/">
          <script type="application/ld+json">{"@context":"https://schema.org","@type":"HowTo","name":"Old"}</script>
          <script type="application/ld+json">{"@context":"https://schema.org","@type":"Product","aggregateRating":{"@type":"AggregateRating"}}</script>
        </head><body><h1>Main Heading</h1><p>This is real server rendered body copy.</p></body></html>
        """
        sig = sfc.parse_html_signals(html)
        self.assertEqual(sig["title"], "Example Product")
        self.assertEqual(sig["h1"], "Main Heading")
        self.assertEqual(sig["canonicals"], ["https://example.com/"])
        self.assertIn("HowTo", sig["schema_types"])

        findings = {f["check"]: f["status"] for f in sfc.audit_schema_types(sig["schema_types"], sig["schema_errors"])}
        self.assertEqual(findings["deprecated_howto"], "FAIL")
        self.assertEqual(findings["review_stars_verify"], "WARN")


class SeoSnapshotDiffTests(unittest.TestCase):
    def test_catches_four_silent_deploy_killers(self) -> None:
        baseline = {
            "origin": "https://example.com",
            "robots_txt": {"status": 200, "sha256": "aaa", "blocked_search_bots": []},
            "pages": {
                "https://example.com/": {
                    "status": 200,
                    "final_url": "https://example.com/",
                    "title": "Home",
                    "h1": "Home",
                    "canonical": "https://example.com/",
                    "noindex": False,
                    "meta_robots": [],
                    "x_robots_tag": "",
                    "schema_types": ["Organization"],
                },
                "https://example.com/pricing": {
                    "status": 200,
                    "final_url": "https://example.com/pricing",
                    "title": "Pricing",
                    "h1": "Pricing",
                    "canonical": "https://example.com/pricing",
                    "noindex": False,
                    "meta_robots": [],
                    "x_robots_tag": "",
                    "schema_types": ["Product"],
                },
            },
        }
        current = {
            "origin": "https://example.com",
            "robots_txt": {"status": 200, "sha256": "bbb", "blocked_search_bots": ["OAI-SearchBot"]},
            "pages": {
                "https://example.com/": {
                    "status": 200,
                    "final_url": "https://example.com/",
                    "title": "Home",
                    "h1": "Home",
                    "canonical": "https://staging.example.com/",
                    "noindex": True,
                    "meta_robots": ["robots=noindex"],
                    "x_robots_tag": "",
                    "schema_types": [],
                },
                "https://example.com/pricing": {
                    "status": 404,
                    "final_url": "https://example.com/pricing",
                    "title": "",
                    "h1": "",
                    "canonical": None,
                    "noindex": False,
                    "meta_robots": [],
                    "x_robots_tag": "",
                    "schema_types": [],
                },
            },
        }
        diff = snap.diff_snapshots(baseline, current)
        self.assertFalse(diff["passed"])
        types = {item["type"] for item in diff["critical"]}
        self.assertIn("robots_blocked_search_bots", types)
        self.assertIn("became_noindex", types)
        self.assertIn("canonical_changed", types)
        self.assertIn("status_regression", types)


class SeoGuardHookTests(unittest.TestCase):
    def test_blocks_robots_noindex_canonical_delete_and_howto(self) -> None:
        self.assertTrue(guard.evaluate_hook_payload({"tool_name": "Edit", "tool_input": {"file_path": "public/robots.txt", "new_string": "Disallow: /"}}))
        self.assertTrue(guard.evaluate_hook_payload({"tool_name": "Write", "tool_input": {"file_path": "pages/index.html", "content": '<meta name="robots" content="noindex">'}}))
        self.assertTrue(guard.evaluate_hook_payload({"tool_name": "Edit", "tool_input": {"file_path": "pages/index.html", "new_string": '<link rel="canonical" href="https://other.com/">'}}))
        self.assertTrue(guard.evaluate_hook_payload({"tool_name": "Write", "tool_input": {"file_path": "schema.json", "content": '{"@type": "HowTo"}'}}))
        self.assertTrue(guard.evaluate_hook_payload({"tool_name": "Bash", "tool_input": {"command": "rm templates/pricing.html"}}))

    def test_allows_normal_draft_edits(self) -> None:
        self.assertEqual(
            guard.evaluate_hook_payload({"tool_name": "Write", "tool_input": {"file_path": "drafts/post.md", "content": "# Helpful guide"}}),
            [],
        )


class AuthorityMarkTests(unittest.TestCase):
    def test_parse_batch_post_response_and_compute_authority_mark(self) -> None:
        payload = {
            "domain_rating": {
                "license": "https://ahrefs.com/legal/domain-rating-license",
                "targets": [
                    {"target": "mysite.com", "domain_rating": 34.0},
                    {"target": "bigsite.com", "domain_rating": 78.0},
                    {"target": "smallblog.com", "domain_rating": 21.0},
                ],
            }
        }
        ratings, license_url = am.parse_batch_response(payload)
        self.assertEqual(license_url, "https://ahrefs.com/legal/domain-rating-license")
        self.assertEqual(ratings["mysite.com"].dr, 34.0)
        self.assertEqual(ratings["smallblog.com"].dr, 21.0)

        report = am.build_report("mysite.com", ["bigsite.com", "smallblog.com"], ratings, version="dr3", license_url=license_url)
        self.assertEqual(report["authority_mark"]["rank"], 2)
        self.assertEqual(report["authority_mark"]["domain"], "smallblog.com")
        self.assertEqual(report["rows"][0]["comparison"], "higher")
        self.assertEqual(report["rows"][1]["comparison"], "lower")

    def test_single_get_response_parsing(self) -> None:
        payload = {"domain_rating": {"domain_rating": 92.0, "license": "http://ahrefs.com/legal/domain-rating-license"}}
        self.assertEqual(am.find_dr(payload), 92.0)
        self.assertEqual(am.find_license(payload), "http://ahrefs.com/legal/domain-rating-license")

    def test_missing_api_key_exits_cleanly(self) -> None:
        old = os.environ.pop("AHREFS_API_KEY", None)
        old_files = am.DEFAULT_ENV_FILES
        am.DEFAULT_ENV_FILES = ()
        try:
            code = am.main(["--user-domain", "mysite.com", "--serp-domain", "rank1.com"])
            self.assertEqual(code, 2)
        finally:
            am.DEFAULT_ENV_FILES = old_files
            if old is not None:
                os.environ["AHREFS_API_KEY"] = old


if __name__ == "__main__":
    unittest.main()
