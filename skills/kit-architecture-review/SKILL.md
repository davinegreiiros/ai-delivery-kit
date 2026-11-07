---
name: kit-architecture-review
description: Compara alternativas para uma decisão estrutural em aberto - nova dependência, padrão de módulo, armazenamento, comunicação entre serviços, estado, cache - e registra a escolha como ADR. Use quando o plano depende de uma decisão de arquitetura não tomada ou quando pedirem "qual a melhor abordagem para X". Não implementa.
---

# Revisão de arquitetura

Transforma "acho que devemos usar X" em uma decisão comparada, com trade-offs explícitos e
registrada. Modelo de ADR em `assets/adr.md` (relativo a esta skill).

## 1. Enquadrar a decisão

- Qual é a pergunta, em uma frase? ("Como sincronizar dados offline no app?")
- Forças: requisitos funcionais, restrições (prazo, equipe, custo, plataforma), atributos de
  qualidade prioritários (desempenho, simplicidade, segurança, operabilidade, evolução).
- O que já existe: padrões atuais do projeto, ADRs anteriores, `docs/`. Uma alternativa
  consistente com o que existe começa com vantagem.

## 2. Alternativas

Entre 2 e 4, **incluindo "não mudar nada/solução mais simples"**. Para cada uma: como funciona em
um parágrafo, o que muda no código, custo de adoção e custo de reversão.

## 3. Comparar

| Critério (peso) | Alternativa A | Alternativa B | Alternativa C |
|---|---|---|---|
| <atributo prioritário> (3) | | | |
| Simplicidade/manutenção (2) | | | |
| Custo de reverter (2) | | | |
| Risco (1) | | | |

Use notas 1–5 com uma justificativa curta por célula. A tabela apoia a decisão; não a substitui.

## 4. Recomendar e registrar

- Recomende uma alternativa, diga o que se perde com ela e em que condição você mudaria de ideia.
- **A decisão é do usuário.** Com aprovação, grave `docs/adr/NNNN-<slug>.md` a partir de
  `assets/adr.md` (próximo número livre) e cite o ADR no `plan.md` da mudança.
- Recomendação não aprovada não é ADR: deixe-a em `specs/<ID>/plan.md` como proposta.
