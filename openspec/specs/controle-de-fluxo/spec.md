# controle-de-fluxo Specification

## Purpose

Define o comportamento das estruturas de controle do meuPiá (`se`/`senao`, `enquanto`, `para`, `continue`, `interrompa`) e garante que todo bloco, inclusive vazio, gere um programa executável.

## Requirements

### Requirement: Blocos vazios geram programa executável
O compilador SHALL gerar código executável quando qualquer bloco de comandos estiver vazio, sem nenhum comando ou só com comentários. Isso vale para: corpo de `se`, corpo de `senao`, corpo de `enquanto`, corpo de `para`, corpo de `funcao`, corpo de `metodo` e o bloco `inicio … fim_algoritmo`, com ou sem bloco `var`. Um bloco vazio SHALL não ter nenhum efeito na execução.

#### Scenario: Programa mínimo sem var e sem comandos
- **WHEN** o programa é `algoritmo "T"` seguido de `inicio` e `fim_algoritmo`
- **THEN** a compilação tem sucesso e a execução termina sem erro e sem imprimir nada

#### Scenario: `se` com corpo vazio
- **WHEN** o programa contém `x <- 1`, `se x > 0 entao fim_se` e `escreva("ok")`
- **THEN** a execução imprime `ok`

#### Scenario: `senao` vazio
- **WHEN** o programa contém `x <- 0`, `se x > 0 entao escreva("a") senao fim_se` e `escreva("ok")`
- **THEN** a execução imprime apenas `ok`

#### Scenario: Corpo de `se` só com comentário
- **WHEN** o programa contém `se verdadeiro entao`, depois `// nada`, depois `fim_se` e `escreva("ok")`
- **THEN** a execução imprime `ok`

#### Scenario: `enquanto` e `para` vazios
- **WHEN** o programa contém `enquanto falso faca fim_enquanto`, `para i de 1 ate 3 faca fim_para` e `escreva(i)`
- **THEN** a compilação tem sucesso e a execução imprime `3`

#### Scenario: Função vazia em programa sem var
- **WHEN** o programa, sem bloco `var`, define `funcao f() fim_funcao` e contém `f()` e `escreva("ok")`
- **THEN** a execução imprime `ok`

### Requirement: Limites e passo do `para` aceitam expressões
O compilador SHALL aceitar expressões aritméticas completas nos valores de `de`, `ate` e `passo` do laço `para`.

#### Scenario: Limite final com subtração
- **WHEN** o programa contém `n <- 3` e `para i de 0 ate n - 1 faca escreva(i) fim_para`
- **THEN** a execução imprime `0`, `1` e `2`, um por linha

#### Scenario: Limites com chamada de função
- **WHEN** o programa contém `l <- [5, 6, 7]` e `para i de 1 ate tamanho(l) - 1 faca escreva(l[i]) fim_para`
- **THEN** a execução imprime `6` e `7`, um por linha

### Requirement: Limite final do `para` inclusivo nos dois sentidos
O laço `para v de a ate b passo p` SHALL executar o corpo para cada valor de `v` começando em `a` e avançando de `p` em `p`, enquanto `v <= b` (se `p` > 0) ou `v >= b` (se `p` < 0). Isso vale também quando `p` é uma variável ou expressão cujo sinal só se conhece na execução. Sem `passo`, `p` SHALL valer 1.

#### Scenario: Passo negativo literal
- **WHEN** o programa contém `para i de 3 ate 1 passo -1 faca escreva(i) fim_para`
- **THEN** a execução imprime `3`, `2` e `1`, um por linha

#### Scenario: Passo negativo em variável
- **WHEN** o programa contém `p <- -2` e `para i de 6 ate 2 passo p faca escreva(i) fim_para`
- **THEN** a execução imprime `6`, `4` e `2`, um por linha

#### Scenario: Passo positivo maior que 1
- **WHEN** o programa contém `para i de 0 ate 6 passo 3 faca escreva(i) fim_para`
- **THEN** a execução imprime `0`, `3` e `6`, um por linha

#### Scenario: Intervalo vazio
- **WHEN** o programa contém `para i de 5 ate 1 faca escreva(i) fim_para` e `escreva("fim")`
- **THEN** a execução imprime apenas `fim`

### Requirement: `continue` e `interrompa` em laços
O comando `continue` SHALL pular para a próxima iteração do laço mais interno. O comando `interrompa` SHALL encerrar o laço mais interno.

#### Scenario: continue pula a iteração
- **WHEN** o programa contém `para i de 1 ate 3 faca se i = 2 entao continue fim_se escreva(i) fim_para`
- **THEN** a execução imprime `1` e `3`, um por linha

#### Scenario: interrompa encerra o laço
- **WHEN** o programa contém `para i de 1 ate 3 faca se i = 2 entao interrompa fim_se escreva(i) fim_para`
- **THEN** a execução imprime apenas `1`
