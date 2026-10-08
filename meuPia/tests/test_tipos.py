import pytest

from meuPia.analyzers.lexical_analyzer import LexicalError
from meuPia.analyzers.syntax_analyzer import SyntacticError
from meuPia.tests.helpers import compilar, executar, programa


# --- Tipos declaraveis e valores iniciais ---

def test_valor_inicial_de_logico():
    assert executar(programa('escreva(b)', var='b: logico')) == 'falso'


def test_valor_inicial_de_lista():
    assert executar(programa('l.adicionar(1)\nescreva(tamanho(l))', var='l: lista')) == '1'


def test_valores_iniciais_numericos_e_de_texto():
    codigo = programa('escreva(n + r)\nescreva(tamanho(s))', var='n: inteiro\nr: real\ns: cadeia')
    assert executar(codigo) == '0.0\n0'


def test_tipo_desconhecido():
    with pytest.raises(SyntacticError) as excinfo:
        compilar(programa('', var='x: numero'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 4)


# --- lista e logico nao sao palavras reservadas ---

def test_variavel_chamada_lista():
    assert executar(programa('lista <- 5\nescreva(lista)', var='lista: inteiro')) == '5'


def test_variavel_chamada_lista_com_tipo_lista():
    codigo = programa('lista.adicionar(1)\nescreva(tamanho(lista))', var='lista: lista')
    assert executar(codigo) == '1'


def test_varios_tipos_lista_no_mesmo_bloco_var():
    compilar(programa('', var='a: lista\nb: lista\nc, d: logico\nf: logico'))


def test_variavel_chamada_logico():
    assert executar(programa('logico <- 1\nescreva(logico + 1)', var='logico: inteiro')) == '2'


# --- Leitura de logico ---

def test_leitura_de_verdadeiro():
    assert executar(programa('leia(b)\nescreva(b)', var='b: logico'), entrada=' Verdadeiro \n') == 'verdadeiro'


def test_leitura_de_outro_texto():
    assert executar(programa('leia(b)\nescreva(b)', var='b: logico'), entrada='sim\n') == 'falso'


# --- Criacao de colecoes nativas com novo ---

def test_novo_dicionario():
    codigo = programa('d <- novo dicionario()\nd["a"] <- 1\nescreva(tamanho(d))', var='d: dicionario')
    assert executar(codigo) == '1'


def test_novo_lista_cria_colecoes_independentes():
    codigo = programa(
        'a <- novo lista()\nb <- novo lista()\na.adicionar(1)\nescreva(tamanho(b))', var='a, b: lista'
    )
    assert executar(codigo) == '0'


def test_novo_fila_prioridade():
    codigo = programa(
        'f <- novo filaPrioridade()\nf.inserir(3)\nf.inserir(1)\nescreva(f.remover())', var='f: filaPrioridade'
    )
    assert executar(codigo) == '1'


# --- Literais de string com barra invertida ---

def test_string_terminada_em_barra_invertida():
    assert executar(programa('escreva("a\\\\")')) == 'a\\'


def test_string_com_aspa_escapada():
    assert executar(programa('escreva("diga \\"oi\\"")')) == 'diga "oi"'


def test_string_nao_terminada():
    codigo = 'algoritmo "T"\ninicio\nescreva("abc)\nfim_algoritmo'
    with pytest.raises(LexicalError) as excinfo:
        compilar(codigo)
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 9)
