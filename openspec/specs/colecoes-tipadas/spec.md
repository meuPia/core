# colecoes-tipadas Specification

## Purpose

Define as coleções com tipo de elemento do meuPiá: o `vetor[N] de T`, de tamanho fixo, e a `lista de T`, dinâmica. A spec cobre a declaração, o valor inicial, a verificação do tipo dos elementos (ao compilar e na execução), a faixa de índices, os métodos e as mensagens de erro.

Nos cenários abaixo, "o programa" é um algoritmo completo com as variáveis usadas declaradas em `var`. "Imprime" se refere à saída padrão produzida ao executar o código gerado. "Erro de execução" é uma exceção levantada pelo código gerado, que interrompe o programa e traz a mensagem indicada.

## Requirements

### Requirement: Sintaxe de declaração de coleções tipadas
O compilador SHALL aceitar, na posição de tipo de uma declaração (bloco `var` global e `var` local, com ou sem valor inicial), as formas:
- `vetor[N] de T`, onde `N` é um literal inteiro maior que zero;
- `lista de T`.

`T`, o tipo dos elementos, SHALL ser `inteiro`, `real`, `float`, `cadeia`, `string` ou `logico`. `real` e `float` são o mesmo tipo de elemento, assim como `cadeia` e `string`.

O compilador SHALL rejeitar com erro sintático, indicando a linha e a coluna do token problemático:
- tamanho do vetor que não seja um literal inteiro (variável, expressão ou número real), com a mensagem `o tamanho do vetor precisa ser um número inteiro maior que zero, como vetor[5] de inteiro`;
- tamanho `0`, com a mesma mensagem;
- `vetor[N]` sem `de T`;
- tipo de elemento fora da lista acima, como `lista`, `dicionario`, `filaPrioridade` ou outro `vetor`, com a mensagem `o tipo dos elementos precisa ser inteiro, real, float, cadeia, string ou logico`.

`l: lista`, sem `de`, SHALL continuar sendo a lista sem tipo de elemento, com o comportamento atual.

#### Scenario: Declaração global de vetor e lista tipada
- **WHEN** o programa declara `notas: vetor[5] de inteiro` e `nomes: lista de cadeia` no bloco `var`
- **THEN** a compilação tem sucesso

#### Scenario: Vários nomes na mesma linha
- **WHEN** o programa declara `a, b: vetor[2] de real` e contém `a[0] <- 1.5` e `escreva(b[0])`
- **THEN** a execução imprime `0.0`

#### Scenario: Declaração local com valor
- **WHEN** o bloco `inicio` contém `var v: vetor[3] de inteiro <- [1, 2, 3]` e `escreva(v[2])`
- **THEN** a execução imprime `3`

#### Scenario: Tamanho por variável é rejeitado
- **WHEN** o programa declara `v: vetor[n] de inteiro`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna de `n`

#### Scenario: Tamanho zero é rejeitado
- **WHEN** o programa declara `v: vetor[0] de inteiro`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna do `0`

#### Scenario: Vetor sem tipo de elemento
- **WHEN** o programa declara `v: vetor[3]` seguido da linha `x: inteiro`
- **THEN** a compilação falha com erro sintático que menciona `"de"`

#### Scenario: Tipo de elemento não permitido
- **WHEN** o programa declara `l: lista de dicionario`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna de `dicionario`

### Requirement: Valor inicial das coleções tipadas
Toda variável declarada como `vetor[N] de T` SHALL começar com `N` elementos, todos iguais ao valor inicial de `T` (`0` para `inteiro`, `0.0` para `real`, texto vazio para `cadeia` e `falso` para `logico`). Toda variável declarada como `lista de T` SHALL começar vazia. Cada variável declarada SHALL ter a sua própria coleção, independente das outras.

#### Scenario: Vetor de inteiros começa com zeros
- **WHEN** o programa declara `v: vetor[3] de inteiro` e contém `escreva(v)`
- **THEN** a execução imprime `[0, 0, 0]`

