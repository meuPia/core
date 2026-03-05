import pytest
from meuPia.analyzers.code_generator import CodeGenerator
from meuPia.analyzers.syntax_analyzer import Parser
from meuPia.analyzers.lexical_analyzer import scan_line

def compile_snippet(portugol_code):
    lines = portugol_code.split('\n')
    all_lexemes = []
    
    # Simula o Lexer
    for i, line in enumerate(lines):
        line_clean, lexemes = scan_line(line, i+1)
        all_lexemes.extend(lexemes)
        
    # Simula Parse (opcional para gerar, mas bom para garantir consistencia)
    parser = Parser(all_lexemes)
    parser.parse()
    
    # Gera Codigo
    generator = CodeGenerator(all_lexemes)
    python_code = generator.generate()
    
    return python_code

def test_gen_assignment():
    code = """algoritmo "Attrib"
    var x: inteiro
    inicio
    x <- 10
    fim_algoritmo"""
    
    output = compile_snippet(code)
    assert "x = 10" in output

def test_gen_multidimensional_array_fix():
    # Este teste verifica especificamente o bug de adjacencia ][
    code = """algoritmo "Matrix"
    var m: inteiro
    inicio
    m <- [[1, 2], [3, 4]]
    escreva(m[0][1])
    fim_algoritmo"""
    
    output = compile_snippet(code)
    assert "m = [[1, 2], [3, 4]]" in output
    assert "print(m[0][1])" in output

def test_gen_conditional():
    code = """algoritmo "Cond"
    var x: inteiro
    inicio
    se x > 0 entao
        escreva(x)
    fim_se
    fim_algoritmo"""
    
    output = compile_snippet(code)
    assert "if x>0:" in output
    assert "    print(x)" in output

def test_gen_loop_para():
    code = """algoritmo "Loop"
    var i: inteiro
    inicio
    para i de 1 ate 10 faca
        escreva(i)
    fim_para
    fim_algoritmo"""
    
    output = compile_snippet(code)
    # Range é inclusive no portugol, entao 1 ate 10 vira range(1, 10 + 1, 1)
    assert "for i in range(1, 10 + 1, 1):" in output
    assert "    print(i)" in output

def test_gen_function_call_ia():
    code = """algoritmo "IA"
    var dados: inteiro
    inicio
    ia_treinar(dados)
    fim_algoritmo"""
    
    output = compile_snippet(code)
    assert "ia_treinar(dados)" in output

def test_gen_object_methods():
    code = """algoritmo "Obj"
    var lista: string
    inicio
    lista <- "a,b,c"
    escreva(lista.split(","))
    lista.append("d")
    fim_algoritmo"""
    output = compile_snippet(code)
    assert 'print(lista.split(","))' in output
    assert 'lista.append("d")' in output

def test_gen_enquanto():
    code = """algoritmo "While"
    var x: inteiro
    inicio
    enquanto x < 10 faca
        x <- x + 1
    fim_enquanto
    fim_algoritmo"""
    output = compile_snippet(code)
    assert "while x<10:" in output

def test_gen_leia_typing():
    code = """algoritmo "LeiaType"
    var n: inteiro
    s: string
    inicio
    leia(n)
    leia(s)
    fim_algoritmo"""
    
    # We need to ensure var types are registered in the generator for this test
    # compile_snippet creates a new Generator each time, so it's fresh.
    output = compile_snippet(code)
    
    # Inteiro deve ser int(input())
    assert "n = int(input())" in output
    # String deve ser input()
    assert "s = input()" in output

def test_gen_boolean_logic():
    code = """algoritmo "Bool"
    var x, y, z: inteiro
    inicio
    se (x > 0) e (y < 10) ou (nao (z > 0)) entao
        escreva("Boolean")
    fim_se
    fim_algoritmo"""
    
    output = compile_snippet(code)
    # Check translation of operators
    assert "if (x>0) and (y<10) or ( not (z>0)):" in output

def test_gen_plugin_import():
    code = """algoritmo "Plugin"
    usar "nlp"
    inicio
    fim_algoritmo"""
    
    output = compile_snippet(code)
    # Check that default lib is NOT imported
    assert "from meuPia.lib.meupia_libs import *" not in output
    # Check that plugin lib IS imported with new convention
    assert "from meupia_nlp import *" in output
    assert "except ImportError:" in output

def test_gen_default_import():
    code = """algoritmo "Default"
    inicio
    fim_algoritmo"""
    
    output = compile_snippet(code)
    # Check that default lib is NOT imported (since it was deleted)
    assert "from meuPia.lib.meupia_libs import *" not in output

