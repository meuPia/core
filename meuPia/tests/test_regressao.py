import glob
import os

import pytest

from meuPia.tests.helpers import compilar

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROGRAMAS = sorted(
    glob.glob(os.path.join(RAIZ_PROJETO, 'exemplos', '*.por')) +
    glob.glob(os.path.join(RAIZ_PROJETO, 'meuPia', 'input', '*.por'))
)


def test_ha_programas_para_verificar():
    assert len(PROGRAMAS) >= 5


@pytest.mark.parametrize('caminho', PROGRAMAS, ids=lambda c: os.path.relpath(c, RAIZ_PROJETO))
def test_programa_versionado_compila(caminho):
    with open(caminho, encoding='utf-8') as arquivo:
        python_code = compilar(arquivo.read())
    compile(python_code, caminho, 'exec')
