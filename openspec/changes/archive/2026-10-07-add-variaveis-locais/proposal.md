## Why

Hoje toda variável do meuPiá é global e precisa ser declarada no bloco `var` antes de `funcao` e `inicio` (issue meuPia/core#7). Os alunos não conseguem criar variáveis auxiliares dentro de uma função. Por isso acabam usando globais para resultados intermediários, o que causa efeitos colaterais difíceis de entender, como uma função recursiva que sobrescreve a variável de laço de quem a chamou. Pela mesma limitação, o `codigoTeste` do desafio `ontologia_hospital`, que declara `var` no meio do `inicio`, não compila.

## What Changes

- **Declaração local com `var`** dentro do corpo de `funcao`, de `metodo` e do bloco `inicio`, nas duas formas abaixo, que seguem uma única gramática:
  - **Bloco:** `var` seguido de linhas `nome1, nome2: tipo`. Cada variável recebe o valor inicial do tipo, o mesmo usado nas globais.
  - **Com valor:** `var nome: tipo <- expressão` (aceita `=` no lugar de `<-`). Só pode ter um nome por linha.
  - Um mesmo `var` pode misturar as duas formas, uma por linha, e uma função pode ter várias declarações `var`.
- **Posição:** a declaração pode aparecer em qualquer ponto do nível principal do corpo. Dentro de `se`, `senao`, `enquanto` e `para`, é erro sintático.
- **Escopo e tempo de vida:**
  - A variável local só é visível dentro do corpo onde foi declarada, a partir da linha da declaração.
  - Cada chamada da função cria as suas próprias variáveis locais, inclusive em recursão.
  - Variáveis locais do `inicio` não são visíveis dentro das funções.
- **Novos erros semânticos:**
  - nome local igual ao de uma global, de um parâmetro, de outra local do mesmo corpo, de uma função, de uma classe ou a `self`;
  - uso de uma variável local antes da sua declaração.
- **Builtins:** nomes de variáveis locais passam a contar como nomes declarados pelo usuário e têm prioridade sobre builtins com o mesmo nome.
- **`leia`** sobre uma variável local converte a entrada pelo tipo declarado, como já acontece com as globais.
- **Documentação:** seção sobre variáveis locais no `README.md`, ou no guia da linguagem se ele já existir em `docs/`.

**Adaptações em relação à issue:**
- A issue usa chaves, `;`, `int`, `retornar`, `imprimir`, `para cada` e parâmetros tipados, sintaxe que não pertence ao meuPiá. A proposta adapta tudo ao estilo atual (`<-`, `fim_funcao`, os tipos já existentes).
- Parâmetros tipados (issue meuPia/core#6) ficam fora deste change.
- A issue pede inicialização obrigatória. Aqui ela é atendida de outro jeito: a declaração sem valor recebe o valor inicial do tipo, então nunca existe variável local sem valor.

## Capabilities

### New Capabilities
- `variaveis-locais`: sintaxe, posições permitidas, inicialização, escopo, tempo de vida e conflitos de nome das variáveis declaradas com `var` dentro de `funcao`, `metodo` e `inicio`.

### Modified Capabilities
- `analise-semantica`: o requisito "Nomes válidos em cada escopo" passa a incluir as variáveis locais visíveis em cada ponto do corpo.
- `builtins`: o requisito "Nomes declarados pelo usuário têm prioridade sobre builtins" passa a contar as variáveis locais como declarações do usuário.

## Impact

- **Código:**
  - `meuPia/analyzers/syntax_analyzer.py`: `var` como comando no nível principal de corpos de `funcao`, `metodo` e `inicio`.
  - `meuPia/analyzers/semantic_analyzer.py`: as pré-passagens deixam de tratar um `var` dentro de corpos como bloco global; entram o escopo local por corpo, os conflitos de nome e o uso antes da declaração.
  - `meuPia/analyzers/code_generator.py`: gera atribuições locais; o `global` de funções, métodos e `main()` deixa de listar variáveis locais; `leia` passa a conhecer os tipos locais.
- **Testes:** um novo `meuPia/tests/test_variaveis_locais.py`, um cenário de desafio com variáveis locais e ajustes nos testes de análise semântica e builtins.
- **Compatibilidade:** todo programa que compila hoje continua compilando, porque `var` fora do topo do programa hoje é sempre erro sintático. O teste de regressão dos `.por` cobre isso.
- **Ecossistema:**
  - O `codigoTeste` original de `ontologia_hospital` passa a compilar quando o Lab o anexa ao `inicio`.
  - O realce de sintaxe do Lab não muda, porque `var` já é palavra-chave.
- **Versão:** bump minor para 1.3.0 no `setup.py`, porque é funcionalidade nova da linguagem.
