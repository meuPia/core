import glob
import os

import pytest

from meuPia.tests.helpers import compilar

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA_GOLDEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'golden')

# Programas sem 'var' local devem gerar exatamente o mesmo Python de antes (saida congelada em golden/)
PROGRAMAS = sorted(
    glob.glob(os.path.join(RAIZ_PROJETO, 'exemplos', '*.por')) +
    glob.glob(os.path.join(RAIZ_PROJETO, 'meuPia', 'input', '*.por'))
)


@pytest.mark.parametrize('caminho', PROGRAMAS, ids=lambda c: os.path.basename(c))
def test_codigo_gerado_igual_ao_golden(caminho):
    nome = os.path.splitext(os.path.basename(caminho))[0]
    with open(caminho, encoding='utf-8') as arquivo:
        gerado = compilar(arquivo.read())
    with open(os.path.join(PASTA_GOLDEN, f'{nome}.py'), encoding='utf-8') as arquivo:
        esperado = arquivo.read()
    assert gerado == esperado
