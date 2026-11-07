---
name: kit-systematic-debugging
description: Investiga bugs, falhas de teste, erros em produção e comportamentos inesperados por reprodução, hipóteses e evidência antes de qualquer correção. Use quando algo "não funciona", "quebrou", "dá erro" ou um teste falha sem causa conhecida. Não use para implementar features.
---

# Debugging sistemático

Regra central: **nenhuma correção sem causa raiz confirmada por evidência.** Mexer no código "para
ver se resolve" é proibido.

## 1. Delimitar o sintoma

Registre em `specs/<ID>/investigation.md` (modelo em `references/investigation.md`):
- comportamento esperado × observado, nas palavras de quem relatou;
- mensagem de erro e stack trace **completos** (não resuma);
- ambiente: versão, branch/commit, SO, dados de entrada, frequência (sempre / às vezes / uma vez);
- desde quando: o que mudou perto disso (`git log --since`, deploy, dependência, config).

## 2. Reproduzir

- Construa a menor reprodução possível: teste automatizado > script > passos manuais.
- Não reproduz? Não corrija. Colete mais dados (logs, input exato, ambiente) ou adicione
  instrumentação temporária e marque-a para remoção.
- Intermitente? Rode N vezes, registre a taxa e suspeite de concorrência, ordem, tempo, cache ou
  estado compartilhado.

## 3. Isolar

Use a técnica mais barata que serve:
- **Ler o stack trace de baixo para cima** até o primeiro frame do seu código.
- **Bisseção no histórico:** `git bisect` com o teste de reprodução quando "funcionava antes".
- **Bisseção no código/dados:** corte entrada ou caminho pela metade até o mínimo que falha.
- **Diferença entre ambientes:** compare config, versões e dados entre onde falha e onde não falha.

## 4. Hipóteses

Liste de 2 a 4 hipóteses. Para cada uma: evidência a favor, evidência contra e um experimento que a
**refuta**. Execute o experimento mais barato primeiro e anote o resultado. Só promova a "causa
raiz" a hipótese que explica **todos** os sintomas observados.

## 5. Corrigir

1. Escreva um teste de regressão que **falha** por causa do bug.
2. Aplique a menor correção que ataca a causa, não o sintoma.
3. O teste passa; a suíte inteira continua passando.
4. Procure o mesmo padrão em outros lugares (`grep` pelo idioma defeituoso) e registre.
5. Remova instrumentação temporária.

Se a correção mudar comportamento, contrato ou mais de um módulo, volte ao `$kit-sdd` com a causa
documentada antes de implementar.

## Sinais de alerta — pare e reavalie

- Terceira tentativa de correção sem sucesso → a hipótese está errada; volte ao passo 3.
- A correção precisa de `sleep`, `retry` ou `try/catch` genérico → provavelmente mascara o sintoma.
- "Funciona na minha máquina" → o passo 3 (diferença entre ambientes) ainda não foi feito.
