import pytest

from meuPia.tests.helpers import compilar, executar
from meuPia.tests.test_desafio_variaveis_locais import montar_como_o_lab

# Desafio "Boletim da turma": o aluno escreve as funcoes usando vetor e lista com tipo
CODIGO_ALUNO = '''algoritmo "BoletimDaTurma"
var
    notas: vetor[5] de real
    nomes: vetor[5] de cadeia

funcao maior_nota(v)
    var maior: real <- v[0]
    var i: inteiro
    para i de 1 ate tamanho(v) - 1 faca
        se v[i] > maior entao
            maior <- v[i]
        fim_se
    fim_para
    retorne maior
fim_funcao

funcao aprovados(ns, vs)
    var lista_aprovados: lista de cadeia
    var i: inteiro
    para i de 0 ate tamanho(vs) - 1 faca
        se vs[i] >= 6 entao
            lista_aprovados.adicionar(ns[i])
        fim_se
    fim_para
    lista_aprovados.ordenar()
    retorne lista_aprovados
fim_funcao

inicio
    escreva("Corrigindo provas...")
fim_algoritmo'''

# codigoTeste do desafio, anexado ao inicio pelo Lab
CODIGO_TESTE = '''var resultado: lista de cadeia
notas <- [7, 4.5, 9.5, 6, 3]
nomes <- ["Rey", "Finn", "Ana", "Poe", "Kylo"]
resultado <- aprovados(nomes, notas)

esperar_igual(maior_nota(notas), 9.5, "Encontrou a maior nota")
esperar_igual(resultado.tamanho(), 3, "Três alunos aprovados")
esperar_igual(resultado[0], "Ana", "Aprovados em ordem alfabética")'''

# Mesmas verificacoes sem o plugin de testes
CODIGO_TESTE_SEM_PLUGIN = '''var resultado: lista de cadeia
notas <- [7, 4.5, 9.5, 6, 3]
nomes <- ["Rey", "Finn", "Ana", "Poe", "Kylo"]
resultado <- aprovados(nomes, notas)
escreva(maior_nota(notas))
escreva(resultado)'''


def sem_plugin(codigo_aluno, codigo_teste):
    return codigo_aluno.replace('fim_algoritmo', '') + '\n' + codigo_teste + '\nfim_algoritmo'


def test_desafio_com_colecoes_tipadas_compila():
    compile(compilar(montar_como_o_lab(CODIGO_ALUNO, CODIGO_TESTE)), 'desafio', 'exec')


def test_desafio_com_colecoes_tipadas_produz_o_resultado():
    saida = executar(sem_plugin(CODIGO_ALUNO, CODIGO_TESTE_SEM_PLUGIN))
    assert saida == "Corrigindo provas...\n9.5\n['Ana', 'Poe', 'Rey']"


def test_desafio_com_colecoes_tipadas_passa_nos_testes():
    pytest.importorskip('meupia_testes')
    saida = executar(montar_como_o_lab(CODIGO_ALUNO, CODIGO_TESTE))
    assert saida.count('[TESTE_OK]') == 3
    assert '[TESTE_FALHA]' not in saida


def test_aluno_que_mistura_tipos_recebe_erro_em_portugues():
    codigo = sem_plugin(CODIGO_ALUNO, 'notas <- [7, 4.5, 9.5, 6, 3]\nnomes[0] <- 10')
    with pytest.raises(TypeError, match='o vetor só aceita valores do tipo cadeia; recebeu 10'):
        executar(codigo)
