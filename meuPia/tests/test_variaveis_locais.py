import pytest

from meuPia.analyzers.lexical_analyzer import scan_line
from meuPia.analyzers.semantic_analyzer import SemanticError
from meuPia.analyzers.syntax_analyzer import Parser, SyntacticError
from meuPia.tests.helpers import compilar, executar, programa


def analisar(codigo):
    """Roda apenas lexico e sintatico."""
    lexemas = []
    for i, linha in enumerate(codigo.split('\n')):
        lexemas.extend(scan_line(linha, i + 1)[1])
    Parser(lexemas).parse()
    return lexemas


def funcao(corpo, params=''):
    return f'funcao f({params})\n{corpo}\nfim_funcao'


# --- Sintaxe da declaracao local ---

def test_sintaxe_forma_com_valor():
    analisar(programa('escreva(f(4))', antes=funcao('var r: inteiro <- a * 2\nretorne r', 'a')))


def test_sintaxe_valor_com_igual():
    analisar(programa('escreva(f())', antes=funcao('var t: cadeia = "oi"\nretorne t')))


def test_sintaxe_forma_de_bloco():
    analisar(programa('escreva(f())', antes=funcao('var\nsoma, contador: inteiro\nnomes: lista\nretorne soma')))


def test_sintaxe_formas_misturadas():
    analisar(programa('escreva(f())', antes=funcao('var\na: inteiro <- 5\nb, c: real\nretorne a + b + c')))


def test_sintaxe_valor_com_mais_de_um_nome():
    # linha 3 = 'var a, b: inteiro <- 0' (algoritmo, funcao, var...); '<-' na coluna 19
    with pytest.raises(SyntacticError) as excinfo:
        analisar(programa('', antes=funcao('var a, b: inteiro <- 0')))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 19)


def test_sintaxe_tipo_desconhecido_em_declaracao_local():
    with pytest.raises(SyntacticError) as excinfo:
        analisar(programa('', antes=funcao('var x: numero')))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 8)


# --- Posicoes permitidas ---

def test_sintaxe_declaracao_no_inicio_depois_de_comandos():
    analisar(programa('escreva("a")\nvar n: inteiro <- 2\nescreva(n)'))


def test_sintaxe_declaracao_em_metodo():
    analisar(programa('', antes='classe C\nmetodo calc(x)\nvar y: inteiro <- x + 1\nretorne y\nfim_funcao\nfim_classe'))


def test_sintaxe_declaracao_dentro_de_se():
    with pytest.raises(SyntacticError) as excinfo:
        analisar(programa('', antes=funcao('se verdadeiro entao\nvar x: inteiro <- 1\nfim_se')))
    assert (excinfo.value.linha, excinfo.value.coluna) == (4, 1)
    assert 'fora de blocos se, enquanto e para' in str(excinfo.value)


