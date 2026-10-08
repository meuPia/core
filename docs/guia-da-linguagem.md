# Guia da Linguagem meuPiá

Este guia ensina a escrever algoritmos em meuPiá, o Portugol do compilador `meuPia-core`. Ele é feito para quem está começando: cada seção tem exemplos curtos que você pode copiar, rodar e modificar.

> **Documentação executável.** Todo exemplo deste guia é compilado e executado pelos testes do projeto (`meuPia/tests/test_guia.py`). Se um exemplo deixar de funcionar, os testes falham. Por isso, o que está escrito aqui é o que o compilador faz de verdade.

Como ler os exemplos:

- Um bloco de código é um algoritmo completo. O bloco **saída** logo depois mostra exatamente o que aparece na tela.
- Quando o programa usa `leia`, um bloco **entrada** mostra o que foi digitado, uma linha por `leia`.
- Exemplos marcados como "não executável" usam um plugin que precisa ser instalado, ou têm um erro de propósito para você ver a mensagem do compilador.

Para compilar e rodar um arquivo `.por` no terminal:

```bash
meupia meu_programa.por
```

```bash
python output/meu_programa.py
```

O `meupia` gera o Python equivalente na pasta `output/`. Se houver erro no seu código, ele mostra a mensagem (veja a [seção 11](#11-mensagens-de-erro)) e não gera o arquivo.

## Sumário

1. [Estrutura de um algoritmo](#1-estrutura-de-um-algoritmo)
2. [Variáveis e tipos](#2-variáveis-e-tipos)
3. [Atribuição, leitura e escrita](#3-atribuição-leitura-e-escrita)
4. [Expressões](#4-expressões)
5. [Controle de fluxo](#5-controle-de-fluxo)
6. [Coleções](#6-coleções)
7. [Funções nativas](#7-funções-nativas)
8. [Funções](#8-funções)
9. [Classes](#9-classes)
10. [Plugins e mPGP](#10-plugins-e-mpgp)
11. [Mensagens de erro](#11-mensagens-de-erro)
12. [Palavras reservadas e limitações conhecidas](#12-palavras-reservadas-e-limitações-conhecidas)

## 1. Estrutura de um algoritmo

Todo programa começa com `algoritmo` e o nome do programa entre aspas, e termina com `fim_algoritmo`. Os comandos que serão executados ficam entre `inicio` e `fim_algoritmo`.

```portugol
algoritmo "OlaMundo"

inicio
    escreva("Olá, mundo!")
fim_algoritmo
```

```text
Olá, mundo!
```

Antes do `inicio` podem vir, nesta ordem:

```
algoritmo "Nome"
usar "plugin"          ← opcional, um por linha (seção 10)
var                    ← opcional: variáveis globais (seção 2)
funcao ... / classe ...  ← opcionais (seções 8 e 9)
inicio
    comandos
fim_algoritmo
```

Tudo depois de `//` até o fim da linha é um **comentário**: o compilador ignora. Use comentários para explicar o seu raciocínio.

```portugol
algoritmo "Comentarios"

// Este programa guarda o nível de força de um padawan
var
    forca: inteiro   // começa em 0

inicio
    forca <- 10 // um comentário também pode vir depois de um comando
    escreva(forca)
fim_algoritmo
```

```text
10
```

## 2. Variáveis e tipos

Uma variável é um nome que guarda um valor. As variáveis do programa são declaradas no bloco `var`, uma linha por tipo, no formato `nome1, nome2: tipo`.

| Tipo | Guarda | Valor inicial |
|---|---|---|
| `inteiro` | números inteiros | `0` |
| `real` ou `float` | números com casas decimais | `0.0` |
| `string` ou `cadeia` | textos | texto vazio |
| `logico` | `verdadeiro` ou `falso` | `falso` |
| `lista` | sequência de valores | lista vazia |
| `dicionario` | pares chave → valor | dicionário vazio |
| `filaPrioridade` | fila que sempre entrega o menor valor | fila vazia |

Toda variável declarada já começa com o valor inicial do seu tipo:

```portugol
algoritmo "ValoresIniciais"

var
    golpes: inteiro
    energia: real
    nome: cadeia
    treinado: logico
    sabres: lista
    mochila: dicionario
    tarefas: filaPrioridade

inicio
    escreva("golpes = ", golpes)
    escreva("energia = ", energia)
    escreva("nome tem ", tamanho(nome), " letras")
    escreva("treinado = ", treinado)
    escreva("sabres = ", sabres)
    escreva("mochila = ", mochila)
    escreva("tarefas na fila = ", tamanho(tarefas))
fim_algoritmo
```

```text
golpes = 0
energia = 0.0
nome tem 0 letras
treinado = falso
sabres = []
mochila = {}
tarefas na fila = 0
```

`real` e `float` são o mesmo tipo, assim como `string` e `cadeia`:

```portugol
algoritmo "Sinonimos"

var
    a: real
    b: float
    c: string
    d: cadeia

inicio
    a <- 1.5
    b <- 2.5
    c <- "Mestre "
    d <- "Yoda"
    escreva(a + b)
    escreva(c + d)
fim_algoritmo
```

```text
4.0
Mestre Yoda
```

`lista` e `logico` só são tipos depois do `:` de uma declaração (e depois de `novo`, seção 6). Em qualquer outro lugar são nomes comuns, então você pode ter uma variável chamada `lista` ou `logico`:

```portugol
algoritmo "NomesLivres"

var
    lista: lista
    logico: inteiro

inicio
    lista.adicionar("Luke")
    logico <- 42
    escreva(tamanho(lista))
    escreva(logico)
fim_algoritmo
```

```text
1
42
```

Um nome só pode ser declarado uma vez no bloco `var`. Usar uma variável que não foi declarada é erro (seção 11).

### Variáveis globais e locais

As variáveis do bloco `var` do topo do programa são **globais**: valem no `inicio` e dentro de todas as funções e métodos.

Também dá para declarar variáveis **locais** com `var` dentro do `inicio`, de uma `funcao` ou de um `metodo`. Elas existem só ali, da linha da declaração em diante. Há duas formas, que podem ser misturadas:

- **Com valor:** `var nome: tipo <- expressão` (ou `= expressão`). Só um nome por linha.
- **Em bloco:** `var` seguido de linhas `nome1, nome2: tipo`. Cada variável começa com o valor inicial do tipo.

```portugol
algoritmo "VarNoInicio"

inicio
    escreva("Preparando o treino...")
    var repeticoes: inteiro <- 3
    var
        golpe: cadeia
        total: inteiro
    golpe <- "corte"
    total <- repeticoes * 2
    escreva(golpe, " x ", total)
fim_algoritmo
```

```text
Preparando o treino...
corte x 6
```

Regras das variáveis locais:

- O `var` local fica no nível principal do corpo. Dentro de `se`, `senao`, `enquanto` ou `para` é erro: declare a variável antes do bloco.
- Usar a variável antes da linha do `var` é erro ("foi usada antes de ser declarada").
- Uma local não pode ter o nome de uma variável global, de um parâmetro, de outra local do mesmo corpo, de uma função ou de uma classe.
- As locais do `inicio` não são vistas dentro das funções. A seção 8 mostra locais em funções.

## 3. Atribuição, leitura e escrita

### Atribuição

Para guardar um valor numa variável, use `<-` ou `=` logo depois do nome:

```portugol
algoritmo "Atribuicao"

var
    x, n: inteiro

inicio
    x <- 1
    n = 2
    escreva(x + n)
fim_algoritmo
```

```text
3
```

> `=` só atribui quando começa um comando (`n = 2`). Dentro de uma expressão, `=` **compara** (seção 4).

### Leitura com `leia`

`leia(v)` espera o usuário digitar uma linha e guarda o valor em `v`, convertido pelo tipo da variável:

- `inteiro`: vira número inteiro;
- `real`/`float`: vira número real;
- `logico`: vira `verdadeiro` só se o texto for `verdadeiro` (ignorando maiúsculas e espaços nas pontas). Qualquer outro texto vira `falso`;
- os outros tipos: guardam o texto digitado.

```portugol
algoritmo "Cadastro"

var
    nome: cadeia
    idade: inteiro
    altura: real
    jedi: logico

inicio
    leia(nome)
    leia(idade)
    leia(altura)
    leia(jedi)
    escreva(nome, " terá ", idade + 1, " anos no ano que vem")
    escreva("altura em dobro: ", altura * 2)
    escreva("é jedi? ", jedi)
fim_algoritmo
```

```entrada
Luke
19
1.72
Verdadeiro
```

```text
Luke terá 20 anos no ano que vem
altura em dobro: 3.44
é jedi? verdadeiro
```

Para `logico`, "sim" não é `verdadeiro`:

```portugol
algoritmo "LeiaLogico"

var
    resposta: logico

inicio
    leia(resposta)
    escreva(resposta)
fim_algoritmo
```

```entrada
sim
```

```text
falso
```

### Escrita com `escreva`

`escreva` aceita um ou mais valores separados por vírgula. Ele os mostra **colados, sem espaço entre eles**, e pula uma linha no final. Valores lógicos aparecem como `verdadeiro` e `falso`.

```portugol
algoritmo "Escreva"

var
    forca: inteiro

inicio
    forca <- 8500
    escreva("Força: ", forca)
    escreva("A", "B", "C")
    escreva(verdadeiro)
    escreva("treinado: ", falso)
fim_algoritmo
```

```text
Força: 8500
ABC
verdadeiro
treinado: falso
```

### Concatenação mágica com `+`

Somar um texto com qualquer outro valor (número, lógico…) gera um texto. Não precisa converter nada:

```portugol
algoritmo "ConcatenacaoMagica"

var
    nomePadawan: cadeia
    nivelForca: inteiro

inicio
    nomePadawan <- "Luke"
    nivelForca <- 8500
    escreva("O nível de força de " + nomePadawan + " é " + nivelForca)
    escreva("Pronto? " + verdadeiro)
fim_algoritmo
```

```text
O nível de força de Luke é 8500
Pronto? verdadeiro
```

Cuidado com a ordem: o `+` é feito da esquerda para a direita. Enquanto só há números, ele soma. Depois que aparece um texto, ele cola. Use parênteses para somar antes:

```portugol
algoritmo "OrdemDaSoma"

inicio
    escreva(1 + 2 + " pontos")
    escreva("pontos: " + 1 + 2)
    escreva("pontos: " + (1 + 2))
fim_algoritmo
```

```text
3 pontos
pontos: 12
pontos: 3
```

### Aspas e barras dentro de textos

Para escrever uma aspa dentro de um texto, use `\"`. Para escrever uma barra invertida, use `\\`:

```portugol
algoritmo "Aspas"

inicio
    escreva("Yoda disse: \"Faça ou não faça\"")
    escreva("barra: \\")
fim_algoritmo
```

```text
Yoda disse: "Faça ou não faça"
barra: \
```

Todo texto precisa fechar as aspas na mesma linha em que abriu.

## 4. Expressões

### Aritméticos

| Operador | Operação |
|---|---|
| `+` | soma (ou concatenação com texto) |
| `-` | subtração e número negativo (`-x`) |
| `*` | multiplicação |
| `/` | divisão: o resultado é **sempre real** |
| `%` ou `mod` | resto da divisão |

```portugol
algoritmo "Aritmetica"

inicio
    escreva(7 + 2)
    escreva(7 - 2)
    escreva(7 * 2)
    escreva(7 / 2)
    escreva(6 / 2)
    escreva(7 % 2)
    escreva(7 mod 3)
    escreva(-7 + 2)
fim_algoritmo
```

```text
9
5
14
3.5
3.0
1
1
-5
```

Repare que `6 / 2` dá `3.0`, e não `3`. Não existe operador de divisão inteira. Para descartar a parte decimal, use `piso(a / b)` (seção 7).

### Relacionais

Comparam dois valores e dão `verdadeiro` ou `falso`. Os dois lados podem ser expressões completas (`x + 1 > tamanho(l) * 2`).

| Operador | Significa |
|---|---|
| `=` ou `==` | igual |
| `<>` ou `!=` | diferente |
| `<` `>` | menor, maior |
| `<=` `>=` | menor ou igual, maior ou igual |

```portugol
algoritmo "Comparacoes"

var
    x: inteiro
    b: logico

inicio
    x <- 1
    escreva(x = 1)
    escreva(x == 1)
    escreva(x <> 2)
    escreva(x != 1)
    escreva(x < 5, " ", x > 5, " ", x <= 1, " ", x >= 2)
    b <- x = 1
    escreva(b)
fim_algoritmo
```

```text
verdadeiro
verdadeiro
verdadeiro
falso
verdadeiro falso verdadeiro falso
verdadeiro
```

Em `b <- x = 1`, o primeiro sinal (`<-`) atribui e o `=` compara: `b` recebe o resultado da comparação. Já o `<-` nunca compara: `se x <- 1 entao` é erro (seção 11).

### Lógicos

| Operador | Resultado |
|---|---|
| `a e b` | `verdadeiro` se os dois forem verdadeiros |
| `a ou b` | `verdadeiro` se pelo menos um for verdadeiro |
| `nao a` | o contrário de `a` |

```portugol
algoritmo "Logicos"

var
    temSabre, temMestre: logico

inicio
    temSabre <- verdadeiro
    temMestre <- falso
    escreva(temSabre e temMestre)
    escreva(temSabre ou temMestre)
    escreva(nao temMestre)
fim_algoritmo
```

```text
falso
verdadeiro
verdadeiro
```

### Precedência

Quando uma expressão mistura operadores, o compilador resolve nesta ordem (do primeiro para o último):

| Ordem | Operadores |
|---|---|
| 1 | `-` negativo (`-x`) |
| 2 | `*` `/` `%` `mod` |
| 3 | `+` `-` |
| 4 | relacionais (`=` `==` `<>` `!=` `<` `>` `<=` `>=`) |
| 5 | `nao` |
| 6 | `e` |
| 7 | `ou` |

Parênteses mudam essa ordem: o que está dentro deles é resolvido primeiro.

```portugol
algoritmo "Precedencia"

var
    x: inteiro

inicio
    escreva(1 + 7 mod 3 * 2)
    escreva((1 + 2) * 3)
    x <- 5
    se nao x > 10 entao
        escreva("nao vale para (x > 10) inteiro")
    fim_se
    se verdadeiro ou falso e falso entao
        escreva("o e vem antes do ou")
    fim_se
fim_algoritmo
```

```text
3
9
nao vale para (x > 10) inteiro
o e vem antes do ou
```

Como o `nao` vem depois dos relacionais, `nao x > 10` significa `nao (x > 10)`. Na dúvida, use parênteses.

## 5. Controle de fluxo

### `se` / `senao`

Executa um bloco só se a condição for verdadeira. O `senao` é opcional e roda quando ela é falsa. Os parênteses em volta da condição são opcionais.

```portugol
algoritmo "ControleDeAcesso"

var
    nivelForca: inteiro

inicio
    nivelForca <- 9001
    se (nivelForca > 9000) entao
        escreva("É mais de 9000!")
    senao
        escreva("Ainda precisa de treinamento.")
    fim_se
fim_algoritmo
```

```text
É mais de 9000!
```

Para testar várias faixas, coloque um `se` dentro do `senao`. Cada `se` fecha com o seu próprio `fim_se`:

```portugol
algoritmo "Faixas"

var
    nota: inteiro

inicio
    nota <- 7
    se nota >= 9 entao
        escreva("Mestre Jedi")
    senao
        se nota >= 6 entao
            escreva("Cavaleiro Jedi")
        senao
            escreva("Padawan")
        fim_se
    fim_se
fim_algoritmo
```

```text
Cavaleiro Jedi
```

A condição pode ser qualquer valor lógico, sem operador relacional: uma variável `logico`, `verdadeiro`, uma chamada de função ou uma negação com `nao`.

```portugol
algoritmo "CondicaoLogica"

var
    pronto: logico

inicio
    pronto <- verdadeiro
    se pronto entao
        escreva("Que a Força esteja com você")
    fim_se
fim_algoritmo
```

```text
Que a Força esteja com você
```

### `enquanto`

Repete o bloco enquanto a condição for verdadeira. Use quando você não sabe quantas voltas o laço vai dar.

```portugol
algoritmo "Contagem"

var
    n: inteiro

inicio
    n <- 3
    enquanto n > 0 faca
        escreva(n, "...")
        n <- n - 1
    fim_enquanto
    escreva("Decolar!")
fim_algoritmo
```

```text
3...
2...
1...
Decolar!
```

### `para`

Repete o bloco para cada valor de uma variável de controle, de um valor inicial **até** um final. Os dois limites entram na contagem. A variável de controle precisa estar declarada.

```portugol
algoritmo "AfinarGuitarra"

var
    corda: inteiro

inicio
    // Iterando pelas 6 cordas de uma guitarra
    para corda de 1 ate 6 passo 1 faca
        escreva("Afinando a corda: " + corda)
    fim_para
fim_algoritmo
```

```text
Afinando a corda: 1
Afinando a corda: 2
Afinando a corda: 3
Afinando a corda: 4
Afinando a corda: 5
Afinando a corda: 6
```

O `passo` é opcional: sem ele, a variável aumenta de 1 em 1. Com `passo` negativo, o laço conta para trás:

```portugol
algoritmo "Passos"

var
    i: inteiro

inicio
    para i de 3 ate 1 passo -1 faca
        escreva(i)
    fim_para
    para i de 0 ate 6 passo 3 faca
        escreva("passo 3: ", i)
    fim_para
fim_algoritmo
```

```text
3
2
1
passo 3: 0
passo 3: 3
passo 3: 6
```

Os valores de `de`, `ate` e `passo` podem ser expressões. É o jeito de percorrer uma lista, que começa na posição 0:

```portugol
algoritmo "Setlist"

var
    musicas: lista
    i: inteiro

inicio
    musicas <- ["Intro", "Riff", "Solo"]
    para i de 0 ate tamanho(musicas) - 1 faca
        escreva(i + 1, ". ", musicas[i])
    fim_para
fim_algoritmo
```

```text
1. Intro
2. Riff
3. Solo
```

Se o início já passou do fim (contando para cima), o laço não roda nenhuma vez:

```portugol
algoritmo "IntervaloVazio"

var
    i: inteiro

inicio
    para i de 5 ate 1 faca
        escreva(i)
    fim_para
    escreva("fim")
fim_algoritmo
```

```text
fim
```

### `continue` e `interrompa`

Dentro de um laço, `continue` pula direto para a próxima volta e `interrompa` sai do laço. Os dois agem sobre o laço mais interno.

```portugol
algoritmo "PularCorda"

var
    corda: inteiro

inicio
    para corda de 1 ate 6 faca
        se corda = 3 entao
            continue      // pula a corda 3
        fim_se
        se corda = 5 entao
            interrompa    // para tudo na corda 5
        fim_se
        escreva("Afinando a corda ", corda)
    fim_para
fim_algoritmo
```

```text
Afinando a corda 1
Afinando a corda 2
Afinando a corda 4
```

```portugol
algoritmo "BuscaEmLargura"

var
    buscando: inteiro

inicio
    buscando = 1
    enquanto buscando = 1 faca
        escreva("Analisando nó...")
        interrompa // Sai do laço imediatamente
    fim_enquanto
fim_algoritmo
```

```text
Analisando nó...
```

### Blocos vazios

Um bloco pode ficar vazio, ou só com comentários, enquanto você ainda não escreveu aquela parte. Isso vale para `se`, `senao`, `enquanto`, `para`, funções, métodos e o próprio `inicio`. Um bloco vazio não faz nada.

```portugol
algoritmo "BlocosVazios"

var
    x: inteiro

inicio
    x <- 1
    se x > 0 entao
        // ainda vou escrever esta parte
    senao
    fim_se
    enquanto falso faca
    fim_enquanto
    escreva("ok")
fim_algoritmo
```

```text
ok
```

## 6. Coleções

### Listas

Uma lista guarda vários valores em ordem. Crie com colchetes: `[1, 2, 3]`. As posições começam em **0**: `l[0]` é o primeiro elemento.

```portugol
algoritmo "Mochila"

var
    itens: lista

inicio
    itens <- ["sabre", "capa"]
    itens.adicionar("holocron")
    escreva(itens[0])
    itens[1] <- "manto"
    escreva(itens)
    escreva(tamanho(itens), " itens")
    escreva("último: ", itens.removerFim())
    escreva(itens.tamanho(), " itens")
fim_algoritmo
```

```text
sabre
['sabre', 'manto', 'holocron']
3 itens
último: holocron
2 itens
```

Ao escrever uma lista inteira, os textos dentro dela aparecem com aspas simples.

```portugol
algoritmo "Repertorio"

var
    acordes, novos: lista

inicio
    acordes <- ["Mi", "Lá"]
    novos <- ["Ré", "Sol"]
    acordes.expandir(novos)
    escreva(tamanho(acordes))
    acordes.limpar()
    escreva(tamanho(acordes))
fim_algoritmo
```

```text
4
0
```

### Dicionários

Um dicionário guarda pares **chave: valor**. Crie com chaves, `{"chave": valor}`, e acesse com colchetes, `d["chave"]`.

```portugol
algoritmo "Inventario"

var
    estoque: dicionario

inicio
    estoque <- {"cordas": 6, "palhetas": 10}
    estoque["capotraste"] <- 1
    escreva(estoque["cordas"])
    escreva(estoque.pegar("palhetas"))
    estoque.atualizar({"palhetas": 12, "afinador": 1})
    escreva(estoque.pegar("palhetas"))
    escreva(tamanho(estoque))
    escreva(estoque.pegar("pedal"))
fim_algoritmo
```

```text
6
10
12
4
None
```

`pegar` devolve nulo quando a chave não existe, e o `escreva` mostra nulo como `None`. Já `estoque["pedal"]`, com colchetes, pararia o programa com erro. `atualizar` recebe **outro dicionário** e copia as chaves dele.

### Fila dupla

`filaDupla()` cria uma fila em que dá para colocar e tirar elementos nas duas pontas. Ela não é um tipo do `var`: declare a variável como `lista` e depois guarde a fila nela.

```portugol
algoritmo "FilaDoTreino"

var
    fila: lista

inicio
    fila <- filaDupla()
    fila.adicionarFim("Luke")
    fila.adicionarFim("Leia")
    fila.adicionarInicio("Rey")
    escreva(fila.tamanho())
    escreva(fila.removerInicio())
    escreva(fila.removerFim())
    escreva(tamanho(fila))
fim_algoritmo
```

```text
3
Rey
Leia
1
```

### Fila de prioridade

Uma `filaPrioridade` sempre entrega o **menor** valor primeiro, não importa a ordem em que eles entraram.

```portugol
algoritmo "Missoes"

var
    missoes: filaPrioridade
    tarefas: filaPrioridade

inicio
    missoes.inserir(3)
    missoes.inserir(1)
    missoes.inserir(2)
    escreva("próxima: ", missoes.espiar())
    escreva(missoes.remover())
    escreva(missoes.remover())
    escreva("restam ", tamanho(missoes))

    // Prioridade com nome: [prioridade, descrição]
    tarefas.inserir([2, "Treinar"])
    tarefas.inserir([1, "Resgatar"])
    escreva(tarefas.remover()[1])
fim_algoritmo
```

```text
próxima: 1
1
2
restam 1
Resgatar
```

### Criando coleções com `novo`

`novo lista()`, `novo dicionario()` e `novo filaPrioridade()` criam uma coleção nova e vazia, separada das outras:

```portugol
algoritmo "NovasColecoes"

var
    a, b: lista
    d: dicionario
    f: filaPrioridade

inicio
    a <- novo lista()
    b <- novo lista()
    a.adicionar(1)
    escreva(tamanho(a), " ", tamanho(b))
    d <- novo dicionario()
    d["jedi"] <- "Obi-Wan"
    escreva(d["jedi"])
    f <- novo filaPrioridade()
    f.inserir(5)
    escreva(f.tamanho())
fim_algoritmo
```

```text
1 0
Obi-Wan
1
```

### Tabela de métodos

Os métodos são chamados com ponto, `colecao.metodo(...)`, e funcionam tanto como comando quanto dentro de uma expressão.

| Método | Onde | O que faz |
|---|---|---|
| `adicionar(v)` | lista, fila dupla | coloca `v` no fim |
| `adicionarFim(v)` | lista, fila dupla | coloca `v` no fim |
| `adicionarInicio(v)` | fila dupla | coloca `v` no início |
| `removerFim()` | lista, fila dupla | tira e devolve o último elemento |
| `removerInicio()` | fila dupla | tira e devolve o primeiro elemento |
| `pegar(c)` | dicionário | devolve o valor da chave `c`, ou nulo se ela não existir |
| `atualizar(d)` | dicionário | copia as chaves do dicionário `d` |
| `expandir(l)` | lista, fila dupla | coloca no fim todos os elementos de `l` |
| `limpar()` | lista, dicionário, fila dupla | remove todos os elementos |
| `tamanho()` | texto, lista, dicionário, filas | número de elementos |
| `inserir(v)` | fila de prioridade | coloca `v` na fila |
| `remover()` | fila de prioridade | tira e devolve o menor valor |
| `espiar()` | fila de prioridade | devolve o menor valor sem tirar (nulo se a fila estiver vazia) |

> Escreva sempre `tamanho()` **com parênteses**. `x.tamanho` sem parênteses não dá erro de compilação, mas mostra um texto interno do Python em vez do número.

## 7. Funções nativas

O meuPiá já vem com estas funções:

| Função | Resultado |
|---|---|
| `tamanho(x)` | número de elementos de um texto, lista, dicionário ou fila |
| `raiz(x)` | raiz quadrada (real) |
| `potencia(x, y)` | `x` elevado a `y` (real) |
| `absoluto(x)` | valor sem sinal |
| `teto(x)` | arredonda para cima |
| `piso(x)` | arredonda para baixo |
| `seno(x)`, `cosseno(x)`, `tangente(x)` | trigonometria, com o ângulo em radianos |
| `pi` | a constante π. É um valor, usado **sem** parênteses |

```portugol
algoritmo "Matematica"

inicio
    escreva(raiz(16))
    escreva(potencia(2, 10))
    escreva(absoluto(-3))
    escreva(teto(2.1), " ", piso(2.9))
    escreva(seno(0), " ", cosseno(0), " ", tangente(0))
    escreva(teto(pi))
    escreva(piso(7 / 2))
    escreva(tamanho("Yoda"))
fim_algoritmo
```

```text
4.0
1024.0
3
3 2
0.0 1.0 0.0
4
3
4
```

### Seus nomes têm prioridade

Se você declarar uma variável, parâmetro, função ou classe com o mesmo nome de uma função nativa, vale **o seu**, no programa inteiro, e a nativa fica indisponível. Isso vale para `tamanho`, `raiz`, `potencia`, `seno`, `cosseno`, `tangente`, `teto`, `piso`, `pi`, `absoluto`, `verdadeiro`, `falso` e `filaDupla`.

```portugol
algoritmo "MeuPi"

var
    pi: inteiro

funcao raiz(x)
    retorne x + 1
fim_funcao

inicio
    pi <- 3
    escreva(pi)
    escreva(raiz(9))
fim_algoritmo
```

```text
3
10
```

## 8. Funções

Uma função é um pedaço de código com nome, que você pode chamar várias vezes. Ela é declarada antes do `inicio`, recebe **parâmetros sem tipo** entre parênteses e fecha com `fim_funcao`. `retorne` devolve um valor para quem chamou.

```portugol
algoritmo "Calculadora"

funcao somarSinais(a, b)
    retorne a + b
fim_funcao

inicio
    escreva(somarSinais(10, 5))
fim_algoritmo
```

```text
15
```

Uma função também pode só executar comandos, sem `retorne`. Dentro dela, você usa as variáveis globais normalmente, e as mudanças continuam valendo depois da chamada:

```portugol
algoritmo "Placar"

var
    pontos: inteiro

funcao marcar(valor)
    pontos <- pontos + valor
fim_funcao

funcao anunciar(nome)
    escreva(nome, " tem ", pontos, " pontos")
fim_funcao

inicio
    marcar(10)
    marcar(5)
    anunciar("Han")
fim_algoritmo
```

```text
Han tem 15 pontos
```

Os parâmetros e as variáveis declaradas com `var` dentro da função são **locais**: só existem durante aquela chamada. Cada chamada tem as suas, inclusive quando a função chama a si mesma (recursão):

```portugol
algoritmo "Fatorial"

funcao fatorial(n)
    var r: inteiro <- 1
    se n > 1 entao
        r <- n * fatorial(n - 1)   // cada chamada tem o seu próprio r
    fim_se
    retorne r
fim_funcao

funcao media(a, b)
    var soma: inteiro <- a + b
    retorne soma / 2
fim_funcao

inicio
    escreva("5! = ", fatorial(5))
    escreva("média: ", media(7, 8))
fim_algoritmo
```

```text
5! = 120
média: 7.5
```

Uma função pode devolver um lógico e ser usada direto como condição:

```portugol
algoritmo "EsvaziarMochila"

var
    mochila: lista

funcao vazia(l)
    retorne tamanho(l) = 0
fim_funcao

inicio
    mochila <- ["sabre", "capa"]
    enquanto nao vazia(mochila) faca
        escreva("tirando ", mochila.removerFim())
    fim_enquanto
    escreva("vazia? ", vazia(mochila))
fim_algoritmo
```

```text
tirando capa
tirando sabre
vazia? verdadeiro
```

Resumo do que uma função enxerga: os seus parâmetros, as suas variáveis locais (depois da linha do `var`), as variáveis globais, as outras funções, as classes e as funções nativas. As variáveis locais do `inicio` e de outras funções **não** são visíveis.

## 9. Classes

Uma classe é um molde para criar objetos que juntam dados (atributos) e ações (métodos).

- A classe começa com `classe Nome` e termina com `fim_classe`.
- Cada método começa com `metodo nome(parâmetros)` e termina com **`fim_funcao`**.
- O método `construtor` roda quando o objeto é criado com `novo Nome(...)`.
- Dentro dos métodos, os atributos são acessados sempre com **`self.`** (`self.nome`). Um atributo passa a existir quando você atribui um valor a ele, normalmente no `construtor`. Você não escreve `self` nos parâmetros: o compilador acrescenta sozinho.

```portugol
algoritmo "SistemaAgentes"

var
    inspetor: inteiro   // guarda o objeto (veja a nota abaixo)

classe AgenteBusca
    metodo construtor(n)
        self.nome <- n
    fim_funcao

    metodo investigar(ambiente)
        escreva(self.nome + " está investigando: " + ambiente)
    fim_funcao
fim_classe

inicio
    inspetor <- novo AgenteBusca("Agente Lang")
    inspetor.investigar("Rede Neural")
fim_algoritmo
```

```text
Agente Lang está investigando: Rede Neural
```

> **Nota:** ainda não existe um tipo para classes no `var` (`inspetor: AgenteBusca` dá erro). Por enquanto, declare a variável que vai guardar o objeto com qualquer tipo, como `inteiro`. O valor inicial é trocado pelo objeto na atribuição `inspetor <- novo AgenteBusca(...)`.

Cada objeto tem os seus próprios atributos, e um método pode devolver valores com `retorne`:

```portugol
algoritmo "Guitarras"

var
    g1, g2: inteiro

classe Guitarra
    metodo construtor(modelo, cordas)
        self.modelo <- modelo
        self.cordas <- cordas
        self.afinada <- falso
    fim_funcao

    metodo afinar()
        self.afinada <- verdadeiro
    fim_funcao

    metodo descricao()
        retorne self.modelo + " (" + self.cordas + " cordas) afinada: " + self.afinada
    fim_funcao
fim_classe

inicio
    g1 <- novo Guitarra("Stratocaster", 6)
    g2 <- novo Guitarra("Baixo", 4)
    g1.afinar()
    escreva(g1.descricao())
    escreva(g2.descricao())
fim_algoritmo
```

```text
Stratocaster (6 cordas) afinada: verdadeiro
Baixo (4 cordas) afinada: falso
```

## 10. Plugins e mPGP

O meuPiá pode ganhar funções novas com **plugins**. Para usar um, escreva `usar "nome"` logo depois da linha `algoritmo`:

| Plugin | Para quê |
|---|---|
| `usar "ia"` | Inteligência Artificial e ciência de dados |
| `usar "maker"` | IoT e robótica (ESP32/Pico) |
| `usar "espacial"` | controlar foguetes no Kerbal Space Program |
| `usar "testes"` | asserções para testar o seu algoritmo |
| `usar "grid"` | grade visual do Lab para algoritmos de busca |

Exemplo com o plugin `maker` (não executável aqui, porque precisa do plugin instalado):

```portugol nao-executar
algoritmo "PiscaLed"
usar "maker"

var
    led: inteiro

inicio
    led <- 2
    iot_configurar_pino(led, "saida")
    enquanto verdadeiro faca
        iot_ligar(led)
        iot_esperar(1000)
        iot_desligar(led)
        iot_esperar(1000)
    fim_enquanto
fim_algoritmo
```

As funções disponíveis (`iot_ligar`, etc.) vêm do plugin. Consulte a documentação de cada um.

Se o programa usar um plugin que não está instalado, ele para logo no começo com a mensagem `Erro: O plugin 'maker' não está instalado. Execute: mpgp instale maker`.

### Instalando plugins com o mPGP

O **mPGP** (meuPiá Gerenciador de Pacotes) é instalado junto com o `meupia`. Ele tem dois comandos:

```bash
mpgp list
```

Mostra os plugins disponíveis e marca os que já estão instalados.

```bash
mpgp instale maker
```

Baixa e instala o plugin (troque `maker` pelo nome desejado).

### Usando um arquivo Python seu

Com um nome que não está na tabela, `usar` importa um arquivo Python seu. Por exemplo, `usar "minhas_funcoes"` importa as funções de `minhas_funcoes.py`. O arquivo precisa estar num lugar em que o Python o encontre, como a mesma pasta do `.py` gerado.

```portugol nao-executar
algoritmo "UsaMeuModulo"
usar "minhas_funcoes"

inicio
    saudar("Luke")
fim_algoritmo
```

Se o arquivo não for encontrado, o programa para com `Erro: O arquivo local 'minhas_funcoes' não foi encontrado.`

## 11. Mensagens de erro

Quando o código tem um problema, o compilador não gera o programa e mostra **uma** mensagem neste formato:

```
Erro <etapa> na linha L, coluna C: <descrição>
```

- **etapa** diz em que fase o compilador encontrou o problema:
  - `léxico`: um caractere que não faz parte da linguagem, ou um texto sem aspas de fechamento;
  - `sintático`: o código não segue a gramática (palavra faltando ou fora do lugar);
  - `semântico`: a gramática está certa, mas o significado não (variável não declarada, nome repetido…).
- **linha** e **coluna** apontam o trecho do `.por` em que o compilador percebeu o problema, contando a partir de 1.

No terminal, o `meupia` mostra a mensagem depois de `[COMPILATION ERROR]:`.

### Erro léxico

```portugol nao-executar
algoritmo "ErroLexico"

var
    x: inteiro

inicio
    x <- 7 $ 2
fim_algoritmo
```

```text
Erro léxico na linha 7, coluna 12: caractere desconhecido "$"
```

O `$` não existe no meuPiá. A coluna 12 é exatamente onde ele está.

### Erro sintático

```portugol nao-executar
algoritmo "ErroSintatico"

var
    x: inteiro

inicio
    se x > 0 entao
        escreva("positivo")
fim_algoritmo
```

```text
Erro sintático na linha 9, coluna 1: comando inesperado: "fim_algoritmo"
```

Faltou o `fim_se`. O compilador só percebe isso quando chega ao `fim_algoritmo`, ainda dentro do `se`. **A linha do erro é onde o compilador percebeu o problema, que às vezes fica depois do engano de verdade.** Olhe também as linhas de cima.

Outro erro sintático comum é usar `<-` para comparar:

```portugol nao-executar
algoritmo "SetaNaCondicao"

var
    x: inteiro

inicio
    se x <- 1 entao
    fim_se
fim_algoritmo
```

```text
Erro sintático na linha 7, coluna 10: "<-" serve para atribuir; para comparar use "=" ou "=="
```

### Erro semântico

```portugol nao-executar
algoritmo "ControleDeAcesso"

inicio
    se (nivelForca > 9000) entao
        escreva("É mais de 9000!")
    fim_se
fim_algoritmo
```

```text
Erro semântico na linha 4, coluna 9: a variável "nivelForca" não foi declarada no bloco var
```

A gramática está certa, mas `nivelForca` nunca foi declarada. Para corrigir, declare-a no `var` (como no exemplo "ControleDeAcesso" da seção 5).

### Erros durante a execução

Se o programa compila, mas algo dá errado enquanto ele roda (dividir por zero, acessar uma posição que não existe na lista, digitar texto num `leia` de `inteiro`), quem mostra o erro é o Python, em inglês. Por exemplo, `escreva(1 / 0)` compila, mas para com `ZeroDivisionError: division by zero`.

## 12. Palavras reservadas e limitações conhecidas

### Palavras reservadas

Estas palavras fazem parte da linguagem e não podem ser usadas como nome de variável, função ou classe:

| Grupo | Palavras |
|---|---|
| Estrutura | `algoritmo`, `usar`, `var`, `inicio`, `fim_algoritmo` |
| Funções e classes | `funcao`, `retorne`, `fim_funcao`, `classe`, `metodo`, `fim_classe`, `novo` |
| Condicional | `se`, `entao`, `senao`, `fim_se` |
| Laços | `enquanto`, `faca`, `fim_enquanto`, `para`, `de`, `ate`, `passo`, `fim_para`, `continue`, `interrompa` |
| Entrada e saída | `leia`, `escreva` |
| Operadores | `e`, `ou`, `nao`, `mod` |
| Tipos | `inteiro`, `real`, `float`, `string`, `cadeia`, `dicionario`, `filaPrioridade` |

As formas acentuadas `então`, `senão`, `não`, `faça` e `até` também são aceitas.

Não são reservadas, mas têm um significado especial:

- `lista` e `logico` são tipos só depois do `:` e do `novo` (seção 2);
- `verdadeiro`, `falso`, `pi` e os nomes das funções nativas podem ser redeclarados, mas aí deixam de funcionar como nativos (seção 7);
- `self` é o próprio objeto dentro de um método.

### Limitações conhecidas

O que ainda **não** existe no meuPiá:

- **Parâmetros com tipo.** Escreva `funcao somar(a, b)`, sem tipo:

  ```portugol nao-executar
  algoritmo "ParametroTipado"
  funcao somar(inteiro a, inteiro b)
      retorne a + b
  fim_funcao
  inicio
      escreva(somar(1, 2))
  fim_algoritmo
  ```

  ```text
  Erro sintático na linha 2, coluna 14: esperado ")", encontrado "inteiro"
  ```

- **Atributos declarados na classe.** Os atributos são criados atribuindo `self.atributo` dentro de um método:

  ```portugol nao-executar
  algoritmo "AtributoDeclarado"
  classe Agente
      string nome
      metodo construtor(n)
          self.nome <- n
      fim_funcao
  fim_classe
  inicio
  fim_algoritmo
  ```

  ```text
  Erro sintático na linha 3, coluna 5: esperado "fim_classe", encontrado "string"
  ```

- **Acessar atributo sem `self.`.** Dentro do método, `nome` sozinho é uma variável, não o atributo:

  ```portugol nao-executar
  algoritmo "SemSelf"
  classe Agente
      metodo construtor(n)
          nome <- n
      fim_funcao
  fim_classe
  inicio
  fim_algoritmo
  ```

  ```text
  Erro semântico na linha 4, coluna 9: a variável "nome" não foi declarada no bloco var
  ```

- **Tipo de classe no `var`.** Use qualquer tipo para a variável que guarda o objeto (seção 9):

  ```portugol nao-executar
  algoritmo "TipoDeClasse"
  classe Agente
  fim_classe
  inicio
      var inspetor: Agente
  fim_algoritmo
  ```

  ```text
  Erro sintático na linha 5, coluna 19: esperado um tipo (inteiro, real, cadeia, logico, lista...), encontrado "Agente"
  ```

- **`var` dentro de `se`, `senao`, `enquanto` e `para`.** Declare a variável antes do bloco:

  ```portugol nao-executar
  algoritmo "VarNoLaco"
  var
      i: inteiro
  inicio
      para i de 1 ate 3 faca
          var dobro: inteiro <- i * 2
      fim_para
  fim_algoritmo
  ```

  ```text
  Erro sintático na linha 6, coluna 9: declare variáveis com var fora de blocos se, enquanto e para
  ```

- **Divisão inteira.** `/` sempre dá real. Use `piso(a / b)` para descartar a parte decimal (seção 7).

- **Comparação encadeada.** `1 < x < 5` não é aceito. Escreva `x > 1 e x < 5`.

- **`para` com limites ou passo reais.** Os valores de `de`, `ate` e `passo` precisam ser inteiros. Com valores reais, o programa compila, mas para com erro ao rodar:

  ```portugol nao-executar
  algoritmo "ParaReal"
  var
      i: real
  inicio
      para i de 0.5 ate 2 faca
          escreva(i)
      fim_para
  fim_algoritmo
  ```

- **`tamanho` sem parênteses.** Use `x.tamanho()` ou `tamanho(x)`. `x.tamanho` mostra um texto interno do Python (seção 6).
