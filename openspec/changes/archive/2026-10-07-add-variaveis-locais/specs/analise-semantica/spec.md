## MODIFIED Requirements

### Requirement: Nomes válidos em cada escopo
Dentro de `inicio`, o compilador SHALL aceitar como nome todo identificador que seja:
- variável do bloco `var` global;
- variável local declarada no `inicio` em uma linha anterior;
- nome de `funcao` ou de `classe`;
- builtin;
- chamada de função (com parênteses).

Dentro de `funcao` ou `metodo`, SHALL aceitar a variável global, o nome de `funcao` ou `classe`, o builtin e a chamada de função, além dos parâmetros e das variáveis locais declaradas naquele mesmo corpo em uma linha anterior. Dentro de `metodo`, `self` também é aceito. Variáveis locais do `inicio` e de outros corpos SHALL não ser aceitas.

Fora desses casos, um identificador SHALL causar erro semântico de variável não declarada.

#### Scenario: Variável não declarada em inicio
- **WHEN** o programa não declara `y` e contém `escreva(y)` na linha 4, coluna 13
- **THEN** a compilação falha com erro semântico citando `y`, linha 4 e coluna 13

#### Scenario: Parâmetro de método é local
- **WHEN** o programa define `classe P metodo construtor(nome) self.nome <- nome fim_funcao fim_classe`
- **THEN** a análise semântica aceita `nome` e `self` dentro do método

#### Scenario: Variável não declarada dentro de método
- **WHEN** o programa define `classe P metodo m() escreva(zzz) fim_funcao fim_classe`
- **THEN** a compilação falha com erro semântico citando `zzz`

#### Scenario: Variável local aceita depois da declaração
- **WHEN** uma função contém `var t: inteiro <- 1` e, depois, `retorne t + 1`
- **THEN** a análise semântica aceita `t`

#### Scenario: Var local não vira global
- **WHEN** uma função declara `var t: inteiro` e o `inicio` contém `escreva(t)`
- **THEN** a compilação falha com erro semântico citando `t`
