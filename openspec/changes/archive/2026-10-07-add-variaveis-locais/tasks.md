## 1. Base de não regressão

- [x] 1.1 Antes de alterar qualquer código, gerar o Python dos `.por` de `exemplos/` e `meuPia/input/` com o compilador atual e salvar em `meuPia/tests/golden/<nome>.py`. Criar `test_golden.py`, que compila cada `.por` e compara com o arquivo golden. Verificar que o teste passa na versão atual.

## 2. Parser: linha de declaração e var local

- [x] 2.1 Escrever os testes sintáticos da spec `variaveis-locais`: forma com valor, valor com `=`, forma de bloco, formas misturadas, valor com mais de um nome (erro no `<-`), tipo desconhecido, `var` dentro de `se` e de `para` (erro no `var`) e `var` em `inicio` e em `metodo`. Verificar que falham.
- [x] 2.2 Extrair `grammar_declaration_line(permite_valor)` de `grammar_variable_block` (D1). Verificar que `test_syntax.py`, `test_tipos.py` e `test_golden.py` continuam passando.
- [x] 2.3 Implementar `grammar_local_declaration()`, o contador `profundidade_bloco` e o `var` em `statement()` (D2). Verificar que os testes sintáticos de 2.1 passam (os de execução ainda podem falhar).
- [x] 2.4 Implementar `Parser.ler_declaracao_local(lexeme_pairs, pos)`, que devolve nomes, posições, tipo e intervalo da expressão de cada linha (D3). Verificar com testes unitários: expressão de uma linha, expressão de várias linhas (lista literal) e bloco com vários nomes.

## 3. Analisador semântico

- [x] 3.1 Escrever os testes de escopo, conflitos e uso antes da declaração da spec `variaveis-locais`, e os novos cenários de `analise-semantica`: local aceita depois da declaração e local que não vira global. Verificar que falham.
- [x] 3.2 Fazer a pré-passagem de globais ignorar `VAR` dentro de corpos (D4). Verificar que um programa com `var` local deixa de gerar "declaração duplicada" e que `test_semantic.py` e `test_analise_semantica.py` passam.
- [x] 3.3 Implementar o escopo local por corpo: pré-varredura de `declaradas_no_corpo`, `locais_visiveis` em ordem, conflitos com global, parâmetro, `self`, local, função e classe, a validação da expressão antes de registrar o nome e a mensagem "foi usada antes de ser declarada" (D4). Verificar que os testes de 3.1 passam.

## 4. Gerador de código

- [x] 4.1 Escrever os testes de execução: forma com valor, bloco com valor inicial do tipo, várias declarações, `inicio` depois de comandos, método, recursão com `fat(5)` = `120`, local reinicializada (`11`), mesmo nome em funções diferentes, `leia` em local inteira e lógica, e local chamada `piso` (spec `builtins`). Verificar que falham.
- [x] 4.2 Extrair `valor_inicial(tipo)` de `gen_variables`. Verificar com `test_golden.py`, que deve continuar sem nenhuma diferença.
- [x] 4.3 Implementar `gen_local_declaration()`, `self.local_types` por `def` e a consulta de tipos locais no `leia` (D5). Verificar que os testes de 4.1 passam, exceto o de `piso`.
- [x] 4.4 Atualizar `collect_user_names` para ignorar `VAR` em corpos e incluir os nomes locais (D5). Verificar que o teste da local `piso` passa e que `test_builtins.py` continua verde.

## 5. Desafios, documentação e versão

- [x] 5.1 Criar o teste de desafio: programa montado como o Lab faz (código do aluno + `usar "testes"` + `codigoTeste` com `var legado, sus, tuss: dicionario` e `var resultado: inteiro` no `inicio`, no estilo do `ontologia_hospital`). Verificar que compila e, se o meupia-testes estiver instalado, que os `esperar_igual` passam.
- [x] 5.2 Documentar variáveis locais: se `docs/guia-da-linguagem.md` existir, acrescentar uma seção nele; se não, acrescentar uma seção "Variáveis locais" no `README.md`. Incluir as duas formas, as posições permitidas, o escopo, os conflitos e exemplos. Verificar que cada exemplo da documentação compila (se o guia tiver `test_guia.py`, ele deve passar).
- [x] 5.3 Fazer o bump do `setup.py` para `1.3.0`. Verificar com um build num diretório descartável (`python -m build --outdir <scratch>`).

## 6. Verificação integrada

- [x] 6.1 Rodar `pytest --cov=meuPia.analyzers --cov=meuPia.compiler --cov-branch`. Verificar que tudo passa, que a cobertura de branches continua ≥ 90% em cada módulo e que `test_golden.py` não tem diferenças.
- [x] 6.2 Compilar os 14 desafios de `../desafios` (só o `codigoInicial` e também montados como o Lab) com um script descartável. Verificar que nenhum desafio que compilava deixou de compilar e que o `ontologia_hospital` montado passa a compilar.
- [x] 6.3 Rodar `openspec validate add-variaveis-locais --strict` e conferir cada requisito das três specs contra os testes.
