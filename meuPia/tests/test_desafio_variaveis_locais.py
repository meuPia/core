import re

import pytest

from meuPia.tests.helpers import compilar, executar

# Solucao de aluno no estilo do desafio ontologia_hospital, usando variavel local na funcao
CODIGO_ALUNO = '''algoritmo "JSONLD"
var sinonimos: lista

funcao consolidar_nomes(json_legado, json_sus, json_tuss)
    var nomes: lista <- []
    nomes.adicionar(json_legado.pegar("descricao"))
    nomes.adicionar(json_sus.pegar("procedimento"))
    nomes.adicionar(json_tuss.pegar("termo"))
    retorne nomes
fim_funcao

inicio
    escreva("Fundindo prontuários pelo @id...")
fim_algoritmo'''

# codigoTeste original do desafio: declara variaveis dentro do inicio
CODIGO_TESTE = '''var legado, sus, tuss : dicionario
var resultado : inteiro

legado <- {"descricao": "Hemograma"}
sus <- {"procedimento": "Hemograma Completo"}
tuss <- {"termo": "Hemograma com Plaquetas"}

resultado <- consolidar_nomes(legado, sus, tuss)

esperar_igual(resultado.tamanho(), 3, "O motor extraiu e fundiu os 3 sinônimos caóticos")
esperar_igual(resultado[0], "Hemograma", "Extraiu corretamente a chave do sistema legado")'''


def montar_como_o_lab(codigo_aluno, codigo_teste):
    # Mesma montagem de meuPia-lab/src/engine/wasm.js
    codigo = re.sub('fim_algoritmo', '', codigo_aluno, flags=re.IGNORECASE)
    if 'usar "testes"' not in codigo.lower():
        codigo = re.sub(r'(algoritmo\s+"[^"]*")', r'\1\nusar "testes"', codigo, count=1, flags=re.IGNORECASE)
    return codigo + '\n\n// --- TESTES AUTOMATIZADOS ---\n' + codigo_teste + '\nfim_algoritmo'


def test_desafio_com_var_no_inicio_compila():
    compile(compilar(montar_como_o_lab(CODIGO_ALUNO, CODIGO_TESTE)), 'desafio', 'exec')


def test_desafio_com_var_no_inicio_passa_nos_testes():
    pytest.importorskip('meupia_testes')
    saida = executar(montar_como_o_lab(CODIGO_ALUNO, CODIGO_TESTE))
    assert saida.count('[TESTE_OK]') == 2
    assert '[TESTE_FALHA]' not in saida
