#!/usr/bin/env python3
"""Negative fixtures for scripts/check_contract.py.

    python tests/checker/test_checker.py          # from the repo root
    python -m unittest discover -s tests/checker  # equivalent

The contract checker is the only mechanical gate this package has, and a regex that
stops matching does not fail loudly: it silently stops checking. Every check therefore
owns at least one fixture here that *breaks the repo on purpose* and asserts the check
fires. `test_every_check_has_a_fixture` fails when a new check lands without one.

A fixture is a MUTATION applied to a throwaway copy of the repo (docs/, templates/,
skills/), not a hand-built mini-repo: mutations stay readable when the real content
changes, and a hand-built repo would drift out of shape within a release.
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
CHECKER = os.path.join(ROOT, "scripts", "check_contract.py")
COPIED = ("docs", "templates", "skills")

SKILL = "skills/%s/SKILL.md"
PREP = SKILL % "ttrpg-session-prep"
LOG = SKILL % "ttrpg-session-log"
AUDIT = SKILL % "ttrpg-continuity-audit"
ARC = SKILL % "ttrpg-campaign-arc"
SETUP = SKILL % "ttrpg-campaign-setup"
PROFILE = "templates/campaign-profile.md"
BUNDLED_PROFILE = "skills/ttrpg-campaign-setup/references/campaign-profile.md"
PRINCIPLES = "docs/PRINCIPLES.md"

RESULT = re.compile(r"^(ERROR|WARN)\s+\[([A-Z0-9-]+)\]\s+(.*)$")


# ---------- mutation helpers (each takes the temp repo root) --------------

def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def write(root, rel, text):
    with open(os.path.join(root, rel), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def append(rel, text):
    def mutate(root):
        write(root, rel, read(root, rel) + text)
    return mutate


def replace(rel, old, new, count=1):
    def mutate(root):
        src = read(root, rel)
        if old not in src:
            raise AssertionError("fixture anchor missing in %s: %r" % (rel, old))
        write(root, rel, src.replace(old, new, count))
    return mutate


def each(*mutations):
    def mutate(root):
        for m in mutations:
            m(root)
    return mutate


def set_principles(text_fn):
    """Rewrite docs/PRINCIPLES.md AND the nine bundled copies, so a principles fixture
    tests what it means to test instead of tripping BUNDLE-IDENTICAL nine times."""
    def mutate(root):
        text = text_fn(read(root, PRINCIPLES))
        write(root, PRINCIPLES, text)
        skills = os.path.join(root, "skills")
        for d in sorted(os.listdir(skills)):
            p = os.path.join(skills, d, "references", "PRINCIPLES.md")
            if os.path.isfile(p):
                with open(p, "w", encoding="utf-8", newline="") as fh:
                    fh.write(text)
    return mutate


def set_profile(text_fn):
    """Same for the schema and its bundled copy in ttrpg-campaign-setup."""
    def mutate(root):
        text = text_fn(read(root, PROFILE))
        write(root, PROFILE, text)
        write(root, BUNDLED_PROFILE, text)
    return mutate


# ---------- the harness ---------------------------------------------------

class CheckerCase(unittest.TestCase):
    """Runs the checker over a mutated copy of the repo and reads its verdict."""

    def run_checker(self, mutation=None, args=()):
        tmp = tempfile.mkdtemp(prefix="ttrpg-checker-")
        self.addCleanup(shutil.rmtree, tmp, True)
        for d in COPIED:
            shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d))
        # BUNDLE-IDENTICAL also compares this canonical source against its bundled copy under
        # skills/, already copied above; scripts/ itself is otherwise out of scope here.
        os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, "scripts", "check_links.py"),
                        os.path.join(tmp, "scripts", "check_links.py"))
        if mutation:
            mutation(tmp)
        proc = subprocess.run(
            [sys.executable, CHECKER, tmp] + list(args),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.stdout.decode("utf-8", "replace")
        errors, warns = set(), set()
        for line in out.splitlines():
            m = RESULT.match(line.strip())
            if m:
                (errors if m.group(1) == "ERROR" else warns).add(m.group(2))
        return proc.returncode, errors, warns, out

    def assert_fires(self, mutation, code, level="ERROR", exact=True, args=()):
        """The mutation makes exactly `code` fire (nothing else, when exact) at `level`."""
        rc, errors, warns, out = self.run_checker(mutation, args)
        fired = errors if level == "ERROR" else warns
        other = warns if level == "ERROR" else errors
        self.assertIn(code, fired, "expected %s [%s]; got:\n%s" % (level, code, out))
        if exact:
            self.assertEqual(fired, {code}, "extra %ss fired:\n%s" % (level, out))
            self.assertFalse(other, "the fixture disturbed another level:\n%s" % out)
        self.assertEqual(rc, 1 if (level == "ERROR" or "--strict" in args) else 0,
                         "unexpected exit code:\n%s" % out)


class TestBaseline(CheckerCase):
    def test_clean_copy_is_green(self):
        rc, errors, warns, out = self.run_checker()
        self.assertEqual((rc, errors, warns), (0, set(), set()), out)

    def test_clean_copy_is_green_under_strict(self):
        rc, _e, _w, out = self.run_checker(args=("--strict",))
        self.assertEqual(rc, 0, out)


class TestSlotsAndPrinciples(CheckerCase):
    def test_slot_resolves(self):
        self.assert_fires(append(PREP, "\nRead `A.bogus_slot` first.\n"), "SLOT-RESOLVES")

    def test_no_legacy_slots(self):
        self.assert_fires(append(PREP, "\nSee \u00a72 of the profile.\n"), "NO-LEGACY-SLOTS")

    def test_dead_slot(self):
        self.assert_fires(
            set_profile(lambda s: s.replace(
                "- **`B.cadence`**",
                "- **`B.unread_slot`** - a slot no skill branches on\n- **`B.cadence`**", 1)),
            "DEAD-SLOT")

    def test_setup_only_slot_is_exempt_from_dead_slot(self):
        rc, errors, _w, out = self.run_checker(set_profile(lambda s: s.replace(
            "- **`B.cadence`**",
            "- **`B.unread_slot`** *(setup-only)* - recorded for the humans\n- **`B.cadence`**",
            1)))
        self.assertEqual((rc, errors), (0, set()), out)

    def test_principle_resolves(self):
        # P99 also breaks the advertised range: this fixture asserts the pair.
        rc, errors, _w, out = self.run_checker(append(PREP, "\nApply P99 throughout.\n"))
        self.assertEqual(errors, {"PRINCIPLE-RESOLVES", "PRINCIPLE-RANGE"}, out)
        self.assertEqual(rc, 1)

    def test_uncited_principle_is_only_a_warning(self):
        # A new principle also breaks every advertised range (that is check 6's job, and
        # test_principle_range_understated owns it): --only isolates the warning here.
        self.assert_fires(
            set_principles(lambda s: s + "\n### P16\n\nA principle nobody cites.\n"),
            "PRINCIPLE-RESOLVES", level="WARN",
            args=("--only", "PRINCIPLE-RESOLVES"))

    def test_principle_range_understated(self):
        self.assert_fires(replace(PREP, "(`P1`\u2026`P15`)", "(`P1`\u2026`P12`)"),
                          "PRINCIPLE-RANGE")


class TestBundles(CheckerCase):
    def test_bundled_schema_drift(self):
        self.assert_fires(append(BUNDLED_PROFILE, "\n<!-- forked -->\n"), "BUNDLE-IDENTICAL")

    def test_bundled_principles_drift(self):
        self.assert_fires(
            append("skills/ttrpg-session-log/references/PRINCIPLES.md", "\n<!-- forked -->\n"),
            "BUNDLE-IDENTICAL")

    def test_bundled_principles_missing(self):
        def mutate(root):
            os.remove(os.path.join(root, "skills/ttrpg-table-recap/references/PRINCIPLES.md"))
        # The entrypoint's link to the deleted file breaks in the same move: both are the
        # point - a missing bundle is a dangling link on the installed copy.
        rc, errors, _w, out = self.run_checker(mutate)
        self.assertEqual(errors, {"BUNDLE-IDENTICAL"}, out)
        self.assertEqual(rc, 1)

    def test_bundled_check_links_drift(self):
        self.assert_fires(
            append("skills/ttrpg-campaign-setup/references/check_links.py",
                   "\n# forked\n"),
            "BUNDLE-IDENTICAL")

    def test_bundled_check_links_missing(self):
        def mutate(root):
            os.remove(os.path.join(
                root, "skills/ttrpg-campaign-setup/references/check_links.py"))
        rc, errors, _w, out = self.run_checker(mutate)
        self.assertEqual(errors, {"BUNDLE-IDENTICAL"}, out)
        self.assertEqual(rc, 1)

    def test_bundled_overlay_template_drift(self):
        self.assert_fires(
            append("skills/ttrpg-campaign-setup/references/overlay-SKILL.md",
                   "\n<!-- forked -->\n"),
            "BUNDLE-IDENTICAL")

    def test_bundled_overlay_template_missing(self):
        def mutate(root):
            os.remove(os.path.join(
                root, "skills/ttrpg-campaign-setup/references/overlay-SKILL.md"))
        rc, errors, _w, out = self.run_checker(mutate)
        self.assertEqual(errors, {"BUNDLE-IDENTICAL"}, out)
        self.assertEqual(rc, 1)


class TestLinks(CheckerCase):
    def test_link_escapes(self):
        self.assert_fires(append(PREP, "\nSee [principles](../../docs/PRINCIPLES.md).\n"),
                          "LINK-ESCAPES")

    def test_link_broken(self):
        self.assert_fires(append(PREP, "\nSee [notes](references/missing.md).\n"),
                          "LINK-BROKEN")

    def test_backtick_reference_broken(self):
        self.assert_fires(append(PREP, "\nHand `references/missing.md` to a sub-agent.\n"),
                          "LINK-BROKEN")


class TestFrontmatter(CheckerCase):
    def test_name_must_equal_folder(self):
        self.assert_fires(replace(PREP, "name: ttrpg-session-prep", "name: ttrpg-prep-session"),
                          "FRONTMATTER")

    def test_description_needs_a_use_when(self):
        self.assert_fires(replace(PREP, "Use when asked to prepare", "Invoke it to prepare"),
                          "FRONTMATTER")

    def test_description_needs_a_sibling_boundary(self):
        self.assert_fires(
            replace(PREP,
                    " Does not record what happened (see ttrpg-session-log), write the opening "
                    "recap (see ttrpg-table-recap), create standalone entity notes (see "
                    "ttrpg-entity-note), or plan the arc above the session (see "
                    "ttrpg-campaign-arc).", ""),
            "FRONTMATTER")

    def test_unknown_sibling_skill(self):
        self.assert_fires(replace(PREP, "see ttrpg-session-log", "see ttrpg-session-ledger"),
                          "FRONTMATTER")

    def test_unexpected_frontmatter_key(self):
        self.assert_fires(replace(PREP, "license: MIT", "license: MIT\nauthor: someone"),
                          "FRONTMATTER")

    def test_description_over_budget(self):
        self.assert_fires(replace(PREP, "license: MIT", "x" * 1100 + "\nlicense: MIT"),
                          "FRONTMATTER")

    def test_unfinished_todo_in_body(self):
        self.assert_fires(append(PREP, "\n[TODO: write the derailment table]\n"), "FRONTMATTER")

    def test_todo_inside_a_fence_is_example_text(self):
        rc, errors, _w, out = self.run_checker(
            append(PREP, "\n```markdown\n[TODO: this is a placeholder in a skeleton]\n```\n"))
        self.assertEqual((rc, errors), (0, set()), out)


class TestOwnership(CheckerCase):
    def test_section_ownership(self):
        self.assert_fires(
            each(append(PREP, "\n## The evening's toll ledger\n"),
                 append(LOG, "\n## The evening's toll ledger\n")),
            "SECTION-OWNERSHIP")

    def test_artifact_type_has_one_owner(self):
        self.assert_fires(
            append(PREP, "\n```markdown\ntype: session-log\n```\n"), "ARTIFACT-CONTRACT")

    def test_skeleton_without_a_type_key(self):
        self.assert_fires(
            append(AUDIT, "\n```markdown\n---\n<frontmatter per C.frontmatter: report tag>\n"
                          "---\n```\n"),
            "ARTIFACT-CONTRACT")

    def test_profile_type_belongs_to_the_schema(self):
        self.assert_fires(
            append(AUDIT, "\n```markdown\ntype: campaign-profile\n```\n"), "ARTIFACT-CONTRACT")


class TestAgnosticism(CheckerCase):
    def test_system_name(self):
        self.assert_fires(append(PREP, "\nWorks best in Pathfinder games.\n"), "NO-SYSTEM-NAMES")

    def test_note_tool_name(self):
        self.assert_fires(append(PREP, "\nOpen the note in Obsidian.\n"), "NO-SYSTEM-NAMES")

    def test_system_name_in_the_schema_is_not_exempt(self):
        self.assert_fires(set_profile(lambda s: s + "\n> e.g. Blades in the Dark\n"),
                          "NO-SYSTEM-NAMES")

    def test_mechanics_leak_is_a_warning(self):
        self.assert_fires(append(PREP, "\nRecord the hit points lost.\n"),
                          "MECHANICS-LEAK", level="WARN")

    def test_strict_promotes_a_warning_to_failure(self):
        rc, _e, warns, out = self.run_checker(
            append(PREP, "\nRecord the hit points lost.\n"), args=("--strict",))
        self.assertIn("MECHANICS-LEAK", warns, out)
        self.assertEqual(rc, 1, "--strict must fail on a warning:\n%s" % out)

    def test_encoding_replacement_character(self):
        # In a SKILL.md this fires FRONTMATTER too (deliberate belt-and-braces); a reference
        # file isolates the check that owns encoding damage everywhere.
        self.assert_fires(
            append("skills/ttrpg-session-prep/references/red-team.md",
                   "\nA damaged \ufffd character.\n"), "ENCODING")

    def test_encoding_damage_in_a_skill_md_also_fails_frontmatter(self):
        rc, errors, _w, out = self.run_checker(append(PREP, "\nA damaged \ufffd character.\n"))
        self.assertEqual(errors, {"ENCODING", "FRONTMATTER"}, out)
        self.assertEqual(rc, 1)

    def test_encoding_literal_escape(self):
        self.assert_fires(append(PREP, "\nA literal \\u00e8 escape.\n"), "ENCODING")


class TestPhase0(CheckerCase):
    def test_override_mapped(self):
        # Deleting the branch also falsifies the phase0 marker that declares it: both checks
        # fire, from opposite directions, which is the belt-and-braces this spine is worth.
        rc, errors, _w, out = self.run_checker(
            replace(ARC, "**`E.overrides` branch \u2014 mandatory.**",
                    "The profile may switch defaults off through `E.overrides`."))
        self.assertEqual(errors, {"OVERRIDE-MAPPED", "PHASE0-PROTOCOL"}, out)
        self.assertEqual(rc, 1)

    def test_missing_phase0_marker(self):
        self.assert_fires(
            replace(PREP, "<!-- phase0: find-profile, d-shape, overrides -->\n", ""),
            "PHASE0-PROTOCOL")

    def test_marker_declares_an_element_it_does_not_implement(self):
        # The rewording is the realistic case: the marker survives, the protocol does not.
        self.assert_fires(
            each(replace(PREP, "**Find it before declaring it missing.**", "**Read the profile.**"),
                 replace(PREP, "search by frontmatter", "look at the frontmatter")),
            "PHASE0-PROTOCOL")

    def test_marker_omits_an_element_the_role_requires(self):
        self.assert_fires(
            replace(PREP, "<!-- phase0: find-profile, d-shape, overrides -->",
                    "<!-- phase0: find-profile, overrides -->"),
            "PHASE0-PROTOCOL")

    def test_marker_declares_an_unknown_element(self):
        self.assert_fires(
            replace(PREP, "<!-- phase0: find-profile, d-shape, overrides -->",
                    "<!-- phase0: find-profile, d-shape, overrides, vibes -->"),
            "PHASE0-PROTOCOL")

    def test_d_shape_branch(self):
        self.assert_fires(
            replace(PREP, "**`D.shape` branch \u2014 mandatory.**",
                    "On `D.shape`, use your judgement."),
            "PHASE0-PROTOCOL")

    def test_setup_keeps_its_own_search_protocol(self):
        self.assert_fires(
            replace(SETUP, "Search before you conclude", "Look around a bit"),
            "PHASE0-PROTOCOL")


class TestBudget(CheckerCase):
    def test_entrypoint_over_budget_warns(self):
        self.assert_fires(append(PREP, "\n" + ("padding for the budget check. " * 200)),
                          "ENTRYPOINT-BUDGET", level="WARN")

    def test_budget_is_reported_in_the_summary(self):
        _rc, _e, _w, out = self.run_checker()
        self.assertIn("entrypoints ~", out)
        self.assertIn("budget", out)


class TestCli(CheckerCase):
    def test_only_runs_one_check(self):
        rc, errors, _w, out = self.run_checker(
            each(append(PREP, "\nRead `A.bogus_slot` first.\n"),
                 append(LOG, "\nWorks best in Pathfinder games.\n")),
            args=("--only", "SLOT-RESOLVES"))
        self.assertEqual(errors, {"SLOT-RESOLVES"}, out)
        self.assertEqual(rc, 1)

    def test_json_output_is_machine_readable(self):
        import json
        rc, _e, _w, out = self.run_checker(
            append(PREP, "\nRead `A.bogus_slot` first.\n"), args=("--format", "json"))
        payload = json.loads(out)
        self.assertEqual(rc, 1)
        self.assertEqual([f["check"] for f in payload["findings"]], ["SLOT-RESOLVES"])
        self.assertEqual(payload["counts"]["errors"], 1)

    def test_list_names_every_check(self):
        proc = subprocess.run([sys.executable, CHECKER, "--list"],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.stdout.decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 0, out)
        self.assertIn("SLOT-RESOLVES", out)
        self.assertIn("PHASE0-PROTOCOL", out)


class TestCoverage(unittest.TestCase):
    """Every registered check owns at least one fixture above. A check that lands without
    one is a check nobody has ever seen fire."""

    def test_every_check_has_a_fixture(self):
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import check_contract
        registered = {c.code for c in check_contract.CHECKS}
        with open(os.path.abspath(__file__), encoding="utf-8") as fh:
            src = fh.read()
        exercised = set(re.findall(r'"([A-Z][A-Z0-9-]{4,})"', src)) & registered
        missing = sorted(registered - exercised)
        self.assertFalse(missing, "checks with no negative fixture: %s" % ", ".join(missing))


if __name__ == "__main__":
    unittest.main(verbosity=2)
