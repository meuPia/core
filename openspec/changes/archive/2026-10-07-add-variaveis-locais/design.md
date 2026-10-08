## Context

A motivação está em proposal.md e o comportamento esperado está nas specs `variaveis-locais`, `analise-semantica` e `builtins` deste change.

**Estado atual**
- O pipeline faz quatro passadas independentes sobre a mesma lista de tokens: lexer → `Parser` (só valida) → `SemanticAnalyzer` → `CodeGenerator`. Cada componente recebe apenas `lexeme_pairs`. Esse contrato é usado por `compiler.main`, pelos helpers de teste e, indiretamente, pelo Lab.
- O token `VAR` já existe. O parser só o aceita no topo do programa (`parse()` → `grammar_variable_block`). Dentro de um corpo, `statement()` rejeita `var` com "comando inesperado".
- **`SemanticAnalyzer.get_declared_variables`:** trata todo `VAR` como início de bloco global até encontrar `funcao`, `classe`, `metodo` ou `inicio`. Um `var` dentro de um corpo de função faria os identificadores seguintes serem registrados como globais.
- **`CodeGenerator.collect_user_names`:** tem a mesma falha.
- **Escopo no Python gerado:**
  - funções, métodos e `main()` recebem `global <todas as globais exceto parâmetros>`;
  - qualquer nome atribuído e não listado no `global` já vira variável local do Python;
  - as regras de escopo e de tempo de vida da spec, incluindo a recursão, são exatamente as do Python.
- **`gen_leia`:** escolhe a conversão consultando `self.var_types`, que só tem as globais.

## Goals / Non-Goals

**Goals:**
- Uma única gramática de declaração (`nomes : tipo [<- expr]`) compartilhada pelo `var` global e pelo local, com a inicialização permitida só no local.
- Manter o contrato atual: cada componente continua recebendo apenas `lexeme_pairs`, e os construtores não mudam.
- Garantir que, sem nenhum `var` local, o código gerado seja byte a byte igual ao da versão 1.2.0.

