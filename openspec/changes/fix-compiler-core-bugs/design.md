## Context

A motivação está em proposal.md (seção Why) e o comportamento esperado está nas specs deste change. Este documento descreve só o "como".

**Estado atual do pipeline**
- O compilador faz quatro passadas independentes sobre a mesma lista de tokens (`{"token", "lexeme", "code_index"}`):
  - `scan_line`, o lexer;
  - `Parser`, que só valida e não constrói árvore;
  - `SemanticAnalyzer`, que faz uma varredura linear com flags;
  - `CodeGenerator`, que concatena texto Python e repassa quase todos os tokens de expressão um a um.
- Como as regras de precedência do Python coincidem com as que queremos (`not` abaixo dos relacionais, `and` acima de `or`), o gerador não precisa de árvore: basta o parser aceitar a gramática certa.

**Restrições**
- O meuPia-lab chama `main("main.por", "output")` e decide se houve sucesso checando a existência de `output/main.py`. O Lab ignora o valor de retorno.
- O entry point `meupia=meuPia.compiler:main` executa `sys.exit(main())`, então o valor retornado por `main()` vira o código de saída do processo.
- [test_lexical.py](../../../meuPia/tests/test_lexical.py) espera que `=` produza o token `ATR`, e outros testes dependem dos nomes de tokens atuais.
- Não pode haver dependências de runtime (o pacote roda no Pyodide). O estilo de indentação é de 2 espaços no lexer e no parser e de 4 no gerador.

## Goals / Non-Goals

**Goals:**
- Corrigir os erros sem reescrever a arquitetura: continuar com o pipeline baseado em lista de tokens.
- Ter uma única fonte de verdade para builtins, compartilhada entre o analisador semântico e o gerador.
- Fazer os testes novos verificarem comportamento (executando o código gerado), não o texto.

**Non-Goals:**
- Construir uma AST. Fica para o change do Tutor e dos Snapshots, que vai precisar de um mapa de linhas.
- Validar tipos (por exemplo, impedir `inteiro <- "texto"`).
- Aceitar `real` no `para`. `range` continua exigindo inteiros, e `ate n / 2` segue dando erro de execução.

## Decisions

### D1. Gramática de expressões única no parser
Substituir `grammar_arithmetic_expression`, `grammar_arithmetic_term`, `grammar_logic_expression`, `grammar_logic_comparison` e `grammar_logic_operand` por uma descida recursiva com um nível por precedência:

```
expressao   := ou
ou          := e ("ou" e)*
e           := nao ("e" nao)*
nao         := "nao" nao | relacional
relacional  := aditiva (op_rel aditiva)?
aditiva     := mult (("+"|"-") mult)*
mult        := unario (("*"|"/"|"%"|"mod") unario)*
unario      := "-" unario | primario
primario    := ID cauda | NUMINT | STRING | "novo" (TIPO|ID) args
             | "[" lista? "]" | "{" pares? "}" | "(" expressao ")"
cauda       := ("." ID | args | "[" expressao "]")*
```

- `se`, `enquanto`, `retorne`, `escreva`, os argumentos de chamada, os índices e os limites do `para` passam a usar `expressao`.
- Não há ambiguidade com parênteses, porque `(` sempre abre uma `expressao`.
- O gerador continua repassando os tokens, porque o Python aplica a mesma precedência.
- **Alternativa descartada:** gerar uma AST agora. Isso dobraria o tamanho do change e mexeria no gerador inteiro.

### D2. `=` decidido pelo contexto, sem token novo
- O lexer continua emitindo `ATR` para `<-` e para `=`.
- `LOGIGUAL` ganha o valor `'=='`, o que acaba com o alias do Enum. Um teste vai garantir que nenhum valor de `TokenEnum` se repete.
- Dentro de `relacional`, o parser aceita `ATR` como operador **somente se o lexema for `=`**. Um `<-` ali vira erro sintático.
- No gerador, dentro de uma expressão, `ATR` com lexema `=` vira `==`.
- **Alternativa descartada:** criar um token `IGUAL` só para o `=`. Isso quebraria `test_scan_assignment_equal` e o formato dos `.tem` sem nenhum ganho.

### D3. Novos operadores no lexer
- `!=` gera `LOGDIFF`, e o `!` sozinho continua sendo erro léxico.
- `%` e a palavra-chave `mod` geram o novo token `OPMOD`, que vira `%` em Python.
- `mod` passa a ser uma palavra reservada (veja Riscos).

