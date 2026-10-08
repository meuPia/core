## Purpose

Define os tipos que podem ser declarados no bloco `var`, o valor inicial de cada um, a criação de coleções nativas com `novo` e a forma dos literais de string.

## ADDED Requirements

### Requirement: Tipos declaráveis e valores iniciais
O compilador SHALL aceitar os tipos abaixo no bloco `var` e SHALL inicializar cada variável declarada com o valor indicado antes do primeiro comando de `inicio`:

| Tipo | Valor inicial |
|---|---|
| `inteiro` | `0` |
| `real` ou `float` | `0.0` |
| `string` ou `cadeia` | texto vazio |
| `logico` | `falso` |
| `lista` | lista vazia |
| `dicionario` | dicionário vazio |
| `filaPrioridade` (qualquer combinação de maiúsculas e minúsculas) | fila de prioridade vazia |

Um tipo fora dessa lista SHALL causar erro sintático.

#### Scenario: Valor inicial de logico
- **WHEN** o programa declara `b: logico` e contém `escreva(b)`
- **THEN** a execução imprime `falso`

#### Scenario: Valor inicial de lista
- **WHEN** o programa declara `l: lista` e contém `l.adicionar(1)` e `escreva(tamanho(l))`
- **THEN** a execução imprime `1`

#### Scenario: Valores iniciais numéricos e de texto
- **WHEN** o programa declara `n: inteiro`, `r: real` e `s: cadeia` e contém `escreva(n + r)` e `escreva(tamanho(s))`
- **THEN** a execução imprime `0.0` e `0`, um por linha

#### Scenario: Tipo desconhecido
- **WHEN** o programa declara `x: numero`
- **THEN** a compilação falha com erro sintático indicando a linha e a coluna de `numero`

### Requirement: `lista` e `logico` não são palavras reservadas
Os nomes `lista` e `logico` SHALL funcionar como tipo apenas na posição de tipo de uma declaração do bloco `var` (depois de `:`) e logo depois de `novo`. Em qualquer outra posição, SHALL funcionar como identificadores comuns. Assim, um programa pode declarar e usar uma variável chamada `lista` ou `logico`.

#### Scenario: Variável chamada lista
- **WHEN** o programa declara `lista: inteiro` e contém `lista <- 5` e `escreva(lista)`
- **THEN** a compilação tem sucesso e a execução imprime `5`

#### Scenario: Variável chamada lista com tipo lista
- **WHEN** o programa declara `lista: lista` e contém `lista.adicionar(1)` e `escreva(tamanho(lista))`
- **THEN** a execução imprime `1`

#### Scenario: Vários tipos lista no mesmo bloco var
- **WHEN** o programa declara `a: lista` e `b: lista` em linhas separadas
- **THEN** a compilação tem sucesso, sem erro de declaração duplicada

### Requirement: Leitura de logico
O comando `leia` sobre uma variável `logico` SHALL atribuir `verdadeiro` quando o texto lido, sem espaços nas pontas e ignorando maiúsculas e minúsculas, for `verdadeiro`. Para qualquer outro texto, SHALL atribuir `falso`.

#### Scenario: Leitura de verdadeiro
- **WHEN** o programa declara `b: logico`, contém `leia(b)` e `escreva(b)`, e a entrada é `Verdadeiro`
- **THEN** a execução imprime `verdadeiro`

#### Scenario: Leitura de outro texto
- **WHEN** o programa declara `b: logico`, contém `leia(b)` e `escreva(b)`, e a entrada é `sim`
- **THEN** a execução imprime `falso`

### Requirement: Criação de coleções nativas com novo
A expressão `novo T()`, onde `T` é `dicionario`, `lista` ou `filaPrioridade`, SHALL produzir uma nova coleção vazia desse tipo, independente das outras já existentes.

#### Scenario: novo dicionario
- **WHEN** o programa declara `d: dicionario` e contém `d <- novo dicionario()`, `d["a"] <- 1` e `escreva(tamanho(d))`
- **THEN** a execução imprime `1`

#### Scenario: novo lista
- **WHEN** o programa declara `a, b: lista` e contém `a <- novo lista()`, `b <- novo lista()`, `a.adicionar(1)` e `escreva(tamanho(b))`
- **THEN** a execução imprime `0`

#### Scenario: novo filaPrioridade continua funcionando
- **WHEN** o programa declara `f: filaPrioridade` e contém `f <- novo filaPrioridade()`, `f.inserir(3)`, `f.inserir(1)` e `escreva(f.remover())`
- **THEN** a execução imprime `1`

### Requirement: Literais de string com barra invertida
Um literal de string SHALL terminar na primeira aspa dupla que não estiver escapada. Uma aspa é escapada quando é precedida por um número ímpar de barras invertidas consecutivas. Uma string sem aspa de fechamento na mesma linha SHALL causar erro léxico indicando a linha e a coluna da aspa de abertura.

#### Scenario: String terminada em barra invertida
- **WHEN** o programa contém `escreva("a\\")`
- **THEN** a compilação tem sucesso e a execução imprime `a\`

#### Scenario: Aspa escapada dentro da string
- **WHEN** o programa contém `escreva("diga \"oi\"")`
- **THEN** a execução imprime `diga "oi"`

#### Scenario: String não terminada
- **WHEN** a linha 3 do programa é `escreva("abc)`, com a aspa de abertura na coluna 9
- **THEN** a compilação falha com erro léxico indicando linha 3, coluna 9