def test_sintaxe_declaracao_dentro_de_laco():
    with pytest.raises(SyntacticError) as excinfo:
        analisar(programa('para i de 1 ate 2 faca\nvar x: inteiro\nfim_para', var='i: inteiro'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (6, 1)
    assert 'fora de blocos se, enquanto e para' in str(excinfo.value)


# --- Leitura de declaracoes pelo parser (usada pelo semantico e pelo gerador) ---

def posicao_do_var(lexemas, ocorrencia=0):
    indices = [i for i, t in enumerate(lexemas) if t['token'] == 'VAR']
    return indices[ocorrencia]


def test_ler_declaracao_com_expressao_de_uma_linha():
    lexemas = analisar(programa('var r: inteiro <- 1 + 2\nescreva(r)'))
    inicio_var = posicao_do_var(lexemas)
    linhas, fim = Parser.ler_declaracao_local(lexemas, inicio_var)
    assert len(linhas) == 1
    assert [nome for nome, _ in linhas[0]['nomes']] == ['r']
    assert linhas[0]['tipo'] == 'inteiro'
    ini, fim_expr = linhas[0]['expressao']
    assert [t['lexeme'] for t in lexemas[ini:fim_expr]] == ['1', '+', '2']
    assert lexemas[fim]['lexeme'] == 'escreva'


def test_ler_declaracao_com_expressao_de_varias_linhas():
    lexemas = analisar(programa('var m: lista <- [\n[0, 1],\n[2, 3]\n]\nescreva(m)'))
    linhas, fim = Parser.ler_declaracao_local(lexemas, posicao_do_var(lexemas))
    ini, fim_expr = linhas[0]['expressao']
    assert lexemas[ini]['lexeme'] == '[' and lexemas[fim_expr - 1]['lexeme'] == ']'
    assert fim == fim_expr
    assert lexemas[fim]['lexeme'] == 'escreva'


def test_ler_declaracao_em_bloco_com_varios_nomes():
    lexemas = analisar(programa('var\na, b: inteiro\nc: logico <- verdadeiro\nescreva(a)'))
    linhas, fim = Parser.ler_declaracao_local(lexemas, posicao_do_var(lexemas))
    assert [[n for n, _ in l['nomes']] for l in linhas] == [['a', 'b'], ['c']]
    assert [l['tipo'] for l in linhas] == ['inteiro', 'logico']
    assert linhas[0]['expressao'] is None and linhas[1]['expressao'] is not None
    assert [lexemas[p]['lexeme'] for _, p in linhas[0]['nomes']] == ['a', 'b']
    assert lexemas[fim]['lexeme'] == 'escreva'


# --- Escopo da variavel local ---

def erro_semantico(codigo):
    with pytest.raises(SemanticError) as excinfo:
        compilar(codigo)
    return excinfo.value


def test_local_de_uma_funcao_nao_e_visivel_em_outra():
    codigo = programa('', antes='funcao a()\nvar t: inteiro <- 1\nretorne t\nfim_funcao\nfuncao b()\nretorne t\nfim_funcao')
    erro = erro_semantico(codigo)
    assert '"t"' in str(erro)
    assert erro.linha == 7


def test_local_do_inicio_nao_e_visivel_em_funcao():
    codigo = programa('var k: inteiro <- 1\nescreva(f())', antes=funcao('retorne k'))
    assert '"k"' in str(erro_semantico(codigo))


# --- Conflitos de nome ---

def test_conflito_local_com_global():
    # linha 5 = 'var x: inteiro <- 1' (algoritmo, var, x: inteiro, funcao, var...); 'x' na coluna 5
    codigo = programa('', var='x: inteiro', antes=funcao('var x: inteiro <- 1'))
    erro = erro_semantico(codigo)
    assert '"x"' in str(erro)
    assert (erro.linha, erro.coluna) == (5, 5)


def test_conflito_local_com_parametro():
    assert '"a"' in str(erro_semantico(programa('', antes=funcao('var a: inteiro', 'a'))))


def test_conflito_local_com_self():
    codigo = programa('', antes='classe P\nmetodo m()\nvar self: inteiro\nfim_funcao\nfim_classe')
    assert '"self"' in str(erro_semantico(codigo))


def test_conflito_local_declarada_duas_vezes():
    erro = erro_semantico(programa('', antes=funcao('var t: inteiro\nescreva(t)\nvar t: real')))
    assert '"t"' in str(erro)
    assert (erro.linha, erro.coluna) == (5, 5)


def test_conflito_local_com_nome_de_funcao():
    codigo = programa('var g: inteiro', antes='funcao g()\nretorne 1\nfim_funcao')
    assert '"g"' in str(erro_semantico(codigo))


# --- Uso antes da declaracao ---

def test_uso_antes_do_var():
    erro = erro_semantico(programa('', antes=funcao('escreva(t)\nvar t: inteiro <- 1')))
    assert 'foi usada antes de ser declarada' in str(erro)
    assert '"t"' in str(erro)
    assert (erro.linha, erro.coluna) == (3, 9)


def test_valor_inicial_nao_pode_usar_a_propria_variavel():
    erro = erro_semantico(programa('', antes=funcao('var x: inteiro <- x + 1')))
    assert 'foi usada antes de ser declarada' in str(erro)


# --- Execucao: sintaxe, posicoes, escopo e tempo de vida ---

def test_executa_forma_com_valor():
    assert executar(programa('escreva(f(4))', antes=funcao('var r: inteiro <- a * 2\nretorne r', 'a'))) == '8'


def test_executa_valor_com_igual():
    assert executar(programa('escreva(f())', antes=funcao('var t: cadeia = "oi"\nretorne t'))) == 'oi'


def test_executa_bloco_com_valor_inicial_do_tipo():
    corpo = 'var\nsoma, contador: inteiro\nnomes: lista\nescreva(soma + contador, tamanho(nomes))'
    assert executar(programa('f()', antes=funcao(corpo))) == '00'


def test_executa_formas_misturadas():
    corpo = 'var\na: inteiro <- 5\nb, c: real\nescreva(a + b + c)'
    assert executar(programa('f()', antes=funcao(corpo))) == '5.0'


def test_executa_varias_declaracoes():
    corpo = 'var x: inteiro <- 1\nx <- x + 1\nvar y: inteiro <- x * 10\nretorne y'
    assert executar(programa('escreva(f())', antes=funcao(corpo))) == '20'


def test_executa_declaracao_no_inicio_depois_de_comandos():
    assert executar(programa('escreva("a")\nvar n: inteiro <- 2\nescreva(n)')) == 'a\n2'


def test_executa_declaracao_em_metodo():
    classe = 'classe C\nmetodo calc(x)\nvar y: inteiro <- x + 1\nretorne y\nfim_funcao\nfim_classe'
    assert executar(programa('c <- novo C()\nescreva(c.calc(1))', var='c: inteiro', antes=classe)) == '2'


def test_executa_var_no_inicio_como_codigo_teste():
    corpo = 'escreva("x")\nvar legado, sus: dicionario\nvar resultado: inteiro\nlegado <- {"a": 1}\nescreva(tamanho(legado))'
    assert executar(programa(corpo)) == 'x\n1'


def test_executa_mesmo_nome_local_em_funcoes_diferentes():
    antes = 'funcao a()\nvar t: inteiro <- 1\nretorne t\nfim_funcao\nfuncao b()\nvar t: inteiro <- 2\nretorne t\nfim_funcao'
    assert executar(programa('escreva(a() + b())', antes=antes)) == '3'


def test_executa_recursao_com_variavel_local():
    antes = 'funcao fat(n)\nvar r: inteiro <- 1\nse n > 1 entao\nr <- n * fat(n - 1)\nfim_se\nretorne r\nfim_funcao'
    assert executar(programa('escreva(fat(5))', antes=antes)) == '120'


def test_executa_local_reinicializada_a_cada_chamada():
    antes = 'funcao conta()\nvar c: inteiro\nc <- c + 1\nretorne c\nfim_funcao'
    assert executar(programa('escreva(conta(), conta())', antes=antes)) == '11'


def test_local_nao_altera_global_de_mesmo_valor():
    antes = 'funcao f()\nvar aux: inteiro <- 99\nretorne aux\nfim_funcao'
    assert executar(programa('g <- 1\nescreva(f(), g)', var='g: inteiro', antes=antes)) == '991'


# --- Leitura de variavel local ---

def test_leia_em_local_inteira():
    assert executar(programa('var n: inteiro\nleia(n)\nescreva(n + 1)'), entrada='41\n') == '42'


def test_leia_em_local_logica():
    antes = funcao('var b: logico\nleia(b)\nretorne b')
    assert executar(programa('escreva(f())', antes=antes), entrada='verdadeiro\n') == 'verdadeiro'


# --- Builtins: local tem prioridade ---

def test_variavel_local_chamada_piso():
    assert executar(programa('escreva(f())', antes=funcao('var piso: inteiro <- 2\nretorne piso'))) == '2'
