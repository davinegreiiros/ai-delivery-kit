# Contribuindo

Sugestões e correções são bem-vindas via issue ou pull request.

## Criar ou alterar uma skill

1. Crie `skills/kit-<nome>/SKILL.md` com frontmatter:
   ```yaml
   ---
   name: kit-<nome>
   description: O que faz. Use quando <gatilhos>. Não use para <limites>.
   ---
   ```
2. Coloque modelos em `assets/`, material de consulta em `references/` e código em `scripts/` —
   sempre dentro da pasta da skill e citados no `SKILL.md` com caminho relativo.
3. Adicione `agents/openai.yaml` com `interface.display_name`, `short_description` e `default_prompt`.
4. Scripts: Python 3.9+ sem dependências externas, com testes em `tests/`.
5. Rode:
   ```bash
   python3 scripts/validate_kit.py
   python3 -m unittest discover -s tests -v
   ```
6. Registre a mudança no `CHANGELOG.md`. Nova versão: atualize `version` em todos os manifests.

## Princípios

- **Cliente-neutro:** nada de recurso exclusivo de um agente no `SKILL.md`; diferenças ficam nos
  manifests e no instalador.
- **Humano decide:** gates de aprovação para spec, plano de risco, mudanças incompatíveis e
  qualquer ação externa (commit, push, publicar em tracker).
- **Evidência acima de opinião:** achados e documentação citam arquivo + símbolo.
