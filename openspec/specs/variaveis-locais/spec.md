# variaveis-locais Specification

## Purpose

Permite declarar com `var` variáveis visíveis só dentro do corpo de uma `funcao`, de um `metodo` ou do bloco `inicio`, para que o aluno guarde resultados intermediários sem criar variáveis globais.

Nos cenários, "corpo" é o trecho entre o cabeçalho e `fim_funcao` (em `funcao` e `metodo`) ou entre `inicio` e `fim_algoritmo`. "Imprime" é a saída padrão da execução do código gerado.

## Requirements

### Requirement: Sintaxe da declaração local
Uma declaração local SHALL começar com `var`, seguida de uma ou mais linhas de declaração. Cada linha SHALL ter a forma `nome1, nome2, …: tipo`, em que `tipo` é um dos tipos aceitos no bloco `var` global (incluindo os contextuais `lista` e `logico`).

Uma linha com **um único nome** SHALL aceitar, opcionalmente, `<- expressão` ou `= expressão` no fim, e nesse caso a variável começa com o valor da expressão. Sem expressão, a variável SHALL começar com o valor inicial do seu tipo, o mesmo das variáveis globais.

Uma linha com mais de um nome seguida de expressão SHALL causar erro sintático. A declaração termina na primeira linha que não seja uma declaração.

#### Scenario: Forma com valor
- **WHEN** o programa define `funcao dobro(a) var r: inteiro <- a * 2 retorne r fim_funcao` e contém `escreva(dobro(4))`
- **THEN** a execução imprime `8`

#### Scenario: Valor com `=`
- **WHEN** o programa define `funcao f() var t: cadeia = "oi" retorne t fim_funcao` e contém `escreva(f())`
- **THEN** a execução imprime `oi`

#### Scenario: Forma de bloco com valor inicial do tipo
- **WHEN** uma função contém `var` seguido das linhas `soma, contador: inteiro` e `nomes: lista`, e depois `escreva(soma + contador, tamanho(nomes))`
- **THEN** a chamada imprime `00`

#### Scenario: Formas misturadas no mesmo var
- **WHEN** uma função contém `var` seguido das linhas `a: inteiro <- 5` e `b, c: real`, e depois `escreva(a + b + c)`
- **THEN** a chamada imprime `5.0`

#### Scenario: Várias declarações var na mesma função
- **WHEN** uma função contém `var x: inteiro <- 1`, depois `x <- x + 1`, depois `var y: inteiro <- x * 10` e `retorne y`
- **THEN** a função retorna `20`

#### Scenario: Valor com mais de um nome
- **WHEN** uma função contém `var a, b: inteiro <- 0`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna do `<-`

#### Scenario: Tipo desconhecido em declaração local
- **WHEN** uma função contém `var x: numero`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna de `numero`

### Requirement: Posições permitidas para a declaração local
A declaração local SHALL ser aceita em qualquer ponto do nível principal do corpo de `funcao`, de `metodo` e do bloco `inicio`, antes ou depois de outros comandos. Dentro do corpo de `se`, `senao`, `enquanto` ou `para`, `var` SHALL causar erro sintático informando que variáveis devem ser declaradas fora desses blocos.

#### Scenario: Declaração no inicio depois de comandos
- **WHEN** o bloco `inicio` contém `escreva("a")`, depois `var n: inteiro <- 2` e `escreva(n)`
- **THEN** a execução imprime `a` e depois `2`

#### Scenario: Declaração em método
- **WHEN** a classe `C` tem `metodo calc(x) var y: inteiro <- x + 1 retorne y fim_funcao`, e o programa contém `c <- novo C()` e `escreva(c.calc(1))`
- **THEN** a execução imprime `2`

#### Scenario: Declaração dentro de se
- **WHEN** uma função contém `se verdadeiro entao var x: inteiro <- 1 fim_se`
- **THEN** a compilação falha com erro sintático na linha e na coluna do `var`, com uma mensagem informando que variáveis devem ser declaradas fora de `se`, `enquanto` e `para`

#### Scenario: Declaração dentro de laço
- **WHEN** o bloco `inicio` contém `para i de 1 ate 2 faca var x: inteiro fim_para`
- **THEN** a compilação falha com erro sintático na linha e na coluna do `var`

#### Scenario: Var no inicio como no codigoTeste dos desafios
- **WHEN** o bloco `inicio` contém `escreva("x")`, depois `var legado, sus: dicionario`, depois `var resultado: inteiro`, e então `legado <- {"a": 1}` e `escreva(tamanho(legado))`
- **THEN** a compilação tem sucesso e a execução imprime `x` e depois `1`

### Requirement: Escopo da variável local
Uma variável local SHALL ser visível apenas no corpo em que foi declarada, a partir da linha da sua declaração até o fim desse corpo. Ela SHALL não ser visível em outras funções, em outros métodos nem, quando declarada no `inicio`, dentro de funções e métodos.

#### Scenario: Local de uma função não é visível em outra
- **WHEN** o programa define `funcao a() var t: inteiro <- 1 retorne t fim_funcao` e `funcao b() retorne t fim_funcao`
- **THEN** a compilação falha com erro semântico citando `t` na função `b`

#### Scenario: Local do inicio não é visível em função
- **WHEN** o programa define `funcao f() retorne k fim_funcao` e o `inicio` contém `var k: inteiro <- 1` e `escreva(f())`
- **THEN** a compilação falha com erro semântico citando `k`

#### Scenario: Mesmo nome local em funções diferentes
- **WHEN** o programa define `funcao a() var t: inteiro <- 1 retorne t fim_funcao` e `funcao b() var t: inteiro <- 2 retorne t fim_funcao`, e contém `escreva(a() + b())`
- **THEN** a execução imprime `3`

### Requirement: Tempo de vida da variável local
Cada execução do corpo SHALL criar novas variáveis locais, inicializadas de novo pela declaração. Valores de uma chamada SHALL não ser vistos por outra chamada da mesma função, inclusive em chamadas recursivas, e SHALL não alterar variáveis globais.

#### Scenario: Recursão com variável local
- **WHEN** o programa define `funcao fat(n) var r: inteiro <- 1 se n > 1 entao r <- n * fat(n - 1) fim_se retorne r fim_funcao` e contém `escreva(fat(5))`
- **THEN** a execução imprime `120`

#### Scenario: Local reinicializada a cada chamada
- **WHEN** o programa define `funcao conta() var c: inteiro c <- c + 1 retorne c fim_funcao` e contém `escreva(conta(), conta())`
- **THEN** a execução imprime `11`

### Requirement: Conflitos de nome com variável local
Declarar uma variável local SHALL causar erro semântico quando o nome já for:
- uma variável global;
- um parâmetro do mesmo corpo;
- `self` dentro de método;
- outra variável local do mesmo corpo;
- o nome de uma `funcao` ou `classe`.

A mensagem SHALL citar o nome e indicar a linha e a coluna da declaração local.

#### Scenario: Local com nome de global
- **WHEN** o programa declara a global `x: inteiro` e uma função contém `var x: inteiro <- 1`
- **THEN** a compilação falha com erro semântico citando `x`, na linha e na coluna da declaração local

#### Scenario: Local com nome de parâmetro
- **WHEN** o programa define `funcao f(a) var a: inteiro fim_funcao`
- **THEN** a compilação falha com erro semântico citando `a`

#### Scenario: Local declarada duas vezes no mesmo corpo
- **WHEN** uma função contém `var t: inteiro` e, mais adiante, `var t: real`
- **THEN** a compilação falha com erro semântico citando `t`, na linha e na coluna da segunda declaração

#### Scenario: Local com nome de função
- **WHEN** o programa define `funcao g() retorne 1 fim_funcao` e o `inicio` contém `var g: inteiro`
- **THEN** a compilação falha com erro semântico citando `g`

### Requirement: Uso antes da declaração
Usar uma variável local antes da linha da sua declaração, no mesmo corpo, SHALL causar erro semântico com uma mensagem própria, informando que a variável foi usada antes de ser declarada, com a linha e a coluna do uso.

#### Scenario: Uso antes do var
- **WHEN** uma função contém `escreva(t)` e, na linha seguinte, `var t: inteiro <- 1`
- **THEN** a compilação falha com erro semântico informando que `t` foi usada antes de ser declarada, na linha e na coluna do `escreva(t)`

### Requirement: Leitura de variável local
O comando `leia` sobre uma variável local SHALL converter a entrada pelo tipo declarado, com as mesmas regras das variáveis globais.

#### Scenario: leia em local inteira
- **WHEN** o `inicio` contém `var n: inteiro`, `leia(n)` e `escreva(n + 1)`, e a entrada é `41`
- **THEN** a execução imprime `42`

#### Scenario: leia em local lógica
- **WHEN** uma função contém `var b: logico`, `leia(b)` e `retorne b`, o `inicio` contém `escreva(f())`, e a entrada é `verdadeiro`
- **THEN** a execução imprime `verdadeiro`