**Non-Goals:**
- Inicialização com expressão no `var` global. A gramática permitiria, mas isso mudaria a ordem de avaliação no topo do módulo e fica para outro change.
- Escopo de bloco (variável visível só dentro de um `se`). A restrição de posição evita esse caso.
- Verificar tipos. O tipo declarado só define o valor inicial e a conversão do `leia`.
- Parâmetros tipados (issue meuPia/core#6).

## Decisions

### D1. Uma linha de declaração única no parser
- Extrair de `grammar_variable_block` um método `grammar_declaration_line(permite_valor)`: `ID ("," ID)* ":" tipo` e, quando `permite_valor` for verdadeiro e houver um único nome, `(ATR) expressao` opcional.
- `ATR` cobre tanto `<-` quanto `=`, que o lexer já emite como `ATR`.
- Com mais de um nome seguido de `ATR`, o erro sintático aponta para o `ATR`.
- O `var` global chama a linha com `permite_valor=False`. O comportamento atual não muda.
- **O que é uma linha de declaração:** um `ID` seguido de `,` ou `:`. Nenhum comando começa assim (comandos com `ID` continuam com `<-`, `=`, `(`, `.` ou `[`), então não há ambiguidade, mesmo sem tokens de quebra de linha.
- **Alternativa descartada:** gramáticas separadas para a forma de bloco e para a forma com valor. Duplicaria as regras de tipo contextual (`lista`/`logico`) e geraria duas mensagens de erro diferentes para o mesmo problema.

### D2. `var` como comando, só no nível principal do corpo
- O `Parser` ganha o contador `profundidade_bloco`, incrementado nos corpos de `se`/`senao`, `enquanto` e `para`.
- `statement()` passa a aceitar `VAR`:
  - com profundidade 0, chama `grammar_local_declaration()`, que é `var` seguido de linhas de declaração com `permite_valor=True`;
  - com profundidade maior que 0, gera o erro sintático "declare variáveis com var fora de blocos se, enquanto e para" na posição do `var`.
- Os corpos de `funcao`, `metodo` e `inicio` já chamam `statement()`, então não precisam de outra mudança.

### D3. Os outros componentes leem a declaração usando o próprio parser
O analisador semântico e o gerador precisam saber onde termina a expressão de inicialização, e os tokens não carregam quebra de linha.
- **Solução:** criar `Parser.ler_declaracao_local(lexeme_pairs, pos)`. Ele cria um `Parser` posicionado no `var` e roda `grammar_local_declaration()` registrando, para cada linha:
  - os nomes e as posições deles;
  - o tipo;
  - o intervalo de tokens da expressão `[inicio, fim)`.

  O retorno é a lista de linhas mais a posição logo depois da declaração.
- Assim, o limite da expressão é decidido pela gramática real, sem heurística, e os construtores dos componentes não mudam.
- **Alternativas descartadas:**
  - Anotar os tokens durante o `parse()`: criaria dependência da ordem de execução, e os testes que rodam o semântico sem o parser quebrariam em silêncio.
  - Usar o número da linha do `code_index`: falharia em expressões de várias linhas, como uma lista literal.

### D4. Analisador semântico
**Pré-passagem de globais (`get_declared_variables`):**
- Rastreia se está dentro de um corpo (de `funcao`/`metodo` até `fim_funcao`) e ignora os `VAR` que encontrar ali.
- Continua parando em `inicio`.
- Passa a registrar as posições de declaração globais. Os nomes de função e classe continuam em `callable_names`.

**Passagem de uso, ao entrar num corpo (`funcao`, `metodo`, `inicio`):**
- Pré-varre o corpo até `fim_funcao`/`fim_algoritmo`. Para cada `VAR`, lê a declaração (D3) e monta `declaradas_no_corpo`, um mapa de nome para a posição da declaração.
- Começa com `locais_visiveis` contendo só os parâmetros (e `self` nos métodos).

**Ao encontrar `VAR` no corpo, para cada linha, na ordem:**
1. Para cada nome, confere os conflitos: global, parâmetro, `self`, local já visível, função ou classe. Se houver conflito, gera erro na posição do nome.
2. Valida os identificadores da expressão com `locais_visiveis`. Assim, `var x: inteiro <- x + 1` acusa `x` usada antes de ser declarada.
3. Acrescenta os nomes a `locais_visiveis`.

**Identificador não aceito:**
- Se estiver em `declaradas_no_corpo` com posição posterior, a mensagem é `a variável "t" foi usada antes de ser declarada`.
- Caso contrário, a mensagem continua `não foi declarada no bloco var`.

### D5. Gerador de código
- **Valor inicial:** extrair `valor_inicial(tipo)` de `gen_variables` e reutilizar na forma de bloco local.
- **Declaração local:** `gen_statement` trata `VAR` com `gen_local_declaration()`. Para cada linha, emite `nome = <expressão>` (usando `gen_expression` no intervalo da linha) ou `nome = <valor inicial>`, e registra o nome em `self.local_types[nome] = tipo`.
- **Escopo dos tipos locais:** `self.local_types` é zerado ao abrir cada `def` (função, método e `main`).
- **`leia`:** consulta `self.local_types` antes de `self.var_types`.
- **`global`:** a linha emitida no início de funções, métodos e `main()` continua usando só `self.var_types`. Como local com nome de global é erro (D4), um nome nunca aparece nas duas listas.
- **`collect_user_names`:** passa a ignorar `VAR` dentro de corpos na regra de bloco global e acrescenta os nomes lidos com `ler_declaracao_local`. Com isso, uma local chamada `piso` desativa o builtin.

### D6. Testes
- Novo `meuPia/tests/test_variaveis_locais.py`, com um teste por cenário da spec `variaveis-locais`. Usa o helper `executar()` para os casos de sucesso e confere `linha`/`coluna` nos de erro.
- Novos cenários de `analise-semantica` e `builtins` nos arquivos de teste existentes.
- Teste de desafio: um programa no formato que o Lab monta (código do aluno + `usar "testes"` + `codigoTeste` com `var` no `inicio`). Usa `esperar_igual` só se o meupia-testes estiver instalado; caso contrário, apenas compila.
- Teste de não regressão: compilar os `.por` versionados e comparar com o código gerado pela 1.2.0 (goal de saída byte a byte igual).

## Risks / Trade-offs

- **[Risco] Erro em código que o aluno não escreveu.** Num desafio, o aluno pode declarar no `inicio` uma local com o mesmo nome de uma `var` do `codigoTeste` anexado pelo Lab, e o erro de conflito apontaria para o código de teste. → Mitigação: a mensagem cita a linha, e o mapeamento de linhas do Lab já trata erros dentro do `codigoTeste`. Os autores de desafios devem preferir nomes específicos nos testes.
- **[Risco] `ler_declaracao_local` roda o parser de novo para cada `var`.** → É desprezível para o tamanho dos programas de aula, e o parser já validou o programa inteiro antes.
- **[Trade-off] Sem escopo de bloco.** Proibir `var` dentro de `se`/`enquanto`/`para` é mais restritivo que linguagens como Java, mas é previsível e evita `UnboundLocalError` em tempo de execução. A restrição pode ser relaxada depois sem quebrar programas.
- **[Trade-off] A inicialização obrigatória da issue foi substituída pelo valor inicial do tipo.** O objetivo (nunca ler uma variável sem valor) é atendido. A diferença está registrada na proposal.

## Migration Plan

1. Bump para `1.3.0` no `setup.py`.
2. Depois do merge, publicar na PyPI e atualizar a versão fixada no Lab (`src/engine/wasm.js`).
3. Nenhum programa existente precisa mudar.
4. **Rollback:** voltar a versão fixada no Lab para 1.2.0.
