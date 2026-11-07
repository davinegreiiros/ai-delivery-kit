# Checklist de segurança por categoria

## Segredos
- Chaves, tokens, senhas ou connection strings no código, testes, fixtures, docs ou CI.
- `.env` versionado ou fora do `.gitignore`; segredo impresso em log ou mensagem de erro.
- Chave de cliente (mobile/web) com permissões de servidor.

## Injeção
- SQL/NoSQL montado por concatenação ou interpolação — exigir query parametrizada/ORM.
- Comando de shell com entrada externa — exigir lista de argumentos, nunca `shell=True`/string.
- Caminho de arquivo vindo do usuário sem normalizar e restringir a um diretório (path traversal).
- HTML/JS renderizado com entrada sem escape (XSS); `innerHTML`, `dangerouslySetInnerHTML`, `v-html`.
- Desserialização de dados não confiáveis (`pickle`, `yaml.load` sem safe loader, `eval`).
- SSRF: URL fornecida pelo usuário buscada pelo servidor sem allowlist.

## Autenticação
- Endpoint novo sem exigir autenticação quando os vizinhos exigem.
- Token sem expiração, sem verificação de assinatura ou com algoritmo `none`.
- Comparação de segredo sem tempo constante; senha sem hash forte (bcrypt/argon2/scrypt).
- Recuperação de senha ou magic link reutilizável, previsível ou sem expiração.

## Autorização
- Acesso a recurso por ID sem checar se pertence ao usuário (IDOR).
- Checagem só no front-end ou só na UI.
- Regra de papel/permissão duplicada e divergente entre camadas.
- Políticas de banco (ex.: RLS) desativadas ou permissivas demais para a tabela nova.

## Dados pessoais
- Coleta além do necessário para o caso de uso.
- Dados pessoais/sensíveis em logs, analytics, mensagens de erro ou URLs.
- Retenção e exclusão não definidas; exportação sem controle de acesso.
- Base legal e consentimento quando a legislação aplicável (ex.: LGPD) exigir.

## Criptografia e transporte
- HTTP sem TLS; verificação de certificado desabilitada.
- Algoritmos fracos (MD5/SHA1 para senha, ECB, chaves fixas no código); aleatoriedade não criptográfica para tokens.

## Dependências
- Pacote novo: mantido, popular, sem typosquatting, licença compatível.
- Versão com vulnerabilidade conhecida; lockfile não atualizado.

## Configuração
- Debug/stack trace habilitado em produção; CORS `*` com credenciais.
- Headers de segurança ausentes em app web; rate limit ausente em login e endpoints caros.
- Permissões amplas em IAM, bucket público, porta exposta.

## Mobile
- Token em armazenamento inseguro (SharedPreferences/UserDefaults em texto) em vez de Keychain/Keystore.
- Deep link aceitando parâmetros sem validação; WebView com JS e acesso a arquivos.
- Permissões do app além do necessário.

## IA / LLM
- Entrada do usuário ou de documentos externos concatenada no prompt com acesso a ferramentas (prompt injection).
- Saída do modelo executada como código, SQL ou comando sem validação.
- Dados sensíveis enviados ao provedor sem necessidade.