#### Scenario: Vetor de lógicos começa com falso
- **WHEN** o programa declara `v: vetor[2] de logico` e contém `escreva(v[1])`
- **THEN** a execução imprime `falso`

#### Scenario: Lista tipada começa vazia
- **WHEN** o programa declara `l: lista de cadeia` e contém `escreva(tamanho(l))`
- **THEN** a execução imprime `0`

#### Scenario: Vetores da mesma linha são independentes
- **WHEN** o programa declara `a, b: vetor[2] de inteiro` e contém `a[0] <- 7` e `escreva(b[0])`
- **THEN** a execução imprime `0`

### Requirement: Tipo dos elementos verificado na execução
Toda operação que coloca um valor numa coleção tipada SHALL verificar o tipo do valor: atribuição da coleção inteira, atribuição por índice (`v[i] <- x`), `adicionar`, `adicionarFim`, `inserir` e `expandir`. A verificação SHALL valer também quando a coleção é acessada dentro de uma função que a recebeu como parâmetro.

Regras de aceitação por tipo de elemento:
- `inteiro`: aceita números inteiros; recusa lógicos e números reais;
- `real`: aceita números inteiros e reais, e guarda o valor como real; recusa lógicos;
- `cadeia`: aceita textos;
- `logico`: aceita `verdadeiro` e `falso`.

Um valor recusado SHALL causar erro de execução com a mensagem `a lista só aceita valores do tipo T; recebeu V` (ou `o vetor só aceita ...`). `T` é o tipo de elemento declarado e `V` é o valor recebido. Textos aparecem entre aspas duplas e lógicos como `verdadeiro`/`falso`. Nenhum elemento SHALL ser alterado pela operação recusada.

#### Scenario: Adicionar valor de outro tipo
- **WHEN** o programa declara `l: lista de inteiro` e contém `l.adicionar("Ana")`
- **THEN** a execução para com erro de execução de mensagem `a lista só aceita valores do tipo inteiro; recebeu "Ana"`

#### Scenario: Atribuição por índice de outro tipo
- **WHEN** o programa declara `v: vetor[2] de cadeia` e contém `v[0] <- 5`
- **THEN** a execução para com erro de execução de mensagem `o vetor só aceita valores do tipo cadeia; recebeu 5`

#### Scenario: Inteiro aceito em coleção de real
- **WHEN** o programa declara `l: lista de real` e contém `l.adicionar(2)` e `escreva(l[0])`
- **THEN** a execução imprime `2.0`

#### Scenario: Lógico recusado em coleção de inteiro
- **WHEN** o programa declara `v: vetor[1] de inteiro` e contém `v[0] <- verdadeiro`
- **THEN** a execução para com erro de execução de mensagem `o vetor só aceita valores do tipo inteiro; recebeu verdadeiro`

#### Scenario: Real recusado em coleção de inteiro
- **WHEN** o programa declara `l: lista de inteiro` e contém `l.adicionar(2.5)`
- **THEN** a execução para com erro de execução de mensagem `a lista só aceita valores do tipo inteiro; recebeu 2.5`

#### Scenario: Verificação dentro de uma função
- **WHEN** o programa declara `l: lista de inteiro`, define `funcao poe(c) c.adicionar("x") fim_funcao` e contém `poe(l)`
- **THEN** a execução para com erro de execução de mensagem `a lista só aceita valores do tipo inteiro; recebeu "x"`

#### Scenario: Expandir com elemento de outro tipo não altera a lista
- **WHEN** o programa declara `l: lista de inteiro`, contém `l.adicionar(1)` e `l.expandir([2, "tres"])`, e o erro é capturado pelo teste
- **THEN** a execução para com erro de execução e `l` continua com um único elemento, `1`

