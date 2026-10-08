# analise-semantica Specification

## Purpose

Define quais nomes um programa pode usar em cada escopo (`inicio`, `funcao`, `metodo`), quais usos o compilador rejeita, e o formato padronizado das mensagens de erro de compilação mostradas ao aluno.

## Requirements

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

### Requirement: Classe depois do bloco var
Declarar uma `classe` depois de um bloco `var` SHALL encerrar esse bloco. Os identificadores dentro da classe (nomes de métodos, parâmetros, atributos) SHALL não ser registrados como variáveis globais.

#### Scenario: Classe com parâmetros repetidos entre métodos após var
- **WHEN** o programa declara `var p: inteiro`, depois define a classe `Pessoa` com `metodo construtor(nome) self.nome <- nome fim_funcao` e `metodo ola() escreva("oi " + self.nome) fim_funcao`, e contém `p <- novo Pessoa("Ana")` e `p.ola()`
- **THEN** a compilação tem sucesso e a execução imprime `oi Ana`

### Requirement: Nomes depois de ponto não são verificados como variáveis
Um identificador que aparece logo após `.` SHALL ser tratado como membro do objeto à esquerda (atributo ou método) e SHALL não ser verificado como variável declarada.

#### Scenario: Acesso a atributo sem chamada
- **WHEN** o programa declara `f: filaPrioridade` e contém `f.inserir(1)` e `escreva(f.heap)`
- **THEN** a compilação tem sucesso e a execução imprime `[1]`

#### Scenario: Atributo encadeado em self
- **WHEN** um método contém `self.pos.x <- 1`
- **THEN** a análise semântica não acusa `pos` nem `x`

### Requirement: Declaração duplicada
Declarar no bloco `var` um nome que já foi declarado SHALL causar erro semântico de declaração duplicada, indicando o nome, a linha e a coluna da segunda declaração.

#### Scenario: Variável declarada duas vezes
- **WHEN** o programa declara `x: inteiro` na linha 3 e `x: real` na linha 4, coluna 5
- **THEN** a compilação falha com erro semântico de declaração duplicada citando `x`, linha 4 e coluna 5

### Requirement: Formato padronizado das mensagens de erro
Toda falha de compilação SHALL produzir uma única mensagem em português do Brasil, no formato `Erro <etapa> na linha <L>, coluna <C>: <descrição>`. `<etapa>` SHALL ser `léxico`, `sintático` ou `semântico`. `<L>` e `<C>` são a linha e a coluna (contadas a partir de 1) do trecho do `.por` que causou o erro. Quando o erro acontece no fim do arquivo, `<L>` e `<C>` SHALL indicar o último trecho lido. Quando o arquivo não tem nenhum trecho, SHALL indicar linha 1, coluna 1. A mensagem SHALL não conter texto em inglês nem nomes internos de tokens.

#### Scenario: Erro léxico
- **WHEN** a linha 3 do programa é `x <- 7 $ 2`, com `$` na coluna 8
- **THEN** a mensagem é `Erro léxico na linha 3, coluna 8: …`, com uma descrição que cita o caractere `$`

#### Scenario: Erro sintático no fim do arquivo
- **WHEN** o programa termina sem `fim_algoritmo`
- **THEN** a mensagem começa com `Erro sintático na linha` e indica a posição do último trecho do arquivo

#### Scenario: Arquivo vazio
- **WHEN** o arquivo `.por` está vazio
- **THEN** a mensagem é `Erro sintático na linha 1, coluna 1: …`, e não uma exceção interna do compilador

#### Scenario: Erro semântico sem nomes internos
- **WHEN** o programa usa uma variável `y` não declarada
- **THEN** a mensagem começa com `Erro semântico na linha` e não contém as palavras `Undeclared`, `identifier`, `ID` nem `ATR`
