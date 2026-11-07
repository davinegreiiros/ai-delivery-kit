#!/usr/bin/env python3
"""Valida a rastreabilidade de uma ou mais pastas specs/<ID>/.

Uso:
    python3 check_specs.py specs/ABC-123 [specs/ABC-124 ...]
    python3 check_specs.py --all specs

Regras:
- Modo rápido: pasta com somente tasks.md é aceita.
- spec.md precisa de "Status:" e de pelo menos um critério CA-n.
- Tarefa marcada [x] exige spec com Status APROVADA.
- Spec APROVADA não pode ter perguntas abertas.
- Com plan.md, cada CA-n da spec deve aparecer no plano.
- Com todas as tarefas concluídas, cada CA-n deve ter evidência preenchida em tasks.md.

Sai com código 1 se houver erro; avisos não falham.
"""
import argparse
import re
import sys
from pathlib import Path
from typing import List, Set, Tuple

CA_RE = re.compile(r"\bCA-\d+\b")
STATUS_RE = re.compile(r"^Status:\s*(\S+)", re.MULTILINE)
TASK_RE = re.compile(r"^\s*-\s*\[( |x|X)\]", re.MULTILINE)
EMPTY_QUESTION = {"", "(nenhuma)", "nenhuma", "-"}


def section(text: str, title: str) -> str:
    """Conteúdo de uma seção '## título' até a próxima seção '## '."""
    match = re.search(
        r"^##\s+" + re.escape(title) + r"\s*$(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1) if match else ""


def open_questions(spec: str) -> List[str]:
    items = []
    for line in section(spec, "Perguntas abertas").splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        content = line.lstrip("-").strip()
        if content.lower() not in EMPTY_QUESTION:
            items.append(content)
    return items


def evidenced_criteria(tasks: str) -> Set[str]:
    """CA-n com a segunda coluna preenchida na tabela de evidências."""
    found = set()
    for line in section(tasks, "Evidências").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and CA_RE.fullmatch(cells[0]) and cells[1]:
            found.add(cells[0])
    return found


def check(spec_dir: Path) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    spec_file, plan_file, tasks_file = (spec_dir / n for n in ("spec.md", "plan.md", "tasks.md"))

    if not spec_dir.is_dir():
        return [f"pasta não encontrada: {spec_dir}"], []

    tasks = tasks_file.read_text(encoding="utf-8") if tasks_file.exists() else ""
    marks = TASK_RE.findall(tasks)
    done = sum(1 for m in marks if m.lower() == "x")

    if not spec_file.exists():
        if tasks_file.exists() and not plan_file.exists():
            warnings.append("modo rápido: só tasks.md (confirme que a mudança é trivial)")
        else:
            errors.append("spec.md ausente")
        return errors, warnings

    spec = spec_file.read_text(encoding="utf-8")
    status_match = STATUS_RE.search(spec)
    status = status_match.group(1).upper() if status_match else ""
    criteria = sorted(set(CA_RE.findall(section(spec, "Critérios de aceite"))))

    if not status:
        errors.append("spec.md sem linha 'Status:'")
    if not criteria:
        errors.append("spec.md sem critérios de aceite CA-n")

    questions = open_questions(spec)
    if status == "APROVADA" and questions:
        errors.append(f"spec APROVADA com perguntas abertas: {questions}")
    if done and status != "APROVADA":
        errors.append(f"{done} tarefa(s) concluída(s) com spec em status '{status or '?'}'")

    if plan_file.exists():
        plan = plan_file.read_text(encoding="utf-8")
        missing = [c for c in criteria if c not in plan]
        if missing:
            errors.append(f"critérios sem estratégia de teste no plan.md: {missing}")
    elif status == "APROVADA":
        warnings.append("spec aprovada sem plan.md")

    if not tasks_file.exists():
        if status == "APROVADA":
            warnings.append("tasks.md ainda não criado")
    elif marks and done == len(marks):
        missing = [c for c in criteria if c not in evidenced_criteria(tasks)]
        if missing:
            errors.append(f"todas as tarefas concluídas, mas sem evidência para: {missing}")
    elif marks:
        warnings.append(f"{len(marks) - done} de {len(marks)} tarefa(s) pendente(s)")

    return errors, warnings


def main(argv: List[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--all", action="store_true", help="trata cada caminho como pasta specs/")
    args = parser.parse_args(argv)

    dirs: List[Path] = []
    for path in args.paths:
        dirs.extend(sorted(p for p in path.iterdir() if p.is_dir()) if args.all else [path])

    failed = False
    for spec_dir in dirs:
        errors, warnings = check(spec_dir)
        label = "ERRO" if errors else "OK"
        print(f"[{label}] {spec_dir}")
        for msg in errors:
            print(f"  erro: {msg}")
        for msg in warnings:
            print(f"  aviso: {msg}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
