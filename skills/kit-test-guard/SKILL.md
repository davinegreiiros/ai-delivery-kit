---
name: kit-test-guard
description: Mede a suíte de testes e a cobertura antes (baseline) e depois (final) de uma implementação e bloqueia a conclusão se testes falharem ou a cobertura cair. Use dentro do kit-sdd imediatamente antes e depois de alterar código, ou quando pedirem para comparar testes antes e depois.
---

# Test Guard

Evidência objetiva de que a mudança não quebrou nada. Script: `scripts/test_guard.py` (Python 3.9+,
sem dependências), relativo à pasta desta skill.

## Configuração (uma vez por projeto)

`.kit/quality.json` na raiz do projeto:

```json
{
  "test_command": "npm test -- --coverage",
  "coverage_regex": "All files\\s*\\|\\s*([\\d.]+)",
  "coverage_tolerance": 0.5,
  "timeout_seconds": 1800
}
```

- `test_command`: o comando real de testes do projeto (confira no `AGENTS.md`).
- `coverage_regex` (opcional): regex com **um grupo** que captura a porcentagem total na saída.
  Exemplos em `references/coverage-regex.md`.
- `coverage_tolerance`: queda máxima aceita em pontos percentuais (padrão `0`).

Sem o arquivo, pergunte o comando de testes, crie a config e mostre ao usuário.

## Uso

```bash
python3 <skill>/scripts/test_guard.py baseline --id <ID>   # antes de alterar código
python3 <skill>/scripts/test_guard.py final --id <ID>      # depois da implementação
```

Os resultados ficam em `.kit/quality/<ID>-baseline.json` e `<ID>-final.json` (sugira versionar só
se o time quiser histórico; caso contrário, adicione `.kit/quality/` ao `.gitignore`).

## Interpretação

| Resultado | Ação |
|---|---|
| Baseline com testes falhando | Registre em `tasks.md` como pré-existente; não conserte sem combinar escopo |
| `final` falha nos testes | Não declare pronto; corrija ou use `$kit-systematic-debugging` |
| Cobertura caiu além da tolerância | Escreva os testes que faltam para o código novo |
| Regex configurada não casou | Ajuste a regex; não remova a checagem para passar |

Nunca edite os JSONs gerados à mão nem rode `baseline` de novo depois de alterar código.
