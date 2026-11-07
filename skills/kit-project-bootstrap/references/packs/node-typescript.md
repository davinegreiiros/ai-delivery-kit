# Pack: Node.js / TypeScript

Use quando houver `package.json`. Descubra o gerenciador pelo lockfile: `package-lock.json` → npm,
`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun.

## Comandos usuais (confira `scripts` no package.json)
| Ação | Comando |
|---|---|
| Dependências | `npm ci` / `pnpm install --frozen-lockfile` |
| Testes + cobertura | `npm test -- --coverage` (Jest/Vitest) |
| Tipos | `npx tsc --noEmit` |
| Lint/format | `npm run lint`, `npx prettier --check .` |

`quality.json`: `coverage_regex` = `"All files\\s*\\|\\s*([\\d.]+)"` para relatórios istanbul.

## Pontos para a constituição
- `strict: true` no `tsconfig`; evitar `any` em código novo.
- Validação de entrada na borda (zod, valibot, class-validator) para tudo que vem de fora.
- Variáveis de ambiente validadas na inicialização; `.env` fora do Git.
- Next.js/React: separar código de servidor e cliente; segredos nunca em `NEXT_PUBLIC_*`.
