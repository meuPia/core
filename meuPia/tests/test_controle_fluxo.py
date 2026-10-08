from meuPia.tests.helpers import executar, programa


# --- Blocos vazios geram programa executavel ---

def test_programa_minimo_sem_var_e_sem_comandos():
    assert executar('algoritmo "T"\ninicio\nfim_algoritmo') == ''


def test_se_com_corpo_vazio():
    codigo = programa('x <- 1\nse x > 0 entao\nfim_se\nescreva("ok")', var='x: inteiro')
    assert executar(codigo) == 'ok'


def test_senao_vazio():
    codigo = programa('x <- 0\nse x > 0 entao\nescreva("a")\nsenao\nfim_se\nescreva("ok")', var='x: inteiro')
    assert executar(codigo) == 'ok'


def test_corpo_de_se_so_com_comentario():
    codigo = programa('se verdadeiro entao\n// nada\nfim_se\nescreva("ok")')
    assert executar(codigo) == 'ok'


def test_enquanto_e_para_vazios():
    codigo = programa(
        'enquanto falso faca\nfim_enquanto\npara i de 1 ate 3 faca\nfim_para\nescreva(i)',
        var='i: inteiro'
    )
    assert executar(codigo) == '3'


def test_funcao_vazia_em_programa_sem_var():
    codigo = programa('f()\nescreva("ok")', antes='funcao f()\nfim_funcao')
    assert executar(codigo) == 'ok'


def test_metodo_vazio():
    codigo = programa(
        'p <- novo P()\np.m()\nescreva("ok")',
        var='p: inteiro',
        antes='classe P\nmetodo m()\nfim_funcao\nfim_classe'
    )
    assert executar(codigo) == 'ok'


# --- Limites e passo do para aceitam expressoes ---

def test_para_limite_final_com_subtracao():
    codigo = programa('n <- 3\npara i de 0 ate n - 1 faca\nescreva(i)\nfim_para', var='n, i: inteiro')
    assert executar(codigo) == '0\n1\n2'


def test_para_limites_com_chamada_de_funcao():
    codigo = programa(
        'l <- [5, 6, 7]\npara i de 1 ate tamanho(l) - 1 faca\nescreva(l[i])\nfim_para',
        var='l, i: inteiro'
    )
    assert executar(codigo) == '6\n7'


# --- Limite final do para inclusivo nos dois sentidos ---

def para(cabecalho, var='i, p: inteiro', antes=''):
    return executar(programa(f'{antes}\npara {cabecalho} faca\nescreva(i)\nfim_para', var=var))


def test_para_passo_negativo_literal():
    assert para('i de 3 ate 1 passo -1') == '3\n2\n1'


def test_para_passo_negativo_em_variavel():
    assert para('i de 6 ate 2 passo p', antes='p <- -2') == '6\n4\n2'


def test_para_passo_positivo_maior_que_um():
    assert para('i de 0 ate 6 passo 3') == '0\n3\n6'


def test_para_intervalo_vazio():
    codigo = programa('para i de 5 ate 1 faca\nescreva(i)\nfim_para\nescreva("fim")', var='i: inteiro')
    assert executar(codigo) == 'fim'


def test_para_passo_zero_e_erro_de_execucao():
    import pytest
    with pytest.raises(ValueError, match='passo'):
        para('i de 1 ate 3 passo 0')


# --- continue e interrompa ---

def test_continue_pula_iteracao():
    codigo = programa(
        'para i de 1 ate 3 faca\nse i = 2 entao\ncontinue\nfim_se\nescreva(i)\nfim_para', var='i: inteiro'
    )
    assert executar(codigo) == '1\n3'


def test_interrompa_encerra_laco():
    codigo = programa(
        'para i de 1 ate 3 faca\nse i = 2 entao\ninterrompa\nfim_se\nescreva(i)\nfim_para', var='i: inteiro'
    )
    assert executar(codigo) == '1'
