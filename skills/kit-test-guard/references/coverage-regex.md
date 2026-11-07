# Regex de cobertura por ferramenta

Cada regex tem exatamente um grupo de captura com a porcentagem total. Em JSON, escape a barra
invertida (`\\`).

| Ferramenta | Comando típico | `coverage_regex` (valor JSON) |
|---|---|---|
| Jest / Vitest (istanbul) | `npx jest --coverage` | `"All files\\s*\\|\\s*([\\d.]+)"` |
| pytest-cov | `pytest --cov` | `"TOTAL.*?([\\d.]+)%"` |
| coverage.py | `coverage run -m pytest && coverage report` | `"TOTAL.*?([\\d.]+)%"` |
| Go | `go test -cover ./...` | `"coverage:\\s*([\\d.]+)%"` (casa o primeiro pacote; prefira um relatório agregado) |
| Flutter / Dart + lcov | `flutter test --coverage && lcov --summary coverage/lcov.info` | `"lines\\.*:\\s*([\\d.]+)%"` |
| JaCoCo (Gradle) | relatório CSV/HTML | gere um resumo em texto e capture o total |
| .NET coverlet | `dotnet test /p:CollectCoverage=true` | `"Total\\s*\\|\\s*([\\d.]+)%"` |

Teste a regex antes de configurar:

```bash
<comando de teste> 2>&1 | python3 -c "import re,sys; m=re.search(r'<regex sem escape JSON>', sys.stdin.read()); print(m.group(1) if m else 'NÃO CASOU')"
```
