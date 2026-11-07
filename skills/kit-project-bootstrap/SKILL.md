---
name: kit-project-bootstrap
description: Prepara um repositório para usar o ai-delivery-kit com qualquer agente (Claude Code, Codex, Gemini, Copilot, Cursor) - cria AGENTS.md, arquivos-ponte por cliente, constituição, config de testes, docs/ e specs/. Use quando pedirem "prepare este repositório para o kit" ou "configure SDD neste projeto". Não implementa features.
---

# Bootstrap de projeto

Prepara a estrutura **sem alterar código da aplicação** e **sem sobrescrever** o que já existe.
Caminhos `assets/` e `references/` são relativos à pasta desta skill.

## 1. Verificar o estado

- `git status --short`: com mudanças não commitadas, avise e pergunte se continua.
- Já existe `.kit/constitution.md`? Então é **atualização**: compare com os assets e proponha só o
  que falta.

## 2. Inspecionar o projeto

Descubra pela evidência (manifests, CI, README, scripts), nunca por suposição:
linguagem, framework, gerenciador de pacotes, comandos de instalar/testar/lint/rodar, branch base,
convenção de commits (veja `git log --oneline -20`). Se houver um pack em `references/packs/` para a
stack, leia **só esse** e use-o para preencher lacunas.

Classifique a documentação: **EXISTENTE** (preserve, só acrescente), **PARCIAL** (mantenha o útil,
preencha lacunas) ou **AUSENTE/NOVO** (crie o mínimo, sem inventar arquitetura).

## 3. Criar os arquivos (somente os que não existem)

| Arquivo | Origem | Para quem |
|---|---|---|
| `AGENTS.md` | `assets/AGENTS.md` com stack e comandos reais | Codex, Copilot, Cursor, Gemini (via ponte) e humanos |
| `CLAUDE.md` | `assets/CLAUDE.md` (importa `@AGENTS.md`) | Claude Code |
| `GEMINI.md` | `assets/GEMINI.md` (importa `@AGENTS.md`) | Gemini CLI / Antigravity |
| `.kit/constitution.md` | `assets/constitution.md`, com a seção "Perfil do projeto" preenchida | todos |
| `.kit/quality.json` | `assets/quality.json` com o comando real de testes | `kit-test-guard` |
| `docs/README.md` | visão mínima; para mapeamento completo use `$kit-system-mapping` | todos |
| `docs/adr/`, `specs/` | pastas com `.gitkeep` | todos |

`AGENTS.md`, `CLAUDE.md` ou `GEMINI.md` já existe? **Acrescente** a seção do kit ao final, sem
remover conteúdo. Adicione `.kit/quality/` ao `.gitignore` (resultados locais do test guard).

## 4. CI (opcional, pergunte)

Projeto no GitHub? Ofereça copiar `assets/github-workflow.yml` para
`.github/workflows/kit-specs.yml`. Ele valida `specs/` em cada PR, começa **informativo**
(`continue-on-error: true`) e pode virar bloqueante depois que o time confiar no gate.

## 5. Encerrar

Mostre a lista de arquivos criados/alterados e o diff. Sugira `$kit-system-mapping` se a
documentação ficou AUSENTE/PARCIAL. **Não faça commit.**
