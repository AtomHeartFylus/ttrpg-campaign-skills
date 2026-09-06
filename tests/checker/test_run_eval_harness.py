#!/usr/bin/env python3
"""Synthetic test of tests/run_eval.py's own detection mechanism.

    python3 tests/checker/test_run_eval_harness.py
    python -m unittest discover -s tests/checker

Not an eval - a test of the HARNESS that grades evals. Builds a minimal pristine snapshot by
hand, then writes, modifies and deletes files under it, and asserts that:

  * `find_artifacts()` reports the deletion (pristine minus current snapshot) as `deleted`,
    separately from `changed` (new-or-modified) - the gap this file exists to close: a run that
    silently deletes a pristine file used to be invisible to the harness entirely.
  * the `untouched` and `no-new-files` mechanical check kinds both FAIL when a pristine file is
    deleted, proving the box a rubric actually ticks goes red on a deletion, not just that a
    Python list happens to contain a filename.
  * an `allow`/`allow_new` pattern can excuse a genuinely NEW file, but can NEVER excuse the
    deletion of a pristine one - even when the deleted file's name happens to match the pattern.
    A deletion is not a creation wearing the deleted file's old name; the two must never be
    confused by a regex that only meant to whitelist output.
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
TESTS = os.path.join(ROOT, "tests")
sys.path.insert(0, TESTS)
import run_eval  # noqa: E402


class HarnessDeletionCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ttrpg-run-eval-harness-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.dest = os.path.join(self.tmp, "work")
        os.makedirs(self.dest)
        self.write("A.md", "# A\noriginal\n")
        self.write("B.md", "# B\nkeep me\n")
        self.state = {"pristine": run_eval.snapshot(self.dest)}
        self.spec = {}  # no artifact.type wanted -> find_artifacts falls back to `changed`

    def write(self, rel, text):
        path = os.path.join(self.dest, rel)
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)

    # ---------- find_artifacts sees the deletion ----------

    def test_deleted_pristine_file_is_reported_separately_from_changed(self):
        os.remove(os.path.join(self.dest, "B.md"))
        self.write("C.md", "# C\nnew file\n")  # a created file, to prove it does NOT get
                                                 # mislabeled as a deletion or vice versa
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        self.assertEqual(deleted, ["B.md"])
        self.assertEqual(changed, ["C.md"])
        self.assertNotIn("B.md", changed)

    def test_modification_alone_is_changed_not_deleted(self):
        self.write("A.md", "# A\nedited\n")
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        self.assertEqual(changed, ["A.md"])
        self.assertEqual(deleted, [])

    def test_untouched_nothing_modified_or_deleted_passes(self):
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check({"kind": "untouched"}, "", self.dest, self.state,
                                        changed, artifacts, deleted)
        self.assertTrue(ok, detail)

    # ---------- the mechanical box actually goes red ----------

    def test_untouched_fails_when_a_pristine_file_is_deleted(self):
        os.remove(os.path.join(self.dest, "B.md"))
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check({"kind": "untouched"}, "", self.dest, self.state,
                                        changed, artifacts, deleted)
        self.assertFalse(ok, "the 'untouched' box must fail when a pristine file is deleted")
        self.assertIn("B.md", detail)

    def test_no_new_files_fails_when_a_pristine_file_is_deleted(self):
        os.remove(os.path.join(self.dest, "B.md"))
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check({"kind": "no-new-files"}, "", self.dest, self.state,
                                        changed, artifacts, deleted)
        self.assertFalse(ok, "the 'no-new-files' box must fail when a pristine file is deleted")
        self.assertIn("B.md", detail)

    def test_no_new_files_still_fails_on_a_plain_creation(self):
        # Regression guard: the deletion fix must not have weakened the pre-existing behaviour.
        self.write("C.md", "new\n")
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check({"kind": "no-new-files"}, "", self.dest, self.state,
                                        changed, artifacts, deleted)
        self.assertFalse(ok, detail)
        self.assertIn("C.md", detail)

    def test_allow_new_pattern_does_not_excuse_the_deletion_untouched(self):
        # Regression for the residual defect: `allow_new` is documented as excusing a
        # genuinely NEW file by name, never the deletion of a pre-existing one. A deletion
        # whose old filename happens to match the pattern must still fail the box.
        os.remove(os.path.join(self.dest, "B.md"))
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check({"kind": "untouched", "allow_new": [r"^B\.md$"]}, "",
                                        self.dest, self.state, changed, artifacts, deleted)
        self.assertFalse(ok, "a deletion must never be excused by an allow_new pattern")
        self.assertIn("B.md", detail)

    def test_allow_pattern_does_not_excuse_the_deletion_no_new_files(self):
        # Same regression, for the sibling check kind and its `allow` key.
        os.remove(os.path.join(self.dest, "B.md"))
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check({"kind": "no-new-files", "allow": [r"^B\.md$"]}, "",
                                        self.dest, self.state, changed, artifacts, deleted)
        self.assertFalse(ok, "a deletion must never be excused by an allow pattern")
        self.assertIn("B.md", detail)

    def test_allow_new_pattern_still_excuses_a_genuinely_new_file_untouched(self):
        # Guard against overcorrecting: allow_new must still do its documented job for an
        # actually NEW file (e.g. a report the skill is expected to write).
        self.write("AUDIT-report.md", "new report\n")
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check(
            {"kind": "untouched", "allow_new": [r".*[Rr]eport.*"]}, "",
            self.dest, self.state, changed, artifacts, deleted)
        self.assertTrue(ok, detail)

    def test_allow_pattern_still_excuses_a_genuinely_new_file_no_new_files(self):
        self.write("AUDIT-report.md", "new report\n")
        changed, artifacts, deleted = run_eval.find_artifacts(self.dest, self.state, self.spec)
        ok, detail = run_eval.run_check(
            {"kind": "no-new-files", "allow": [r".*[Rr]eport.*"]}, "",
            self.dest, self.state, changed, artifacts, deleted)
        self.assertTrue(ok, detail)


class HarnessCliCase(unittest.TestCase):
    def test_list_prints_runnable_scenario_syntax(self):
        runner = os.path.join(TESTS, "run_eval.py")
        proc = subprocess.run([sys.executable, runner, "--list"],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("campaign-setup --scenario B", proc.stdout)
        self.assertNotRegex(proc.stdout, r"^campaign-setup-B\\s", re.M)


if __name__ == "__main__":
    unittest.main(verbosity=2)
