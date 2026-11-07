# Pack: Python

Use quando houver `pyproject.toml`, `requirements*.txt` ou `setup.py`. Descubra o gerenciador:
`uv.lock` → uv, `poetry.lock` → Poetry, `Pipfile.lock` → pipenv, senão pip.

## Comandos usuais
| Ação | Comando |
|---|---|
| Dependências | `uv sync` / `poetry install` / `pip install -r requirements.txt` |
| Testes + cobertura | `pytest --cov` |
| Lint/format | `ruff check .`, `ruff format --check .` |
| Tipos | `mypy .` ou `pyright` (se configurado) |

`quality.json`: `coverage_regex` = `"TOTAL.*?([\\d.]+)%"`.

## Pontos para a constituição
- Type hints em código novo; versão mínima do Python declarada.
- Sem `eval`, `pickle` ou `yaml.load` inseguro com dados externos; `subprocess` sem `shell=True`.
- Django/FastAPI: migrações revisadas e reversíveis; validação via serializers/Pydantic.
