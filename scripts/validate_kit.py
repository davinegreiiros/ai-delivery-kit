#!/usr/bin/env python3
"""Valida a estrutura do ai-delivery-kit antes de publicar.

Verifica:
- cada skills/<nome>/SKILL.md segue o padrão Agent Skills (frontmatter name/description,
  name igual ao nome da pasta, limites de tamanho);
- arquivos citados como assets/, references/ ou scripts/ existem;
- cada skill tem agents/openai.yaml (metadados de UI do Codex);
- manifests de Claude Code, Codex e Gemini têm o mesmo nome e versão;
- o CHANGELOG.md tem uma entrada e o README.md mostra a versão atual;
- install.ps1 é ASCII puro, sem BOM (o `irm | iex` quebra com BOM e o PowerShell 5.1
  lê arquivos sem BOM como ANSI).

Uso: python3 scripts/validate_kit.py [raiz-do-kit]
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"(?<![\w/<>.-])((?:assets|references|scripts)/[\w./-]+\.\w+)")
SKILL_MENTION_RE = re.compile(r"\bkit-[a-z0-9-]+\b")
MAX_NAME, MAX_DESCRIPTION = 64, 1024

MANIFESTS = [
    ("plugin.json", ("name",), ("version",)),
    (".claude-plugin/plugin.json", ("name",), ("version",)),
    (".codex-plugin/plugin.json", ("name",), ("version",)),
    ("gemini-extension.json", ("name",), ("version",)),
    (".claude-plugin/marketplace.json", ("plugins", 0, "name"), ("plugins", 0, "version")),
]


def parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data: Dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_skill(skill_dir: Path, skills_root: Path) -> List[str]:
    errors: List[str] = []
    label = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{label}: SKILL.md ausente"]
    text = skill_md.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    if meta is None:
        return [f"{label}: frontmatter YAML ausente ou malformado"]

    name, description = meta.get("name", ""), meta.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{label}: name '{name}' difere do nome da pasta")
    if not NAME_RE.match(name) or len(name) > MAX_NAME:
        errors.append(f"{label}: name deve ter até {MAX_NAME} caracteres [a-z0-9-]")
    if not description:
        errors.append(f"{label}: description ausente")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{label}: description com {len(description)} caracteres (máx. {MAX_DESCRIPTION})")

    for line in text.splitlines():
        for ref in REF_RE.findall(line):
            candidates = [skill_dir] + [
                skills_root / other for other in SKILL_MENTION_RE.findall(line)
            ]
            if not any((base / ref).exists() for base in candidates):
                errors.append(f"{label}: referência inexistente '{ref}'")

    if not (skill_dir / "agents" / "openai.yaml").exists():
        errors.append(f"{label}: agents/openai.yaml ausente")
    for json_file in skill_dir.rglob("*.json"):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: JSON inválido em {json_file.relative_to(skill_dir)}: {exc}")
    return errors


def dig(data, path: Tuple) -> Optional[str]:
    for key in path:
        try:
            data = data[key]
        except (KeyError, IndexError, TypeError):
            return None
    return data


def check_manifests(root: Path) -> Tuple[List[str], Optional[str]]:
    errors: List[str] = []
    seen: Dict[str, Tuple[str, str]] = {}
    for rel, name_path, version_path in MANIFESTS:
        path = root / rel
        if not path.exists():
            errors.append(f"manifest ausente: {rel}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: JSON inválido: {exc}")
            continue
        seen[rel] = (dig(data, name_path), dig(data, version_path))
    names = {v[0] for v in seen.values()}
    versions = {v[1] for v in seen.values()}
    if len(names) > 1:
        errors.append(f"nomes divergentes entre manifests: {seen}")
    if len(versions) > 1:
        errors.append(f"versões divergentes entre manifests: {seen}")
    version = versions.pop() if len(versions) == 1 else None
    return errors, version


def validate(root: Path) -> List[str]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return ["pasta skills/ ausente"]
    errors: List[str] = []
    skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append("nenhuma skill encontrada")
    for skill_dir in skill_dirs:
        errors.extend(check_skill(skill_dir, skills_root))

    installer = root / "install.ps1"
    if installer.exists():
        raw = installer.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append("install.ps1 começa com BOM: 'irm | iex' falha no Windows")
        elif any(b > 127 for b in raw):
            errors.append("install.ps1 tem caracteres não ASCII (use texto sem acentos)")

    manifest_errors, version = check_manifests(root)
    errors.extend(manifest_errors)
    readme = root / "README.md"
    if version and readme.exists() and f"versão {version}" not in readme.read_text(encoding="utf-8"):
        errors.append(f"README.md sem a linha de status 'versão {version}'")
    changelog = root / "CHANGELOG.md"
    if version and changelog.exists():
        if f"[{version}]" not in changelog.read_text(encoding="utf-8"):
            errors.append(f"CHANGELOG.md sem entrada para [{version}]")
    elif version:
        errors.append("CHANGELOG.md ausente")
    return errors


def main(argv: List[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    root = Path(argv[0]) if argv else Path(__file__).resolve().parents[1]
    errors = validate(root)
    for msg in errors:
        print(f"erro: {msg}")
    skills = len([p for p in (root / "skills").glob("*/SKILL.md")]) if (root / "skills").is_dir() else 0
    print(f"{'FALHOU' if errors else 'OK'}: {skills} skills verificadas, {len(errors)} erro(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
