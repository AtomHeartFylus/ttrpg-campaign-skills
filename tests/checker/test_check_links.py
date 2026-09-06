#!/usr/bin/env python3
"""Positive and negative mini-repos for scripts/check_links.py.

    python3 tests/checker/test_check_links.py
    python -m unittest discover -s tests/checker

`check_links.py` is not one of scripts/check_contract.py's registered CHECKS (it validates a
campaign vault, not this package), so it is not subject to `test_every_check_has_a_fixture` -
but a link checker with no fixture of its own is exactly the kind of check this repo's
philosophy warns about, so it gets one here.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRIPT = os.path.join(ROOT, "scripts", "check_links.py")
FIXTURE = os.path.join(ROOT, "tests", "fixture-campaign")


def write(root, rel, text):
    path = os.path.join(root, rel)
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def run(root, fmt="text"):
    args = [sys.executable, SCRIPT, root]
    if fmt == "json":
        args.append("--format=json")
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    return proc.returncode, proc.stdout, proc.stderr


class LinkCheckerCase(unittest.TestCase):
    def mini_repo(self):
        tmp = tempfile.mkdtemp(prefix="ttrpg-links-")
        self.addCleanup(shutil.rmtree, tmp, True)
        return tmp

    # ---------- positive: a small, fully-resolving vault ------------------

    def test_clean_vault_exits_zero(self):
        root = self.mini_repo()
        write(root, "Hub.md", "See [[Entity One]] and [[Entity Two|alias]] and "
                               "[[Entity One#Some Heading]].\n"
                               "Also a relative [markdown link](Entities/Entity Two.md).\n")
        write(root, "Entities/Entity One.md", "# Entity One\n")
        write(root, "Entities/Entity Two.md", "# Entity Two\n")
        code, out, err = run(root)
        self.assertEqual(code, 0, err or out)
        self.assertIn("0 broken", out)

    def test_same_file_heading_link_not_checked(self):
        root = self.mini_repo()
        write(root, "Note.md", "[[#A heading with no other file]]\n")
        code, out, _ = run(root)
        self.assertEqual(code, 0, out)

    def test_wikilink_inside_fenced_code_block_ignored(self):
        root = self.mini_repo()
        write(root, "Note.md", "```\n[[Nonexistent Note]]\n```\n")
        code, out, _ = run(root)
        self.assertEqual(code, 0, out)

    def test_wikilink_inside_inline_code_span_ignored(self):
        root = self.mini_repo()
        write(root, "Note.md", "The syntax is `[[wikilinks]]`, no escaping.\n")
        code, out, _ = run(root)
        self.assertEqual(code, 0, out)

    def test_markdown_link_to_url_not_checked(self):
        root = self.mini_repo()
        write(root, "Note.md", "[external](https://example.invalid/page.md)\n")
        code, out, _ = run(root)
        self.assertEqual(code, 0, out)

    # ---------- negative: each must be caught, exactly ---------------------

    def test_broken_wikilink_reported(self):
        root = self.mini_repo()
        write(root, "Hub.md", "See [[Missing Note]].\n")
        code, out, _ = run(root)
        self.assertEqual(code, 1)
        self.assertIn("1 broken", out)
        self.assertIn("Hub.md:1 -> Missing Note [wikilink]", out)

    def test_broken_wikilink_with_alias_and_heading_reported(self):
        root = self.mini_repo()
        write(root, "Hub.md", "See [[Missing Note#Some Heading|shown text]].\n")
        code, out, _ = run(root)
        self.assertEqual(code, 1)
        self.assertIn("Missing Note [wikilink]", out)

    def test_broken_markdown_link_reported(self):
        root = self.mini_repo()
        write(root, "Hub.md", "[dangling](Entities/Nobody.md)\n")
        code, out, _ = run(root)
        self.assertEqual(code, 1)
        self.assertIn("Hub.md:1 -> Entities/Nobody.md [mdlink]", out)

    def test_json_format_reports_broken_list(self):
        root = self.mini_repo()
        write(root, "Hub.md", "See [[Missing Note]].\n")
        code, out, _ = run(root, fmt="json")
        self.assertEqual(code, 1)
        data = json.loads(out)
        self.assertEqual(data["broken_count"], 1)
        self.assertEqual(data["broken"][0]["target"], "Missing Note")

    def test_exit_code_matches_broken_count(self):
        root = self.mini_repo()
        write(root, "Hub.md", "Clean note, no links.\n")
        code, _out, _err = run(root)
        self.assertEqual(code, 0)


class FixtureCampaignCase(unittest.TestCase):
    """Runs the shipped checker against the real fixture. Never mutated: the fixture is dirty
    on purpose (tests/README.md). check_links.py is stricter than anything that read this vault
    before it, and surfaced two dangling references beyond the originally-seeded [[Eel-Market
    Buyer]] link when it first ran here: a Session 6 prep note and a Bell-Wight stat block,
    neither of which this trimmed, two-session fixture ever included. Both were genuine (not a
    false positive) and are now folded into seeded defect #4 alongside it
    (tests/evals/continuity-audit.md, tests/check_fixture.py) rather than left as unaccounted-for
    noise the continuity-audit eval's answer key did not mention."""

    def test_fixture_reports_the_known_broken_links_and_nothing_else(self):
        code, out, err = run(FIXTURE)
        self.assertEqual(code, 1, err or out)
        self.assertIn("4 broken", out)
        expected_targets = {
            "Eel-Market Buyer",
            "Session 6 — The Long Reach",
            "Bell-Wight — stats",
        }
        found_targets = {line.split(" -> ", 1)[1].rsplit(" [", 1)[0]
                         for line in out.splitlines() if " -> " in line}
        self.assertEqual(found_targets, expected_targets)


if __name__ == "__main__":
    unittest.main()
