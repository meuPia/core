import pytest
from meuPia.analyzers.syntax_analyzer import Parser, SyntacticError
from meuPia.analyzers.lexical_analyzer import scan_line

def mock_lexemes(code_lines):
    all_lexemes = []
    for i, line in enumerate(code_lines):
        line_clean, lexemes = scan_line(line, i+1)
        all_lexemes.extend(lexemes)
    return all_lexemes

def test_syntax_full_algorithm():
    code = [
        'algoritmo "Teste"',
        'var x, y : inteiro',
        'inicio',
        '   x = 10',
        '   y = 20',
        '   escreva(x + y)',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    # expect no exception
    parser.parse()

def test_syntax_loop():
    code = [
        'algoritmo "Loop"',
        'inicio',
        '   para i de 1 ate 10 faca',
        '       escreva(i)',
        '   fim_para',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_conditional():
    code = [
        'algoritmo "Cond"',
        'inicio',
        '   se x > 10 entao',
        '       escreva("Maior")',
        '   senao',
        '       escreva("Menor")',
        '   fim_se',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_object_methods():
    code = [
        'algoritmo "Objetos"',
        'var texto: string',
        'inicio',
        '   texto = "henry"',
        '   escreva(texto.upper())',
        '   texto.replace("h", "H")',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_error_missing_tokens():
    code = [
        'algoritmo "Erro"',
        'inicio',
        '   se x > 10', # Missing entao
        '       escreva("Erro")',
        '   fim_se',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    with pytest.raises(SyntacticError) as excinfo:
        parser.parse()
    assert 'Esperado "então"' in str(excinfo.value)

def test_syntax_error_invalid_var_block():
    code = [
        'algoritmo "ErroVar"',
        'var x', # Missing type
        'inicio',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    with pytest.raises(SyntacticError):
        parser.parse()

def test_syntax_nested_arrays():
    code = [
        'algoritmo "Matrix"',
        'var m: inteiro',
        'inicio',
        '   m = [[1,2], [3,4]]',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_complex_arrays():
    code = [
        'algoritmo "Matrix"',
        'var m: inteiro',
        'inicio',
        '   m = [[1, 2], [3, 4]]',
        '   escreva(m[0][1])',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_dictionary():
    code = [
        'algoritmo "Dict"',
        'var d: inteiro',
        'inicio',
        '   d = {}',
        '   d = {"nome": "Henry", "idade": 30}',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    
    parser.parse()

def test_syntax_function_declaration():
    code = [
        'algoritmo "Func"',
        'funcao multiplicar(a, b)',
        '   retorne a * b',
        'fim_funcao',
        'inicio',
        '   escreva(multiplicar(2, 3))',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_direct_indexing_assignment():
    code = [
        'algoritmo "Index"',
        'var lista: inteiro',
        'inicio',
        '   lista = 10',
        '   dicionario["nome"] = "Henry"',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse() # Deve falhar aqui

def test_syntax_deque_methods():
    code = [
        'algoritmo "FilaDupla"',
        'var f: inteiro',
        'inicio',
        '   f = filaDupla()',
        '   f.inserirInicio(10)',
        '   f.expandir([20, 30])',
        '   f.removerFim()',
        '   f.removerInicio()',
        '   f.limpar()',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_oop_class():
    code = [
        'algoritmo "OOP"',
        'classe Animal',
        '   metodo falar(som)',
        '       escreva(som)',
        '   fim_funcao',
        'fim_classe',
        'var',
        '   meu_pet: string',
        'inicio',
        '   meu_pet = novo Animal()',
        '   meu_pet.falar("Miau")',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse()

def test_syntax_unary_minus():
    code = [
        'algoritmo "Negativo"',
        'inicio',
        '   escreva(-1)',
        '   escreva(5 + -3)',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    parser = Parser(lexemes)
    parser.parse() 