# Compatibilidade de contratos

## Geralmente compatível (aditiva)
- Adicionar endpoint, operação, evento ou tipo novo.
- Adicionar campo **opcional** na requisição.
- Adicionar campo na resposta/evento (se consumidores ignoram campos desconhecidos — confirme).
- Adicionar valor de enum **na requisição** aceito pelo provedor.
- Relaxar validação (aceitar mais formatos).

## Incompatível (quebra consumidores)
- Remover ou renomear endpoint, campo, evento ou tipo.
- Tornar obrigatório um campo antes opcional na requisição.
- Mudar tipo, formato, unidade ou semântica de um campo (ex.: reais → centavos, local → UTC).
- Adicionar valor de enum **na resposta** quando consumidores fazem `switch` exaustivo.
- Restringir validação; mudar códigos de erro, paginação ou autenticação.
- Mudar ordem ou chave de particionamento de eventos quando consumidores dependem dela.

## Estratégias de transição
| Estratégia | Quando usar |
|---|---|
| Expandir e contrair | Adicione o novo ao lado do antigo, migre consumidores, remova o antigo depois |
| Versão nova (`/v2`, `evento.v2`) | Mudança ampla ou consumidores externos fora do seu controle |
| Feature flag / negociação | Consumidores migram em momentos diferentes |
| Depreciação anunciada | Header `Deprecation`/`Sunset`, changelog e data de remoção |

Apps mobile exigem cuidado extra: versões antigas continuam instaladas por meses.
