## 1. Base de testes

- [x] 1.1 Criar `meuPia/tests/helpers.py` com `compilar(codigo)` e `executar(codigo, entrada="")`, que rodam o pipeline completo e executam o Python gerado capturando stdin/stdout (D13). Verificar com um teste de fumaça que `executar` de "Olá" imprime `Olá`.
- [x] 1.2 Renomear o primeiro `test_gen_plugin_import` (linha 109 de `test_generator_core.py`) para um nome único. Verificar que a contagem do `pytest` sobe de 61 para 62.
- [x] 1.3 Adicionar `pytest-cov` a `extras_require["dev"]` no `setup.py`. Verificar que `pytest --cov=meuPia --cov-branch` roda.

## 2. CLI: código de saída (prioridade 1)

- [x] 2.1 Escrever `test_cli.py` com os cenários da spec `cli` (sucesso → 0; erro, arquivo inexistente e sem argumentos → ≠0; `python -m meuPia.compiler`; `main()` em caso de erro não grava `.py` nem propaga exceção). Verificar que os testes de código de saída falham.
- [x] 2.2 Alterar `compiler.main` para retornar 0, 1 ou 2, chamar `sys.exit(main(...))` no `__main__` e validar com `compile()` antes de gravar o arquivo (D12). Verificar que `test_cli.py` passa.

## 3. Blocos vazios (prioridade 1)

- [x] 3.1 Escrever em `test_controle_fluxo.py` os cenários do requisito "Blocos vazios geram programa executável", usando `executar`. Verificar que falham com `IndentationError`.
- [x] 3.2 Implementar no gerador a emissão de `pass` para todo bloco sem corpo, sem contar a linha `global` (D5). Remover o `has_content` específico de método. Verificar que os testes de 3.1 e todo o `test_generator_core.py` passam.

## 4. Erros padronizados

- [x] 4.1 Escrever os cenários do requisito "Formato padronizado das mensagens de erro" (léxico, sintático em fim de arquivo, arquivo vazio, semântico sem nomes internos). Verificar que falham.
- [x] 4.2 Criar a classe `ErroCompilacao` e fazer `LexicalError`, `SyntacticError` e `SemanticError` herdarem dela. Criar o helper de posição (incluindo fim de arquivo e lista vazia) e a tabela de descrições de token em pt-BR (D11). Traduzir todas as mensagens. Verificar que 4.1 passa.
- [x] 4.3 Atualizar as asserções de mensagem em `test_semantic.py` (`Undeclared variable`, `Double declaration`) para o novo formato. Verificar que o `pytest` inteiro passa.

## 5. Lexer: tokens e strings

- [x] 5.1 Escrever testes de lexer para: `LOGIGUAL` distinto de `ATR` (nenhum valor de `TokenEnum` repetido), `==`, `!=`, `%`, `mod`, `logico`, `lista`, string terminada em `\\`, aspa escapada e coluna do erro de string não terminada. Verificar que falham.
- [x] 5.2 Dar a `LOGIGUAL` o valor `'=='`, adicionar `OPMOD`, mapear `!=` para `LOGDIFF`, adicionar a keyword `mod` (`logico` e `lista` continuam como `ID`, por serem tipos contextuais), e corrigir `match_token_string` (D2, D3, D8, D9). Verificar que 5.1 e o `test_lexical.py` existente passam, inclusive `test_scan_assignment_equal`.

## 6. Parser: gramática de expressões

- [x] 6.1 Escrever em `test_expressoes.py` todos os cenários da spec `expressoes`, e em `test_controle_fluxo.py` os de limites do `para` com expressões. Verificar que falham.
- [x] 6.2 Substituir as gramáticas aritmética e lógica pela descida recursiva única do D1. Ela deve aceitar `ATR` com lexema `=` como relacional e rejeitar `<-` dentro de expressões. Usar `expressao` em `se`, `enquanto`, `retorne`, nos limites e no passo do `para`, em argumentos e em índices. Verificar que o `test_syntax.py` existente continua passando.
- [x] 6.3 Ajustar o gerador: dentro de expressões, `ATR` com lexema `=` vira `==` e `OPMOD` vira `%`. Verificar que os testes de 6.1 passam.

## 7. Laço para

