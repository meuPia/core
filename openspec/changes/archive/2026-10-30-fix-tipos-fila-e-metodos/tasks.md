## 1. Testes que reproduzem os bugs

- [x] 1.1 Adicionar a `test_tipos.py` os cenários de tipos com maiúsculas (valor inicial, `leia`, local, elemento de lista tipada, `novo Dicionario()`). Verificar que falham.
- [x] 1.2 Adicionar a `test_builtins.py` os cenários de `filaPrioridade()` e de métodos de classe com nome de método de coleção. Verificar que falham.
- [x] 1.3 Adicionar a `test_analise_semantica.py` os cenários de métodos repetidos e sinônimos. Verificar que falham.

## 2. Correções

- [x] 2.1 Em `grammar_tipo`, guardar o tipo em minúsculas quando ele é palavra-chave; em `grammar_tipo_elemento`, devolver o elemento em minúsculas. No gerador, comparar `dicionario` sem diferenciar caixa. Verificar 1.1.
- [x] 2.2 Em `grammar_primario`, aceitar `filaPrioridade` seguido de `(` como chamada. Verificar 1.2.
- [x] 2.3 Em `gen_method_definition`, traduzir o nome do método por `METODOS`, como já acontece nas chamadas. Verificar 1.2.
- [x] 2.4 No semântico, recusar dois métodos da mesma classe com o mesmo nome no Python. Verificar 1.3.

## 3. Verificação

- [x] 3.1 Rodar a suíte completa: 379 testes passando, 2 pulados.
- [x] 3.2 Comparar o Python gerado antes e depois para `exemplos/`, `meuPia/input/` e os desafios: 20 de 20 idênticos.
- [x] 3.3 Atualizar `docs/referencia-do-dialeto.md`.
- [x] 3.4 Sincronizar as specs principais e arquivar o change.
