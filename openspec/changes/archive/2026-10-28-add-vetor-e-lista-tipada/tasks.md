## 1. Base de não regressão

- [x] 1.1 Rodar `pytest` na versão atual e registrar que toda a suíte passa, incluindo `test_golden.py` e `test_guia.py`. Esta é a linha de base para o goal de byte a byte igual.

## 2. Parser: leitura do tipo

- [x] 2.1 Em `meuPia/utils/builtins.py`, acrescentar `vetor` a `TIPOS_CONTEXTUAIS` e criar `TIPOS_ELEMENTO`. Verificar que `test_tipos.py` e `test_syntax.py` continuam passando.
- [x] 2.2 Escrever os testes sintáticos da spec `colecoes-tipadas`, requisito "Sintaxe de declaração": declaração global e local, vários nomes, tamanho por variável, tamanho `0`, tamanho real (`5.0`), vetor sem `de` e tipo de elemento não permitido, conferindo linha, coluna e mensagem. Escrever também os cenários "Variável chamada vetor" de `tipos-e-declaracoes`. Verificar que falham.
- [x] 2.3 Implementar `grammar_tipo()` e os campos `elemento`/`tamanho` na linha de declaração (D1). Verificar que os testes sintáticos de 2.2 passam e que `test_variaveis_locais.py` continua passando.
- [x] 2.4 Implementar `Parser.ler_bloco_var(lexeme_pairs, pos)` e, em `grammar_id_statement`, o registro opcional de `atribuicoes`, com `Parser.ler_atribuicoes(lexeme_pairs)` (D1, D4). Verificar com testes unitários: bloco com tipo simples e com coleção tipada; uma atribuição `v <- [1, 2]` registrada; `se v = [1, 2] entao` não registrada; `v[0] <- 1` e `a.b <- 1` não registradas.

## 3. Runtime: classes `_Lista` e `_Vetor`

- [x] 3.1 Escrever os testes de execução da spec `colecoes-tipadas`: valor inicial, tipo dos elementos verificado na execução, atribuição de coleção inteira, faixa de índices, tamanho fixo e métodos, com a mensagem exata em cada caso de erro. Escrever também o cenário "Valor inicial de vetor" de `tipos-e-declaracoes`. Verificar que falham.
- [x] 3.2 No `CodeGenerator`, escrever o cabeçalho de runtime com `_elemento`, `_valor_msg`, `_Lista` e `_Vetor` (D2). As classes cobrem `__getitem__`/`__setitem__` com faixa, `append`, `extend` atômico, `insert`, `__iadd__`, `pop`, `sort` e os métodos `inserir`, `remover`, `removerEm`, `buscar`, `contem` e `ordenar`. O `_Vetor` bloqueia todo método que muda o tamanho. O cabeçalho só é emitido quando o programa declara uma coleção tipada. Verificar compilando um programa sem coleções tipadas e conferindo que `test_golden.py` passa sem regerar nada.
- [x] 3.3 Fazer `gen_variables` usar `Parser.ler_bloco_var`, guardar a linha de tipo em `var_types`/`local_types` e gerar o valor inicial `_Vetor(...)`/`_Lista(...)`, um objeto por nome (D3). Verificar que os cenários de valor inicial de 3.1 passam.
- [x] 3.4 Implementar a conversão `receber` nas atribuições a nome simples e no valor inicial de `var` local. Implementar também `self.params_atuais`, com a ordem de resolução local → parâmetro → global (D3). Verificar que os cenários de atribuição, verificação de tipo, faixa, tamanho fixo e métodos de 3.1 passam. Incluir um teste em que um parâmetro com o nome de uma global tipada recebe um número sem erro.
- [x] 3.5 Garantir que `gen_leia` não usa a linha de tipo de forma errada: o erro é semântico (seção 4), e o gerador nunca chega a ver `leia` de coleção. Verificar com `test_tipos.py` e os testes de `leia` existentes.

## 4. Analisador semântico

- [x] 4.1 Escrever os testes da spec `colecoes-tipadas`, requisitos "Listas literais verificadas ao compilar" e "leia não aceita coleção tipada": elemento de tipo errado (linha 5, coluna 14), quantidade errada (coluna do `[`), valor inicial de `var` local, lista com expressão aceita, `verdadeiro` redeclarado pelo usuário não verificado, e `leia(v)`. Verificar que falham.
- [x] 4.2 Registrar `tipos_globais` em `get_declared_variables` e `tipos_locais` em `validate_local_declaration`/`enter_body` (D4). Verificar que `test_semantic.py`, `test_analise_semantica.py` e `test_variaveis_locais.py` continuam passando.
- [x] 4.3 Implementar o verificador de lista literal e o uso de `Parser.ler_atribuicoes` na passagem de uso, além do erro de `leia` em coleção tipada (D4). Verificar que os testes de 4.1 passam.

## 5. Documentação, exemplo e desafio

- [x] 5.1 Atualizar `docs/guia-da-linguagem.md` (D5):
  - tabela de tipos da seção 2;
  - subseções "Vetores" e "Listas com tipo" na seção 6, com o exemplo da issue adaptado;
  - tabela de métodos;
  - erros novos na seção 11;
  - `vetor` como nome não reservado na seção 12;
  - nota sobre `/` produzir real.

  Verificar que `test_guia.py` executa os novos exemplos e passa.
- [x] 5.2 Acrescentar ao `README.md` a subseção "Vetores e listas com tipo", com um exemplo curto e link para o guia. Verificar visualmente o Markdown renderizado.
- [x] 5.3 Criar `exemplos/boletim.por` e gerar `meuPia/tests/golden/boletim.py` com o compilador novo. Revisar o golden à mão e executá-lo para conferir a saída. Verificar que `test_golden.py` e `test_regressao.py` passam.
- [x] 5.4 Criar `meuPia/tests/test_desafio_colecoes_tipadas.py`, com uma solução de aluno no formato de desafio do Lab que usa `vetor` e `lista de T`, e asserções sobre a saída. Verificar que passa.

## 6. Fechamento

- [x] 6.1 Bump para `1.4.0` no `setup.py`. Verificar que `pip install -e .` funciona e que `meupia exemplos/boletim.por` gera o arquivo em `output/`.
- [x] 6.2 Rodar a suíte inteira com `pytest` e verificar que tudo passa, incluindo `test_golden.py` sem nenhum golden existente alterado.
- [x] 6.3 Rodar `openspec validate add-vetor-e-lista-tipada --strict` e verificar que não há erros.