### Requirement: Atribuição de uma coleção inteira
Atribuir um valor a uma variável declarada como `vetor[N] de T` ou `lista de T` (com `<-`, com `=` ou no valor inicial de um `var` local) SHALL seguir estas regras:
- se o valor for uma coleção tipada do mesmo tipo (mesmo `T` e, no vetor, mesmo `N`), a variável SHALL passar a se referir a essa mesma coleção, como acontece com `lista`;
- se o valor for outra lista (lista literal, `lista`, `novo lista()`, coleção tipada de outro tipo), a variável SHALL receber uma coleção nova do tipo declarado, com os mesmos elementos, cada um verificado pelas regras de tipo;
- no `vetor`, a lista atribuída SHALL ter exatamente `N` elementos. Senão, SHALL causar erro de execução com a mensagem `o vetor tem N posições, mas recebeu M elementos`;
- qualquer outro valor (número, texto, lógico, dicionário) SHALL causar erro de execução com a mensagem `o vetor só recebe uma lista de valores; recebeu V` (ou `a lista só recebe ...`).

#### Scenario: Vetor recebe lista literal
- **WHEN** o programa declara `notas: vetor[5] de inteiro` e contém `notas <- [8, 7, 9, 10, 6]` e `escreva(notas[0])`
- **THEN** a execução imprime `8`

#### Scenario: Lista tipada recebe novo lista
- **WHEN** o programa declara `l: lista de cadeia` e contém `l <- novo lista()`, `l.adicionar("Ana")` e `escreva(tamanho(l))`
- **THEN** a execução imprime `1`

#### Scenario: Coleção do mesmo tipo é compartilhada
- **WHEN** o programa declara `a, b: lista de inteiro` e contém `b <- a`, `a.adicionar(1)` e `escreva(tamanho(b))`
- **THEN** a execução imprime `1`

#### Scenario: Tamanho errado em atribuição ao vetor
- **WHEN** o programa declara `v: vetor[3] de inteiro`, define `funcao dois() retorne [1, 2] fim_funcao` e contém `v <- dois()`
- **THEN** a execução para com erro de execução de mensagem `o vetor tem 3 posições, mas recebeu 2 elementos`

#### Scenario: Valor que não é lista
- **WHEN** o programa declara `l: lista de inteiro`, define `funcao cinco() retorne 5 fim_funcao` e contém `l <- cinco()`
- **THEN** a execução para com erro de execução de mensagem `a lista só recebe uma lista de valores; recebeu 5`

### Requirement: Listas literais verificadas ao compilar
Quando o lado direito de uma atribuição a uma variável declarada como coleção tipada for uma lista literal formada só de literais simples, o analisador semântico SHALL verificar a lista antes da execução. Isso vale para atribuições com `<-` ou `=` e para o valor inicial de um `var` local. São literais simples: números, com ou sem `-` na frente, textos, `verdadeiro` e `falso` (quando esses nomes não foram declarados pelo programa).
- Um elemento que a coleção recusaria pelas regras de tipo SHALL causar erro semântico na linha e na coluna do elemento, com a mensagem `"nome" só aceita valores do tipo T; este valor é do tipo U`.
- Num `vetor[N]`, uma lista literal com quantidade de elementos diferente de `N` SHALL causar erro semântico na linha e na coluna do `[`, com a mensagem `o vetor "nome" tem N posições, mas a lista tem M elementos`.

Uma lista literal que contenha qualquer outra coisa (variável, chamada, expressão) SHALL ser deixada para a verificação na execução.

#### Scenario: Elemento literal de tipo errado
- **WHEN** o programa declara `notas: vetor[3] de inteiro` e a linha 5 é `notas <- [8, "sete", 9]`, com `"sete"` na coluna 14
- **THEN** a compilação falha com erro semântico na linha 5, coluna 14, com a mensagem `"notas" só aceita valores do tipo inteiro; este valor é do tipo cadeia`

#### Scenario: Quantidade errada em lista literal
- **WHEN** o programa declara `notas: vetor[5] de inteiro` e contém `notas <- [8, 7]`
- **THEN** a compilação falha com erro semântico na coluna do `[`, com a mensagem `o vetor "notas" tem 5 posições, mas a lista tem 2 elementos`

