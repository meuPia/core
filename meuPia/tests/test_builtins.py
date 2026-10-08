from meuPia.tests.helpers import executar, programa


# --- Nomes declarados pelo usuario tem prioridade sobre builtins ---

def test_variavel_chamada_pi():
    assert executar(programa('pi <- 3\nescreva(pi)', var='pi: inteiro')) == '3'


def test_funcao_do_usuario_chamada_raiz():
    codigo = programa('escreva(raiz(9))', antes='funcao raiz(x)\nretorne x + 1\nfim_funcao')
    assert executar(codigo) == '10'


def test_parametro_chamado_teto():
    codigo = programa('escreva(limite(7))', antes='funcao limite(teto)\nretorne teto\nfim_funcao')
    assert executar(codigo) == '7'


def test_builtin_disponivel_sem_conflito():
    assert executar(programa('escreva(raiz(9))')) == '3.0'


# --- Constantes builtin sem parenteses ---

def test_constante_pi_sem_parenteses():
    assert executar(programa('escreva(teto(pi))')) == '4'


# --- tamanho como funcao e como metodo ---

def test_metodo_tamanho_em_fila_dupla():
    codigo = programa(
        'd <- filaDupla()\nd.adicionarFim(1)\nd.adicionarInicio(0)\nescreva(d.tamanho())', var='d: inteiro'
    )
    assert executar(codigo) == '2'


def test_metodo_tamanho_em_fila_prioridade():
    codigo = programa('f.inserir(5)\nescreva(f.tamanho())', var='f: filaPrioridade')
    assert executar(codigo) == '1'


def test_funcao_tamanho_em_fila_prioridade():
    codigo = programa('f.inserir(5)\nescreva(tamanho(f))', var='f: filaPrioridade')
    assert executar(codigo) == '1'


def test_metodo_tamanho_em_lista_e_texto():
    codigo = programa('l <- [1, 2, 3]\ns <- "ab"\nescreva(l.tamanho() + s.tamanho())', var='l: lista\ns: cadeia')
    assert executar(codigo) == '5'


# --- Metodos de colecao traduzidos ---

def test_remocao_em_expressao():
    codigo = programa(
        'd <- filaDupla()\nd.adicionarFim(1)\nd.adicionarFim(2)\nescreva(d.removerInicio() + d.removerFim())',
        var='d: inteiro'
    )
    assert executar(codigo) == '3'


def test_pegar_e_atualizar_em_dicionario():
    codigo = programa('m.atualizar({"a": 1})\nescreva(m.pegar("a"))', var='m: dicionario')
    assert executar(codigo) == '1'


def test_metodos_de_lista():
    codigo = programa(
        'l.adicionar(1)\nl.expandir([2, 3])\nescreva(l.removerFim())\nl.limpar()\nescreva(tamanho(l))',
        var='l: lista'
    )
    assert executar(codigo) == '3\n0'


# --- escreva com um ou mais argumentos ---

def test_escreva_varios_argumentos():
    assert executar(programa('x <- 5\nescreva("x=", x)', var='x: inteiro')) == 'x=5'


def test_escreva_logico_em_argumento_unico():
    assert executar(programa('escreva(verdadeiro)')) == 'verdadeiro'


def test_escreva_logico_entre_varios_argumentos():
    assert executar(programa('escreva("ativo: ", falso)')) == 'ativo: falso'


def test_escreva_concatenacao_com_mais():
    assert executar(programa('n <- 2\nescreva("n=" + n)', var='n: inteiro')) == 'n=2'
