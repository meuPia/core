import contextlib
import io
import sys

from meuPia.analyzers.code_generator import CodeGenerator
from meuPia.analyzers.lexical_analyzer import scan_line
from meuPia.analyzers.semantic_analyzer import SemanticAnalyzer
from meuPia.analyzers.syntax_analyzer import Parser


def compilar(codigo):
    """Roda o pipeline completo (lexico, sintatico, semantico, gerador) e retorna o Python gerado."""
    lexemas = []
    for i, linha in enumerate(codigo.split('\n')):
        _, tokens = scan_line(linha, i + 1)
        lexemas.extend(tokens)

    Parser(lexemas).parse()
    SemanticAnalyzer(lexemas).validate()
    return CodeGenerator(lexemas).generate()


def executar(codigo, entrada=""):
    """Compila e executa o programa Portugol, retornando o que foi impresso (sem a quebra de linha final)."""
    python_code = compilar(codigo)
    saida = io.StringIO()
    stdin_original = sys.stdin
    sys.stdin = io.StringIO(entrada)
    try:
        with contextlib.redirect_stdout(saida):
            exec(python_code, {'__name__': '__main__'})
    finally:
        sys.stdin = stdin_original
    return saida.getvalue().rstrip('\n')


def programa(corpo, var='', antes=''):
    """Monta um algoritmo completo a partir do corpo de 'inicio', do bloco var e das declaracoes anteriores."""
    partes = ['algoritmo "Teste"']
    if var:
        partes.append(f'var\n{var}')
    if antes:
        partes.append(antes)
    partes.append('inicio')
    partes.append(corpo)
    partes.append('fim_algoritmo')
    return '\n'.join(partes)
