## ADDED Requirements

### Requirement: Métodos repetidos na mesma classe
Declarar numa mesma classe dois métodos com o mesmo nome SHALL causar erro semântico na linha e na coluna do nome do segundo método, com a mensagem `o método "m" foi declarado mais de uma vez na classe "C"`. Declarar dois métodos com nomes sinônimos na tabela de métodos de coleção (como `adicionar` e `adicionarFim`) SHALL causar erro semântico na mesma posição, com a mensagem `os métodos "adicionar" e "adicionarFim" são o mesmo método no meuPiá; escolha outro nome para um deles`. Classes diferentes SHALL poder ter métodos com o mesmo nome.

#### Scenario: Métodos sinônimos
- **WHEN** a classe `C` define `metodo adicionar(v)` e, na linha 5, `metodo adicionarFim(v)`, com o nome na coluna 8
- **THEN** a compilação falha com erro semântico na linha 5, coluna 8, citando `"adicionar"` e `"adicionarFim"`

#### Scenario: Método declarado duas vezes
- **WHEN** a classe `C` define `metodo m()` duas vezes, a segunda na linha 5
- **THEN** a compilação falha com erro semântico na linha 5, coluna 8, citando `"m"`

#### Scenario: Mesmo método em classes diferentes
- **WHEN** a classe `A` define `metodo adicionar(v)` e a classe `B` define `metodo adicionarFim(v)`
- **THEN** a compilação tem sucesso
