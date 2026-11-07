---
name: kit-code-review
description: Revisão técnica somente leitura do diff atual contra a spec da mudança - correção, escopo, testes, segurança e docs. Use ao final do fluxo kit-sdd ou quando pedirem para revisar a mudança antes do PR. Não altera arquivos.
---

# Code Review

Revise o diff (`git diff` contra a branch base) **sem editar nada**. Compare com
`specs/<ID>/spec.md` e `plan.md` quando existirem.

## Checklist

1. **Correção** — a lógica faz o que o critério de aceite pede? Casos de borda: vazio, nulo, limite,
   concorrência, erro de rede.
2. **Escopo** — há mudança que nenhuma tarefa justifica? Arquivo alterado fora do `impact.md`?
3. **Testes** — cada `CA-n` tem teste? Os testes falhariam se o código estivesse errado?
4. **Segurança** — segredo no código, entrada sem validação, SQL/comando montado com string,
   permissão faltando, dado pessoal em log. Superfície sensível → recomende `$kit-security-review`.
5. **Contratos** — mudança quebra consumidor de API/evento/schema sem versionamento?
   (`$kit-contract-first` classifica a compatibilidade.)
6. **Docs e rastreabilidade** — comportamento documentado mudou sem atualizar `docs/`? Tarefas de
   `tasks.md` marcadas sem evidência? Rode `check_specs.py` da skill `kit-sdd`.
7. **Simplicidade** — código morto, duplicação de algo que já existe no projeto, abstração sem uso.

## Saída

Liste os achados do mais grave ao menos grave:

```
[ALTO|MÉDIO|BAIXO] arquivo:linha — problema
  Cenário: entrada/estado concreto → resultado errado
  Sugestão: correção em uma frase
```

Inclua só achados que você consegue justificar com um cenário concreto. Sem achados, diga
"Nenhum problema encontrado" e liste o que foi verificado.
