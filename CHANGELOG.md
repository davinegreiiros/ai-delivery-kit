# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem
[SemVer](https://semver.org/lang/pt-BR/).

## [1.0.1] - 2026-11-07

### Corrigido
- `install.ps1`: o BOM UTF-8 quebrava `irm | iex` ("Unexpected attribute 'CmdletBinding'");
  o script agora é ASCII puro e o `validate_kit.py` impede a regressão.
- Antigravity (app e CLI) não lia `~/.agents/skills`: os instaladores agora também criam links em
  `~/.gemini/config/skills` (`--client antigravity`; incluído em `all`).
- Marketplace do Codex usa a origem `url` documentada para plugin na raiz do repositório.
- CI: Python 3.9 testado no Ubuntu 24.04 (o 26.04 não tem build 3.9); actions atualizadas para v7.

### Alterado
- README: comandos completos e copiáveis por sistema (macOS/Linux e Windows), status da versão,
  resultado esperado, desenvolvimento local e princípios de adoção.
- CI executa os comandos do README como estão escritos, inclusive pelas URLs reais.

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
