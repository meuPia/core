## ADDED Requirements

### Requirement: Tipos em qualquer combinação de maiúsculas e minúsculas
Os tipos `inteiro`, `real`, `float`, `string`, `cadeia`, `dicionario` e `filaPrioridade` SHALL ter o mesmo significado em qualquer combinação de maiúsculas e minúsculas: o mesmo valor inicial, a mesma conversão no `leia` e, nos que podem ser tipo de elemento, as mesmas regras de `lista de T` e `vetor[N] de T`. O mesmo vale para `dicionario` depois de `novo`.

#### Scenario: Valores iniciais com maiúsculas
- **WHEN** o programa declara `a: INTEIRO`, `r: Real`, `s: Cadeia` e `d: DICIONARIO` e contém `escreva(a + 1)`, `escreva(r)` e `escreva(tamanho(s), tamanho(d))`
- **THEN** a execução imprime `1`, `0.0` e `00`, um por linha

#### Scenario: leia em tipo com maiúsculas
- **WHEN** o programa declara `n: Inteiro`, contém `leia(n)` e `escreva(n + 1)`, e a entrada é `41`
- **THEN** a execução imprime `42`

#### Scenario: Declaração local com maiúsculas
- **WHEN** o bloco `inicio` contém `var x: Float` e `escreva(x)`
- **THEN** a execução imprime `0.0`

#### Scenario: Elemento de lista tipada com maiúsculas
- **WHEN** o programa declara `l: lista de Real` e contém `l.adicionar(2)` e `escreva(l)`
- **THEN** a execução imprime `[2.0]`

#### Scenario: novo Dicionario
- **WHEN** o programa declara `d: dicionario` e contém `d <- novo Dicionario()`, `d["a"] <- 1` e `escreva(tamanho(d))`
- **THEN** a execução imprime `1`
