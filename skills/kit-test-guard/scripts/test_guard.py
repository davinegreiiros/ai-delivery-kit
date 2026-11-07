#!/usr/bin/env python3
"""Compara testes e cobertura antes (baseline) e depois (final) de uma mudança.

Uso:
    python3 test_guard.py baseline --id ABC-123 [--config .kit/quality.json]
    python3 test_guard.py final --id ABC-123 [--config .kit/quality.json]
    python3 test_guard.py final --id ABC-123 --command "pytest --cov"

Códigos de saída: 0 = ok, 1 = gate falhou, 2 = erro de configuração/uso.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_CONFIG = Path(".kit/quality.json")
RESULTS_DIR = Path(".kit/quality")
TAIL_LINES = 40


class ConfigError(Exception):
    pass


def load_config(path: Path, command_override: Optional[str]) -> Dict[str, Any]:
    config: Dict[str, Any] = {}
    if path.exists():
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigError(f"{path} não é JSON válido: {exc}")
    elif not command_override:
        raise ConfigError(f"{path} não encontrado; crie-o ou use --command")
    if command_override:
        config["test_command"] = command_override
    if not config.get("test_command"):
        raise ConfigError("test_command ausente na configuração")
    regex = config.get("coverage_regex")
    if regex:
        try:
            if re.compile(regex).groups != 1:
                raise ConfigError("coverage_regex precisa de exatamente um grupo de captura")
        except re.error as exc:
            raise ConfigError(f"coverage_regex inválida: {exc}")
    return config


def git_commit() -> Optional[str]:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=10
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def parse_coverage(output: str, regex: Optional[str]) -> Optional[float]:
    if not regex:
        return None
    match = re.search(regex, output)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def run_suite(config: Dict[str, Any]) -> Dict[str, Any]:
    command = config["test_command"]
    timeout = config.get("timeout_seconds", 1800)
    started = time.time()
    try:
        # O comando vem da configuração do próprio projeto (fonte confiável), por isso shell=True.
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        exit_code, output = proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        partial = exc.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", "replace")
        output = partial + f"\n[test_guard] tempo esgotado após {timeout}s"
    return {
        "command": command,
        "exit_code": exit_code,
        "passed": exit_code == 0,
        "coverage": parse_coverage(output, config.get("coverage_regex")),
        "coverage_expected": bool(config.get("coverage_regex")),
        "duration_seconds": round(time.time() - started, 2),
        "commit": git_commit(),
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "output_tail": output.splitlines()[-TAIL_LINES:],
    }


def compare(baseline: Optional[Dict[str, Any]], final: Dict[str, Any], tolerance: float) -> List[str]:
    """Retorna a lista de falhas do gate (vazia = aprovado)."""
    failures: List[str] = []
    if not final["passed"]:
        failures.append(f"testes falharam (exit code {final['exit_code']})")
    if final["coverage_expected"] and final["coverage"] is None:
        failures.append("coverage_regex configurada, mas não casou com a saída final")
    if baseline is None:
        failures.append("baseline ausente: rode 'baseline' antes de alterar o código")
        return failures
    before, after = baseline.get("coverage"), final["coverage"]
    if before is not None and after is not None and after < before - tolerance:
        failures.append(
            f"cobertura caiu de {before:.2f}% para {after:.2f}% (tolerância {tolerance:.2f} p.p.)"
        )
    return failures


def result_path(change_id: str, stage: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", change_id)
    return RESULTS_DIR / f"{safe}-{stage}.json"


def print_summary(stage: str, result: Dict[str, Any]) -> None:
    coverage = "n/a" if result["coverage"] is None else f"{result['coverage']:.2f}%"
    status = "PASSOU" if result["passed"] else "FALHOU"
    print(f"[{stage}] testes: {status} | cobertura: {coverage} | {result['duration_seconds']}s")
    if not result["passed"]:
        print("--- últimas linhas da saída ---")
        print("\n".join(result["output_tail"]))


def main(argv: List[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("stage", choices=["baseline", "final"])
    parser.add_argument("--id", required=True, help="ID da mudança (pasta specs/<ID>)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--command", help="sobrescreve test_command da configuração")
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config, args.command)
    except ConfigError as exc:
        print(f"erro de configuração: {exc}", file=sys.stderr)
        return 2

    result = run_suite(config)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = result_path(args.id, args.stage)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print_summary(args.stage, result)
    print(f"resultado salvo em {path}")

    if args.stage == "baseline":
        if not result["passed"]:
            print("aviso: baseline com falhas — registre como pré-existente em tasks.md")
        return 0

    baseline_file = result_path(args.id, "baseline")
    baseline = None
    if baseline_file.exists():
        baseline = json.loads(baseline_file.read_text(encoding="utf-8"))
    failures = compare(baseline, result, float(config.get("coverage_tolerance", 0)))
    if failures:
        for msg in failures:
            print(f"GATE FALHOU: {msg}")
        return 1
    print("GATE OK: testes passando e cobertura sem queda além da tolerância")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
