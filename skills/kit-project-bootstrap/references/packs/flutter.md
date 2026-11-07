# Pack: Flutter / Dart

Use para preencher o perfil da constituição e o `AGENTS.md` quando houver `pubspec.yaml`.
Confirme cada item no projeto; o pack só sugere.

## Comandos usuais
| Ação | Comando |
|---|---|
| Dependências | `flutter pub get` |
| Testes + cobertura | `flutter test --coverage` |
| Análise estática | `flutter analyze` |
| Formatação | `dart format --set-exit-if-changed .` |
| Rodar | `flutter run` |
| Código gerado | `dart run build_runner build --delete-conflicting-outputs` |

`quality.json`: `test_command` = `flutter test --coverage && lcov --summary coverage/lcov.info`,
`coverage_regex` = `"lines\\.*:\\s*([\\d.]+)%"` (requer `lcov` instalado).

## Pontos para a constituição
- Gerência de estado adotada (Bloc, Riverpod, Provider…) — não misturar no mesmo módulo.
- Arquivos gerados (`*.g.dart`, `*.freezed.dart`) não são editados à mão.
- Segredos e chaves fora do app; `--dart-define`/flavors para ambiente.
- Versões antigas do app continuam em uso: mudanças de API exigem `$kit-contract-first`.
- Testes de widget para telas com regra; golden tests só se o projeto já usa.
