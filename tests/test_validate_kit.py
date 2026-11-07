import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_kit  # noqa: E402


class ValidateKitTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self):
        self._tmp.cleanup()

    def skill_md(self, name):
        return self.root / "skills" / name / "SKILL.md"

    def test_real_kit_is_valid(self):
        self.assertEqual(validate_kit.validate(ROOT), [])

    def test_name_must_match_folder(self):
        path = self.skill_md("kit-sdd")
        path.write_text(path.read_text(encoding="utf-8").replace("name: kit-sdd", "name: outro"), encoding="utf-8")
        errors = validate_kit.validate(self.root)
        self.assertTrue(any("difere do nome da pasta" in e for e in errors))

    def test_missing_reference_is_reported(self):
        (self.root / "skills" / "kit-sdd" / "assets" / "plan.md").unlink()
        errors = validate_kit.validate(self.root)
        self.assertTrue(any("assets/plan.md" in e for e in errors))

    def test_cross_skill_reference_resolves(self):
        # kit-issue-intake cita assets/spec.md da skill kit-sdd na mesma linha.
        errors = [e for e in validate_kit.validate(self.root) if e.startswith("kit-issue-intake")]
        self.assertEqual(errors, [])

    def test_version_drift_is_reported(self):
        path = self.root / "gemini-extension.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = "9.9.9"
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = validate_kit.validate(self.root)
        self.assertTrue(any("versões divergentes" in e for e in errors))

    def test_missing_frontmatter(self):
        self.skill_md("kit-code-review").write_text("# sem frontmatter\n", encoding="utf-8")
        errors = validate_kit.validate(self.root)
        self.assertTrue(any("frontmatter" in e for e in errors))

    def test_description_too_long(self):
        path = self.skill_md("kit-code-review")
        text = path.read_text(encoding="utf-8")
        start = text.index("description:")
        end = text.index("\n", start)
        path.write_text(text[:start] + "description: " + "x" * 1100 + text[end:], encoding="utf-8")
        errors = validate_kit.validate(self.root)
        self.assertTrue(any("máx. 1024" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
