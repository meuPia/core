import re

import pytest

from meuPia.analyzers.semantic_analyzer import SemanticError
from meuPia.analyzers.syntax_analyzer import Parser, SyntacticError
from meuPia.analyzers.lexical_analyzer import scan_line
from meuPia.tests.helpers import compilar, executar, programa


def erro_execucao(tipo, mensagem, codigo):
    with pytest.raises(tipo, match=f'^{re.escape(mensagem)}$'):
        executar(codigo)


def lexemas(codigo):
    pares = []
    for i, linha in enumerate(codigo.split('\n')):
        _, tokens = scan_line(linha, i + 1)
        pares.extend(tokens)
    return pares


# --- Sintaxe de declaracao ---

def test_declaracao_global_de_vetor_e_lista_tipada():
    compilar(programa('', var='notas: vetor[5] de inteiro\nnomes: lista de cadeia'))


def test_varios_nomes_na_mesma_linha():
    codigo = programa('a[0] <- 1.5\nescreva(b[0])', var='a, b: vetor[2] de real')
    assert executar(codigo) == '0.0'


def test_declaracao_local_com_valor():
    assert executar(programa('var v: vetor[3] de inteiro <- [1, 2, 3]\nescreva(v[2])')) == '3'


def test_tamanho_por_variavel_e_rejeitado():
    with pytest.raises(SyntacticError) as excinfo:
        compilar(programa('', var='v: vetor[n] de inteiro'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 10)
    assert excinfo.value.descricao == 'o tamanho do vetor precisa ser um número inteiro maior que zero, como vetor[5] de inteiro'


def test_tamanho_zero_e_rejeitado():
    with pytest.raises(SyntacticError) as excinfo:
        compilar(programa('', var='v: vetor[0] de inteiro'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 10)


def test_tamanho_real_e_rejeitado():
    with pytest.raises(SyntacticError) as excinfo:
        compilar(programa('', var='v: vetor[5.0] de inteiro'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 10)


def test_vetor_sem_tipo_de_elemento():
    with pytest.raises(SyntacticError) as excinfo:
        compilar(programa('', var='v: vetor[3]\nx: inteiro'))
    assert '"de"' in excinfo.value.descricao


def test_tipo_de_elemento_nao_permitido():
    with pytest.raises(SyntacticError) as excinfo:
        compilar(programa('', var='l: lista de dicionario'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 13)
    assert excinfo.value.descricao == 'o tipo dos elementos precisa ser inteiro, real, float, cadeia, string ou logico'


def test_vetor_de_vetor_nao_permitido():
    with pytest.raises(SyntacticError):
        compilar(programa('', var='m: vetor[2] de vetor[2] de inteiro'))


def test_lista_sem_de_continua_sem_tipo():
    codigo = programa('l.adicionar(1)\nl.adicionar("a")\nescreva(tamanho(l))', var='l: lista')
    assert executar(codigo) == '2'


# --- Helpers do parser ---

def test_ler_bloco_var_com_tipos():
    pares = lexemas('var\nx: inteiro\nv: vetor[3] de real\nl: lista de cadeia\ninicio')
    linhas, fim = Parser.ler_bloco_var(pares, 0)
    assert [(l['tipo'], l['elemento'], l['tamanho']) for l in linhas] == [
        ('inteiro', None, None), ('vetor', 'real', 3), ('lista', 'cadeia', None)]
    assert pares[fim]['token'] == 'INICIO'


def test_ler_atribuicoes():
    codigo = programa('v <- [1, 2]\nse v = [1, 2] entao\nfim_se\nv[0] <- 1\nself.b <- 1')
    pares = lexemas(codigo)
    atribuicoes = Parser.ler_atribuicoes(pares)
    assert [pares[alvo]['lexeme'] for alvo, _, _ in atribuicoes] == ['v']
    _, inicio, fim = atribuicoes[0]
    assert [p['lexeme'] for p in pares[inicio:fim]] == ['[', '1', ',', '2', ']']


# --- Valor inicial ---

def test_vetor_de_inteiros_comeca_com_zeros():
    assert executar(programa('escreva(v)', var='v: vetor[3] de inteiro')) == '[0, 0, 0]'


def test_vetor_de_logicos_comeca_com_falso():
    assert executar(programa('escreva(v[1])', var='v: vetor[2] de logico')) == 'falso'


def test_lista_tipada_comeca_vazia():
    assert executar(programa('escreva(tamanho(l))', var='l: lista de cadeia')) == '0'


def test_vetores_da_mesma_linha_sao_independentes():
    assert executar(programa('a[0] <- 7\nescreva(b[0])', var='a, b: vetor[2] de inteiro')) == '0'


def test_vetores_locais_da_mesma_linha_sao_independentes():
    assert executar(programa('var\na, b: vetor[2] de inteiro\na[0] <- 7\nescreva(b[0])')) == '0'


def test_vetor_de_cadeia_comeca_com_textos_vazios():
    assert executar(programa('escreva(tamanho(v[0]))\nescreva(v[1] + "x")', var='v: vetor[2] de cadeia')) == '0\nx'


# --- Tipo dos elementos verificado na execucao ---

def test_adicionar_valor_de_outro_tipo():
    erro_execucao(TypeError, 'a lista só aceita valores do tipo inteiro; recebeu "Ana"',
                  programa('l.adicionar("Ana")', var='l: lista de inteiro'))


def test_atribuicao_por_indice_de_outro_tipo():
    erro_execucao(TypeError, 'o vetor só aceita valores do tipo cadeia; recebeu 5',
                  programa('v[0] <- 5', var='v: vetor[2] de cadeia'))


def test_inteiro_aceito_em_colecao_de_real():
    assert executar(programa('l.adicionar(2)\nescreva(l[0])', var='l: lista de real')) == '2.0'


def test_logico_recusado_em_colecao_de_inteiro():
    erro_execucao(TypeError, 'o vetor só aceita valores do tipo inteiro; recebeu verdadeiro',
                  programa('v[0] <- verdadeiro', var='v: vetor[1] de inteiro'))


def test_real_recusado_em_colecao_de_inteiro():
    erro_execucao(TypeError, 'a lista só aceita valores do tipo inteiro; recebeu 2.5',
                  programa('l.adicionar(2.5)', var='l: lista de inteiro'))


def test_tipo_declarado_aparece_na_mensagem():
    erro_execucao(TypeError, 'a lista só aceita valores do tipo string; recebeu 1',
                  programa('l.adicionar(1)', var='l: lista de string'))


def test_verificacao_dentro_de_uma_funcao():
    codigo = programa('poe(l)', var='l: lista de inteiro', antes='funcao poe(c)\nc.adicionar("x")\nfim_funcao')
    erro_execucao(TypeError, 'a lista só aceita valores do tipo inteiro; recebeu "x"', codigo)


def test_expandir_com_elemento_de_outro_tipo_nao_altera_a_lista():
    codigo = programa('l.adicionar(1)\nl.expandir([2, "tres"])', var='l: lista de inteiro')
    python_code = compilar(codigo)
    escopo = {'__name__': 'teste'}
    exec(python_code, escopo)
    with pytest.raises(TypeError):
        escopo['main']()
    assert list(escopo['l']) == [1]


def test_inserir_verifica_tipo():
    erro_execucao(TypeError, 'a lista só aceita valores do tipo logico; recebeu 0',
                  programa('l.inserir(0, 0)', var='l: lista de logico'))


def test_elemento_cadeia_concatena_como_texto():
    codigo = programa('l.adicionar("a")\nescreva(l[0] + verdadeiro)', var='l: lista de cadeia')
    assert executar(codigo) == 'averdadeiro'


# --- Atribuicao de uma colecao inteira ---

def test_vetor_recebe_lista_literal():
    codigo = programa('notas <- [8, 7, 9, 10, 6]\nescreva(notas[0])', var='notas: vetor[5] de inteiro')
    assert executar(codigo) == '8'


def test_lista_tipada_recebe_novo_lista():
    codigo = programa('l <- novo lista()\nl.adicionar("Ana")\nescreva(tamanho(l))', var='l: lista de cadeia')
    assert executar(codigo) == '1'


def test_colecao_do_mesmo_tipo_e_compartilhada():
    codigo = programa('b <- a\na.adicionar(1)\nescreva(tamanho(b))', var='a, b: lista de inteiro')
    assert executar(codigo) == '1'


def test_colecao_de_outro_tipo_e_copiada_e_verificada():
    codigo = programa('a <- [1, 2]\nb <- a\nescreva(b[0])\na.adicionar(3)\nescreva(tamanho(b))',
                      var='a: lista\nb: lista de real')
    assert executar(codigo) == '1.0\n2'


def test_atribuicao_com_igual():
    assert executar(programa('v = [4, 5]\nescreva(v[1])', var='v: vetor[2] de inteiro')) == '5'


def test_tamanho_errado_em_atribuicao_ao_vetor():
    codigo = programa('v <- dois()', var='v: vetor[3] de inteiro', antes='funcao dois()\nretorne [1, 2]\nfim_funcao')
    erro_execucao(ValueError, 'o vetor tem 3 posições, mas recebeu 2 elementos', codigo)


def test_valor_que_nao_e_lista():
    codigo = programa('l <- cinco()', var='l: lista de inteiro', antes='funcao cinco()\nretorne 5\nfim_funcao')
    erro_execucao(TypeError, 'a lista só recebe uma lista de valores; recebeu 5', codigo)


def test_parametro_com_nome_de_global_tipada_nao_e_convertido():
    codigo = programa('escreva(f(5))', var='v: vetor[2] de inteiro',
                      antes='funcao f(v)\nv <- v + 1\nretorne v\nfim_funcao')
    assert executar(codigo) == '6'


def test_global_tipada_atribuida_dentro_de_funcao():
    codigo = programa('preenche()\nescreva(v)', var='v: vetor[2] de inteiro',
                      antes='funcao preenche()\nv <- [3, 4]\nfim_funcao')
    assert executar(codigo) == '[3, 4]'


# --- Listas literais verificadas ao compilar ---

def test_elemento_literal_de_tipo_errado():
    codigo = programa('\nnotas <- [8, "sete", 9]', var='notas: vetor[3] de inteiro')
    with pytest.raises(SemanticError) as excinfo:
        compilar(codigo)
    assert (excinfo.value.linha, excinfo.value.coluna) == (6, 14)
    assert excinfo.value.descricao == '"notas" só aceita valores do tipo inteiro; este valor é do tipo cadeia'


def test_elemento_literal_na_linha_5():
    codigo = 'algoritmo "T"\nvar\nnotas: vetor[3] de inteiro\ninicio\nnotas <- [8, "sete", 9]\nfim_algoritmo'
    with pytest.raises(SemanticError) as excinfo:
        compilar(codigo)
    assert (excinfo.value.linha, excinfo.value.coluna) == (5, 14)


def test_quantidade_errada_em_lista_literal():
    with pytest.raises(SemanticError) as excinfo:
        compilar(programa('notas <- [8, 7]', var='notas: vetor[5] de inteiro'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (5, 10)
    assert excinfo.value.descricao == 'o vetor "notas" tem 5 posições, mas a lista tem 2 elementos'


def test_valor_inicial_de_var_local_verificado():
    with pytest.raises(SemanticError) as excinfo:
        compilar(programa('var nomes: lista de cadeia <- ["Ana", 3]'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (3, 39)


def test_quantidade_errada_em_var_local():
    with pytest.raises(SemanticError):
        compilar(programa('var v: vetor[3] de inteiro <- [1, 2]'))


def test_literais_negativos_e_reais():
    codigo = programa('l <- [-1, 2.5]\nescreva(l)', var='l: lista de real')
    assert executar(codigo) == '[-1.0, 2.5]'
    with pytest.raises(SemanticError) as excinfo:
        compilar(programa('l <- [1, -2.5]', var='l: lista de inteiro'))
    assert excinfo.value.descricao == '"l" só aceita valores do tipo inteiro; este valor é do tipo real'


def test_logico_literal():
    with pytest.raises(SemanticError) as excinfo:
        compilar(programa('l <- [verdadeiro, 1]', var='l: lista de logico'))
    assert excinfo.value.descricao == '"l" só aceita valores do tipo logico; este valor é do tipo inteiro'


def test_lista_com_expressao_fica_para_a_execucao():
    codigo = programa('v <- [x, x + 1]\nescreva(v[1])', var='v: vetor[2] de inteiro\nx: inteiro')
    assert executar(codigo) == '1'


def test_verdadeiro_redeclarado_nao_e_verificado():
    codigo = programa('verdadeiro <- 1\nl <- [verdadeiro]\nescreva(l[0])', var='l: lista de inteiro\nverdadeiro: inteiro')
    assert executar(codigo) == '1'


def test_comparacao_com_lista_nao_e_verificada():
    codigo = programa('se v = [1] entao\nescreva("igual")\nfim_se', var='v: vetor[2] de inteiro')
    assert executar(codigo) == ''


def test_local_tipada_em_funcao_verificada():
    antes = 'funcao f()\nvar l: lista de inteiro\nl <- ["x"]\nfim_funcao'
    with pytest.raises(SemanticError):
        compilar(programa('', antes=antes))


# --- Faixa de indices ---

def test_leitura_do_ultimo_elemento():
    assert executar(programa('v[2] <- 9\nescreva(v[2])', var='v: vetor[3] de inteiro')) == '9'


def test_indice_igual_ao_tamanho():
    erro_execucao(IndexError, 'índice 5 fora do vetor de tamanho 5 (use de 0 a 4)',
                  programa('escreva(v[5])', var='v: vetor[5] de inteiro'))


def test_indice_negativo():
    erro_execucao(IndexError, 'índice -1 fora da lista de tamanho 1 (use de 0 a 0)',
                  programa('l.adicionar(1)\nescreva(l[-1])', var='l: lista de inteiro'))


def test_indice_em_lista_vazia():
    erro_execucao(IndexError, 'índice 0 fora da lista vazia',
                  programa('l[0] <- 1', var='l: lista de inteiro'))


def test_percorrer_um_vetor_com_para():
    codigo = programa('v <- [1, 2, 3]\npara i de 0 ate tamanho(v) - 1 faca\nsoma <- soma + v[i]\nfim_para\nescreva(soma)',
                      var='v: vetor[3] de inteiro\ni, soma: inteiro')
    assert executar(codigo) == '6'


# --- Vetor tem tamanho fixo ---

TAMANHO_FIXO = 'o vetor tem tamanho fixo e não aceita adicionar nem remover elementos'


@pytest.mark.parametrize('comando', [
    'v.adicionar(1)', 'v.adicionarFim(1)', 'v.adicionarInicio(1)', 'v.removerFim()', 'v.removerInicio()',
    'v.expandir([1])', 'v.limpar()', 'v.inserir(0, 1)', 'v.remover(0)', 'v.removerEm(0)',
])
def test_metodos_que_mudam_o_tamanho_do_vetor(comando):
    erro_execucao(ValueError, TAMANHO_FIXO, programa(comando, var='v: vetor[2] de inteiro'))


# --- Metodos ---

def test_exemplo_da_issue_com_lista_de_cadeia():
    corpo = 'nomes.adicionar("Ana")\nnomes.adicionar("Bruno")\nnomes.remover("Ana")\nescreva(nomes.tamanho())\nescreva(nomes[0])'
    assert executar(programa(corpo, var='nomes: lista de cadeia')) == '1\nBruno'


def test_inserir_em_posicao():
    codigo = programa('l <- [1, 3]\nl.inserir(1, 2)\nescreva(l)', var='l: lista de inteiro')
    assert executar(codigo) == '[1, 2, 3]'


def test_inserir_no_fim():
    codigo = programa('l <- [1]\nl.inserir(1, 2)\nescreva(l)', var='l: lista de inteiro')
    assert executar(codigo) == '[1, 2]'


def test_remover_por_posicao_em_expressao():
    codigo = programa('l <- ["a", "b", "c"]\nescreva(l.removerEm(1))\nescreva(tamanho(l))', var='l: lista de cadeia')
    assert executar(codigo) == 'b\n2'


def test_buscar_e_contem():
    codigo = programa('v <- [4, 5, 6]\nescreva(v.buscar(6))\nescreva(v.buscar(9))\nescreva(v.contem(5))',
                      var='v: vetor[3] de inteiro')
    assert executar(codigo) == '2\n-1\nverdadeiro'


def test_ordenar_vetor():
    codigo = programa('v <- [3, 1, 4, 2]\nv.ordenar()\nescreva(v)', var='v: vetor[4] de inteiro')
    assert executar(codigo) == '[1, 2, 3, 4]'


def test_ordenar_lista_de_cadeia():
    codigo = programa('l <- ["Rey", "Ana", "Luke"]\nl.ordenar()\nescreva(l[0], " ", l[2])', var='l: lista de cadeia')
    assert executar(codigo) == 'Ana Rey'


def test_remover_valor_ausente():
    erro_execucao(ValueError, 'o valor 9 não está na lista', programa('l.remover(9)', var='l: lista de inteiro'))


def test_inserir_fora_da_faixa():
    erro_execucao(IndexError, 'posição 3 fora da lista de tamanho 0 (use de 0 a 0)',
                  programa('l.inserir(3, 1)', var='l: lista de inteiro'))


def test_remover_em_fora_da_faixa():
    erro_execucao(IndexError, 'índice 2 fora da lista de tamanho 1 (use de 0 a 0)',
                  programa('l <- [1]\nl.removerEm(2)', var='l: lista de inteiro'))


def test_remover_fim_em_lista_vazia():
    erro_execucao(ValueError, 'a lista está vazia', programa('l.removerFim()', var='l: lista de inteiro'))


def test_metodos_herdados_da_lista():
    codigo = programa('l.adicionar(1)\nl.adicionarFim(2)\nl.expandir([3])\nescreva(l.removerFim())\nl.limpar()\nescreva(tamanho(l))',
                      var='l: lista de inteiro')
    assert executar(codigo) == '3\n0'


def test_filaprioridade_nao_e_afetada():
    codigo = programa('f.inserir(3)\nf.inserir(1)\nescreva(f.remover())', var='f: filaPrioridade\nv: vetor[1] de inteiro')
    assert executar(codigo) == '1'


# --- leia ---

def test_leia_em_vetor():
    with pytest.raises(SemanticError) as excinfo:
        compilar(programa('leia(v)', var='v: vetor[3] de inteiro'))
    assert (excinfo.value.linha, excinfo.value.coluna) == (5, 6)
    assert excinfo.value.descricao == 'leia não lê uma coleção inteira; leia um valor numa variável e guarde com v[i] <- valor'


def test_leia_em_lista_tipada_local():
    with pytest.raises(SemanticError):
        compilar(programa('var l: lista de inteiro\nleia(l)'))