- [x] 7.1 Escrever os cenários do requisito "Limite final do para inclusivo nos dois sentidos" e de `continue`/`interrompa`. Verificar que o de passo negativo falha.
- [x] 7.2 Adicionar `_faixa` ao cabeçalho gerado e emitir `for v in _faixa(a, b, p):` (D4). Verificar que 7.1 passa e ajustar `test_gen_loop_para` se ele checar o texto do `range`.

## 8. Tipos e novo

- [x] 8.1 Escrever em `test_tipos.py` os cenários da spec `tipos-e-declaracoes` (valores iniciais, `lista`/`logico` como nomes de variável, `leia` de logico, `novo dicionario/lista/filaPrioridade`, tipo desconhecido). Verificar que falham.
- [x] 8.2 Implementar `logico` e `lista` como tipos contextuais (posição de tipo no `var` e depois de `novo`; o semântico ignora a posição de tipo), os valores iniciais de `logico` e `lista`, o `leia` de logico e o mapeamento dos `TIPO` em expressões para `dict`, `list` e `FilaPrioridade` (D8). Verificar que 8.1 passa.

## 9. Builtins e escreva

- [x] 9.1 Escrever em `test_builtins.py` os cenários da spec `builtins` (nomes do usuário com prioridade, `pi`, `tamanho` como método e função, métodos de coleção em expressões, `escreva` com vários argumentos e lógicos). Verificar que falham.
- [x] 9.2 Criar `meuPia/utils/builtins.py` com as tabelas `FUNCOES_BUILTIN`, `CONSTANTES_BUILTIN` e `METODOS`, e substituir as duas cadeias de `if/elif` do gerador por elas (D6). Verificar que o `test_generator_core.py` existente continua passando.
- [x] 9.3 Implementar a pré-passagem de nomes declarados, a regra "depois de `.` só vale `METODOS`", a reescrita de `x.tamanho()` para `len(x)` e o `__len__` da `FilaPrioridade` (D6). Verificar os cenários de nomes e de `tamanho` de 9.1.
- [x] 9.4 Adicionar `_escreva` e `_texto` ao cabeçalho e aceitar vários argumentos em `escreva` no parser e no gerador (D7). Verificar os cenários de `escreva` de 9.1.

## 10. Análise semântica

- [x] 10.1 Escrever em `test_analise_semantica.py` os cenários da spec `analise-semantica` (escopos, classe depois de `var`, atributos depois de `.`, `self`, método com variável não declarada, declaração duplicada com linha e coluna). Verificar que falham.
- [x] 10.2 Reescrever o `SemanticAnalyzer` como máquina de estados com pré-passagem e escopos de `funcao` e `metodo`, usando `meuPia/utils/builtins.py` para os nomes builtin (D10). Verificar que 10.1 e o `test_semantic.py` passam.

## 11. Exemplos, regressão e versão

- [x] 11.1 Atualizar `exemplos/smart_security.por` para a sintaxe atual: renomear a variável `classe` e trocar `fimenquanto`/`fimalgoritmo` por `fim_enquanto`/`fim_algoritmo`. Verificar compilando com `meupia exemplos/smart_security.por` (código de saída 0).
- [x] 11.2 Criar `test_regressao.py`, parametrizado sobre `exemplos/*.por` e `meuPia/input/*.por`, que compila cada arquivo e valida o Python gerado com `compile()`. Verificar que todos passam.
- [x] 11.3 Fazer o bump do `setup.py` para `1.2.0`. Verificar com `pip install -e .` seguido de `meupia --help` ou de uma compilação.

## 12. Verificação integrada

- [x] 12.1 Rodar `pytest --cov=meuPia/analyzers --cov=meuPia/compiler --cov-branch`. Verificar que todos os testes passam e que a cobertura de branches em `meuPia/analyzers` e `meuPia/compiler.py` é ≥ 90%.
- [x] 12.2 Compilar o `codigoInicial` dos 14 desafios de `../desafios/*.json` com um script descartável na scratchpad. Verificar que os 11 que compilavam continuam compilando, que só falham, por erro do próprio desafio, `fila_prioridade_simples` (aspa sobrando), `fio_de_ariadne` (parâmetro chamado `inicio`) e `radar_motoboy` (`mapa_global` não declarado). O `!=` e o tipo `lista` devem ser aceitos.
- [x] 12.3 Rodar `openspec validate fix-compiler-core-bugs --strict` e conferir a implementação contra cada requisito das 6 specs.
