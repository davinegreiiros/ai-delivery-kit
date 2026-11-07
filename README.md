# ai-delivery-kit

[![ci](https://github.com/davinegreiiros/ai-delivery-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/davinegreiiros/ai-delivery-kit/actions/workflows/ci.yml)
[![licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue.svg)](LICENSE)

Kit de **Spec-Driven Development (SDD)** para agentes de código. Ensina o agente a especificar,
mapear impacto, planejar, testar, depurar, revisar e documentar **antes** de declarar uma tarefa
pronta — com gates humanos nos pontos de decisão e gates automáticos onde dá para medir.

Funciona com **Claude Code, OpenAI Codex, Gemini CLI/Antigravity, GitHub Copilot e Cursor**: as
skills seguem o padrão aberto [Agent Skills](https://agentskills.io) (`SKILL.md`), e cada cliente
recebe seu manifest.

```
pedido ─► spec.md ─(aprovação)─► impact.md ─► plan.md + tasks.md ─(aprovação se risco)─►
          baseline de testes ─► código + testes ─► test guard final ─► check_specs ─► review
```

## Skills

| Skill | Quando o agente usa |
|---|---|
| `kit-sdd` | **Automaticamente** em qualquer mudança de código; orquestra as demais |
| `kit-project-bootstrap` | Preparar um repositório: `AGENTS.md`, pontes por cliente, constituição, `docs/`, `specs/` |
| `kit-issue-intake` | Transformar um issue/card (GitHub, GitLab, Jira, Linear) em rascunho de spec |
| `kit-change-impact` | Mapear o que a mudança afeta antes de planejar |
| `kit-contract-first` | Mudança em API, evento ou schema compartilhado |
| `kit-architecture-review` | Decisão estrutural em aberto → comparação de alternativas + ADR |
| `kit-test-guard` | Testes e cobertura antes/depois; bloqueia queda de cobertura |
| `kit-systematic-debugging` | Bug sem causa conhecida: reproduzir → isolar → hipóteses → correção com teste de regressão |
| `kit-security-review` | Mudanças em auth, dados pessoais, entrada externa, segredos |
| `kit-code-review` | Revisão do diff contra a spec antes do PR |
| `kit-system-mapping` | Documentar um sistema existente (brownfield) em `docs/` |

Packs de stack (Flutter, Node.js/TypeScript, Python) ajudam o bootstrap a preencher comandos e regras.

## Instalação

### Rápida (todos os clientes de uma vez)

Pré-requisito: **Git** instalado. Python 3.9+ só é necessário para os gates automáticos.

**macOS e Linux** (Terminal; no Windows também funciona dentro do WSL):

```bash
curl -fsSL https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.sh | bash
```

**Windows** (PowerShell 5.1 ou 7+, sem precisar de administrador):

```powershell
irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1 | iex
```

O instalador clona o kit em `~/.ai-delivery-kit` (`%USERPROFILE%\.ai-delivery-kit` no Windows) e
cria links (junctions no Windows) em:

| Destino | Lido por |
|---|---|
| `~/.claude/skills` | Claude Code |
| `~/.agents/skills` | Codex, Gemini CLI/Antigravity, GitHub Copilot, Cursor |

### Atualizar, escolher clientes e remover

| Ação | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Atualizar | rode o comando de instalação de novo | rode o comando de instalação de novo |
| Só Claude Code | `curl -fsSL <url>/install.sh \| bash -s -- --client claude` | `& ([scriptblock]::Create((irm <url>/install.ps1))) -Client claude` |
| Só Codex/Gemini/Copilot/Cursor | `curl -fsSL <url>/install.sh \| bash -s -- --client agents` | `& ([scriptblock]::Create((irm <url>/install.ps1))) -Client agents` |
| Remover | `~/.ai-delivery-kit/install.sh --uninstall` | `& ([scriptblock]::Create((irm <url>/install.ps1))) -Uninstall` |

`<url>` = `https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main`. Remover só apaga
os links que apontam para o kit; depois, se quiser, apague a pasta `.ai-delivery-kit`.

Copilot e Cursor também leem `~/.claude/skills`; se usar só eles, instale com `agents` para não ver
as skills duplicadas.

### Por cliente (plugin/extensão nativos)

| Cliente | Comando |
|---|---|
| Claude Code | `/plugin marketplace add davinegreiiros/ai-delivery-kit` e depois `/plugin install ai-delivery-kit@ai-delivery-kit` |
| Codex | `codex plugin marketplace add davinegreiiros/ai-delivery-kit` e instale pelo app/`/plugins` |
| Gemini CLI | `gemini extensions install https://github.com/davinegreiiros/ai-delivery-kit` |
| GitHub Copilot / Cursor | instalador acima (`--client agents`), ou copie para o projeto (abaixo) |

### No projeto (para o time inteiro, sem instalar nada)

macOS / Linux:

```bash
~/.ai-delivery-kit/install.sh --project /caminho/do/projeto
```

Windows:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1))) -Project C:\caminho\do\projeto
```

Copia as skills para `.claude/skills/` e `.agents/skills/` do projeto. Faça commit dessas pastas e
qualquer pessoa que clonar o repositório já terá as skills em todos os clientes.

## Uso

1. Abra o projeto no seu agente e peça:
   > Prepare este repositório para o ai-delivery-kit. Não faça commit.

   Ele cria `AGENTS.md` (lido por Codex, Copilot e Cursor), `CLAUDE.md` e `GEMINI.md` (que importam o
   `AGENTS.md`), `.kit/constitution.md`, `.kit/quality.json`, `docs/` e `specs/`.
2. Revise a constituição e os comandos detectados.
3. Peça mudanças normalmente — o agente segue o fluxo sozinho:
   > Implemente o issue #42.
   > O login está falhando no Android, investigue.
   > Adicione filtro por data na listagem de pedidos.

Mudanças triviais usam o **modo rápido** (só `tasks.md`), sem burocracia.

### Gates automáticos

O agente roda estes scripts sozinho; os comandos abaixo servem para rodar à mão ou no CI.
No Windows, troque `python3` por `python` (ou `py`) e `~/` por `$HOME\`.

```bash
# rastreabilidade: spec aprovada, CA-n com teste no plano e evidência no fim
python3 ~/.ai-delivery-kit/skills/kit-sdd/scripts/check_specs.py --all specs

# testes e cobertura antes/depois (configurado em .kit/quality.json)
python3 ~/.ai-delivery-kit/skills/kit-test-guard/scripts/test_guard.py baseline --id 42
python3 ~/.ai-delivery-kit/skills/kit-test-guard/scripts/test_guard.py final --id 42
```

No GitHub, o bootstrap oferece o workflow `kit-specs`, que roda o `check_specs` em cada PR —
começa informativo e pode virar bloqueante.

## Estrutura do repositório

```
skills/kit-*/            SKILL.md + assets/ references/ scripts/ agents/openai.yaml
.claude-plugin/          manifest e marketplace do Claude Code
plugin.json              manifest portátil (Codex)
.codex-plugin/           manifest legado do Codex
.agents/plugins/         marketplace do Codex
gemini-extension.json    extensão do Gemini CLI (+ GEMINI.md)
install.sh / install.ps1 instaladores
scripts/validate_kit.py  valida skills e manifests
tests/                   testes (unittest, sem dependências)
```

Requisitos: Git; Python 3.9+ para os scripts de gate.

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md). Antes de abrir PR:

```bash
python3 scripts/validate_kit.py && python3 -m unittest discover -s tests -v
```

## Licença

[MIT](LICENSE) © Davi Negreiros
