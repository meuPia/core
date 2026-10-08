from meuPia.tests.helpers import executar, programa


def test_executar_ola():
    assert executar(programa('escreva("Olá")')) == 'Olá'


def test_executar_com_entrada():
    codigo = programa('leia(n)\nescreva(n + 1)', var='n: inteiro')
    assert executar(codigo, entrada='41\n') == '42'
