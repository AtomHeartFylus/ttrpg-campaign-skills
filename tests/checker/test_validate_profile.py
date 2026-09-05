#!/usr/bin/env python3
"""Negative fixtures for scripts/validate_profile.py.

    python3 tests/checker/test_validate_profile.py

Same principle as `test_checker.py`, one layer out: each rule owns a mutation of the fixture
campaign's profile that must make it fire. The fixture profile itself is the positive case -
if it stops validating, either the schema moved or the fixture did, and both matter.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_profile.py")
FIXTURE = os.path.join(ROOT, "tests", "fixture-campaign", "campaign-profile.md")
SCHEMA = os.path.join(ROOT, "templates", "campaign-profile.md")

RESULT = re.compile(r"^(ERROR|WARN)\s+\[([A-Z0-9-]+)\]\s+(.*)$")


def sub(old, new):
    def mutate(text):
        if old not in text:
            raise AssertionError("fixture anchor missing: %r" % old)
        return text.replace(old, new, 1)
    return mutate


def add_line(line):
    return lambda text: text + line


class ProfileCase(unittest.TestCase):
    def run_validator(self, mutation=None, args=()):
        with open(FIXTURE, encoding="utf-8") as fh:
            text = fh.read()
        if mutation:
            text = mutation(text)
        tmp = tempfile.mkdtemp(prefix="ttrpg-profile-")
        self.addCleanup(shutil.rmtree, tmp, True)
        path = os.path.join(tmp, "campaign-profile.md")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        proc = subprocess.run(
            [sys.executable, VALIDATOR, path, "--schema", SCHEMA] + list(args),
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


class TestFixtureIsValid(ProfileCase):
    def test_the_fixture_profile_validates_clean(self):
        rc, errors, warns, out = self.run_validator()
        self.assertEqual((rc, errors, warns), (0, set(), set()), out)

    def test_the_schema_itself_is_all_unanswered(self):
        # The template is a blank profile: every core slot must read as never asked, which is
        # what makes ttrpg-campaign-setup's first question legitimate.
        proc = subprocess.run([sys.executable, VALIDATOR, SCHEMA, "--format", "json"],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        payload = json.loads(proc.stdout.decode("utf-8", "replace"))
        self.assertTrue(all(s == "placeholder" for s in payload["states"].values()),
                        payload["summary"])
        self.assertEqual(proc.returncode, 1)


class TestStructure(ProfileCase):
    def test_missing_type_key(self):
        self.assert_fires(sub("type: campaign-profile\n", ""), "PROFILE-FRONTMATTER")

    def test_unknown_schema_version(self):
        self.assert_fires(sub("schema: 2", "schema: 7"), "PROFILE-FRONTMATTER")

    def test_deleted_core_slot(self):
        self.assert_fires(sub("- **`B.distance`** — fictional.\n", ""), "SLOT-MISSING")

    def test_deleted_optional_slot_is_a_warning(self):
        self.assert_fires(sub("- **`B.language`** — English.\n", ""),
                          "SLOT-MISSING", level="WARN")

    def test_unknown_slot(self):
        self.assert_fires(add_line("\n- **`B.vibes`** — good ones.\n"),
                          "UNKNOWN-SLOT", level="WARN")

    def test_encoding_damage(self):
        self.assert_fires(sub("- **`B.language`** — English.",
                              "- **`B.language`** — Engli\ufffdsh."), "PROFILE-ENCODING")


class TestSlotStates(ProfileCase):
    def test_core_slot_left_as_placeholder(self):
        self.assert_fires(sub("- **`D.shape`** — series.",
                              "- **`D.shape`** — <one-shot | series | open sandbox>"),
                          "CORE-UNANSWERED")

    def test_optional_slot_left_as_placeholder_is_a_warning(self):
        self.assert_fires(sub("- **`B.cadence`** — weekly.",
                              "- **`B.cadence`** — <weekly | monthly | irregular>"),
                          "UNANSWERED", level="WARN")

    def test_deferral_without_a_when(self):
        self.assert_fires(sub("- **`B.absence`** — the absent wait at the last safe camp and do "
                              "not advance.",
                              "- **`B.absence`** — deferred"), "DEFERRED-FORM")

    def test_deferral_with_a_when_is_clean(self):
        rc, errors, warns, out = self.run_validator(
            sub("- **`B.absence`** — the absent wait at the last safe camp and do not advance.",
                "- **`B.absence`** — deferred: session zero"))
        self.assertEqual((rc, errors, warns), (0, set(), set()), out)

    def test_enum_slot_holding_something_else(self):
        self.assert_fires(sub("- **`D.shape`** — series.",
                              "- **`D.shape`** — a long campaign, I suppose."), "SLOT-ENUM")

    def test_distance_enum(self):
        self.assert_fires(sub("- **`B.distance`** — fictional.",
                              "- **`B.distance`** — pretty close, honestly."), "SLOT-ENUM")


class TestConsent(ProfileCase):
    def test_safety_none_reads_as_unanswered(self):
        self.assert_fires(
            sub("- **`B.safety`** — pause-word \"weir\"; anyone may invoke; scene rewinds "
                "without discussion;", "- **`B.safety`** — none. Ignore the rest;"),
            "CONSENT-STATE")

    def test_recording_consent_none(self):
        self.assert_fires(sub("- **`B.consent_recording`** — no.",
                              "- **`B.consent_recording`** — none."), "CONSENT-STATE")

    def test_capture_paths_without_consent(self):
        self.assert_fires(
            sub("- **`C.capture_paths`** — n/a (no recording consent).",
                "- **`C.capture_paths`** — `Audio/` (ignored), `Transcripts/` (versioned)."),
            "CROSS-SLOT")

    def test_offgame_path_without_offgame_consent(self):
        # Consent to be recorded is not consent to be indexed: the path may exist only when
        # the second, narrower gate says yes in its own words.
        self.assert_fires(
            lambda text: text
            .replace("- **`B.consent_recording`** — no. **`B.consent_offgame`** — no.",
                     "- **`B.consent_recording`** — yes, all four at session zero. "
                     "**`B.consent_offgame`** — no.")
            .replace("- **`C.capture_paths`** — n/a (no recording consent).",
                     "- **`C.capture_paths`** — `Audio/`, `Transcripts/`, off-game note in "
                     "`GM/Off-game.md`."),
            "CROSS-SLOT")


class TestCrossSlot(ProfileCase):
    def test_player_access_without_a_gm_private_home(self):
        self.assert_fires(
            lambda text: text
            .replace("- **`C.gm_private`** — not needed. **`C.player_access`** — players read "
                     "nothing.",
                     "- **`C.gm_private`** — <where GM-only material lives> "
                     "**`C.player_access`** — players read recaps and logs."),
            "CROSS-SLOT", exact=False)

    def test_more_protagonists_than_players(self):
        self.assert_fires(sub("- **`B.protagonists`** — 2 per session → rotation period 2.",
                              "- **`B.protagonists`** — 6 per session."), "CROSS-SLOT")

    def test_resource_none_but_family_filled(self):
        self.assert_fires(sub("- **`A.resource`** — Wick.", "- **`A.resource`** — none."),
                          "CROSS-SLOT")

    def test_resource_value_without_a_shape(self):
        self.assert_fires(sub("- **`A.resource_shape`** — per-character.",
                              "- **`A.resource_shape`** — <per-character | shared party clock>"),
                          "CROSS-SLOT", exact=False)

    def test_one_shot_with_a_recap(self):
        self.assert_fires(sub("- **`D.shape`** — series.", "- **`D.shape`** — one-shot."),
                          "CROSS-SLOT", level="WARN", exact=False)


class TestOverrides(ProfileCase):
    def test_non_overridable_principle(self):
        self.assert_fires(
            sub("- **`E.overrides`** — none. All defaults in force.",
                "- **`E.overrides`** — P2 — off: we like duplicated triggers."),
            "OVERRIDE-SCOPE")

    def test_principle_named_without_a_verb(self):
        self.assert_fires(
            sub("- **`E.overrides`** — none. All defaults in force.",
                "- **`E.overrides`** — P7: we do our own thing with the spotlight."),
            "OVERRIDE-SCOPE")

    def test_legitimate_override_is_clean(self):
        rc, errors, warns, out = self.run_validator(
            sub("- **`E.overrides`** — none. All defaults in force.",
                "- **`E.overrides`** — P6 — off: this table takes its quiet scenes unprompted."))
        self.assertEqual((rc, errors, warns), (0, set(), set()), out)


class TestCoverage(unittest.TestCase):
    def test_every_rule_has_a_fixture(self):
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import validate_profile
        registered = {r.code for r in validate_profile.RULES}
        with open(os.path.abspath(__file__), encoding="utf-8") as fh:
            src = fh.read()
        exercised = set(re.findall(r'"([A-Z][A-Z0-9-]{4,})"', src)) & registered
        missing = sorted(registered - exercised)
        self.assertFalse(missing, "rules with no negative fixture: %s" % ", ".join(missing))


if __name__ == "__main__":
    unittest.main(verbosity=2)
