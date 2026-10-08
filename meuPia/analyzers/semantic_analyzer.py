from typing import Dict, List

from ..utils.builtins import CONSTANTES_BUILTIN, FUNCOES_BUILTIN
from ..utils.erros import ErroCompilacao, posicao
from ..utils.token_enum import TokenEnum
from .syntax_analyzer import Parser

class SemanticError(ErroCompilacao):
  etapa = 'semântico'

class SemanticAnalyzer:
  def __init__(self, lexemePairs: List[Dict[str, str]]):
    self.lexeme_pairs = lexemePairs
    self.declared_vars = []
    self.callable_names = set() # nomes de funcao e classe
    self.params = set()
    self.locais_visiveis = set()
    self.declaradas_no_corpo = {}
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['token']

    return TokenEnum.END_OF_FILE.name

  def current_lexeme(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['lexeme']

    return ' '

  def erro(self, descricao: str) -> SemanticError:
    linha, coluna = posicao(self.lexeme_pairs, self.pos)
    return SemanticError(descricao, linha, coluna)

  def advance(self):
    self.pos += 1

  def check_token(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name

  def token_at(self, index: int) -> str:
    if 0 <= index < len(self.lexeme_pairs):
      return self.lexeme_pairs[index]['token']
    return TokenEnum.END_OF_FILE.name

  def validate(self):
    self.get_declared_variables()
    self.validate_variable_usage()

  # ----------------
  # Validations
  # ----------------
  def get_declared_variables(self):
    # Pre-passagem: variaveis globais (blocos var do topo) e nomes de funcao e classe
    in_var_block = False
    in_body = False # 'var' dentro de funcao/metodo e declaracao local, nao global

    while self.pos < len(self.lexeme_pairs):
      if self.check_token(TokenEnum.VAR) and not in_body:
        in_var_block = True

      elif self.check_token_any([TokenEnum.FUNCAO, TokenEnum.CLASSE, TokenEnum.METODO]):
        # Qualquer declaracao encerra o bloco var
        in_var_block = False
        in_body = not self.check_token(TokenEnum.CLASSE)
        if not self.check_token(TokenEnum.METODO) and self.token_at(self.pos + 1) == TokenEnum.ID.name:
          self.callable_names.add(self.lexeme_pairs[self.pos + 1]['lexeme'])

      elif self.check_token(TokenEnum.FIMFUNCAO):
        in_body = False

      elif self.check_token(TokenEnum.INICIO):
        break

      elif in_var_block and self.check_token(TokenEnum.ID) and not self.is_type_position():
        lexeme = self.current_lexeme()

        if self.is_variable_declared(lexeme):
          raise self.erro(f'a variável "{lexeme}" foi declarada mais de uma vez')
        
        self.declared_vars.append(self.lexeme_pairs[self.pos])

      self.advance()

  def validate_variable_usage(self):
    self.pos = 0
    in_code_block = False

    while self.pos < len(self.lexeme_pairs):
      if self.check_token(TokenEnum.INICIO):
        in_code_block = True
        self.enter_body(set())

      elif self.check_token(TokenEnum.CLASSE):
        self.advance() # Passa o nome da classe

      elif self.check_token_any([TokenEnum.FUNCAO, TokenEnum.METODO]):
        is_method = self.check_token(TokenEnum.METODO)
        self.advance() # Passa 'funcao'/'metodo'
        self.advance() # Passa o nome
        self.advance() # Passa o '('

        # Parametros sao locais ao corpo; metodos tambem enxergam 'self'
        params = {'self'} if is_method else set()
        while self.pos < len(self.lexeme_pairs) and not self.check_token(TokenEnum.PARFE):
          if self.check_token(TokenEnum.ID):
            params.add(self.current_lexeme())
          self.advance()

        in_code_block = True
        self.enter_body(params)

      elif self.check_token(TokenEnum.FIMFUNCAO):
        in_code_block = False
        self.enter_body(set())

      elif in_code_block and self.check_token(TokenEnum.VAR):
        self.validate_local_declaration()
        continue # validate_local_declaration ja posiciona depois da declaracao

      elif in_code_block and self.check_token(TokenEnum.ID):
        self.validate_identifier()

      self.advance()

  def enter_body(self, params: set):
    # Novo corpo (funcao, metodo ou inicio): so os parametros sao visiveis no comeco
    self.params = params
    self.locais_visiveis = set(params)
    self.declaradas_no_corpo = self.scan_body_declarations(self.pos)

  def scan_body_declarations(self, inicio: int) -> dict:
    # Todas as variaveis locais declaradas no corpo, para diferenciar "usada antes" de "nao declarada"
    declaradas = {}
    j = inicio
    while self.token_at(j) not in (TokenEnum.FIMFUNCAO.name, TokenEnum.FIMALGORITMO.name, TokenEnum.END_OF_FILE.name):
      if self.token_at(j) == TokenEnum.VAR.name:
        linhas, j = Parser.ler_declaracao_local(self.lexeme_pairs, j)
        for linha in linhas:
          for nome, posicao_nome in linha['nomes']:
            declaradas.setdefault(nome, posicao_nome)
      else:
        j += 1
    return declaradas

  def validate_local_declaration(self):
    linhas, fim = Parser.ler_declaracao_local(self.lexeme_pairs, self.pos)

    for linha in linhas:
      nomes_da_linha = set()
      for nome, posicao_nome in linha['nomes']:
        conflito = self.local_name_conflict(nome, nomes_da_linha)
        if conflito:
          raise self.erro_em(conflito, posicao_nome)
        nomes_da_linha.add(nome)

      # O valor inicial e avaliado antes de a variavel existir
      if linha['expressao']:
        inicio_expr, fim_expr = linha['expressao']
        for indice in range(inicio_expr, fim_expr):
          self.pos = indice
          if self.check_token(TokenEnum.ID):
            self.validate_identifier()

      self.locais_visiveis |= nomes_da_linha

    self.pos = fim

  def local_name_conflict(self, nome: str, nomes_da_linha: set) -> str:
    if nome == 'self' and 'self' in self.params:
      return '"self" é reservado dentro de métodos e não pode ser declarado com var'
    if nome in self.params:
      return f'"{nome}" já é um parâmetro deste bloco; escolha outro nome para a variável'
    if self.is_variable_declared(nome):
      return f'a variável "{nome}" já existe como variável global; escolha outro nome'
    if nome in self.locais_visiveis or nome in nomes_da_linha:
      return f'a variável "{nome}" já foi declarada neste bloco'
    if nome in self.callable_names:
      return f'"{nome}" já é o nome de uma função ou classe; escolha outro nome para a variável'
    return ''

  def validate_identifier(self):
    lexeme = self.current_lexeme()
    if self.is_valid_name(lexeme, self.locais_visiveis):
      return
    if lexeme in self.declaradas_no_corpo:
      raise self.erro(f'a variável "{lexeme}" foi usada antes de ser declarada')
    raise self.erro(f'a variável "{lexeme}" não foi declarada no bloco var')

  def erro_em(self, descricao: str, pos: int) -> SemanticError:
    linha, coluna = posicao(self.lexeme_pairs, pos)
    return SemanticError(descricao, linha, coluna)

  def is_valid_name(self, lexeme: str, local_vars: set) -> bool:
    if self.token_at(self.pos - 1) == TokenEnum.PONTO.name:
      return True # Membro de objeto (atributo ou metodo): nao e variavel
    if self.token_at(self.pos + 1) == TokenEnum.PARAB.name:
      return True # Chamada: erros de funcao inexistente ficam para a execucao
    if lexeme in CONSTANTES_BUILTIN or lexeme in FUNCOES_BUILTIN:
      return True
    return self.is_variable_declared(lexeme) or lexeme in local_vars or lexeme in self.callable_names

  def check_token_any(self, expected: List[TokenEnum]) -> bool:
    return any(self.check_token(t) for t in expected)

  def is_type_position(self) -> bool:
    return self.token_at(self.pos - 1) == TokenEnum.COLON.name

  def is_variable_declared(self, lexeme) -> bool:
    return any(var['lexeme'] == lexeme for var in self.declared_vars)
