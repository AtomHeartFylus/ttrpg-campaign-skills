"""Scene-local visual ownership and eval coverage; behavior stays in the eval."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/ttrpg-session-visuals/SKILL.md"
EXAMPLE = SKILL.parent / "references/example-session-visuals.md"
EVAL = ROOT / "tests/evals/session-visuals.md"


class SessionVisualsContract(unittest.TestCase):
    def test_release_hygiene_tracks_visuals_eval(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import check_release
        self.assertEqual(check_release.EVAL_BY_SKILL.get("ttrpg-session-visuals"),
                         "tests/evals/session-visuals.md")

    def test_skill_declares_boundaries_and_cue_fields(self):
        text = SKILL.read_text(encoding="utf-8")
        for fragment in ("Session visuals: enabled — use ttrpg-session-visuals after session prep",
                         "E.overrides", "D.shape", "B.safety", "C.player_access", "C.gm_private",
                         "cue id", "show", "change", "stop", "brief only", "provenance",
                         "playback", "blank", "silent", "scene-local", "standalone", "reply only",
                         "preserve", "visual blocks"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), text.lower())
        self.assertNotRegex(text, r"(?m)^type: (?:session-visuals|session-prep)\s*$")
        self.assertNotIn("Never write the prep", text)

    def test_profile_finder_is_identical(self):
        prep = (ROOT / "skills/ttrpg-session-prep/SKILL.md").read_text(encoding="utf-8")
        visual = SKILL.read_text(encoding="utf-8")
        pattern = r"\*\*Find it before declaring it missing\.\*\*.*?already answered\."
        expected = re.search(pattern, prep, re.S)
        actual = re.search(pattern, visual, re.S)
        self.assertIsNotNone(expected)
        self.assertIsNotNone(actual)
        self.assertEqual(expected.group(), actual.group())

    def test_prep_opt_out_check_rejects_inline_visual_cues(self):
        sys.path.insert(0, str(ROOT / "tests"))
        import run_eval
        spec = run_eval.load_eval("session-prep", "A")[0]
        check = next(c for c in spec["mechanical"] if c["id"] == "no-automatic-visuals")
        with tempfile.TemporaryDirectory() as work:
            prep = Path(work) / "prep.md"
            for body, expected in (("# Text-only prep\n", True),
                                   ("# Prep\n**Visual cue V1**\n- Asset: brief only\n", False)):
                prep.write_text(body, encoding="utf-8")
                passed, _ = run_eval.run_check(check, body, work, {}, ["prep.md"], ["prep.md"])
                self.assertEqual(passed, expected)

    def test_compact_example_and_scoped_asset_evidence(self):
        example = EXAMPLE.read_text(encoding="utf-8")
        # The at-table line owns the cue, conditions, brief or link, and fallback.
        line = next((line for line in example.splitlines()
                     if re.search(r"Visual cue V1.*show / change / stop", line, re.I)), "")
        for field in ("show", "change", "stop", "brief only", "blank"):
            with self.subTest(field=field):
                self.assertIn(field, line.lower())
        note = next((line for line in example.splitlines()
                     if "asset note" in line.lower()), "")
        for field in ("V1", "unknown", "inspected", "playback", "not tested"):
            with self.subTest(field=field):
                self.assertIn(field.lower(), note.lower())
        skill = SKILL.read_text(encoding="utf-8").lower()
        for requirement in ("explicitly scoped", "identical", "asset changes"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, skill)

    def test_example_and_eval_have_machine_contract(self):
        example = EXAMPLE.read_text(encoding="utf-8")
        self.assertNotRegex(example, r"(?m)^type: (?:session-visuals|session-prep)\s*$")
        self.assertIn("show / change / stop", example.lower())
        self.assertIn("brief only", example.lower())
        text = EVAL.read_text(encoding="utf-8")
        spec = json.loads(re.search(r"<!-- eval-spec\s*(\{.*?\})\s*-->", text, re.S).group(1))
        self.assertEqual(spec["skill"], "ttrpg-session-visuals")
        self.assertEqual(set(spec["scenarios"]), set("ABCDEF"))
        self.assertEqual(spec["scenarios"]["F"]["artifact"]["type"], "session-prep")
        self.assertEqual(spec["scenarios"]["F"]["setup"], [],
                         "one-off success must not pre-enable a standing agreement")
        self.assertEqual(spec["scenarios"]["A"]["artifact"]["type"], "session-prep")
        self.assertIn("no-new-files", {c["kind"] for c in spec["scenarios"]["A"]["mechanical"]})
        for scenario in ("B", "C", "D", "E"):
            with self.subTest(scenario=scenario):
                kinds = {c["kind"] for c in spec["scenarios"][scenario]["mechanical"]}
                self.assertTrue({"untouched", "no-new-files"}.issubset(kinds),
                                "refusal scenarios must detect both edits and new files")


if __name__ == "__main__":
    unittest.main()
