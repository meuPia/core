import pytest
from meuPia.analyzers.lexical_analyzer import scan_line, LexicalError
from meuPia.utils.token_enum import TokenEnum

def test_scan_keywords():
    line = "para de ate faca se senao"
    _, tokens = scan_line(line, 1)
    
    expected = [
        TokenEnum.PARA.name,
        TokenEnum.DE.name,
        TokenEnum.ATE.name,
        TokenEnum.FACA.name,
        TokenEnum.SE.name,
        TokenEnum.SENAO.name
    ]
    
    assert len(tokens) == 6
    for i, token_data in enumerate(tokens):
        assert token_data['token'] == expected[i]

def test_scan_symbols():
    line = "[ ] ( ) <- , : ."
    _, tokens = scan_line(line, 1)
    
    expected = [
        TokenEnum.COLCHETEA.name,
        TokenEnum.COLCHETEF.name,
        TokenEnum.PARAB.name,
        TokenEnum.PARFE.name,
        TokenEnum.ATR.name,
        TokenEnum.COMMA.name,
        TokenEnum.COLON.name,
        TokenEnum.PONTO.name
    ]
    
    assert len(tokens) == 8
    for i, token_data in enumerate(tokens):
        assert token_data['token'] == expected[i]

def test_scan_literals():
    line = '"texto" 123'
    _, tokens = scan_line(line, 1)
    
    assert len(tokens) == 2
    assert tokens[0]['token'] == TokenEnum.STRING.name
    assert tokens[0]['lexeme'] == '"texto"'
    
    assert tokens[1]['token'] == TokenEnum.NUMINT.name
    assert tokens[1]['lexeme'] == '123'

def test_scan_identifiers():
    line = "variavel_1 x y"
    _, tokens = scan_line(line, 1)
    
    assert len(tokens) == 3
    assert tokens[0]['token'] == TokenEnum.ID.name
    assert tokens[0]['lexeme'] == 'variavel_1'

def test_scan_operators():
    line = "+ - * / > < >= <= = <>"
    _, tokens = scan_line(line, 1)
    
    expected = [
        TokenEnum.OPMAIS.name,
        TokenEnum.OPMENOS.name,
        TokenEnum.OPMULTI.name,
        TokenEnum.OPDIVI.name,
        TokenEnum.LOGMAIOR.name,
        TokenEnum.LOGMENOR.name,
        TokenEnum.LOGMAIORIGUAL.name,
        TokenEnum.LOGMENORIGUAL.name,
        TokenEnum.LOGIGUAL.name,
        TokenEnum.LOGDIFF.name
    ]
    
    assert len(tokens) == len(expected)
    for i, token_data in enumerate(tokens):
        assert token_data['token'] == expected[i]

def test_invalid_char():
    with pytest.raises(LexicalError):
        scan_line("var $ x", 1)

def test_scan_dict_braces():
    line = "{ }"
    _, tokens = scan_line(line, 1)
    
    assert len(tokens) == 2
    assert tokens[0]['token'] == TokenEnum.CHAVEA.name
    assert tokens[1]['token'] == TokenEnum.CHAVEF.name