## ADDED Requirements

### Requirement: filaPrioridade como função nativa
A chamada `filaPrioridade()`, sem `novo`, SHALL criar uma fila de prioridade vazia, independente das outras, como `novo filaPrioridade()`. Ela SHALL funcionar em qualquer posição em que uma expressão é aceita.

#### Scenario: Atribuição de filaPrioridade()
- **WHEN** o programa contém `f <- filaPrioridade()`, `f.inserir(3)`, `f.inserir(1)` e `escreva(f.remover())`
- **THEN** a execução imprime `1`

#### Scenario: filaPrioridade() dentro de expressão
- **WHEN** o programa contém `escreva(tamanho(filaPrioridade()))`
- **THEN** a execução imprime `0`

### Requirement: Métodos de classe com nome de método de coleção
Um método de classe do usuário cujo nome está na tabela de métodos de coleção (`adicionar`, `adicionarFim`, `adicionarInicio`, `removerFim`, `removerInicio`, `pegar`, `atualizar`, `expandir`, `limpar`, `tamanho`) SHALL ser executado pelas chamadas `objeto.nome(...)`, feitas de fora ou de dentro da classe (`self.nome(...)`). Um método `tamanho` SHALL também ser usado por `tamanho(objeto)`. Os métodos de lista, dicionário, fila dupla e fila de prioridade SHALL continuar com o comportamento da tabela.

#### Scenario: Classe com adicionar, removerFim e tamanho
- **WHEN** a classe `Pilha` define `adicionar(v)`, `removerFim()` e `tamanho()` sobre uma lista `self.itens`, e o programa contém `p <- novo Pilha()`, `p.adicionar(1)`, `p.adicionar(2)` e `escreva(p.removerFim(), p.tamanho())`
- **THEN** a execução imprime `21`

#### Scenario: tamanho nativo usa o método tamanho da classe
- **WHEN** o programa contém `p <- novo Pilha()`, `p.adicionar(7)` e `escreva(tamanho(p))`
- **THEN** a execução imprime `1`

#### Scenario: Listas continuam funcionando
- **WHEN** o programa contém `p <- novo Pilha()`, `l <- [1]`, `l.adicionar(2)`, `p.adicionar(3)` e `escreva(tamanho(l), p.tamanho())`
- **THEN** a execução imprime `21`

#### Scenario: Chamada de dentro da classe
- **WHEN** o `construtor` da classe `C` contém `self.n <- 0` e `self.adicionar(5)`, o método `adicionar(v)` contém `self.n <- self.n + v`, e o programa contém `c <- novo C()` e `escreva(c.n)`
- **THEN** a execução imprime `5`
