## MODIFIED Requirements

### Requirement: Nomes declarados pelo usuário têm prioridade sobre builtins
Um nome declarado pelo programa SHALL sempre se referir à declaração do usuário em todo o programa, mesmo quando coincide com um builtin. Contam como declaração: variável do bloco `var` global, variável local declarada com `var` em `funcao`, `metodo` ou `inicio`, parâmetro de `funcao` ou `metodo`, nome de `funcao` e nome de `classe`. O builtin com esse nome fica indisponível no programa. Os builtins cobertos por esta regra são `tamanho`, `raiz`, `potencia`, `seno`, `cosseno`, `tangente`, `teto`, `piso`, `pi`, `absoluto`, `verdadeiro`, `falso`, `filaDupla` e `filaPrioridade`.

#### Scenario: Variável chamada pi
- **WHEN** o programa declara `pi: inteiro` e contém `pi <- 3` e `escreva(pi)`
- **THEN** a execução imprime `3`

#### Scenario: Função do usuário chamada raiz
- **WHEN** o programa define `funcao raiz(x) retorne x + 1 fim_funcao` e contém `escreva(raiz(9))`
- **THEN** a execução imprime `10`

#### Scenario: Parâmetro chamado teto
- **WHEN** o programa define `funcao limite(teto) retorne teto fim_funcao` e contém `escreva(limite(7))`
- **THEN** a execução imprime `7`

#### Scenario: Builtin disponível quando não há conflito
- **WHEN** o programa não declara `raiz` e contém `escreva(raiz(9))`
- **THEN** a execução imprime `3.0`

#### Scenario: Variável local chamada piso
- **WHEN** uma função contém `var piso: inteiro <- 2` e `retorne piso`, e o programa contém `escreva(f())`
- **THEN** a execução imprime `2`
