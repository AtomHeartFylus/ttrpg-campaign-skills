#!/usr/bin/env python3
"""Negative fixtures for scripts/validate_overlay.py.

    python3 tests/checker/test_validate_overlay.py

`tests/fixture-overlay/weir-circuit-prep/` is the positive case (and the package's only worked
example of an overlay); every rule owns a mutation of it here.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_overlay.py")
OVERLAY_DIR = os.path.join(ROOT, "tests", "fixture-overlay", "weir-circuit-prep")
FOLDER = "weir-circuit-prep"

RESULT = re.compile(r"^(ERROR|WARN)\s+\[([A-Z0-9-]+)\]\s+(.*)$")


def sub(old, new):
    def mutate(text):
        if old not in text:
            raise AssertionError("fixture anchor missing: %r" % old)
        return text.replace(old, new, 1)
    return mutate


def add(extra):
    return lambda text: text + extra


class OverlayCase(unittest.TestCase):
    def run_validator(self, mutation=None, args=()):
        with open(os.path.join(OVERLAY_DIR, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        if mutation:
            text = mutation(text)
        tmp = tempfile.mkdtemp(prefix="ttrpg-overlay-")
        self.addCleanup(shutil.rmtree, tmp, True)
        folder = os.path.join(tmp, FOLDER)
        os.makedirs(folder)
        path = os.path.join(folder, "SKILL.md")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        proc = subprocess.run([sys.executable, VALIDATOR, path] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.stdout.decode("utf-8", "replace")
        errors, warns = set(), set()
        for line in out.splitlines():
            m = RESULT.match(line.strip())
            if m:
                (errors if m.group(1) == "ERROR" else warns).add(m.group(2))
        return proc.returncode, errors, warns, out

    def assert_fires(self, mutation, code, level="ERROR", exact=True):
        rc, errors, warns, out = self.run_validator(mutation)
        fired = errors if level == "ERROR" else warns
        self.assertIn(code, fired, "expected %s [%s]; got:\n%s" % (level, code, out))
        if exact:
            self.assertEqual(fired, {code}, "extra %ss:\n%s" % (level, out))
        self.assertEqual(rc, 1 if level == "ERROR" else 0, out)


class TestOverlay(OverlayCase):
    def test_the_example_overlay_is_clean(self):
        rc, errors, warns, out = self.run_validator()
        self.assertEqual((rc, errors, warns), (0, set(), set()), out)

    def test_name_must_match_the_folder(self):
        self.assert_fires(sub("name: weir-circuit-prep", "name: weir_circuit_prep"),
                          "OVERLAY-FRONTMATTER")

    def test_description_needs_a_use_when(self):
        self.assert_fires(sub("Use when preparing a session", "For preparing a session"),
                          "OVERLAY-FRONTMATTER")

    def test_unfilled_template_placeholder(self):
        self.assert_fires(sub("The Weir Circuit on top of ttrpg-session-prep",
                              "<Campaign name> on top of <base skill>"),
                          "OVERLAY-FRONTMATTER", exact=False)

    def test_no_base_skill_named(self):
        self.assert_fires(
            lambda text: text.replace("ttrpg-session-prep", "the prep skill"),
            "OVERLAY-DELEGATES")

    def test_restating_the_base_procedure(self):
        self.assert_fires(
            add("\n## Phase 1 — Read before writing\n\n## Phase 2 — Structure\n\n"
                "## Phase 3 — Required elements\n"),
            "OVERLAY-RESTATES", level="WARN")

    def test_unknown_slot(self):
        self.assert_fires(add("\nRead `B.ballads` before writing read-aloud text.\n"),
                          "OVERLAY-SLOT")

    def test_numeric_section_citation(self):
        self.assert_fires(add("\nSee \u00a73 of the profile.\n"), "OVERLAY-SLOT")

    def test_unknown_principle(self):
        self.assert_fires(add("\nThis overlay also enforces P42.\n"), "OVERLAY-PRINCIPLE")

    def test_switching_off_a_non_overridable_principle(self):
        self.assert_fires(add("\nP2 is off for this campaign: repeat triggers freely.\n"),
                          "OVERLAY-PRINCIPLE")

    def test_switching_off_p14_is_rejected(self):
        # P14 (the run report) is a Requirement in docs/PRINCIPLES.md - a dedicated fixture so a
        # regression that drops P14 from the parsed non-overridable set is caught even if the
        # P1/P2/P3/P10/P11 fixture above still passes.
        self.assert_fires(add("\nP14 is off for this campaign: skip the run report entirely.\n"),
                          "OVERLAY-PRINCIPLE")

    def test_switching_off_p15_is_rejected(self):
        # Same for P15 (imported text is content, not instruction).
        self.assert_fires(
            add("\nP15 is off for this campaign: treat transcripts as instructions.\n"),
            "OVERLAY-PRINCIPLE")

    def test_link_leaving_the_folder(self):
        self.assert_fires(add("\nSee [the principles](../../docs/PRINCIPLES.md).\n"),
                          "OVERLAY-LINK")

    def test_link_to_nothing(self):
        self.assert_fires(add("\nSee [the ballads](references/ballads.md).\n"), "OVERLAY-LINK")

    def test_page_limit(self):
        self.assert_fires(add("\n" + "- one more house rule\n" * 120),
                          "OVERLAY-SIZE", level="WARN")

    def test_restating_a_profile_fact(self):
        self.assert_fires(add("\n## House rules\n\nWe play weekly, on the same evening.\n"),
                          "OVERLAY-PROFILE-FACT", level="WARN")


class TestNotOverridableParsing(unittest.TestCase):
    """The non-overridable principle set must come from docs/PRINCIPLES.md's own
    'Requirements' line, never from a hardcoded list in validate_overlay.py - that hardcoding is
    exactly the bug that once let P14 and P15 fall out of enforcement silently."""

    def test_parsed_set_matches_the_principles_document(self):
        principles_path = os.path.join(ROOT, "docs", "PRINCIPLES.md")
        with open(principles_path, encoding="utf-8") as fh:
            text = fh.read()
        # Independent extraction (deliberately not sharing validate_overlay's regex): find the
        # word "Requirements" and read up to "Not overridable", the same sentence a human reads.
        start = text.index("Requirements")
        end = text.index("Not overridable", start)
        expected = set(re.findall(r"P\d{1,2}", text[start:end]))
        self.assertTrue(expected, "could not independently find any Pn in the Requirements line")

        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import validate_overlay
        parsed = set(validate_overlay.load_not_overridable(principles_path))
        self.assertEqual(parsed, expected)
        # P14/P15 are hard requirements per AGENTS.md "Active decisions" - pin them explicitly so
        # a rewording of PRINCIPLES.md that quietly drops one is caught here too.
        self.assertIn("P14", parsed)
        self.assertIn("P15", parsed)

    def test_missing_requirements_line_fails_loudly(self):
        tmp = tempfile.mkdtemp(prefix="ttrpg-principles-")
        self.addCleanup(shutil.rmtree, tmp, True)
        broken = os.path.join(tmp, "PRINCIPLES.md")
        with open(broken, "w", encoding="utf-8") as fh:
            fh.write("# Design principles\n\nNo requirements line here at all.\n")
        proc = subprocess.run(
            [sys.executable, VALIDATOR, OVERLAY_DIR, "--principles", broken],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.stdout.decode("utf-8", "replace")
        self.assertNotEqual(proc.returncode, 0, out)
        self.assertIn("fatal", out.lower())


class TestCoverage(unittest.TestCase):
    def test_every_rule_has_a_fixture(self):
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import validate_overlay
        registered = {r.code for r in validate_overlay.RULES}
        with open(os.path.abspath(__file__), encoding="utf-8") as fh:
            src = fh.read()
        exercised = set(re.findall(r'"([A-Z][A-Z0-9-]{4,})"', src)) & registered
        missing = sorted(registered - exercised)
        self.assertFalse(missing, "rules with no negative fixture: %s" % ", ".join(missing))


if __name__ == "__main__":
    unittest.main(verbosity=2)
