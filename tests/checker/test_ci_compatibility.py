"""Guard the contract job's supported Python/runner combinations without a YAML dependency."""

import re
import unittest
from pathlib import Path


class CICompatibilityTests(unittest.TestCase):
    def test_contract_runner_matrix(self):
        workflow = (Path(__file__).resolve().parents[2] / ".github/workflows/ci.yml").read_text(
            encoding="utf-8"
        )
        # This intentionally parses the contract job's current inline mapping format only.
        job = re.search(r"(?ms)^  contract:\s*\n(.*?)(?=^  [\w-]+:|\Z)", workflow)
        self.assertIsNotNone(job, "contract job missing")
        rows = re.findall(
            r'^\s*-\s*\{\s*os:\s*([\w.-]+),\s*python:\s*["\']([\d.]+)["\']\s*\}\s*$',
            job.group(1),
            re.MULTILINE,
        )
        self.assertEqual(
            [os for os, version in rows if os.startswith("ubuntu-") and version == "3.9"],
            ["ubuntu-24.04"],
            "Python 3.9 must use the supported Ubuntu runner, not a floating image",
        )
        for row in (
            ("ubuntu-latest", "3.11"),
            ("ubuntu-latest", "3.13"),
            ("macos-latest", "3.13"),
            ("windows-latest", "3.13"),
        ):
            with self.subTest(row=row):
                self.assertIn(row, rows)


if __name__ == "__main__":
    unittest.main()
