from typing import Dict, List

from ..utils.builtins import CONSTANTES_BUILTIN, FUNCOES_BUILTIN
from ..utils.erros import ErroCompilacao, posicao
from ..utils.token_enum import TokenEnum

class SemanticError(ErroCompilacao):
  etapa = 'semântico'

class SemanticAnalyzer:
  def __init__(self, lexemePairs: List[Dict[str, str]]):
    self.lexeme_pairs = lexemePairs
    self.declared_vars = []
    self.callable_names = set() # nomes de funcao e classe
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
    # Pre-passagem: variaveis globais (blocos var) e nomes de funcao e classe
    in_var_block = False

    while self.pos < len(self.lexeme_pairs):
      if self.check_token(TokenEnum.VAR):
        in_var_block = True

      elif self.check_token_any([TokenEnum.FUNCAO, TokenEnum.CLASSE, TokenEnum.METODO]):
        # Qualquer declaracao encerra o bloco var
        in_var_block = False
        if not self.check_token(TokenEnum.METODO) and self.token_at(self.pos + 1) == TokenEnum.ID.name:
          self.callable_names.add(self.lexeme_pairs[self.pos + 1]['lexeme'])

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
    local_vars = set()

    while self.pos < len(self.lexeme_pairs):
      if self.check_token(TokenEnum.INICIO):
        in_code_block = True
        local_vars = set()

      elif self.check_token(TokenEnum.CLASSE):
        self.advance() # Passa o nome da classe

      elif self.check_token_any([TokenEnum.FUNCAO, TokenEnum.METODO]):
        is_method = self.check_token(TokenEnum.METODO)
        self.advance() # Passa 'funcao'/'metodo'
        self.advance() # Passa o nome
        self.advance() # Passa o '('

        # Parametros sao locais ao corpo; metodos tambem enxergam 'self'
        local_vars = {'self'} if is_method else set()
        while self.pos < len(self.lexeme_pairs) and not self.check_token(TokenEnum.PARFE):
          if self.check_token(TokenEnum.ID):
            local_vars.add(self.current_lexeme())
          self.advance()

        in_code_block = True

      elif self.check_token(TokenEnum.FIMFUNCAO):
        in_code_block = False
        local_vars = set()

      elif in_code_block and self.check_token(TokenEnum.ID):
        lexeme = self.current_lexeme()

        if not self.is_valid_name(lexeme, local_vars):
          raise self.erro(f'a variável "{lexeme}" não foi declarada no bloco var')

      self.advance()

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
