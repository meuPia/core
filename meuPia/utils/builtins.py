# Nomes que so funcionam como tipo na posicao de tipo do 'var' e logo depois de 'novo'
TIPOS_CONTEXTUAIS = ('lista', 'logico')

# Funcoes nativas: nome no Portugol -> nome no Python
FUNCOES_BUILTIN = {
  'tamanho': 'len',
  'raiz': 'math.sqrt',
  'potencia': 'math.pow',
  'seno': 'math.sin',
  'cosseno': 'math.cos',
  'tangente': 'math.tan',
  'teto': 'math.ceil',
  'piso': 'math.floor',
  'absoluto': 'abs',
  'filaDupla': 'deque',
  'filaPrioridade': 'FilaPrioridade',
}

# Constantes nativas, usadas sem parenteses
CONSTANTES_BUILTIN = {
  'pi': 'math.pi',
  'verdadeiro': 'True',
  'falso': 'False',
}

# Metodos de colecao, aplicados apenas a nomes que vem depois de '.'
METODOS = {
  'adicionar': 'append',
  'pegar': 'get',
  'atualizar': 'update',
  'adicionarInicio': 'appendleft',
  'adicionarFim': 'append',
  'removerInicio': 'popleft',
  'removerFim': 'pop',
  'expandir': 'extend',
  'limpar': 'clear',
  'tamanho': '__len__',
}
