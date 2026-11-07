---
name: kit-security-review
description: Revisão de segurança somente leitura de um diff ou módulo - segredos, injeção, autenticação, autorização, dados pessoais, dependências e configuração. Use quando a mudança toca login, permissões, dados sensíveis, entrada externa, uploads, integrações ou quando pedirem revisão de segurança. Não altera arquivos.
---

# Revisão de segurança

Analise **sem editar**. Escopo padrão: o diff contra a branch base; com pedido explícito, um módulo.
Checklist detalhado por categoria em `references/checklist.md` — leia só as categorias que o diff toca.

## 1. Mapear a superfície

Para o código em escopo, identifique:
- **Entradas não confiáveis:** HTTP (corpo, query, headers, cookies), arquivos, filas, webhooks,
  deep links, variáveis de ambiente controladas por terceiros, respostas de APIs externas.
- **Ativos:** credenciais, tokens, dados pessoais/sensíveis, dinheiro, permissões administrativas.
- **Fronteiras:** onde a entrada atravessa para banco, shell, sistema de arquivos, HTML, outro
  serviço ou log.

## 2. Usar as ferramentas que o projeto já tem

Procure e rode, se existirem e forem só leitura: auditoria de dependências (`npm audit`,
`pip-audit`, `dart pub outdated`, `govulncheck`…), scanner de segredos (`gitleaks`, `trufflehog`),
SAST configurado (Semgrep, CodeQL). **Não instale ferramentas sem autorização.** Registre o que
rodou e o que não estava disponível.

## 3. Revisar por categoria

Siga `references/checklist.md` nas categorias relevantes: segredos, injeção, autenticação,
autorização, dados pessoais, criptografia, dependências, configuração, mobile, IA/LLM.

## 4. Relatar

```
[CRÍTICO|ALTO|MÉDIO|BAIXO] arquivo:linha (símbolo) — vulnerabilidade
  Cenário de ataque: quem, com qual entrada, obtém o quê
  Correção: mudança concreta em uma ou duas frases
```

- Severidade = impacto × facilidade de exploração. Sem cenário de ataque concreto, não é achado:
  liste em "Pontos a confirmar".
- **Nunca** copie o valor de um segredo encontrado no relatório: cite arquivo, linha e tipo.
- Segredo real exposto → recomende **revogar/rotacionar** antes de remover do código; remover do
  histórico Git não basta.
- Termine com: ferramentas executadas, categorias revisadas e o que ficou fora do escopo.
