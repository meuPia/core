import pytest

from meuPia.analyzers.syntax_analyzer import SyntacticError
from meuPia.tests.helpers import compilar, executar, programa


def se_ok(condicao, antes='', var='x: inteiro'):
    corpo = f'{antes}\nse {condicao} entao\nescreva("ok")\nfim_se'
    return executar(programa(corpo, var=var))


# --- Comparacao entre expressoes aritmeticas completas ---

def test_soma_no_lado_esquerdo():
    assert se_ok('x + 1 > 0', antes='x <- 0') == 'ok'


def test_expressao_entre_parenteses():
    assert se_ok('(x + 1) > 0', antes='x <- 0') == 'ok'


def test_literal_negativo_no_lado_direito():
    assert se_ok('x > -1', antes='x <- 0') == 'ok'


def test_menos_unario_no_lado_esquerdo():
    assert se_ok('-x < 0', antes='x <- 2') == 'ok'


def test_chamada_e_indexacao_nos_dois_lados():
    assert se_ok('tamanho(l) * 2 >= l[0] + l[1]', antes='l <- [3, 1]', var='l: inteiro') == 'ok'


def test_comparacao_entre_parenteses_combinada_com_logico():
    assert se_ok('(x > 0) e (x < 10) ou (x = 0)', antes='x <- 0') == 'ok'


# --- Condicao sem operador relacional ---

def test_condicao_literal_logico():
    assert se_ok('verdadeiro', var='') == 'ok'


def test_condicao_variavel_logica():
    assert se_ok('b', antes='b <- verdadeiro', var='b: logico') == 'ok'


def test_condicao_chamada_de_funcao_com_nao():
    codigo = programa(
        'l <- [1]\nenquanto nao vazio(l) faca\nl.removerFim()\nfim_enquanto\nescreva(tamanho(l))',
        var='l: inteiro',
        antes='funcao vazio(l)\nretorne tamanho(l) = 0\nfim_funcao'
    )
    assert executar(codigo) == '0'


# --- Significado de =, == e <- conforme o contexto ---

def test_atribuicao_com_seta_e_com_igual():
    codigo = programa('x <- 1\nn = 2\nescreva(x + n)', var='x, n: inteiro')
    assert executar(codigo) == '3'


def test_igualdade_com_igual_e_igual_duplo():
    codigo = programa(
        'x <- 1\nse x = 1 entao\nescreva("a")\nfim_se\nse x == 1 entao\nescreva("b")\nfim_se',
        var='x: inteiro'
    )
    assert executar(codigo) == 'a\nb'


def test_igualdade_como_valor_atribuido():
    codigo = programa('x <- 1\nb <- x = 1\nescreva(b)', var='x: inteiro\nb: logico')
    assert executar(codigo) == 'verdadeiro'


def test_seta_dentro_de_condicao_e_rejeitada():
    codigo = programa('se x <- 1 entao\nfim_se', var='x: inteiro')
    with pytest.raises(SyntacticError) as excinfo:
        compilar(codigo)
    # linha 5 = 'se x <- 1 entao' (algoritmo, var, x: inteiro, inicio, se...); '<-' na coluna 6
    assert excinfo.value.linha == 5
    assert excinfo.value.coluna == 6


# --- Operador != ---

def test_diferente_com_exclamacao():
    assert se_ok('x != 1', antes='x <- 0') == 'ok'


def test_diferente_com_menor_maior():
    assert se_ok('x <> 1', antes='x <- 0') == 'ok'


# --- Operador de resto ---

def test_resto_com_porcentagem():
    assert executar(programa('x <- 7 % 2\nescreva(x)', var='x: inteiro')) == '1'


def test_resto_com_mod():
    assert executar(programa('x <- 7 mod 3\nescreva(x)', var='x: inteiro')) == '1'


def test_resto_com_precedencia_de_multiplicacao():
    assert executar(programa('x <- 1 + 7 mod 3 * 2\nescreva(x)', var='x: inteiro')) == '3'


# --- Precedencia ---

def test_e_antes_de_ou():
    assert se_ok('verdadeiro ou falso e falso', var='') == 'ok'


def test_nao_aplicado_a_comparacao():
    assert se_ok('nao x > 10', antes='x <- 5') == 'ok'


def test_parenteses_mudam_precedencia():
    assert executar(programa('x <- (1 + 2) * 3\nescreva(x)', var='x: inteiro')) == '9'
