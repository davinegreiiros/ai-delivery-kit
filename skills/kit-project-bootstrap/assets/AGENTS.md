# <Nome do projeto>

<Uma frase: o que o sistema faz e para quem.>

## Fluxo de trabalho

Este repositório usa o **ai-delivery-kit**. Para qualquer mudança de código, testes, configuração
ou comportamento, siga a skill `kit-sdd` — mesmo que o pedido não a mencione. Bugs sem causa
conhecida começam por `kit-systematic-debugging`.

- Regras inegociáveis: [.kit/constitution.md](.kit/constitution.md)
- Documentação do sistema: [docs/README.md](docs/README.md)
- Especificações por mudança: `specs/<ID>/` (`spec.md`, `impact.md`, `plan.md`, `tasks.md`)

Se as skills `kit-*` não estiverem instaladas no seu cliente, siga o mesmo ciclo manualmente:
spec aprovada → impacto → plano e tarefas → testes antes/depois → revisão.

## Comandos

| Ação | Comando |
|---|---|
| Instalar dependências | |
| Rodar testes | |
| Lint/format | |
| Rodar localmente | |

## Convenções

- Branch: `<tipo>/<ID>-<slug>` a partir de `<branch base>`
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`…)
- Não faça commit, push ou deploy sem pedido explícito.
