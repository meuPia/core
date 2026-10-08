## Why

Uma auditoria do meuPia-core encontrou 21 erros, todos reproduzidos com programas Portugol mínimos. Os 61 testes atuais passam com 87% de cobertura, mas só comparam trechos de texto do código gerado e nunca executam o Python produzido, então nenhum desses erros é detectado. Vários deles bloqueiam programas comuns de alunos: `se x + 1 > 0`, `para i de 0 ate n - 1`, blocos vazios e classes declaradas depois de `var`. Além disso, o exemplo oficial e 2 desafios do repositório `desafios` não compilam. A spec do Tutor Socrático e a do Time-Travel dependem de um compilador confiável, e este change estabelece essa base.

## What Changes

**Prioridade 1**
- **CLI**: erro de compilação passa a sair com código ≠ 0. O `main.py` continua não sendo gerado quando há erro, porque o Lab depende disso.
- **Blocos vazios**: `se`/`senao`, `enquanto`, `para`, `funcao` e `inicio` vazios passam a gerar Python válido.

**Expressões e condições**
- Comparações passam a aceitar expressões aritméticas completas dos dois lados: `x + 1 > 0`, `(x + 1) > 0`, `x > -1`.
- Condições passam a aceitar qualquer expressão sem comparação: `se verdadeiro`, `enquanto nao vazio(f)`, `se f(x)`.
- `=` e `==` passam a comparar dentro de expressões; `<-` e `=` atribuem em comandos. **BREAKING**: `se x <- 1` passa a ser erro sintático, e `x == 5` como comando deixa de ser aceito como atribuição.
- Novos operadores: `!=` (sinônimo de `<>`), `%` e `mod` (resto da divisão).

**Laço `para`**
- Limites e passo passam a aceitar expressões completas.
- O limite final é inclusivo também com passo negativo, mesmo quando o passo é uma variável.

**Tipos**
- Novos tipos `logico` (valor inicial falso) e `lista` (valor inicial lista vazia).
- `novo dicionario()` e `novo lista()` passam a criar coleções vazias.

**Builtins e escrita**
- Nomes declarados pelo usuário (variável, parâmetro, função ou classe) deixam de ser trocados por builtins: uma variável `pi` continua sendo do usuário.
- `x.tamanho()` passa a funcionar em qualquer coleção, inclusive filaDupla e filaPrioridade.
- `escreva` passa a aceitar vários argumentos, concatenados sem separador, com lógicos impressos como verdadeiro/falso.
- Strings terminadas em `\\` passam a ser reconhecidas.

**Análise semântica**
- Classe declarada depois de `var` deixa de gerar "declaração duplicada".
- Acesso a atributo (`obj.campo`) e constantes builtin (`pi`) deixam de ser acusados como não declarados.
- O corpo de `metodo` passa a ser validado, com seus parâmetros e `self` como locais.
- **BREAKING**: as mensagens de erro léxico, sintático e semântico passam a ser padronizadas em pt-BR, com linha e coluna do `.por`. Os testes que comparam texto de mensagem serão atualizados.

**Testes e exemplos**
- Novo helper de teste que compila e executa o código gerado e compara o stdout.
- Teste do `compiler.py`, que hoje tem 0% de cobertura.
- Regressão compilando todos os `.por` do repositório.
- Correção do teste duplicado `test_gen_plugin_import` e atualização de `exemplos/smart_security.por` para a sintaxe atual.

## Capabilities

### New Capabilities
- `expressoes`: operadores aritméticos, relacionais e lógicos, precedência, `=`/`==`/`<-` conforme o contexto, `!=`, `%`/`mod` e condições sem comparação.
- `controle-de-fluxo`: `se`/`senao`, `enquanto`, `para` (limites com expressão, passo positivo e negativo), `continue`/`interrompa` e blocos vazios.
- `tipos-e-declaracoes`: tipos do bloco `var` e seus valores iniciais (incluindo `logico` e `lista`), `novo` para tipos nativos e literais de string.
- `builtins`: mapeamento de funções e métodos nativos (`tamanho`, matemática, coleções), a proteção de nomes declarados pelo usuário e o comando `escreva`.
- `analise-semantica`: regras de declaração e uso de variáveis em `inicio`, `funcao` e `metodo`, além do formato das mensagens de erro.
- `cli`: comportamento do comando `meupia` e da função de compilação usada pelo Lab (código de saída e arquivos gerados).

### Modified Capabilities
<!-- Nenhuma: openspec/specs/ ainda está vazio. -->

## Impact

- **Código**:
  - `meuPia/analyzers/lexical_analyzer.py`: novos tokens e operadores, strings com escape.
  - `meuPia/analyzers/syntax_analyzer.py`: nova gramática de expressões e `para`.
  - `meuPia/analyzers/semantic_analyzer.py`: escopos de `classe`/`metodo`, atributos, builtins e mensagens.
  - `meuPia/analyzers/code_generator.py`: `pass` em blocos vazios, `range` do `para`, builtins, `escreva` e tipos.
  - `meuPia/utils/token_enum.py`: separação de `ATR`/`LOGIGUAL` e novos tokens.
  - `meuPia/compiler.py`: código de saída.
- **Testes**:
  - `meuPia/tests/`: novo helper de execução e novos arquivos de teste.
  - Ajuste dos testes de mensagem em `test_semantic.py`.
  - Correção do teste duplicado em `test_generator_core.py`.
- **Exemplos**: `exemplos/smart_security.por`.
- **Consumidores**:
  - meuPia-lab: não precisa de mudança. Ele continua chamando `main(arquivo, "output")` e checando se `main.py` existe. As mensagens de erro exibidas mudam de texto.
  - Repositório `desafios`: o compilador passa a aceitar o `!=` de `fio_de_ariadne` e o tipo `lista` de `radar_motoboy`. Ficam três erros dos próprios desafios, fora deste change:
    - `fio_de_ariadne` usa a palavra reservada `inicio` como nome de parâmetro (linha 5);
    - `radar_motoboy` usa `mapa_global` sem declarar no `var` (linha 26);
    - `fila_prioridade_simples` tem uma aspa sobrando (linha 18).
- **Versão**: bump no `setup.py`.
- **Fora de escopo**:
  - Tutor socrático e snapshots/time-travel.
  - Parâmetros tipados, atributos declarados em classe e `var` dentro de `inicio`.
  - Divisão inteira: `/` continua retornando real.
  - Reescrita do Guia da Linguagem.
