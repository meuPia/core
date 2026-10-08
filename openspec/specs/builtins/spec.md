# builtins Specification

## Purpose

Define as funções, constantes e métodos nativos do meuPiá (tamanho, matemática, coleções), o comando `escreva` e a regra que impede um builtin de sobrescrever um nome declarado pelo aluno.

## Requirements

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

### Requirement: Constantes builtin sem parênteses
A constante `pi` SHALL poder ser usada como valor, sem parênteses, quando o programa não declara um nome `pi`.

#### Scenario: escreva(pi)
- **WHEN** o programa contém `escreva(teto(pi))`
- **THEN** a compilação tem sucesso e a execução imprime `4`

### Requirement: tamanho funciona como função e como método
`tamanho(x)` e `x.tamanho()` SHALL retornar o número de elementos de `x` quando `x` for texto, lista, dicionário, filaDupla ou filaPrioridade.

#### Scenario: Método tamanho em filaDupla
- **WHEN** o programa contém `d <- filaDupla()`, `d.adicionarFim(1)`, `d.adicionarInicio(0)` e `escreva(d.tamanho())`
- **THEN** a execução imprime `2`

#### Scenario: Método tamanho em filaPrioridade
- **WHEN** o programa declara `f: filaPrioridade` e contém `f.inserir(5)` e `escreva(f.tamanho())`
- **THEN** a execução imprime `1`

#### Scenario: Função tamanho em filaPrioridade
- **WHEN** o programa declara `f: filaPrioridade` e contém `f.inserir(5)` e `escreva(tamanho(f))`
- **THEN** a execução imprime `1`

#### Scenario: Método tamanho em lista e texto
- **WHEN** o programa declara `s: cadeia` e contém `l <- [1, 2, 3]`, `s <- "ab"` e `escreva(l.tamanho() + s.tamanho())`
- **THEN** a execução imprime `5`

### Requirement: Métodos de coleção traduzidos
Os métodos abaixo SHALL ter o comportamento indicado, tanto usados como comando quanto dentro de uma expressão:

| Método | Comportamento |
|---|---|
| `adicionar(v)` e `adicionarFim(v)` | inserem no fim |
| `adicionarInicio(v)` | insere no início (filaDupla) |
| `removerFim()` | remove e retorna o último elemento |
| `removerInicio()` | remove e retorna o primeiro elemento (filaDupla) |
| `pegar(c)` | retorna o valor da chave `c` do dicionário, ou nulo se ela não existir |
| `atualizar(d)` | copia as chaves do dicionário `d` para o dicionário |
| `expandir(l)` | anexa todos os elementos de `l` |
| `limpar()` | remove todos os elementos |

#### Scenario: Remoção em expressão
- **WHEN** o programa contém `d <- filaDupla()`, `d.adicionarFim(1)`, `d.adicionarFim(2)` e `escreva(d.removerInicio() + d.removerFim())`
- **THEN** a execução imprime `3`

#### Scenario: pegar e atualizar em dicionário
- **WHEN** o programa declara `m: dicionario` e contém `m.atualizar({"a": 1})` e `escreva(m.pegar("a"))`
- **THEN** a execução imprime `1`

### Requirement: escreva com um ou mais argumentos
O comando `escreva` SHALL aceitar um ou mais argumentos separados por vírgula. Ele SHALL imprimir os argumentos concatenados sem separador, seguidos de uma quebra de linha. Valores lógicos SHALL aparecer como `verdadeiro` e `falso`.

#### Scenario: Vários argumentos
- **WHEN** o programa contém `x <- 5` e `escreva("x=", x)`
- **THEN** a execução imprime `x=5`

#### Scenario: Lógico em argumento único
- **WHEN** o programa contém `escreva(verdadeiro)`
- **THEN** a execução imprime `verdadeiro`

#### Scenario: Lógico entre vários argumentos
- **WHEN** o programa contém `escreva("ativo: ", falso)`
- **THEN** a execução imprime `ativo: falso`

#### Scenario: Concatenação com + continua funcionando
- **WHEN** o programa contém `n <- 2` e `escreva("n=" + n)`
- **THEN** a execução imprime `n=2`
