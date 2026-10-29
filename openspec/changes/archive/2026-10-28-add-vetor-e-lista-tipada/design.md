## Context

A motivação está em proposal.md. O comportamento esperado está nas specs `colecoes-tipadas` e `tipos-e-declaracoes` deste change.

**Estado atual**
- O pipeline faz quatro passadas independentes sobre a mesma lista de tokens: lexer → `Parser` (só valida) → `SemanticAnalyzer` → `CodeGenerator`. Cada componente recebe só `lexeme_pairs`. Quando um componente precisa de estrutura, reaproveita a gramática rodando o `Parser` a partir de uma posição, como faz `Parser.ler_declaracao_local`.
- **Tipo na declaração:** `grammar_declaration_line` lê um único token depois do `:`. Pode ser um `TIPO` ou um ID de `TIPOS_CONTEXTUAIS` (`lista`, `logico`). A linha devolvida tem `tipo` como string.
- **Gerador:** `gen_variables` também lê só um token de tipo. `var_types` e `local_types` mapeiam nome → string de tipo e são usados por `valor_inicial` e `gen_leia`.
- **Python gerado:** a `lista` vira `list` puro. Atribuições viram `nome = expr`, sem conversão.
- **Métodos:** os nomes depois de `.` passam por `METODOS` (`adicionar`→`append`, `removerFim`→`pop`, `tamanho`→`__len__` etc.), qualquer que seja o objeto. `inserir`, `remover` e `espiar` não estão no mapa e chegam ao Python com o mesmo nome, que é como a `FilaPrioridade` funciona.
- **Semântico:** a pré-passagem de globais registra todo ID do bloco `var` que não vem logo depois de `:`. Nenhum dos tokens de `vetor[5] de inteiro` ou `lista de cadeia`, além de `vetor` e `lista`, é ID. Portanto essa pré-passagem já funciona sem mudanças.
- **Não regressão:** `test_golden.py` compara byte a byte o Python gerado para os `.por` versionados.
- **Erros de execução:** há um precedente, o `_faixa` do `para` levanta `ValueError` com mensagem em português.

## Goals / Non-Goals

**Goals:**
- Uma única função de leitura de tipo no parser, usada pelo `var` global, pelo `var` local, pelo semântico e pelo gerador.
- Programas sem coleções tipadas geram Python byte a byte igual ao atual, inclusive o cabeçalho.
- Toda a verificação de execução fica num único lugar, as classes de runtime. O gerador só precisa saber converter na atribuição.
- Manter o contrato atual: os construtores não mudam e cada componente continua recebendo só `lexeme_pairs`.

**Non-Goals:**
- Matrizes (`vetor[3] de vetor[3] de inteiro`) e coleções de coleções.
- Laço `para cada`.
- Parâmetros e retornos tipados, e inferência de tipos além das listas literais.
- `novo vetor(...)` e `dicionario` tipado.
- Levar `inserir`, `remover`, `buscar`, `contem`, `ordenar` e `removerEm` para a `lista` sem tipo. Isso mudaria o Python gerado de todo programa com `lista` e pode ser um change separado.
- Mostrar `verdadeiro`/`falso` em vez de `True`/`False` ao escrever uma coleção inteira de lógicos. Hoje a `lista` já se comporta assim.
- `leia(v[i])`. O `leia` continua aceitando só um nome.

## Decisions

### D1. Descrição do tipo na linha de declaração
`grammar_declaration_line` passa a chamar `grammar_tipo()`, que lê uma destas formas:
- tipo simples: `TIPO` ou ID de `TIPOS_CONTEXTUAIS`;
- `lista de T`: ID `lista` seguido de `DE`;
- `vetor [ N ] de T`: ID `vetor` seguido de `COLCHETEA`.

A linha devolvida mantém `tipo` como string (`'inteiro'`, `'lista'`, `'vetor'` etc.) e ganha `elemento` (`None` ou o nome declarado de `T`) e `tamanho` (`None` ou `int`). Assim, o código que compara `tipo == 'inteiro'` continua funcionando sem mudanças. Os erros de tamanho e de tipo de elemento usam as mensagens da spec, na posição do token problemático.
- O tamanho só é aceito como `NUMINT` formado só de dígitos e com valor maior que zero. Um real como `5.0` também é `NUMINT` e por isso precisa dessa verificação.
- O tipo de elemento é aceito se o lexema, em minúsculas, estiver em `TIPOS_ELEMENTO = ('inteiro', 'real', 'float', 'cadeia', 'string', 'logico')`.
- Em `builtins.py`, `vetor` entra em `TIPOS_CONTEXTUAIS` e `TIPOS_ELEMENTO` passa a ser definido ali.
- Para o gerador, que hoje lê o bloco global token a token, entra `Parser.ler_bloco_var(lexeme_pairs, pos)`, que devolve as linhas e a posição final. Ele espelha `ler_declaracao_local`.

