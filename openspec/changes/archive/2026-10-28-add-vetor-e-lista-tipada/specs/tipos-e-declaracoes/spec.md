## MODIFIED Requirements

### Requirement: Tipos declaráveis e valores iniciais
O compilador SHALL aceitar os tipos abaixo no bloco `var` e SHALL inicializar cada variável declarada com o valor indicado antes do primeiro comando de `inicio`:

| Tipo | Valor inicial |
|---|---|
| `inteiro` | `0` |
| `real` ou `float` | `0.0` |
| `string` ou `cadeia` | texto vazio |
| `logico` | `falso` |
| `lista` | lista vazia |
| `lista de T` | lista vazia que só aceita elementos do tipo `T` |
| `vetor[N] de T` | `N` elementos iguais ao valor inicial de `T` |
| `dicionario` | dicionário vazio |
| `filaPrioridade` (qualquer combinação de maiúsculas e minúsculas) | fila de prioridade vazia |

As regras de `lista de T` e `vetor[N] de T` estão na capability `colecoes-tipadas`. Um tipo fora dessa lista SHALL causar erro sintático.

#### Scenario: Valor inicial de logico
- **WHEN** o programa declara `b: logico` e contém `escreva(b)`
- **THEN** a execução imprime `falso`

#### Scenario: Valor inicial de lista
- **WHEN** o programa declara `l: lista` e contém `l.adicionar(1)` e `escreva(tamanho(l))`
- **THEN** a execução imprime `1`

#### Scenario: Valores iniciais numéricos e de texto
- **WHEN** o programa declara `n: inteiro`, `r: real` e `s: cadeia` e contém `escreva(n + r)` e `escreva(tamanho(s))`
- **THEN** a execução imprime `0.0` e `0`, um por linha

#### Scenario: Valor inicial de vetor
- **WHEN** o programa declara `v: vetor[2] de real` e contém `escreva(v)`
- **THEN** a execução imprime `[0.0, 0.0]`

#### Scenario: Tipo desconhecido
- **WHEN** o programa declara `x: numero`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna de `numero`

### Requirement: `lista` e `logico` não são palavras reservadas
Os nomes `lista`, `logico` e `vetor` SHALL funcionar como tipo apenas na posição de tipo de uma declaração (depois de `:`). `lista` SHALL funcionar como tipo também logo depois de `novo`. Em qualquer outra posição, os três SHALL funcionar como identificadores comuns. Assim, um programa pode declarar e usar uma variável chamada `lista`, `logico` ou `vetor`.

#### Scenario: Variável chamada lista
- **WHEN** o programa declara `lista: inteiro` e contém `lista <- 5` e `escreva(lista)`
- **THEN** a compilação tem sucesso e a execução imprime `5`

#### Scenario: Variável chamada lista com tipo lista
- **WHEN** o programa declara `lista: lista` e contém `lista.adicionar(1)` e `escreva(tamanho(lista))`
- **THEN** a execução imprime `1`

#### Scenario: Vários tipos lista no mesmo bloco var
- **WHEN** o programa declara `a: lista` e `b: lista` em linhas separadas
- **THEN** a compilação tem sucesso, sem erro de declaração duplicada

#### Scenario: Variável chamada vetor
- **WHEN** o programa declara `vetor: lista` e contém `vetor.adicionar(1)` e `escreva(tamanho(vetor))`
- **THEN** a compilação tem sucesso e a execução imprime `1`

#### Scenario: Variável chamada vetor com tipo vetor
- **WHEN** o programa declara `vetor: vetor[2] de inteiro` e contém `vetor[1] <- 4` e `escreva(vetor[1])`
- **THEN** a execução imprime `4`