#### Scenario: Valor inicial de var local verificado
- **WHEN** o bloco `inicio` contém `var nomes: lista de cadeia <- ["Ana", 3]`
- **THEN** a compilação falha com erro semântico na linha e na coluna do `3`

#### Scenario: Lista com expressão fica para a execução
- **WHEN** o programa declara `v: vetor[2] de inteiro` e `x: inteiro`, e contém `v <- [x, x + 1]` e `escreva(v[1])`
- **THEN** a compilação tem sucesso e a execução imprime `1`

### Requirement: Faixa de índices das coleções tipadas
O acesso por índice a um `vetor` ou a uma `lista de T`, para ler ou para atribuir, SHALL aceitar só índices inteiros de `0` a `tamanho - 1`. Um índice fora dessa faixa, inclusive negativo, SHALL causar erro de execução com a mensagem `índice I fora do vetor de tamanho N (use de 0 a N-1)`, ou `índice I fora da lista de tamanho N (use de 0 a N-1)`, onde `N-1` aparece calculado. Numa lista vazia, a mensagem SHALL ser `índice I fora da lista vazia`.

#### Scenario: Leitura do último elemento
- **WHEN** o programa declara `v: vetor[3] de inteiro` e contém `v[2] <- 9` e `escreva(v[2])`
- **THEN** a execução imprime `9`

#### Scenario: Índice igual ao tamanho
- **WHEN** o programa declara `v: vetor[5] de inteiro` e contém `escreva(v[5])`
- **THEN** a execução para com erro de execução de mensagem `índice 5 fora do vetor de tamanho 5 (use de 0 a 4)`

#### Scenario: Índice negativo
- **WHEN** o programa declara `l: lista de inteiro` e contém `l.adicionar(1)` e `escreva(l[-1])`
- **THEN** a execução para com erro de execução de mensagem `índice -1 fora da lista de tamanho 1 (use de 0 a 0)`

#### Scenario: Percorrer um vetor com para
- **WHEN** o programa declara `v: vetor[3] de inteiro` e `i, soma: inteiro`, e contém `v <- [1, 2, 3]`, `para i de 0 ate tamanho(v) - 1 faca soma <- soma + v[i] fim_para` e `escreva(soma)`
- **THEN** a execução imprime `6`

### Requirement: Vetor tem tamanho fixo
Um `vetor` SHALL manter sempre o tamanho declarado. Os métodos que mudam o tamanho (`adicionar`, `adicionarFim`, `adicionarInicio`, `removerFim`, `removerInicio`, `expandir`, `limpar`, `inserir`, `remover` e `removerEm`) SHALL causar erro de execução com a mensagem `o vetor tem tamanho fixo e não aceita adicionar nem remover elementos`, sem alterar o vetor.

#### Scenario: Adicionar em vetor
- **WHEN** o programa declara `v: vetor[2] de inteiro` e contém `v.adicionar(1)`
- **THEN** a execução para com erro de execução de mensagem `o vetor tem tamanho fixo e não aceita adicionar nem remover elementos`

#### Scenario: Limpar vetor
- **WHEN** o programa declara `v: vetor[2] de inteiro` e contém `v.limpar()`
- **THEN** a execução para com erro de execução de mensagem `o vetor tem tamanho fixo e não aceita adicionar nem remover elementos`

### Requirement: Métodos das coleções tipadas
A `lista de T` SHALL ter os métodos da `lista` (`adicionar`, `adicionarFim`, `removerFim`, `expandir`, `limpar`, `tamanho`), com a verificação de tipo, e mais os métodos abaixo. O `vetor` SHALL ter `tamanho`, `buscar`, `contem` e `ordenar`. Os métodos SHALL funcionar como comando e dentro de uma expressão.

