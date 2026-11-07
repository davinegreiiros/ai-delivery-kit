---
name: kit-sdd
description: Fluxo padrão para qualquer pedido que crie ou altere código, testes, configuração ou comportamento em um repositório que usa o ai-delivery-kit (AGENTS.md cita o kit ou existe .kit/constitution.md). Acione automaticamente, mesmo sem o usuário citar a skill. Conduz spec, impacto, plano, implementação com testes e verificação. Não use para perguntas somente leitura.
---

# SDD — Spec-Driven Development

Nenhuma linha de código antes de existir uma spec que diga **o quê** e **por quê**, e um plano que
diga **como** e **como verificar**. Caminhos `assets/` e `scripts/` abaixo são relativos à pasta
desta skill.

## 0. Classificar o pedido

| Tipo | Caminho |
|---|---|
| Bug sem causa confirmada | `$kit-systematic-debugging` primeiro; volte aqui com a causa |
| Mudança trivial (typo, texto, renomear local) | **Modo rápido**: pergunte se pode; registre só `specs/<ID>/tasks.md` e vá ao passo 5 |
| Refatoração sem mudança de comportamento | Spec curta com critério "comportamento idêntico"; testes existentes são a evidência |
| Feature, mudança de regra, integração | Fluxo completo |

Sistema sem `docs/`? Sugira `$kit-system-mapping` antes, ao menos do recorte afetado.

## 1. Identificar a mudança

- ID = número do issue/card (`123`, `ABC-123`) ou `LOCAL-<slug>` sem tracker. Com issue citado,
  use `$kit-issue-intake` para trazer o conteúdo.
- Todo artefato vive em `specs/<ID>/`. Crie a branch `<tipo>/<ID>-<slug>` se o projeto usar branches.

## 2. Ler contexto — somente o necessário

1. `AGENTS.md` e `.kit/constitution.md` — sempre.
2. `docs/` — apenas módulos tocados; ADRs em `docs/adr/` — apenas os relacionados.

Não carregue o repositório inteiro. Registre no `plan.md` o que leu e por quê.

## 3. Spec — `specs/<ID>/spec.md`

Copie `assets/spec.md`. Preencha problema, escopo, fora de escopo, regras, critérios de aceite
numerados (`CA-1`…) e perguntas abertas.

**Gate humano:** mostre a spec e peça aprovação. Pergunta aberta que afeta comportamento → pare e
pergunte; não invente regra de negócio. Só marque `Status: APROVADA` após o "sim".

## 4. Impacto e plano

1. `$kit-change-impact` → `specs/<ID>/impact.md`.
2. Conforme o impacto, acione **somente** o que se aplica:
   - contrato público (API, evento, schema, SDK) → `$kit-contract-first`;
   - decisão estrutural em aberto → `$kit-architecture-review` (gera ADR);
   - autenticação, dados pessoais, entrada externa, segredos → planeje `$kit-security-review`.
3. `specs/<ID>/plan.md` a partir de `assets/plan.md`: abordagem, alternativas, riscos, rollback e
   tabela ligando cada `CA-n` a um teste.
4. `specs/<ID>/tasks.md` a partir de `assets/tasks.md`: passos pequenos e verificáveis.

**Gate humano:** risco MÉDIO/ALTO no impacto → aprovação do plano antes de codar.

## 5. Implementar

- `$kit-test-guard baseline` antes de tocar no código.
- Siga `tasks.md` na ordem e marque `[x]` ao concluir cada tarefa.
- Teste do critério antes ou junto do código; ele precisa falhar sem a mudança.
- Algo fora do escopo apareceu? Pare e pergunte. Não expanda silenciosamente.

## 6. Verificar antes de declarar pronto

1. `$kit-test-guard final` — testes passando, cobertura sem queda. Mostre a saída real.
2. Preencha a tabela de evidências de `tasks.md` para cada `CA-n`.
3. Atualize `docs/` se o comportamento documentado mudou.
4. `python3 scripts/check_specs.py specs/<ID>` — corrija tudo que for `erro`.
5. `$kit-code-review` no diff; `$kit-security-review` se planejado no passo 4.

Termine com: o que mudou, como foi verificado, o que ficou pendente. Não faça commit, push ou
deploy sem pedido explícito.