### D4. `para` com função auxiliar `_faixa`
- O cabeçalho do código gerado ganha `_faixa(inicio, fim, passo)`. Ela retorna `range(inicio, fim + 1, passo)` se `passo > 0` e `range(inicio, fim - 1, passo)` se `passo < 0`.
- Com `passo == 0`, levanta `ValueError("passo do laço para não pode ser zero")`.
- O gerador emite `for v in _faixa(a, b, p):`.
- **Alternativa descartada:** emitir uma expressão condicional inline. Ela avaliaria `p` duas vezes e deixaria o código gerado ilegível para quem o inspeciona no Lab.

### D5. Blocos vazios
- Todo bloco aberto pelo gerador (`if`, `else`, `while`, `for`, `def` de função, de método e de `main`) guarda `len(self.python_code)` antes de gerar o corpo.
- Se nenhuma linha de corpo foi adicionada, emite `pass`.
- A declaração `global` não conta como corpo.
- Isso substitui o `has_content` que hoje só existe em `gen_method_definition`.

### D6. Módulo único de builtins e pré-passagem de nomes do usuário
**Novo módulo** `meuPia/utils/builtins.py`, com três tabelas:
- `FUNCOES_BUILTIN`: `tamanho`→`len`, `raiz`→`math.sqrt`, etc.;
- `CONSTANTES_BUILTIN`: `pi`, `verdadeiro`, `falso`;
- `METODOS`: `adicionar`→`append`, `removerInicio`→`popleft`, etc.

Ele substitui as duas cadeias de `if/elif` duplicadas do gerador.

**Pré-passagem no gerador:**
- Antes de gerar, o gerador coleta os nomes declarados pelo usuário: variáveis do `var`, nomes de `funcao` e `classe`, e parâmetros.
- Um ID só é traduzido por `FUNCOES_BUILTIN` ou `CONSTANTES_BUILTIN` se não estiver nesse conjunto e não vier logo após `.`.
- Depois de `.`, vale apenas a tabela `METODOS`.

**`x.tamanho()`:**
- O método `tamanho` entra na tabela `METODOS` como `__len__`, então `x.tamanho()` vira `x.__len__()`. Texto, lista, dicionário e `deque` já têm esse método.
- **Alternativa descartada durante a implementação:** reescrever o prefixo como `len(<prefixo>)`. O gerador monta expressões como uma lista plana de partes, e achar o início do prefixo (com índices e chamadas encadeadas) seria frágil. O comportamento observável é o mesmo.
- A `FilaPrioridade` ganha `__len__`. O método `len()` continua existindo, para compatibilidade com o código gerado pela versão 1.1.19+.

### D7. `escreva` com a função auxiliar `_escreva`
- O cabeçalho ganha `_escreva(*args)`, que imprime `''.join(_texto(a) for a in args)`.
- `_texto` converte `True`/`False` em `verdadeiro`/`falso` e o resto com `str`.
- O parser passa a aceitar `escreva(expressao ("," expressao)*)`.
- Booleanos dentro de listas continuam aparecendo como `True`/`False`. Isso está registrado como limitação conhecida.

### D8. Tipos `logico` e `lista`, e `novo` para tipos nativos
- `logico` e `lista` são **tipos contextuais**: o lexer os emite como `ID`, ao contrário de `dicionario`, que é reservado.
  - O parser aceita, na posição de tipo do `var`, um `TIPO` ou um `ID` cujo lexema seja `lista` ou `logico`.
  - Depois de `novo`, o parser já aceita `ID`.
  - O gerador só traduz `lista` para `list` quando o nome aparece logo após `novo`.
  - O analisador semântico ignora o `ID` que ocupa a posição de tipo.
  - **Alternativa descartada:** reservar os dois nomes como `dicionario`. É mais simples, mas quebraria programas que usam `lista` como nome de variável, que é uma palavra muito comum.
- Valores iniciais: `False` e `[]`.
- `leia` de uma variável `logico` gera `v = input().strip().lower() == 'verdadeiro'`.
- Em expressões, os `TIPO` `dicionario`, `lista` e `filaPrioridade` viram `dict`, `list` e `FilaPrioridade`. Como `novo` já é omitido, `novo dicionario()` vira `dict()`.

### D9. Strings com barra invertida
- `match_token_string` passa a contar as barras invertidas consecutivas antes da aspa. A string só fecha quando esse número for par.
- A coluna do erro de string não terminada passa a ser `startIndex + 1`, alinhando com a contagem a partir de 1 usada em `code_index`.

### D10. Analisador semântico com escopos explícitos
Reescrever a varredura como uma máquina de estados: `topo` → `var` → `funcao` / `classe` → `metodo` → `inicio`.

**Pré-passagem:** coleta as variáveis globais (somente dentro de blocos `var` no topo) e os nomes de funções e classes.

