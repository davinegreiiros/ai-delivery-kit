---
name: kit-contract-first
description: Define ou evolui contratos compartilhados - APIs REST/GraphQL/gRPC, eventos, schemas de banco expostos, SDKs, formatos de arquivo - antes de implementar, verificando compatibilidade com consumidores. Use quando a mudança cria ou altera uma interface usada por outro sistema, app ou time.
---

# Contract First

O contrato é escrito, revisado e aprovado **antes** do código que o implementa ou consome.
Regras de compatibilidade em `references/compatibility.md` (relativo a esta skill).

## 1. Localizar a fonte canônica

Procure o contrato onde o projeto já mantém: OpenAPI (`openapi.yaml`), GraphQL SDL, `.proto`,
JSON Schema/AsyncAPI para eventos, migrations, tipos compartilhados. Não existe? Proponha o formato
padrão da stack e confirme com o usuário antes de criá-lo. Nunca mantenha duas fontes da verdade.

## 2. Escrever ou alterar o contrato

- Nomes, tipos, obrigatoriedade, formatos (datas ISO 8601, moedas em centavos ou decimal explícito),
  paginação, erros (códigos e corpo), autenticação e limites.
- Exemplos de requisição/resposta ou evento para cada caso de critério de aceite.
- Mudança em contrato existente: classifique cada alteração com `references/compatibility.md`.

## 3. Mapear consumidores

Liste quem consome (apps, serviços, jobs, parceiros). Para cada um: a mudança quebra? Quem
precisa agir? Consumidor em outro repositório só é analisado se o usuário fornecer o caminho.

## 4. Gate

Mostre o diff do contrato e a classificação. **Mudança incompatível exige aprovação explícita** e
um plano de transição: nova versão, período de convivência, depreciação anunciada ou feature flag.

## 5. Implementar a partir do contrato

- Gere tipos/clientes a partir do contrato quando a stack permitir.
- Testes de contrato: o provedor responde conforme o schema; exemplos do contrato viram casos de teste.
- Registre o contrato e sua versão no `plan.md` e em `docs/` do módulo.
