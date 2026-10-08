import re

import pytest

from meuPia.analyzers.lexical_analyzer import LexicalError
from meuPia.analyzers.semantic_analyzer import SemanticError
from meuPia.analyzers.syntax_analyzer import SyntacticError
from meuPia.tests.helpers import compilar, executar, programa

TERMOS_INTERNOS = re.compile(r'Undeclared|Double|identifier|integer value|string value|\bID\b|\bATR\b|\bNUMINT\b')


def erro_de(codigo, tipo):
    with pytest.raises(tipo) as excinfo:
        compilar(codigo)
    return str(excinfo.value)


# --- Formato padronizado das mensagens de erro ---

def test_mensagem_erro_lexico():
    codigo = 'algoritmo "T"\nvar x: inteiro\ninicio\nx <- 7 $ 2\nfim_algoritmo'
    mensagem = erro_de(codigo, LexicalError)
    assert mensagem.startswith('Erro léxico na linha 4, coluna 8: ')
    assert '"$"' in mensagem


def test_mensagem_erro_sintatico_no_fim_do_arquivo():
    codigo = 'algoritmo "T"\ninicio\nescreva("a")'
    mensagem = erro_de(codigo, SyntacticError)
    assert mensagem.startswith('Erro sintático na linha 3, coluna 12: ')
    assert not TERMOS_INTERNOS.search(mensagem)


def test_mensagem_erro_sintatico_arquivo_vazio():
    mensagem = erro_de('', SyntacticError)
    assert mensagem.startswith('Erro sintático na linha 1, coluna 1: ')


def test_mensagem_erro_sintatico_sem_nomes_internos():
    codigo = 'algoritmo "T"\nvar\n: inteiro\ninicio\nfim_algoritmo'
    mensagem = erro_de(codigo, SyntacticError)
    assert mensagem.startswith('Erro sintático na linha ')
    assert not TERMOS_INTERNOS.search(mensagem)


def test_mensagem_erro_semantico_sem_nomes_internos():
    codigo = 'algoritmo "T"\ninicio\nescreva(y)\nfim_algoritmo'
    mensagem = erro_de(codigo, SemanticError)
    assert mensagem.startswith('Erro semântico na linha 3, coluna 9: ')
    assert '"y"' in mensagem
    assert not TERMOS_INTERNOS.search(mensagem)


def test_mensagem_declaracao_duplicada():
    codigo = 'algoritmo "T"\nvar\nx: inteiro\n    x: real\ninicio\nfim_algoritmo'
    mensagem = erro_de(codigo, SemanticError)
    assert mensagem.startswith('Erro semântico na linha 4, coluna 5: ')
    assert '"x"' in mensagem
    assert not TERMOS_INTERNOS.search(mensagem)


def test_erros_compartilham_classe_base():
    from meuPia.utils.erros import ErroCompilacao
    assert issubclass(LexicalError, ErroCompilacao)
    assert issubclass(SyntacticError, ErroCompilacao)
    assert issubclass(SemanticError, ErroCompilacao)


# --- Nomes validos em cada escopo ---

CLASSE_PESSOA = (
    'classe Pessoa\n'
    'metodo construtor(nome)\nself.nome <- nome\nfim_funcao\n'
    'metodo ola()\nescreva("oi " + self.nome)\nfim_funcao\n'
    'fim_classe'
)


def test_parametro_de_metodo_e_local():
    compilar(programa('', antes='classe P\nmetodo construtor(nome)\nself.nome <- nome\nfim_funcao\nfim_classe'))


def test_variavel_nao_declarada_dentro_de_metodo():
    codigo = programa('', antes='classe P\nmetodo m()\nescreva(zzz)\nfim_funcao\nfim_classe')
    mensagem = erro_de(codigo, SemanticError)
    assert '"zzz"' in mensagem


def test_parametro_nao_vaza_entre_metodos():
    codigo = programa('', antes='classe P\nmetodo a(k)\nfim_funcao\nmetodo b()\nescreva(k)\nfim_funcao\nfim_classe')
    assert '"k"' in erro_de(codigo, SemanticError)


def test_builtins_aceitos_em_funcao():
    codigo = programa('escreva(f())', antes='funcao f()\nretorne teto(pi) + absoluto(-1)\nfim_funcao')
    assert executar(codigo) == '5'


# --- Classe depois do bloco var ---

def test_classe_depois_de_var_com_parametros_repetidos():
    codigo = programa('p <- novo Pessoa("Ana")\np.ola()', var='p: inteiro', antes=CLASSE_PESSOA)
    assert executar(codigo) == 'oi Ana'


def test_var_depois_de_classe_continua_sendo_global():
    codigo = programa('x <- 1\nescreva(x)', antes=CLASSE_PESSOA + '\nvar\nx: inteiro')
    assert executar(codigo) == '1'


# --- Nomes depois de ponto nao sao verificados ---

def test_acesso_a_atributo_sem_chamada():
    codigo = programa('f.inserir(1)\nescreva(f.heap)', var='f: filaPrioridade')
    assert executar(codigo) == '[1]'


def test_atributo_encadeado_em_self():
    compilar(programa('', antes='classe P\nmetodo m()\nself.pos.x <- 1\nfim_funcao\nfim_classe'))