*Alternativa considerada:* codificar o tipo como string composta (`'vetor:5:inteiro'`). Foi rejeitada porque obrigaria todo consumidor a fazer parsing de string e mistura dado com formato.

### D2. Classes de runtime `_Lista` e `_Vetor`
O cabeçalho do Python gerado ganha duas classes, `_Lista(list)` e `_Vetor(_Lista)`, e funções auxiliares. Elas são emitidas **só** quando alguma declaração do programa usa `lista de T` ou `vetor`, o que garante o goal de byte a byte igual.
- **Herdar de `list`:** `len`, iteração, `in`, `==`, `+` e a forma impressa por `escreva` continuam iguais às da `lista`, sem nenhum código a mais.
- **Verificação de elemento:** `_elemento(tipo, v, onde)` devolve o valor normalizado ou levanta `TypeError` com a mensagem da spec. `inteiro` aceita `int` que não é `bool`; `real` aceita `int`/`float` que não é `bool` e converte para `float`; `cadeia`/`string` aceita `str` e embrulha em `_S`, para a concatenação continuar igual; `logico` aceita `bool`.
- **Sobrescritas em `_Lista`:** `__setitem__`, `__getitem__` (faixa de índices com `IndexError`), `append` (que atende `adicionar` e `adicionarFim`), `extend` (verifica tudo antes de mudar a lista, para ser atômico), `pop` (lista vazia vira `ValueError`) e os métodos em português `inserir`, `remover`, `removerEm`, `buscar`, `contem` e `ordenar`. Os métodos em português são definidos com o próprio nome, porque não estão em `METODOS`.
- **`_Vetor`:** guarda `n` e sobrescreve com `ValueError` (mensagem de tamanho fixo) todos os métodos que mudam o tamanho, tanto os nomes Python mapeados (`append`, `extend`, `clear`, `pop`, `appendleft`, `popleft`) quanto os em português (`inserir`, `remover`, `removerEm`).
- **Tipos de exceção:** `TypeError` para valor de tipo errado e para "não é lista"; `IndexError` para índice e posição; `ValueError` para tamanho fixo, tamanho errado na atribuição, valor ausente e lista vazia. Segue o precedente do `_faixa`. Os testes conferem a mensagem exata.
- **Mensagens:** `_valor_msg(v)` formata o valor recebido: texto entre aspas duplas, lógico como `verdadeiro`/`falso`, o resto com `str`.

*Alternativa considerada:* inserir verificações inline no código gerado a cada `adicionar` e `v[i] <-`. Foi rejeitada porque o gerador não sabe o tipo de um parâmetro de função, e a spec exige verificação também nesse caso. Com o objeto carregando o próprio tipo, a verificação vale em qualquer lugar.

### D3. Conversão na atribuição
- **`receber`:** `_Lista.receber(tipo, valor)` e `_Vetor.receber(tipo, n, valor)`.
  - Se `valor` já for da mesma classe exata, com o mesmo `tipo` (e `n`), devolvem o próprio objeto. Isso mantém o compartilhamento que a `lista` tem hoje.
  - Se for `list` ou `deque`, constroem uma coleção nova verificando cada elemento (e o tamanho, no vetor).
  - Qualquer outro valor levanta `TypeError` com a mensagem "só recebe uma lista de valores".
- **Gerador:** em `gen_assignment_or_call`, quando o alvo é um nome sem `.` nem `[...]` e o tipo resolvido é coleção tipada, emite `nome = _Vetor.receber('inteiro', 5, <expr>)` (ou `_Lista.receber(...)`). O valor inicial de um `var` local passa pelo mesmo caminho. O valor inicial sem expressão é `_Vetor('inteiro', 5)` ou `_Lista('cadeia')`. Uma chamada é emitida por nome, para que `a, b: vetor[2] de inteiro` gere objetos independentes.
- **Resolução do tipo:** `var_types` e `local_types` passam a guardar a linha de tipo (D1), não só a string. A ordem de busca é: local do `def` atual, depois parâmetro do `def` atual (sem tipo, então sem conversão), depois global. O gerador passa a guardar os parâmetros do `def` atual (`self.params_atuais`). Sem isso, um parâmetro com o mesmo nome de uma global tipada seria convertido por engano.

### D4. Verificação semântica
- **Tipos declarados:**
  - globais: `get_declared_variables` registra as coleções tipadas em `self.tipos_globais` (nome → linha de tipo), usando `Parser.ler_bloco_var`;
  - locais: `validate_local_declaration` registra em `self.tipos_locais`, que é zerado em `enter_body`.
