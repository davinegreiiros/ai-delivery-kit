# Constituição do projeto

Regras inegociáveis para humanos e agentes. Mudar este arquivo exige uma decisão registrada em
`docs/adr/`.

## Núcleo (vale para todo projeto que usa o kit)

1. **Spec antes de código.** Mudança de comportamento só começa com `specs/<ID>/spec.md` aprovada.
2. **Critério de aceite tem evidência.** Todo `CA-n` aponta para um teste ou verificação registrada.
3. **Escopo é contrato.** O diff só contém o que a spec e o plano justificam.
4. **Sem segredos no repositório.** Credenciais ficam em variáveis de ambiente ou cofre.
5. **Dados pessoais** são minimizados, não aparecem em logs e seguem a política aplicável (ex.: LGPD).
6. **Docs vivas.** Se o comportamento documentado mudou, `docs/` muda no mesmo PR.
7. **Humano decide** intenção, risco e exceções. O agente propõe; não decide sozinho o que é
   irreversível (deploy, migração destrutiva, exclusão de dados, push).

## Perfil do projeto (ajuste no bootstrap)

- Stack:
- Comando de teste:
- Comando de lint/format:
- Branch base:
- Convenção de commits:
- Fronteiras arquiteturais (o que não pode depender de quê):
- Restrições específicas:
