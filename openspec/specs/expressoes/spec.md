# expressoes Specification

## Purpose

Define como o meuPiá avalia expressões aritméticas, relacionais e lógicas: quais operadores existem, a precedência entre eles e o significado de `=`, `==` e `<-` conforme o contexto.

Nos cenários abaixo, "o programa" é um algoritmo completo com as variáveis usadas declaradas em `var`. "Imprime" se refere à saída padrão produzida ao executar o código gerado.

## Requirements

### Requirement: Comparação entre expressões aritméticas completas
O compilador SHALL aceitar expressões aritméticas completas, incluindo operadores, parênteses, menos unário, chamadas de função, indexação e acesso a membros, nos dois lados de um operador relacional (`=`, `==`, `<>`, `!=`, `<`, `>`, `<=`, `>=`).

#### Scenario: Soma no lado esquerdo
- **WHEN** o programa contém `x <- 0` e `se x + 1 > 0 entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Expressão entre parênteses
- **WHEN** o programa contém `x <- 0` e `se (x + 1) > 0 entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Literal negativo no lado direito
- **WHEN** o programa contém `x <- 0` e `se x > -1 entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Menos unário no lado esquerdo
- **WHEN** o programa contém `x <- 2` e `se -x < 0 entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Chamada de função e indexação nos dois lados
- **WHEN** o programa contém `l <- [3, 1]` e `se tamanho(l) * 2 >= l[0] + l[1] entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

### Requirement: Condição sem operador relacional
O compilador SHALL aceitar como condição de `se` e `enquanto` qualquer expressão, com ou sem operador relacional: literal lógico, variável, chamada de função ou negação com `nao`.

#### Scenario: Literal lógico
- **WHEN** o programa contém `se verdadeiro entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Variável lógica
- **WHEN** o programa declara `b: logico` e contém `b <- verdadeiro` e `se b entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Chamada de função com nao
- **WHEN** o programa define `funcao vazio(l) retorne tamanho(l) = 0 fim_funcao` e contém `l <- [1]` e `enquanto nao vazio(l) faca l.removerFim() fim_enquanto` e `escreva(tamanho(l))`
- **THEN** a compilação tem sucesso e a execução imprime `0`

### Requirement: Significado de `=`, `==` e `<-` conforme o contexto
O compilador SHALL tratar `<-` e `=` como atribuição quando aparecem logo após o alvo de um comando. Dentro de uma expressão, SHALL tratar `=` e `==` como comparação de igualdade. `<-` dentro de uma expressão SHALL ser um erro sintático.

#### Scenario: Atribuição com `<-` e com `=`
- **WHEN** o programa contém `x <- 1`, `n = 2` e `escreva(x + n)`
- **THEN** a execução imprime `3`

#### Scenario: Igualdade com `=` e com `==`
- **WHEN** o programa contém `x <- 1`, `se x = 1 entao escreva("a") fim_se` e `se x == 1 entao escreva("b") fim_se`
- **THEN** a execução imprime `a` e depois `b`

#### Scenario: Igualdade como valor atribuído
- **WHEN** o programa declara `b: logico` e contém `x <- 1`, `b <- x = 1` e `escreva(b)`
- **THEN** a execução imprime `verdadeiro`

#### Scenario: Seta dentro de condição é rejeitada
- **WHEN** o programa contém `se x <- 1 entao fim_se`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna do `<-`

### Requirement: Operador de diferença `!=`
O compilador SHALL aceitar `!=` como sinônimo exato de `<>`.

#### Scenario: Diferença com `!=`
- **WHEN** o programa contém `x <- 0` e `se x != 1 entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

#### Scenario: Diferença com `<>` continua funcionando
- **WHEN** o programa contém `x <- 0` e `se x <> 1 entao escreva("ok") fim_se`
- **THEN** a compilação tem sucesso e a execução imprime `ok`

### Requirement: Operador de resto `%` e `mod`
O compilador SHALL aceitar `%` e a palavra-chave `mod` como operador de resto da divisão, com a mesma precedência de `*` e `/`.

#### Scenario: Resto com `%`
- **WHEN** o programa contém `x <- 7 % 2` e `escreva(x)`
- **THEN** a execução imprime `1`

#### Scenario: Resto com `mod`
- **WHEN** o programa contém `x <- 7 mod 3` e `escreva(x)`
- **THEN** a execução imprime `1`

#### Scenario: Precedência igual à da multiplicação
- **WHEN** o programa contém `x <- 1 + 7 mod 3 * 2` e `escreva(x)`
- **THEN** a execução imprime `3`

### Requirement: Precedência dos operadores
O compilador SHALL avaliar os operadores nesta ordem, da maior para a menor precedência:
1. menos unário;
2. `*` `/` `%` `mod`;
3. `+` `-`;
4. relacionais;
5. `nao`;
6. `e`;
7. `ou`.

Parênteses SHALL sobrepor essa ordem.

#### Scenario: `e` antes de `ou`
- **WHEN** o programa contém `se verdadeiro ou falso e falso entao escreva("ok") fim_se`
- **THEN** a execução imprime `ok`

#### Scenario: `nao` aplicado a uma comparação
- **WHEN** o programa contém `x <- 5` e `se nao x > 10 entao escreva("ok") fim_se`
- **THEN** a execução imprime `ok`

#### Scenario: Parênteses mudando a precedência
- **WHEN** o programa contém `x <- (1 + 2) * 3` e `escreva(x)`
- **THEN** a execução imprime `9`
