"""Executa os exemplos do guia da linguagem (docs/guia-da-linguagem.md) como testes.

Convencoes do guia:
- ```portugol         algoritmo completo, executado; o bloco ```text seguinte e a saida exata.
                       Um bloco ```entrada opcional entre os dois vira a entrada do programa (leia).
- ```portugol nao-executar
                       nao e executado. Se o proximo bloco for ```text, e o erro de compilacao esperado;
                       senao, o codigo so precisa passar pelo lexico e pelo sintatico (ex.: plugins).
"""
import os
import re
import textwrap

import pytest

from meuPia.analyzers.lexical_analyzer import scan_line
from meuPia.analyzers.syntax_analyzer import Parser
from meuPia.tests.helpers import compilar, executar
from meuPia.utils.erros import ErroCompilacao

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMINHO_GUIA = os.path.join(RAIZ_PROJETO, 'docs', 'guia-da-linguagem.md')

MINIMO_EXECUTAVEIS = 20

# Bloco cercado por ``` (possivelmente indentado dentro de uma lista) ou titulo de secao '## N. Titulo'
PADRAO = re.compile(
    r'^(?P<indent>[ \t]*)```(?P<info>[^\n`]*)\n(?P<corpo>.*?)^(?P=indent)```[ \t]*$'
    r'|^## (?P<secao>\d+)\. (?P<titulo>[^\n]+)$',
    re.MULTILINE | re.DOTALL,
)


def slug(texto):
    texto = texto.lower()
    for de, para in zip('áàâãéêíóôõúç', 'aaaaeeiooouc'):
        texto = texto.replace(de, para)
    return re.sub(r'[^a-z0-9]+', '-', texto).strip('-')


def ler_blocos():
    """Retorna os blocos de codigo do guia, em ordem, com a linguagem, as opcoes, o conteudo e a secao."""
    with open(CAMINHO_GUIA, encoding='utf-8') as arquivo:
        guia = arquivo.read()

    blocos = []
    secao = 's00'
    for m in PADRAO.finditer(guia):
        if m.group('secao'):
            secao = f"s{int(m.group('secao')):02d}-{slug(m.group('titulo'))}"
            continue
        info = m.group('info').split()
        blocos.append({
            'lang': info[0] if info else '',
            'opcoes': info[1:],
            'codigo': textwrap.dedent(m.group('corpo')).rstrip('\n'),
            'secao': secao,
            'linha': guia.count('\n', 0, m.start()) + 1,
        })
    return blocos


def extrair_exemplos():
    """Agrupa cada bloco portugol com a entrada e a saida que vem logo depois dele."""
    blocos = ler_blocos()
    executaveis, nao_executar = [], []
    contagem = {}

    for i, bloco in enumerate(blocos):
        if bloco['lang'] != 'portugol':
            continue
        contagem[bloco['secao']] = contagem.get(bloco['secao'], 0) + 1
        exemplo = {
            'id': f"{bloco['secao']}-ex{contagem[bloco['secao']]}",
            'codigo': bloco['codigo'],
            'linha': bloco['linha'],
            'entrada': '',
            'saida': None,
        }
        j = i + 1
        if j < len(blocos) and blocos[j]['lang'] == 'entrada':
            exemplo['entrada'] = blocos[j]['codigo'] + '\n'
            j += 1
        if j < len(blocos) and blocos[j]['lang'] == 'text':
            exemplo['saida'] = blocos[j]['codigo']

        if 'nao-executar' in bloco['opcoes']:
            nao_executar.append(exemplo)
        else:
            executaveis.append(exemplo)

    return executaveis, nao_executar


EXECUTAVEIS, NAO_EXECUTAR = extrair_exemplos()
ERROS_ESPERADOS = [e for e in NAO_EXECUTAR if e['saida'] is not None]
SO_SINTAXE = [e for e in NAO_EXECUTAR if e['saida'] is None]


def ids(exemplos):
    return [e['id'] for e in exemplos]


@pytest.mark.parametrize('exemplo', EXECUTAVEIS, ids=ids(EXECUTAVEIS))
def test_exemplo_executavel(exemplo):
    assert exemplo['saida'] is not None, (
        f"o exemplo da linha {exemplo['linha']} do guia precisa de um bloco ```text com a saída esperada"
    )
    assert executar(exemplo['codigo'], exemplo['entrada']) == exemplo['saida']


@pytest.mark.parametrize('exemplo', ERROS_ESPERADOS, ids=ids(ERROS_ESPERADOS))
def test_exemplo_com_erro_de_compilacao(exemplo):
    with pytest.raises(ErroCompilacao) as erro:
        compilar(exemplo['codigo'])
    assert str(erro.value) == exemplo['saida']


@pytest.mark.parametrize('exemplo', SO_SINTAXE, ids=ids(SO_SINTAXE))
def test_exemplo_nao_executavel_passa_no_lexico_e_sintatico(exemplo):
    lexemas = []
    for i, linha in enumerate(exemplo['codigo'].split('\n')):
        _, tokens = scan_line(linha, i + 1)
        lexemas.extend(tokens)
    Parser(lexemas).parse()


def test_guia_tem_exemplos_executaveis_suficientes():
    assert len(EXECUTAVEIS) >= MINIMO_EXECUTAVEIS, (
        f'o guia tem {len(EXECUTAVEIS)} exemplos executáveis; o mínimo é {MINIMO_EXECUTAVEIS}'
    )
