# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem
[SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-11-07

### Adicionado
- Skills: `kit-sdd`, `kit-change-impact`, `kit-code-review`, `kit-project-bootstrap`,
  `kit-systematic-debugging`, `kit-security-review`, `kit-test-guard`, `kit-system-mapping`,
  `kit-architecture-review`, `kit-contract-first`, `kit-issue-intake`.
- Gates determinísticos: `check_specs.py` (rastreabilidade spec ↔ plano ↔ evidência) e
  `test_guard.py` (testes e cobertura antes/depois).
- Packs de stack para o bootstrap: Flutter, Node.js/TypeScript, Python.
- Empacotamento para Claude Code (`.claude-plugin/`), Codex (`plugin.json`, `.codex-plugin/`,
  `.agents/plugins/`), Gemini CLI/Antigravity (`gemini-extension.json`); GitHub Copilot e Cursor
  via `~/.agents/skills` e `AGENTS.md`.
- Instaladores `install.sh` (macOS/Linux) e `install.ps1` (Windows), com modo remoto, cópia para
  projeto e desinstalação segura.
- Workflow de CI para projetos (`kit-specs`) e CI do próprio kit em Linux, macOS e Windows.
