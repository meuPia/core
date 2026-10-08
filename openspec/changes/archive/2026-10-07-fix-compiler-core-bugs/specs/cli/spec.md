## Purpose

Define o contrato de compilação usado pelo comando `meupia` e pelo meuPia-lab: argumentos, código de saída, arquivos gerados e o que acontece em caso de erro.

## ADDED Requirements

### Requirement: Código de saída do comando meupia
O comando `meupia <arquivo.por>` SHALL terminar com código de saída `0` quando a compilação tiver sucesso. SHALL terminar com código diferente de `0` quando: houver erro de compilação, o arquivo não existir ou nenhum arquivo for informado.

#### Scenario: Compilação bem-sucedida
- **WHEN** o usuário executa `meupia ok.por` com um programa válido
- **THEN** o processo termina com código `0`

#### Scenario: Erro de compilação
- **WHEN** o usuário executa `meupia ruim.por` com um programa que contém `x <- 7 $ 2`
- **THEN** o processo termina com código diferente de `0`
- **AND** a saída contém `[COMPILATION ERROR]` seguido da mensagem de erro padronizada

#### Scenario: Arquivo inexistente
- **WHEN** o usuário executa `meupia nao_existe.por`
- **THEN** o processo termina com código diferente de `0`

#### Scenario: Nenhum arquivo informado
- **WHEN** o usuário executa `meupia` sem argumentos
- **THEN** o processo termina com código diferente de `0` e mostra como usar o comando

#### Scenario: Execução como módulo
- **WHEN** o usuário executa `python -m meuPia.compiler ruim.por` com um programa inválido
- **THEN** o processo termina com código diferente de `0`

### Requirement: Contrato da função de compilação usada pelo Lab
A função `main(arquivo, pasta_saida)` SHALL, em caso de sucesso, gravar `<pasta_saida>/<nome_do_arquivo_sem_extensão>.py` e retornar `0`. Em caso de erro, SHALL retornar um valor diferente de `0`, SHALL não gravar esse arquivo e SHALL não lançar exceção para quem chamou. A mensagem de erro SHALL ser escrita na saída padrão.

#### Scenario: Sucesso gera o arquivo Python
- **WHEN** o Lab chama `main("main.por", "output")` com um programa válido
- **THEN** o retorno é `0`
- **AND** o arquivo `output/main.py` existe e executa sem erro

#### Scenario: Erro não gera o arquivo
- **WHEN** o Lab chama `main("main.por", "output")` com um programa inválido, e `output/main.py` não existia antes
- **THEN** o retorno é diferente de `0`
- **AND** `output/main.py` continua não existindo
- **AND** nenhuma exceção é propagada para quem chamou

### Requirement: Programas de exemplo do repositório compilam
Todo arquivo `.por` versionado em `exemplos/` e em `meuPia/input/` SHALL compilar sem erro com a versão atual do compilador.

#### Scenario: Exemplo smart_security
- **WHEN** `exemplos/smart_security.por` é compilado
- **THEN** a compilação tem sucesso e o Python gerado é sintaticamente válido

#### Scenario: Programas de entrada
- **WHEN** cada `.por` de `meuPia/input/` é compilado
- **THEN** todos compilam com sucesso
