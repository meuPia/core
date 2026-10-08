## Why

O "Guia da Linguagem meuPiá" foi escrito antes das specs oficiais e contradiz o compilador: só §1, §2 e os laços de §4 funcionam. Os alunos precisam de um guia que reflita o comportamento real e que não volte a ficar desatualizado.

## What Changes

- Novo `docs/guia-da-linguagem.md`, derivado das specs de `openspec/specs/`, com 12 seções para iniciantes.
- Novo `meuPia/tests/test_guia.py`: executa cada exemplo `portugol` e compara com o bloco `text` seguinte (com bloco `entrada` opcional); blocos `portugol nao-executar` seguidos de `text` devem falhar com a mensagem mostrada; os demais só passam pelo léxico e sintático; exige no mínimo 20 exemplos executáveis.
- `README.md`: corrige o exemplo PiscaLed (`fim_enquanto`, `fim_algoritmo`, `mpgp instale maker`), os comandos do mPGP (`mpgp list`, `mpgp instale`) e remove `mpm`; adiciona link para o guia.

## Capabilities

### New Capabilities
Nenhuma.

### Modified Capabilities
Nenhuma. Só documentação e testes: o comportamento do compilador não muda (`skip_specs: true`).

## Impact

- Arquivos: `docs/guia-da-linguagem.md`, `meuPia/tests/test_guia.py`, `README.md`.
- Sem mudança de código do compilador nem de versão.
