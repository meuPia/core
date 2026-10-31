## Why

A referência técnica do dialeto (`docs/referencia-do-dialeto.md`) foi escrita executando o compilador 1.3.0 e encontrou três bugs. Os três compilam sem erro e falham só na execução, ou com um resultado errado sem nenhum erro:

1. Tipos escritos com maiúsculas (`a: INTEIRO`, `r: Real`) são aceitos pelo lexer, mas a variável começa como texto vazio e o `leia` lê texto.
2. `filaPrioridade()` sem `novo` é sempre erro sintático, porque o lexer lê o nome como tipo. A entrada `filaPrioridade` em `FUNCOES_BUILTIN` nunca é alcançada, embora a spec `builtins` a liste.
3. Um método de classe do usuário com nome de método de coleção (`adicionar`, `removerFim`, `tamanho`...) é definido com esse nome, mas toda chamada `obj.adicionar(...)` é traduzida para `append`. O programa falha com `AttributeError`.

## What Changes

- **Tipos em qualquer caixa:** os tipos que são palavras-chave (`inteiro`, `real`, `float`, `string`, `cadeia`, `dicionario`, `filaPrioridade`) passam a ter o mesmo valor inicial e a mesma leitura pelo `leia` em qualquer combinação de maiúsculas e minúsculas, também como tipo de elemento de `lista de T` e `vetor[N] de T` e em `novo Dicionario()`.
- **`filaPrioridade()`:** passa a criar uma fila de prioridade vazia, como `novo filaPrioridade()`.
- **Métodos de classe:** um método declarado com nome de método de coleção passa a ser encontrado pelas chamadas `obj.nome(...)`, inclusive de dentro da própria classe. As listas, dicionários e filas continuam com o comportamento atual.
- **Novo erro semântico:** dois métodos da mesma classe com o mesmo nome, ou com nomes sinônimos (`adicionar` e `adicionarFim`), passam a ser recusados na compilação. Hoje o segundo apagaria o primeiro em silêncio.

## Capabilities

### Modified Capabilities
- `tipos-e-declaracoes`: tipos aceitos em qualquer caixa.
- `builtins`: `filaPrioridade()` como função e métodos de classe com nome de método de coleção.
- `analise-semantica`: métodos repetidos na mesma classe.

## Impact

- **Código:**
  - `meuPia/analyzers/syntax_analyzer.py`: tipo e tipo de elemento em minúsculas; `filaPrioridade(...)` como expressão.
  - `meuPia/analyzers/code_generator.py`: tradução do nome do método na definição; `novo Dicionario()`.
  - `meuPia/analyzers/semantic_analyzer.py`: verificação de métodos repetidos.
- **Testes:** `test_tipos.py`, `test_builtins.py`, `test_analise_semantica.py`.
- **Compatibilidade:** o Python gerado para os exemplos do repositório e os 14 desafios é idêntico ao da versão anterior. Um programa que já tivesse dois métodos sinônimos na mesma classe passa a dar erro de compilação; antes ele perdia um dos métodos sem aviso.
- **Fora de escopo:** `lista`, `logico` e `vetor` continuam valendo como tipo só em minúsculas (item 2 da seção 16 da referência).
