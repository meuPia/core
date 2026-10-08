# meuPiá Core – O Compilador Modular de Portugol

![meuPia](https://github.com/meuPia/core/raw/main/assets/meuPia.png)

## 📖 Overview

> **Nota:** Este projeto é um *fork* evolutivo do [`portugol-compiler`](https://www.google.com/search?q=%5Bhttps://github.com/LuanContarin/portugol-compiler%5D(https://github.com/LuanContarin/portugol-compiler)), focado em interoperabilidade e modularização.

**meuPiá Core** é o motor central do ecossistema meuPiá. Ele é um compilador (transpilador) de Portugol para Python projetado para ser **extensível**.

Diferente de ferramentas educacionais fechadas, o meuPiá permite que você instale **plugins** para expandir as capacidades da linguagem. O Core fornece a infraestrutura de análise, geração de código e o gerenciador de pacotes, enquanto as funcionalidades específicas (como IoT ou Foguetes) são instaladas sob demanda.

**meuPiá Core** fornece:

* **O Compilador:** Analisadores léxico, sintático e semântico que traduzem Portugol para Python otimizado.
* **mPGP (meuPiá Gerenciador de Pacotes):** Uma ferramenta de linha de comando integrada para instalar e gerenciar extensões oficiais.
* **Sistema de Plugins:** Suporte nativo à diretiva `usar "nome_do_plugin"`, permitindo importação dinâmica de bibliotecas.

## ⚙️ How It Works

A arquitetura foi modernizada para suportar extensões:

### 1. Analysis & Validation

O compilador realiza a análise léxica e sintática completa, garantindo a integridade lógica do algoritmo escrito em Portugol.

### 2. Plugin-Aware Code Generation

O `CodeGenerator` identifica as diretivas `usar "..."` e injeta automaticamente as dependências corretas no código Python final, otimizando os imports para o ambiente de destino (seja PC ou Microcontrolador).

### 3. Runtime Modular

O Core mantém apenas as bibliotecas essenciais. Funcionalidades complexas foram movidas para pacotes externos instaláveis via mPGP.

## 🚀 Installation

A maneira mais recomendada de instalar o **meuPiá** é através do índice oficial de pacotes do Python (PyPI).

No seu terminal, execute:

```bash
pip install meupia-core
```

Para Desenvolvedores (Modo Editável)

Se você deseja modificar o código-fonte do compilador:

```bash
# Clone o repositório
git clone https://github.com/meuPia/core.git
cd core

# Instale em modo editável (recomendado para dev)
pip install -e .

```

Isto instalará dois comandos no seu terminal:

* `meupia`: O compilador.
* `mpgp`: O gerenciador de pacotes.

## 📚 Guia da Linguagem

A sintaxe completa do meuPiá, com exemplos testados automaticamente, está no [Guia da Linguagem](docs/guia-da-linguagem.md).

## 📦 mPGP – Gerenciador de Pacotes

O **mPGP** (meuPiá Package Manager) facilita a instalação de módulos adicionais sem que o aluno precise lidar com URLs complexas ou configurações de ambiente.

### Comandos Básicos

```bash
# Listar plugins disponíveis (e quais já estão instalados)
mpgp list

# Instalar um plugin
mpgp instale <nome_do_plugin>
```

### Módulos Oficiais Disponíveis

| Módulo | Comando de Instalação | Descrição |
| --- | --- | --- |
| **Maker** | `mpgp instale maker` | Adiciona suporte a **IoT e Robótica**. Permite compilar Portugol para **ESP32/Pico** (MicroPython). |
| **Espacial** | `mpgp instale espacial` | Adiciona suporte ao **Kerbal Space Program**. Permite controlar foguetes via kRPC. |
| **IA** | `mpgp instale ia` | Adiciona suporte a **Data Science**. Traz algoritmos do Scikit-Learn para o Portugol. |

---

## 🛠️ Usage Examples

### 1. Compilando um Algoritmo Básico

```bash
# Compila o arquivo e gera o Python equivalente na pasta output/
meupia input/ola_mundo.por

```

### 2. Usando Plugins (Ex: IoT/Maker)

Após instalar o módulo maker (`mpgp instale maker`), você pode utilizá-lo no seu código:

```portugol
algoritmo "PiscaLed"
usar "maker"  // <--- Carrega o plugin instalado via mPGP

var led: inteiro
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

### 3. Variáveis Locais

Além das variáveis globais do bloco `var` (antes de `funcao` e `inicio`), é possível declarar variáveis **locais** com `var` dentro de uma `funcao`, de um `metodo` ou do bloco `inicio`. Existem duas formas, que podem ser misturadas no mesmo `var`:

* **Com valor:** `var nome: tipo <- expressao` (ou `= expressao`). Só pode ter um nome por linha.
* **Em bloco:** `var` seguido de linhas `nome1, nome2: tipo`. Cada variável começa com o valor inicial do tipo (`0`, `0.0`, `""`, `falso`, lista vazia…).

```portugol
algoritmo "Medias"

funcao media(a, b)
    var soma: inteiro <- a + b
    var
        resultado: real
        passos: inteiro
    resultado <- soma / 2
    retorne resultado
fim_funcao

funcao fatorial(n)
    var r: inteiro <- 1
    se n > 1 entao
        r <- n * fatorial(n - 1)   // cada chamada tem o seu próprio 'r'
    fim_se
    retorne r
fim_funcao

inicio
    escreva("Média: ", media(7, 8))
    var f: inteiro <- fatorial(5)
    escreva("5! = ", f)
fim_algoritmo
```

Regras:

* **Onde:** em qualquer ponto do nível principal do corpo da `funcao`, do `metodo` ou do `inicio`. Dentro de `se`, `enquanto` e `para` a declaração é erro: declare a variável antes do bloco.
* **Escopo:** a variável só existe no corpo onde foi declarada, da linha da declaração até o fim do corpo. Locais do `inicio` não são vistas dentro das funções.
* **Tempo de vida:** cada chamada da função cria variáveis novas (inclusive em recursão).
* **Nomes:** uma local não pode ter o nome de uma variável global, de um parâmetro, de outra local do mesmo corpo, de uma função, de uma classe nem ser `self`.
* **Ordem:** usar a variável antes da linha do `var` é erro (`a variável "x" foi usada antes de ser declarada`).



## 🙌 Credits

> **meuPiá** é desenvolvido com ❤️ por **[@henryhamon](https://github.com/henryhamon)**.

Este projeto é um *hard fork* e evolução do projeto [portugol-compiler](https://github.com/LuanContarin/portugol-compiler), criado originalmente por **Luan Contarin**. A estrutura de análise léxica e sintática é mantida como a fundação sólida deste compilador.
