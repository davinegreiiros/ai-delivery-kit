---
name: kit-change-impact
description: Mapeia o impacto técnico de uma mudança já especificada antes de planejar ou codar - módulos, contratos, dados, testes, docs e riscos afetados. Use dentro do fluxo kit-sdd ou quando pedirem "qual o impacto de mudar X". Somente leitura no código.
---

# Change Impact

Objetivo: descobrir **tudo que a mudança toca** antes de tocar em algo. Não altere código aqui.

## Como investigar

1. Parta dos critérios de aceite em `specs/<ID>/spec.md`.
2. Encontre os pontos de entrada (rota, comando, tela, job) e siga as chamadas com busca no código.
3. Para cada símbolo que vai mudar, procure quem o usa (chamadores, imports, consumidores de API,
   consultas ao mesmo dado).
4. Verifique: migrações de banco, configs/feature flags, contratos externos (API, eventos, arquivos),
   permissões, testes existentes que cobrem a área, documentação em `docs/`.

## Saída: `specs/<ID>/impact.md`

```markdown
# Impacto — <ID>

## Áreas afetadas
| Área | Arquivo/símbolo | Tipo de mudança | Evidência |
|---|---|---|---|

## Contratos e dados
- API/eventos/schemas alterados e quem consome
- Migração necessária? Reversível?

## Testes
- Existentes que cobrem a área:
- Faltando:

## Riscos
| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|

## Classificação
Risco geral: BAIXO | MÉDIO | ALTO — justificativa em uma linha.
```

Evidência = `arquivo:linha` **mais** o símbolo (função, classe, rota), porque números de linha mudam.
Marque como hipótese o que não foi confirmado lendo o código.