**Encerramento de bloco:** `classe`, `metodo`, `funcao` e `inicio` encerram o bloco `var`.

**Verificação de uso:** em qualquer corpo (`funcao`, `metodo`, `inicio`), um ID é aceito quando:
- vem depois de `.`;
- é seguido de `(`;
- é global, função, classe ou builtin;
- é local (parâmetros, e `self` dentro de `metodo`).

### D11. Erros padronizados
- Nova classe base `ErroCompilacao(Exception)` com os campos `etapa`, `linha`, `coluna` e `descricao`. O `__str__` produz `Erro <etapa> na linha L, coluna C: <descrição>`.
- `LexicalError`, `SyntacticError` e `SemanticError` passam a herdar dela. Os nomes ficam, para não quebrar imports.
- Um helper converte `code_index` (`"L:C"`) em linha e coluna. Em fim de arquivo, usa o último token; numa lista vazia, usa 1:1. Isso também corrige o `IndexError` em `current_code_index`.
- `expect_token` passa a descrever o token esperado em português, por meio de uma tabela `TokenEnum → descrição`, sem expor os nomes internos.

### D12. Contrato do `compiler.main`
- `main()` retorna `0` em sucesso e `1` em erro.
- **Diverge do prompt original, que pedia True/False.** O motivo: `sys.exit(True)` termina com código 1, ou seja, a convenção ficaria invertida.
- O bloco `__main__` passa a chamar `sys.exit(main(...))`.
- Antes de gravar o `.py`, o código gerado passa por `compile(codigo, arquivo, "exec")`. Se o compilador produzir Python inválido (um bug interno), `main()` mostra `Erro interno do compilador: …`, retorna `1` e não grava o arquivo. Assim o Lab nunca executa um `main.py` quebrado.
- O caminho sem argumentos retorna `2`, a convenção para erro de uso.

### D13. Estratégia de testes
- **Helper:** `meuPia/tests/helpers.py` com `compilar(codigo) -> str` e `executar(codigo, entrada="") -> str`. Ele roda o pipeline completo, executa com `exec` num dicionário novo (`__name__ = "__main__"`) e redireciona `stdin` e `stdout`.
- **Um arquivo de teste por capability:** `test_expressoes.py`, `test_controle_fluxo.py`, `test_tipos.py`, `test_builtins.py`, `test_analise_semantica.py` e `test_cli.py`. Cada um tem um teste por cenário das specs.
- **`test_cli.py`:** usa `tmp_path` e `subprocess` com `sys.executable -m meuPia.compiler` para conferir o código de saída real.
- **`test_regressao.py`:** parametrizado sobre `exemplos/*.por` e `meuPia/input/*.por`.
- **Cobertura:** `pytest-cov` entra em `extras_require["dev"]`. O alvo de cobertura de branches fica documentado como comando, não como gate no `pytest.ini`.

## Risks / Trade-offs

- **[Risco] Programas que usam `mod` como nome de variável quebram.** → Mitigação: a busca nos `.por` e desafios atuais não encontrou nenhum uso. O erro sintático vai indicar a linha.
- **[Risco] `x == 5` usado como comando de atribuição deixa de compilar.** → Mitigação: nenhum uso encontrado. A mudança está marcada como BREAKING na proposal.
- **[Risco] A reescrita da gramática pode rejeitar programas que hoje compilam.** → Mitigação: o teste de regressão cobre os `.por` do repositório. Além disso, uma task de verificação manual compila os 14 desafios do repositório irmão `desafios` antes do bump de versão.
- **[Risco] O texto das mensagens de erro muda e o Lab as exibe ao aluno.** → Mitigação: o Lab só repassa o texto, sem fazer parsing. Os testes que comparam mensagens em `test_semantic.py` serão atualizados no mesmo change.
- **[Trade-off] O gerador continua repassando tokens sem árvore.** Novos erros de precedência são evitados pelo parser, mas o mapa de linhas para o Tutor e os Snapshots ainda não existe. Isso fica explicitamente para o próximo change.
- **[Limitação] Ainda faltam algumas conversões.** `escreva([verdadeiro])` continua imprimindo `[True]`, e `para` com limites `real` continua falhando na execução.

## Migration Plan

1. Fazer o bump de versão para `1.2.0` no `setup.py` (minor, por causa das mudanças BREAKING de sintaxe e de mensagens).
2. Publicar no PyPI.
3. Atualizar a versão fixada em `meuPia-lab/src/engine/wasm.js` (`micropip.install("meupia-core=="+version)`). Isso fica num PR separado no repositório do Lab.
4. **Rollback:** reverter a versão fixada no Lab. O pacote antigo continua no PyPI.
