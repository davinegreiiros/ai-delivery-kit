# ai-delivery-kit

[![ci](https://github.com/davinegreiiros/ai-delivery-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/davinegreiiros/ai-delivery-kit/actions/workflows/ci.yml)
[![licença: MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue.svg)](LICENSE)

> **Status:** versão 1.0.1 · licença MIT · Claude Code, Codex, Gemini CLI, Antigravity, GitHub Copilot e Cursor

Kit de **Spec-Driven Development (SDD)** para agentes de código. Ensina o agente a especificar,
mapear impacto, planejar, testar, depurar, revisar e documentar **antes** de declarar uma tarefa
pronta — com gates humanos nos pontos de decisão e gates automáticos onde dá para medir.

As skills seguem o padrão aberto [Agent Skills](https://agentskills.io) (`SKILL.md`), então as
mesmas instruções funcionam em todos os clientes; muda só onde cada um procura as skills.

```
pedido ─► spec.md ─(aprovação)─► impact.md ─► plan.md + tasks.md ─(aprovação se risco)─►
          baseline de testes ─► código + testes ─► test guard final ─► check_specs ─► review
```

## Resultado esperado

Depois de adotar o kit, cada repositório tem:

- `AGENTS.md` — contrato curto para humanos e agentes (com `CLAUDE.md` e `GEMINI.md` apontando para ele);
- `.kit/constitution.md` — regras inegociáveis do projeto;
- `docs/` — o sistema como ele é hoje, com decisões em `docs/adr/`;
- `specs/<ID>/` — spec, impacto, plano, tarefas e evidências de cada mudança;
- código, testes e documentação atualizados no mesmo PR.

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

Pré-requisito: **Git**. Python 3.9+ só é necessário para os gates automáticos.

O instalador clona o kit em `~/.ai-delivery-kit` (`%USERPROFILE%\.ai-delivery-kit` no Windows) e
cria links para as skills em:

| Cliente (`--client`) | Destino | Lido por |
|---|---|---|
| `claude` | `~/.claude/skills` | Claude Code |
| `agents` | `~/.agents/skills` | Codex, Gemini CLI, GitHub Copilot, Cursor |
| `antigravity` | `~/.gemini/config/skills` | Antigravity (app e CLI) |

Sem `--client`, instala para todos (`all`).

### macOS e Linux

No Terminal (no Windows, também vale dentro do WSL).

**Instalar ou atualizar** (todos os clientes):

```bash
curl -fsSL https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.sh | bash
```

**Só um cliente** — troque `claude` por `agents` ou `antigravity`:

```bash
curl -fsSL https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.sh | bash -s -- --client claude
```

**Remover:**

```bash
~/.ai-delivery-kit/install.sh --uninstall
```

### Windows

No PowerShell 5.1 ou 7+, sem precisar de administrador.

**Instalar ou atualizar** (todos os clientes):

```powershell
irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1 | iex
```

**Só um cliente** — troque `claude` por `agents` ou `antigravity`:

```powershell
$kit = irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1
& ([scriptblock]::Create($kit)) -Client claude
```

**Remover:**

```powershell
$kit = irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1
& ([scriptblock]::Create($kit)) -Uninstall
```

### Observações

- **Atualizar** = rodar de novo **o mesmo** comando usado na instalação (o padrão instala para todos).
- **Remover** só apaga os links que apontam para o kit; depois, se quiser, apague a pasta `.ai-delivery-kit`.
- Copilot e Cursor também leem `~/.claude/skills`. Se usar só eles, instale com `agents` para não
  ver as skills duplicadas.

### Alternativa: plugin nativo do cliente

Use **ou** o instalador **ou** o plugin no mesmo cliente — os dois juntos duplicam as skills.

| Cliente | Como instalar |
|---|---|
| Claude Code | `/plugin marketplace add davinegreiiros/ai-delivery-kit` e depois `/plugin install ai-delivery-kit@ai-delivery-kit` |
| Codex | `codex plugin marketplace add davinegreiiros/ai-delivery-kit`; depois abra o `codex`, digite `/plugins` e instale |
| Gemini CLI | `gemini extensions install https://github.com/davinegreiiros/ai-delivery-kit` |
| Antigravity, Copilot, Cursor | use o instalador acima |

### No projeto (para o time inteiro)

Depois de instalar, copie as skills para dentro de um projeto e faça commit delas: quem clonar o
repositório já terá as skills em todos os clientes, sem instalar nada. As cópias vão para
`.claude/skills/` (Claude Code) e `.agents/skills/` (demais clientes, incluindo o Antigravity).

macOS / Linux:

```bash
~/.ai-delivery-kit/install.sh --project /caminho/do/projeto
```

Windows:

```powershell
$kit = irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1
& ([scriptblock]::Create($kit)) -Project C:\caminho\do\projeto
```

### Desenvolvimento local do kit

Para editar as skills e ver o efeito na hora, instale a partir de um clone: os links passam a
apontar para ele. Se já tiver instalado pelo comando remoto, remova antes (`--uninstall`).

```bash
git clone https://github.com/davinegreiiros/ai-delivery-kit.git
cd ai-delivery-kit
./install.sh
```

No Windows, dentro do clone: `powershell -ExecutionPolicy Bypass -File .\install.ps1`.

## Uso

1. Abra o projeto no seu agente e peça:

   > Prepare este repositório para o ai-delivery-kit. Não faça commit.

   Ele cria `AGENTS.md` (lido por Codex, Copilot e Cursor), `CLAUDE.md` e `GEMINI.md` (que
   importam o `AGENTS.md`), `.kit/constitution.md`, `.kit/quality.json`, `docs/` e `specs/`.
2. Revise a constituição e os comandos detectados.
3. Peça mudanças normalmente — o agente segue o fluxo sozinho. Exemplos:
   - "Implemente o issue #42."
   - "O login está falhando no Android, investigue."
   - "Adicione filtro por data na listagem de pedidos."

Mudanças triviais usam o **modo rápido** (só `tasks.md`), sem burocracia.

### Gates automáticos

O agente roda estes scripts sozinho; os comandos abaixo servem para rodar à mão ou no CI. Os
caminhos valem para a instalação pelo instalador; com plugin nativo, os scripts ficam na pasta de
plugins do cliente. No Windows, troque `python3` por `python` (ou `py`) e `~/` por `$HOME\`.

```bash
# rastreabilidade: spec aprovada, CA-n com teste no plano e evidência no fim
python3 ~/.ai-delivery-kit/skills/kit-sdd/scripts/check_specs.py --all specs

# testes e cobertura antes/depois (configurado em .kit/quality.json)
python3 ~/.ai-delivery-kit/skills/kit-test-guard/scripts/test_guard.py baseline --id 42
python3 ~/.ai-delivery-kit/skills/kit-test-guard/scripts/test_guard.py final --id 42
```

No GitHub, o bootstrap oferece o workflow `kit-specs`, que roda o `check_specs` em cada PR —
começa informativo e pode virar bloqueante.

## Princípios de adoção

1. **Comece informativo.** Torne um gate bloqueante só depois de ver que ele não gera falsos positivos.
2. **Preserve o que existe.** Documentação correta é auditada e completada, não reescrita.
3. **Código, spec e docs no mesmo PR** quando o comportamento muda.
4. **Proporcional ao risco.** Mudança trivial usa o modo rápido; risco alto exige plano aprovado.
5. **Evidência acima de opinião.** Achados e docs citam arquivo e símbolo, não só número de linha.

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
