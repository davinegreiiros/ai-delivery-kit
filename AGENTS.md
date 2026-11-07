# ai-delivery-kit — instruções para quem desenvolve o kit

Este repositório **é** o kit (skills no padrão Agent Skills), não um projeto que o usa.

## Estrutura
- `skills/<nome>/SKILL.md` — uma skill por pasta; `name` no frontmatter igual ao nome da pasta.
  Arquivos de apoio ficam **dentro** da skill (`assets/`, `references/`, `scripts/`) para que ela
  funcione copiada sozinha. `agents/openai.yaml` traz os metadados de UI do Codex.
- Manifests: `plugin.json` e `.codex-plugin/` (Codex), `.claude-plugin/` (Claude Code),
  `gemini-extension.json` + `GEMINI.md` (Gemini). Versão e nome iguais em todos.
- `scripts/validate_kit.py` — valida tudo isso; `tests/` — testes com `unittest` (sem dependências).

## Comandos
| Ação | Comando |
|---|---|
| Validar o kit | `python3 scripts/validate_kit.py` |
| Testes | `python3 -m unittest discover -s tests -v` |
| Instalar localmente (links) | `./install.sh --client all` |

## Regras
- Scripts em Python 3.9+ somente com biblioteca padrão; bash compatível com 3.2 (macOS).
- `SKILL.md` curto e acionável: o detalhe vai para `references/`, carregado sob demanda.
- Descrições de skill dizem **quando usar e quando não usar** (é o que o agente lê para decidir).
- Toda mudança de versão atualiza todos os manifests e o `CHANGELOG.md`.
- Não faça commit, push ou tag sem pedido explícito.
