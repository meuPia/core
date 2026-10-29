## Why

A issue meuPia/core#6 pede coleções com tipo: um **Array** de tamanho fixo e uma **Lista** dinâmica, as duas com elementos de um único tipo. Hoje o meuPiá só tem `lista`, que aceita qualquer valor e não tem tamanho fixo. Os desafios não conseguem pedir "um vetor de 5 notas inteiras", e um aluno que mistura textos e números numa lista só descobre o problema bem mais tarde, num erro em inglês do Python. Os métodos que a issue pede (remover por valor, inserir numa posição, buscar, ordenar) também não existem.

## What Changes

- **Novo tipo `vetor[N] de T`** no bloco `var` global e no `var` local: coleção com exatamente `N` elementos do tipo `T`, onde `N` é um inteiro literal maior que zero.
  - Começa com `N` cópias do valor inicial de `T` (`0`, `0.0`, `""` ou `falso`).
  - Os índices vão de `0` a `N - 1`, como na `lista`. Um índice fora dessa faixa, inclusive negativo, é erro de execução com mensagem em português.
  - Atribuir uma lista ao vetor (`notas <- [8, 7, 9, 10, 6]`) exige exatamente `N` elementos do tipo `T`.
  - Métodos que mudam o tamanho (`adicionar`, `removerFim`, `expandir`, `limpar` etc.) são erro de execução.
- **Novo tipo `lista de T`**: lista dinâmica que só aceita elementos do tipo `T`. Começa vazia.
- **Tipos de elemento:** `inteiro`, `real`/`float`, `cadeia`/`string` e `logico`. Um `inteiro` é aceito onde se espera `real` e é guardado como real.
- **Verificação em tempo de execução:** toda entrada de elemento numa coleção tipada passa pela verificação de tipo, seja por atribuição da coleção inteira, atribuição por índice, `adicionar`, `inserir` ou `expandir`. Valor de outro tipo é erro de execução com mensagem em português. A verificação vale também quando a coleção é passada para uma função.
- **Verificação ao compilar, quando dá para ver na hora:** a atribuição de uma lista literal feita só de literais simples (números, textos, `verdadeiro`, `falso`) a um `vetor` ou `lista de T` declarado é verificada pelo analisador semântico. Tipo errado e tamanho errado de vetor viram erro semântico com linha e coluna.
- **Novos métodos nas coleções tipadas:**
  - em `lista de T`: `inserir(posicao, v)`, `remover(v)` (primeira ocorrência), `removerEm(posicao)`, `buscar(v)` (posição ou `-1`), `contem(v)` e `ordenar()`;
  - em `vetor`: `buscar(v)`, `contem(v)` e `ordenar()`;
  - `tamanho()` e `tamanho(x)` nas duas coleções.
- **`vetor` não é palavra reservada:** como `lista` e `logico`, só é tipo depois do `:` de uma declaração. Programas com uma variável chamada `vetor` continuam compilando.
- **Sem mudança para `lista`:** `l: lista` continua sem tipo, aceita qualquer valor e gera o mesmo Python de hoje.
- **Desafio de exemplo e documentação:** um `.por` de exemplo usando `vetor` e `lista de T`, e uma seção nova no guia da linguagem, com exemplos executados pelos testes.

**Adaptações em relação à issue:**
- A issue usa `Array<int> notas = [...]` e `;`, sintaxe que não pertence ao meuPiá. A proposta usa o estilo Portugol do bloco `var`: `notas: vetor[5] de inteiro` e `nomes: lista de cadeia`.
- O "Array imutável ou mutável" da issue fica definido assim: o vetor tem tamanho fixo e elementos mutáveis por índice.
- Iteração usa o `para` com índice que já existe (`para i de 0 ate tamanho(v) - 1`). Um laço `para cada` fica fora deste change.

## Capabilities

### New Capabilities
- `colecoes-tipadas`: declaração, valor inicial, tipos de elemento, verificação de tipo (ao compilar e na execução), tamanho fixo e faixa de índices do `vetor`, métodos e mensagens de erro de `vetor[N] de T` e `lista de T`.

### Modified Capabilities
- `tipos-e-declaracoes`: o requisito "Tipos declaráveis e valores iniciais" passa a incluir `vetor[N] de T` e `lista de T`. O requisito "`lista` e `logico` não são palavras reservadas" passa a incluir `vetor`.

## Impact

- **Código:**
  - `meuPia/utils/builtins.py`: `vetor` em `TIPOS_CONTEXTUAIS` e a lista de tipos de elemento aceitos.
  - `meuPia/analyzers/syntax_analyzer.py`: `grammar_declaration_line` passa a aceitar `vetor [ N ] de T` e `lista de T`. A linha devolvida por `ler_declaracao_local` passa a trazer o tipo completo.
  - `meuPia/analyzers/semantic_analyzer.py`: verifica o tamanho do vetor e as listas literais atribuídas a coleções tipadas, e passa a pular a descrição de tipo inteira nas pré-passagens.
  - `meuPia/analyzers/code_generator.py`: classes de runtime `_Lista` e `_Vetor` no cabeçalho do Python gerado, só quando o programa usa coleções tipadas. Também mudam o valor inicial e a conversão em atribuições a variáveis tipadas.
- **Testes:** novo `meuPia/tests/test_colecoes_tipadas.py`, cenários em `test_tipos.py`, um teste de desafio e os exemplos do guia (`test_guia.py`).
- **Compatibilidade:** sem quebra. Hoje `vetor`, `[` e `de` depois do `:` são sempre erro sintático, e `lista` seguido de `de` também. Programas sem coleções tipadas geram Python byte a byte igual ao atual, o que `test_golden.py` verifica.
- **Ecossistema:** o realce de sintaxe do Lab pode passar a destacar `vetor` como tipo, mas isso é opcional e fica fora deste repositório.
- **Versão:** bump minor para 1.4.0 no `setup.py`, porque é funcionalidade nova da linguagem.
