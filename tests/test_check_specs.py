import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "kit-sdd" / "scripts"))

import check_specs  # noqa: E402

SPEC_OK = """# Spec — X
Status: APROVADA

## Critérios de aceite
- CA-1: algo
- CA-2: outra coisa

## Perguntas abertas
- (nenhuma)
"""

PLAN_OK = """# Plano
## Estratégia de testes
| CA-1 | t1 | unit |
| CA-2 | t2 | unit |
"""

TASKS_DONE = """# Tarefas
- [x] T1 (CA-1)
- [x] T2 (CA-2)

## Evidências
| Critério | Evidência |
|---|---|
| CA-1 | test_a passou |
| CA-2 | test_b passou |
"""


class CheckSpecsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "ABC-1"
        self.dir.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        (self.dir / name).write_text(text, encoding="utf-8")

    def test_complete_spec_passes(self):
        self.write("spec.md", SPEC_OK)
        self.write("plan.md", PLAN_OK)
        self.write("tasks.md", TASKS_DONE)
        self.assertEqual(check_specs.check(self.dir), ([], []))

    def test_fast_mode_only_tasks_is_warning(self):
        self.write("tasks.md", "- [x] corrigir typo\n")
        errors, warnings = check_specs.check(self.dir)
        self.assertEqual(errors, [])
        self.assertTrue(any("modo rápido" in w for w in warnings))

    def test_done_task_requires_approved_spec(self):
        self.write("spec.md", SPEC_OK.replace("APROVADA", "RASCUNHO"))
        self.write("tasks.md", "- [x] T1 (CA-1)\n")
        errors, _ = check_specs.check(self.dir)
        self.assertTrue(any("RASCUNHO" in e for e in errors))

    def test_approved_spec_with_open_question_fails(self):
        self.write("spec.md", SPEC_OK.replace("- (nenhuma)", "- Qual o limite?"))
        errors, _ = check_specs.check(self.dir)
        self.assertTrue(any("perguntas abertas" in e for e in errors))

    def test_criterion_missing_from_plan_fails(self):
        self.write("spec.md", SPEC_OK)
        self.write("plan.md", "| CA-1 | t1 | unit |\n")
        errors, _ = check_specs.check(self.dir)
        self.assertTrue(any("CA-2" in e and "plan.md" in e for e in errors))

    def test_finished_tasks_need_evidence(self):
        self.write("spec.md", SPEC_OK)
        self.write("plan.md", PLAN_OK)
        self.write("tasks.md", TASKS_DONE.replace("test_b passou", ""))
        errors, _ = check_specs.check(self.dir)
        self.assertTrue(any("evidência" in e and "CA-2" in e for e in errors))

    def test_missing_spec_with_plan_is_error(self):
        self.write("plan.md", PLAN_OK)
        errors, _ = check_specs.check(self.dir)
        self.assertIn("spec.md ausente", errors)

    def test_cli_exit_codes(self):
        script = ROOT / "skills" / "kit-sdd" / "scripts" / "check_specs.py"
        self.write("spec.md", SPEC_OK)
        self.write("plan.md", PLAN_OK)
        ok = subprocess.run([sys.executable, str(script), str(self.dir)], capture_output=True)
        self.assertEqual(ok.returncode, 0, ok.stdout)
        self.write("spec.md", "sem status\n")
        bad = subprocess.run(
            [sys.executable, str(script), "--all", str(self.dir.parent)], capture_output=True
        )
        self.assertEqual(bad.returncode, 1)


if __name__ == "__main__":
    unittest.main()
