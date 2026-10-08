import os
import runpy
import subprocess
import sys

import pytest

from meuPia.compiler import main

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROGRAMA_VALIDO = 'algoritmo "Ok"\ninicio\nescreva("ok")\nfim_algoritmo\n'
PROGRAMA_INVALIDO = 'algoritmo "Ruim"\nvar x: inteiro\ninicio\nx <- 7 $ 2\nfim_algoritmo\n'


def rodar_cli(args, cwd):
    env = dict(os.environ, PYTHONPATH=RAIZ_PROJETO)
    return subprocess.run(
        [sys.executable, '-m', 'meuPia.compiler', *args],
        cwd=cwd, env=env, capture_output=True, text=True
    )


def escrever(tmp_path, nome, conteudo):
    caminho = tmp_path / nome
    caminho.write_text(conteudo, encoding='utf-8')
    return caminho


# --- Codigo de saida do comando ---

def test_cli_sucesso_sai_com_zero(tmp_path):
    escrever(tmp_path, 'ok.por', PROGRAMA_VALIDO)
    resultado = rodar_cli(['ok.por'], tmp_path)
    assert resultado.returncode == 0
    assert (tmp_path / 'output' / 'ok.py').exists()


def test_cli_erro_de_compilacao_sai_com_codigo_diferente_de_zero(tmp_path):
    escrever(tmp_path, 'ruim.por', PROGRAMA_INVALIDO)
    resultado = rodar_cli(['ruim.por'], tmp_path)
    assert resultado.returncode != 0
    assert '[COMPILATION ERROR]' in resultado.stdout


def test_cli_arquivo_inexistente_sai_com_codigo_diferente_de_zero(tmp_path):
    resultado = rodar_cli(['nao_existe.por'], tmp_path)
    assert resultado.returncode != 0


def test_cli_sem_argumentos_sai_com_codigo_diferente_de_zero(tmp_path):
    resultado = rodar_cli([], tmp_path)
    assert resultado.returncode != 0
    assert 'meupia <arquivo.por>' in resultado.stdout


# --- Contrato usado pelo Lab ---

def test_main_sucesso_retorna_zero_e_gera_arquivo(tmp_path):
    entrada = escrever(tmp_path, 'main.por', PROGRAMA_VALIDO)
    saida = tmp_path / 'output'
    assert main(str(entrada), str(saida)) == 0
    gerado = saida / 'main.py'
    assert gerado.exists()
    compile(gerado.read_text(encoding='utf-8'), str(gerado), 'exec')


def test_main_erro_nao_gera_arquivo_nem_propaga_excecao(tmp_path):
    entrada = escrever(tmp_path, 'main.por', PROGRAMA_INVALIDO)
    saida = tmp_path / 'output'
    resultado = main(str(entrada), str(saida))
    assert resultado != 0
    assert not (saida / 'main.py').exists()


def test_main_arquivo_inexistente_retorna_diferente_de_zero(tmp_path):
    assert main(str(tmp_path / 'nao_existe.por'), str(tmp_path / 'output')) != 0


# --- Mesmos caminhos executados no processo atual (medidos pela cobertura) ---

def test_main_le_arquivo_de_sys_argv(tmp_path, monkeypatch):
    escrever(tmp_path, 'ok.por', PROGRAMA_VALIDO)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, 'argv', ['meupia', 'ok.por'])
    assert main() == 0
    assert (tmp_path / 'output' / 'ok.py').exists()


def test_main_sem_argumentos_retorna_erro_de_uso(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['meupia'])
    assert main() == 2
    assert 'meupia <arquivo.por>' in capsys.readouterr().out


def test_main_nao_grava_python_invalido_gerado_por_bug_interno(tmp_path, monkeypatch, capsys):
    from meuPia.analyzers.code_generator import CodeGenerator
    monkeypatch.setattr(CodeGenerator, 'generate', lambda self: 'def quebrado(:\n')
    entrada = escrever(tmp_path, 'main.por', PROGRAMA_VALIDO)
    saida = tmp_path / 'output'
    assert main(str(entrada), str(saida)) == 1
    assert not (saida / 'main.py').exists()
    assert 'Erro interno do compilador' in capsys.readouterr().out


# runpy avisa que o modulo ja foi importado pelos outros testes; o aviso e esperado aqui
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_modulo_como_script_sai_com_codigo_de_retorno(tmp_path, monkeypatch):
    escrever(tmp_path, 'ruim.por', PROGRAMA_INVALIDO)
    monkeypatch.chdir(tmp_path)
    for argv, esperado in ([['compiler', 'ruim.por'], 1], [['compiler'], 2]):
        monkeypatch.setattr(sys, 'argv', argv)
        with pytest.raises(SystemExit) as excinfo:
            runpy.run_module('meuPia.compiler', run_name='__main__', alter_sys=True)
        assert excinfo.value.code == esperado