| Método | Onde | Comportamento |
|---|---|---|
| `inserir(p, v)` | lista de T | coloca `v` na posição `p` (de `0` a `tamanho`), empurrando os seguintes |
| `remover(v)` | lista de T | remove a primeira ocorrência de `v` |
| `removerEm(p)` | lista de T | remove e devolve o elemento da posição `p` |
| `buscar(v)` | lista de T, vetor | devolve a posição da primeira ocorrência de `v`, ou `-1` |
| `contem(v)` | lista de T, vetor | devolve `verdadeiro` se `v` estiver na coleção |
| `ordenar()` | lista de T, vetor | ordena os elementos do menor para o maior (textos em ordem alfabética, `falso` antes de `verdadeiro`) |
| `tamanho()` | lista de T, vetor | número de elementos |

`tamanho(x)` SHALL também devolver o número de elementos das duas coleções.

Erros de execução:
- `remover(v)` com `v` ausente: `o valor V não está na lista`;
- `inserir(p, v)` com `p` fora de `0` a `tamanho`: `posição P fora da lista de tamanho N (use de 0 a N)`;
- `removerEm(p)` com `p` fora de `0` a `tamanho - 1`: a mesma mensagem da faixa de índices;
- `removerFim()` numa lista tipada vazia: `a lista está vazia`.

Os métodos `inserir`, `remover`, `removerEm`, `buscar`, `contem` e `ordenar` não são adicionados à `lista` sem tipo. `inserir` e `remover` da `filaPrioridade` continuam com o comportamento atual.

#### Scenario: Exemplo da issue com lista de cadeia
- **WHEN** o programa declara `nomes: lista de cadeia` e contém `nomes.adicionar("Ana")`, `nomes.adicionar("Bruno")`, `nomes.remover("Ana")`, `escreva(nomes.tamanho())` e `escreva(nomes[0])`
- **THEN** a execução imprime `1` e depois `Bruno`

#### Scenario: Inserir em posição
- **WHEN** o programa declara `l: lista de inteiro` e contém `l <- [1, 3]`, `l.inserir(1, 2)` e `escreva(l)`
- **THEN** a execução imprime `[1, 2, 3]`

#### Scenario: Remover por posição em expressão
- **WHEN** o programa declara `l: lista de cadeia` e contém `l <- ["a", "b", "c"]`, `escreva(l.removerEm(1))` e `escreva(tamanho(l))`
- **THEN** a execução imprime `b` e depois `2`

#### Scenario: Buscar e contem
- **WHEN** o programa declara `v: vetor[3] de inteiro` e contém `v <- [4, 5, 6]`, `escreva(v.buscar(6))`, `escreva(v.buscar(9))` e `escreva(v.contem(5))`
- **THEN** a execução imprime `2`, `-1` e `verdadeiro`, um por linha

#### Scenario: Ordenar vetor
- **WHEN** o programa declara `v: vetor[4] de inteiro` e contém `v <- [3, 1, 4, 2]`, `v.ordenar()` e `escreva(v)`
- **THEN** a execução imprime `[1, 2, 3, 4]`

#### Scenario: Remover valor ausente
- **WHEN** o programa declara `l: lista de inteiro` e contém `l.remover(9)`
- **THEN** a execução para com erro de execução de mensagem `o valor 9 não está na lista`

#### Scenario: Inserir fora da faixa
- **WHEN** o programa declara `l: lista de inteiro` e contém `l.inserir(3, 1)`
- **THEN** a execução para com erro de execução de mensagem `posição 3 fora da lista de tamanho 0 (use de 0 a 0)`

#### Scenario: filaPrioridade não é afetada
- **WHEN** o programa declara `f: filaPrioridade` e contém `f.inserir(3)`, `f.inserir(1)` e `escreva(f.remover())`
- **THEN** a execução imprime `1`

### Requirement: leia não aceita coleção tipada
O comando `leia` sobre uma variável declarada como `vetor` ou `lista de T` SHALL causar erro semântico na linha e na coluna do nome, com a mensagem `leia não lê uma coleção inteira; leia um valor numa variável e guarde com nome[i] <- valor`, onde `nome` é substituído pelo nome da variável.

#### Scenario: leia em vetor
- **WHEN** o programa declara `v: vetor[3] de inteiro` e contém `leia(v)`
- **THEN** a compilação falha com erro semântico indicando a linha e a coluna de `v`