def test_gen_plugin_import_ia():
    code = """algoritmo "TesteIA"
    usar "ia"
    inicio
    fim_algoritmo"""
    
    output = compile_snippet(code)
    # Check that mapping is respected
    assert "from meupia_ia.plugin_ia import *" in output
    assert "except ImportError:" in output

def test_gen_dictionary():
    code = """algoritmo "DictGen"
    var pessoa: inteiro
    inicio
    pessoa <- {"nome": "Henry", "idade": 30}
    escreva(pessoa["nome"])
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    assert 'pessoa = {"nome": "Henry", "idade": 30}' in output

def test_gen_function_definition():
    code = """algoritmo "FuncGen"
    funcao somar(a, b)
        retorne a + b
    fim_funcao
    inicio
        escreva(somar(10, 20))
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    # Verifica se a função foi criada no Python corretamente
    assert "def somar(a, b):" in output
    assert "return a+b" in output
    assert "print(somar(10, 20))" in output

def test_gen_direct_assignment():
    code = """algoritmo "GenIndex"
    inicio
        lista = 99
    fim_algoritmo"""
    output = compile_snippet(code)
    assert "lista = 99" in output

def test_gen_builtin_tamanho():
    code = """algoritmo "Tamanho"
    var lista: inteiro
    inicio
    lista = [1]
    escreva(tamanho(lista))
    fim_algoritmo"""
    
    output = compile_snippet(code)
    assert "print(len(lista))" in output

def test_gen_builtin_methods():
    code = """algoritmo "MetodosNativos"
    var lista, dict: inteiro
    inicio
    lista = []
    dict = {}
    
    lista.adicionar(99)
    dict.atualizar({"chave": 1})
    escreva(dict.pegar("chave"))
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    assert "lista.append(99)" in output
    assert "dict.update({\"chave\": 1})" in output
    assert "print(dict.get(\"chave\"))" in output

def test_gen_oop_class_and_instantiation():
    code = """algoritmo "OOPSimples"
    classe Agente
        metodo construtor(nome)
            escreva(nome)
        fim_funcao
        metodo explorar(alvo)
            escreva(alvo)
        fim_funcao
    fim_classe
    var
        meu_agente: string
    inicio
        meu_agente = novo Agente("R2-D2")
        meu_agente.explorar("Marte")
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    assert "class Agente:" in output
    assert "def __init__(self, nome):" in output 
    assert "def explorar(self, alvo):" in output 
    
    assert "meu_agente = Agente(\"R2-D2\")" in output
    assert "meu_agente.explorar(\"Marte\")" in output

def test_gen_deque_methods():
    code = """algoritmo "DequeAcademico"
    var
        fila: string
    inicio
        fila = filaDupla()
        fila.adicionarInicio(10)
        fila.adicionarFim(20)
        fila.removerInicio()
        fila.removerFim()
        fila.expandir([30, 40])
        fila.limpar()
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    assert "from collections import deque" in output
    assert "fila = deque()" in output
    
    assert "fila.appendleft(10)" in output
    assert "fila.append(20)" in output
    assert "fila.popleft()" in output
    assert "fila.pop()" in output
    assert "fila.extend([30, 40])" in output
    assert "fila.clear()" in output

def test_gen_plugin_import():
    code = """algoritmo "Plugin"
    usar "maker" 
    inicio
    fim_algoritmo"""
    
    output = compile_snippet(code)
    assert "from meupia_maker.plugin_iot import *" in output
    assert "except ImportError:" in output

def test_gen_local_file_import():
    code = """algoritmo "ImportLocal"
    usar "meus_calculos"
    inicio
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    assert "from meus_calculos import *" in output
    assert "O ficheiro local 'meus_calculos' não foi encontrado" in output

def test_gen_atribuicao_seta():
    code = """algoritmo "AtribuicaoSeta"
    var x: inteiro
    inicio
        x <- 42
    fim_algoritmo"""
    
    output = compile_snippet(code)
    
    # O Python não usa <-, então o compilador tem que gerar =
    assert "x = 42" in output

def test_gen_fila_prioridade():
    code = """algoritmo "TesteHeap"
    var fila: inteiro
    inicio
        fila <- filaPrioridade()
        fila.inserir(10)
        fila.inserir(5)
        fila.inserir(20)
        escreva(fila.remover()) // Deve imprimir 5
    fim_algoritmo"""
