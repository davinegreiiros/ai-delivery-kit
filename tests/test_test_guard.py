import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "kit-test-guard" / "scripts" / "test_guard.py"
sys.path.insert(0, str(SCRIPT.parent))

import test_guard  # noqa: E402


class TestGuardTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cwd = Path(self._tmp.name)
        self.fake = self.cwd / "fake_suite.py"

    def tearDown(self):
        self._tmp.cleanup()

    def suite(self, coverage, exit_code=0):
        """Cria uma 'suíte de testes' falsa que imprime a cobertura e sai com exit_code."""
        self.fake.write_text(
            f"print('TOTAL     120     10    {coverage}%')\nraise SystemExit({exit_code})\n",
            encoding="utf-8",
        )
        command = f'"{sys.executable}" "{self.fake}"'
        config = {"test_command": command, "coverage_regex": r"TOTAL.*?([\d.]+)%", "coverage_tolerance": 0.5}
        (self.cwd / ".kit").mkdir(exist_ok=True)
        (self.cwd / ".kit" / "quality.json").write_text(json.dumps(config), encoding="utf-8")

    def run_guard(self, stage):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), stage, "--id", "ABC-1"],
            cwd=self.cwd, capture_output=True, text=True, encoding="utf-8", env=env,
        )

    def test_passes_when_coverage_stable(self):
        self.suite(80)
        self.assertEqual(self.run_guard("baseline").returncode, 0)
        self.suite(80.2)
        result = self.run_guard("final")
        self.assertEqual(result.returncode, 0, result.stdout)
        saved = json.loads((self.cwd / ".kit" / "quality" / "ABC-1-final.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["coverage"], 80.2)

    def test_fails_when_coverage_drops_beyond_tolerance(self):
        self.suite(80)
        self.run_guard("baseline")
        self.suite(78)
        result = self.run_guard("final")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cobertura caiu", result.stdout)

    def test_tolerance_allows_small_drop(self):
        self.suite(80)
        self.run_guard("baseline")
        self.suite(79.6)
        self.assertEqual(self.run_guard("final").returncode, 0)

    def test_fails_when_tests_fail(self):
        self.suite(80)
        self.run_guard("baseline")
        self.suite(80, exit_code=1)
        result = self.run_guard("final")
        self.assertEqual(result.returncode, 1)
        self.assertIn("testes falharam", result.stdout)

    def test_failing_baseline_only_warns(self):
        self.suite(80, exit_code=1)
        result = self.run_guard("baseline")
        self.assertEqual(result.returncode, 0)
        self.assertIn("pré-existente", result.stdout)

    def test_final_without_baseline_fails(self):
        self.suite(80)
        result = self.run_guard("final")
        self.assertEqual(result.returncode, 1)
        self.assertIn("baseline ausente", result.stdout)

    def test_missing_config_is_usage_error(self):
        result = self.run_guard("baseline")
        self.assertEqual(result.returncode, 2)

    def test_regex_must_have_one_group(self):
        path = self.cwd / "q.json"
        path.write_text(json.dumps({"test_command": "x", "coverage_regex": "TOTAL"}), encoding="utf-8")
        with self.assertRaises(test_guard.ConfigError):
            test_guard.load_config(path, None)

    def test_compare_flags_unmatched_regex(self):
        final = {"passed": True, "exit_code": 0, "coverage": None, "coverage_expected": True}
        failures = test_guard.compare({"coverage": 80.0}, final, 0)
        self.assertTrue(any("não casou" in f for f in failures))


if __name__ == "__main__":
    unittest.main()
