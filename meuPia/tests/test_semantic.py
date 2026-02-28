import pytest
from meuPia.analyzers.semantic_analyzer import SemanticAnalyzer, SemanticError
from meuPia.analyzers.lexical_analyzer import scan_line

def mock_lexemes(code_lines):
    all_lexemes = []
    for i, line in enumerate(code_lines):
        line_clean, lexemes = scan_line(line, i+1)
        all_lexemes.extend(lexemes)
    return all_lexemes

def test_semantic_valid_variable_usage():
    code = [
        'algoritmo "Valid"',
        'var x: inteiro',
        'inicio',
        '   x <- 10',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    semantic.validate() # Should pass

def test_semantic_undeclared_variable():
    code = [
        'algoritmo "Invalid"',
        'inicio',
        '   x <- 10', # x is undeclared
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    
    with pytest.raises(SemanticError) as excinfo:
        semantic.validate()
    
    assert 'Undeclared variable "x"' in str(excinfo.value)

def test_semantic_double_declaration():
    code = [
        'algoritmo "Double"',
        'var x, x: inteiro',
        'inicio',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    
    with pytest.raises(SemanticError) as excinfo:
        semantic.validate()
        
    assert 'Double declaration for variable "x"' in str(excinfo.value)

def test_semantic_bypass_function_call():
    code = [
        'algoritmo "Func"',
        'inicio',
        '   ia_treinar()', # Function call, declared var check should bypass
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    semantic.validate() # Should pass

def test_semantic_method_call():
    code = [
        'algoritmo "Metodo"',
        'var texto: string',
        'inicio',
        '   texto.upper()', # "upper" deve ser ignorado pela checagem de variáveis pois é seguido de ()
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    semantic.validate() # Should pass

def test_semantic_function_parameters():
    code = [
        'algoritmo "Escopo"',
        'funcao somar(a, b)',
        '   retorne a + b', # 'a' e 'b' devem ser reconhecidos como válidos aqui dentro
        'fim_funcao',
        'inicio',
        '   escreva(somar(1, 2))',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    semantic.validate()

def test_semantic_undeclared_in_function():
    code = [
        'algoritmo "EscopoErro"',
        'funcao somar(a, b)',
        '   retorne a + c', # ERRO! A variável 'c' não existe e não é parâmetro!
        'fim_funcao',
        'inicio',
        '   escreva(somar(1, 2))',
        'fim_algoritmo'
    ]
    lexemes = mock_lexemes(code)
    semantic = SemanticAnalyzer(lexemes)
    
    with pytest.raises(SemanticError) as excinfo:
        semantic.validate()
    
    assert 'Undeclared variable "c"' in str(excinfo.value)