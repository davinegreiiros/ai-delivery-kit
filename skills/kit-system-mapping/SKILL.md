---
name: kit-system-mapping
description: Cria ou atualiza a documentação viva de um sistema existente (brownfield) em docs/ - visão geral, módulos, fluxos, integrações, dados e operação - a partir de evidências do código. Use quando o projeto não tem docs/, quando pedirem "documente/mapeie este sistema" ou antes de uma mudança em área não documentada. Não altera código.
---

# Mapeamento de sistema

Documente o sistema **como ele é hoje**, com evidência. Nada de arquitetura desejada ou inventada.
Modelos em `assets/` (relativos a esta skill).

## Escopo primeiro

Pergunte: sistema inteiro ou só o recorte da próxima mudança? Recorte aprovado é suficiente para
começar; mapeamento completo não é pré-requisito do SDD. Repositórios adicionais (backend, libs
internas) só entram se o usuário fornecer o caminho — não varra o disco nem clone nada sozinho.

## Fases — uma por vez, mostrando o resultado de cada uma

1. **Inventário** — linguagens, frameworks, gerenciadores, pontos de entrada, comandos de
   build/teste/execução (de manifests e CI, não de suposição), estrutura de pastas.
2. **Visão geral** — `docs/README.md` a partir de `assets/overview.md`: propósito, atores, contexto,
   mapa de módulos, glossário.
3. **Módulos** — um `docs/modules/<modulo>.md` por módulo relevante (`assets/module.md`):
   responsabilidade, entradas/saídas, dependências, dados, pontos de atenção.
4. **Fluxos críticos** — 3 a 5 fluxos de negócio principais, com diagrama Mermaid de sequência
   quando ajudar.
5. **Integrações e dados** — serviços externos, filas, bancos, contratos; onde estão os dados pessoais.
6. **Operação** — como rodar local, configurar, fazer deploy e diagnosticar (`docs/operations.md`).
7. **Decisões e lacunas** — decisões visíveis no código viram ADRs retroativos (`docs/adr/`,
   status "Registrada retroativamente"); dúvidas vão para `docs/open-questions.md`.

## Regras de evidência

- Toda afirmação relevante cita `arquivo` + símbolo (função, classe, rota). Número de linha só como
  complemento, porque muda.
- Separe **Fato** (lido no código), **Inferência** (deduzido; diga de quê) e **Pergunta** (não sabido).
- Documentação existente é preservada: compare com o código, corrija divergências e marque o que foi
  alterado. Não reescreva conteúdo correto só para padronizar estilo.
- Não copie segredos, dados reais de clientes nem URLs internas sensíveis para `docs/`.

## Manutenção

Depois do baseline, `docs/` muda junto com o código, no mesmo PR (passo 6 do `$kit-sdd`).