- **Atribuições:** o `Parser` ganha uma lista opcional `atribuicoes`. `grammar_id_statement` a preenche com `(pos_alvo, inicio_expr, fim_expr)` quando o alvo é um nome simples seguido de `<-`/`=`. O semântico obtém essa lista com `Parser.ler_atribuicoes(lexeme_pairs)`, que roda o parse completo de novo, e a consulta quando encontra o ID na passagem de uso.
  - O parser é a fonte de verdade sobre o que é um comando de atribuição. Isso evita confundir `v = [1, 2]` dentro de um `se` (comparação) com uma atribuição.
- **Lista literal:** o intervalo da expressão precisa começar em `[` e terminar no `]` correspondente. Os elementos, separados por vírgula no nível zero, precisam ser `NUMINT`, `- NUMINT`, `STRING`, ou `verdadeiro`/`falso` não declarados pelo usuário. Se algum elemento não for literal simples, nada é verificado.
  - Literal com `.` é `real`, sem `.` é `inteiro`.
  - As regras de aceitação são as mesmas do runtime: `real` aceita `inteiro`.
  - O valor inicial de um `var` local usa o mesmo verificador, com o intervalo `linha['expressao']`.
- **`leia`:** ao encontrar `LEIA ( ID`, se o ID resolver para uma coleção tipada, gera o erro da spec na posição do ID.
- **Resolução de nomes:** local visível, depois parâmetro (sem tipo), depois global, a mesma ordem do D3.

### D5. Documentação, exemplo e desafio
- **Guia:** em `docs/guia-da-linguagem.md`:
  - a tabela de tipos da seção 2 ganha duas linhas;
  - a seção 6 ganha as subseções "Vetores" e "Listas com tipo", e a tabela de métodos ganha os métodos novos;
  - a seção 11 ganha os erros novos;
  - a seção 12 cita `vetor` entre os nomes que não são reservados.

  Todos os exemplos usam blocos ```portugol com saída ```text, executados por `test_guia.py`. Os erros de compilação usam `nao-executar` + `text`.
- **README:** uma subseção curta "Vetores e listas com tipo", com link para o guia.
- **Exemplo e desafio:** `exemplos/boletim.por` (vetor de notas, média, lista de aprovados com `lista de cadeia`, `ordenar`) e o golden correspondente em `meuPia/tests/golden/boletim.py`. Também entra `meuPia/tests/test_desafio_colecoes_tipadas.py`, com uma solução de aluno no formato dos desafios do Lab e asserções sobre a saída.

### D6. Testes
- **`meuPia/tests/test_colecoes_tipadas.py`:** um teste por cenário da spec `colecoes-tipadas`. Os casos de sucesso usam `executar()`. Os erros de execução usam `pytest.raises(<Tipo>, match=re.escape(<mensagem>))`. Os erros de compilação conferem `linha`/`coluna`.
- **`test_tipos.py`:** ganha os novos cenários de `tipos-e-declaracoes`.
- **`test_golden.py`:** continua passando sem regerar os goldens existentes. É a prova do goal de byte a byte igual.

## Risks / Trade-offs

- **[Risco] `/` sempre produz real no Python.** `l.adicionar(4 / 2)` numa `lista de inteiro` falha, porque `4 / 2` é `2.0`. → Mitigação: a mensagem mostra `recebeu 2.0`, o guia explica que `/` dá real e mostra o uso de `piso(...)`. Aceitar reais com valor inteiro foi descartado porque tornaria a regra menos previsível.
- **[Risco] A verificação de execução tem custo em cada operação.** → É desprezível para o tamanho dos programas de aula. A `lista` sem tipo continua sem nenhum custo extra.
- **[Risco] Métodos de `list` não sobrescritos burlariam a verificação**, como `l.sort` ou `l.insert`, se chamados pelos nomes Python. → O aluno só chega a eles digitando o nome em inglês. Também são sobrescritos `insert` e `__iadd__` com verificação, e `sort` delega para `ordenar`. Os nomes em inglês não são documentados.
- **[Trade-off] Atribuir coleção de outro tipo copia, atribuir do mesmo tipo compartilha.** É a única forma de manter o compartilhamento da `lista` e ao mesmo tempo garantir o tipo declarado. A spec registra os dois casos.
- **[Trade-off] Verificação ao compilar só em listas literais.** Cobre o erro mais comum (digitar a lista errada) sem introduzir inferência de tipos no semântico.
- **[Risco] A segunda passada do parser no semântico (D4).** → É o mesmo custo já aceito em `ler_declaracao_local`, e o parser já validou o programa antes.

## Migration Plan

1. Bump para `1.4.0` no `setup.py`.
2. Depois do merge, publicar na PyPI e atualizar a versão fixada no Lab (`src/engine/wasm.js`).
3. Nenhum programa existente precisa mudar.
4. **Rollback:** voltar a versão fixada no Lab para 1.3.0. Programas com `vetor` ou `lista de T` voltam a dar erro sintático, mas nenhum outro programa é afetado.

## Open Questions

- O realce de sintaxe do Lab deve destacar `vetor` como tipo? Isso não afeta este repositório e pode ser decidido no Lab.
