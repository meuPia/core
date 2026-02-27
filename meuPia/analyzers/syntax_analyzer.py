from typing import Dict, List

from ..utils.token_enum import TokenEnum

class SyntacticError(Exception):
  pass

class Parser:
  def __init__(self, lexemePairs: List[Dict[str, str]]):
    self.lexeme_pairs = lexemePairs
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['token']
    
    return TokenEnum.END_OF_FILE.name
  
  def current_lexeme(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['lexeme']
    
    return ' '
  
  def current_code_index(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['code_index']

    return self.lexeme_pairs[-1].get('code_index', 'unknown')

  def peek_next_token(self) -> str:
    if self.pos + 1 < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos + 1]['token']
    return ''

  def expect_token(self, expected: TokenEnum):
    if self.current_token() == expected.name:
      self.pos += 1
      return
    
    lexeme = self.current_lexeme()
    code_index = self.current_code_index()
    raise SyntacticError(f'Esperado "{expected.value}", encontrado "{lexeme}" na linha {code_index}')
  
  def check_token(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name
  
  def check_token_any(self, expected: List[TokenEnum]) -> bool:
    return any(self.current_token() == t.name for t in expected)

  def parse(self):
    self.expect_token(TokenEnum.ALGORITMO)
    self.expect_token(TokenEnum.STRING)
    
    # Optional Plugin Imports
    while self.check_token(TokenEnum.USAR):
        self.expect_token(TokenEnum.USAR)
        self.expect_token(TokenEnum.STRING)

    if self.check_token(TokenEnum.VAR):
      self.grammar_variable_block()

    while self.check_token_any([TokenEnum.FUNCAO, TokenEnum.VAR]):
      if self.check_token(TokenEnum.FUNCAO):
          self.grammar_function_declaration()
      elif self.check_token(TokenEnum.VAR):
          self.grammar_variable_block()

    self.expect_token(TokenEnum.INICIO)

    while not self.check_token_any([TokenEnum.FIMALGORITMO, TokenEnum.END_OF_FILE]):
      self.statement()

    self.expect_token(TokenEnum.FIMALGORITMO)

    if self.pos < len(self.lexeme_pairs):
      extra_lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Código inesperado após "fimalgoritmo": "{extra_lexeme}" na linha {code_index}')

  def statement(self):
    # A função grammar_id_statement agora cuida de TUDO (atribuição, métodos encadeados, etc)
    if self.check_token(TokenEnum.ID):
      self.grammar_id_statement()
    elif self.check_token(TokenEnum.ESCREVA):
      self.grammar_command_escreva()
    elif self.check_token(TokenEnum.LEIA):
      self.grammar_command_leia()
    elif self.check_token(TokenEnum.SE):
      self.grammar_command_se()
    elif self.check_token(TokenEnum.ENQUANTO):
      self.grammar_command_enquanto()
    elif self.check_token(TokenEnum.PARA):
      self.grammar_command_para()
    elif self.check_token(TokenEnum.RETORNE):
      self.grammar_command_retorne()
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Token inesperado "{lexeme}" na linha {code_index}')

  def grammar_id_statement(self):
    self.expect_token(TokenEnum.ID)
    
    # Consome os métodos/propriedades encadeados (ex: pessoa.endereco.rua)
    while self.check_token(TokenEnum.PONTO):
      self.expect_token(TokenEnum.PONTO)
      self.expect_token(TokenEnum.ID)
      
    if self.check_token(TokenEnum.ATR):
      self.expect_token(TokenEnum.ATR)
      self.grammar_arithmetic_expression()
      
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      if not self.check_token(TokenEnum.PARFE):
          self.grammar_arithmetic_expression()
          while self.check_token(TokenEnum.COMMA):
              self.expect_token(TokenEnum.COMMA)
              self.grammar_arithmetic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      code_index = self.current_code_index()
      raise SyntacticError(f'Comando inválido após identificador na linha {code_index}')

  # ----------------
  # Gramáticas
  # ----------------

  def grammar_variable_block(self):
    self.expect_token(TokenEnum.VAR)

    while self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)

      # IDs opcionais separados por vírgula
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)

      self.expect_token(TokenEnum.COLON)
      self.expect_token(TokenEnum.TIPO)

  def grammar_command_escreva(self):
    self.expect_token(TokenEnum.ESCREVA)
    self.expect_token(TokenEnum.PARAB)
    self.grammar_arithmetic_expression()
    self.expect_token(TokenEnum.PARFE)

  def grammar_command_leia(self):
    self.expect_token(TokenEnum.LEIA)
    self.expect_token(TokenEnum.PARAB)

    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Esperado variável no comando leia, encontrado "{lexeme}" na linha {code_index}')

    self.expect_token(TokenEnum.PARFE)
  
  def grammar_command_se(self):
    self.expect_token(TokenEnum.SE)
    self.grammar_logic_expression()

    self.expect_token(TokenEnum.ENTAO)
    while not self.check_token_any([TokenEnum.SENAO, TokenEnum.FIMSE]):
      self.statement()
    
    if self.check_token(TokenEnum.SENAO):
      self.expect_token(TokenEnum.SENAO)
      while not self.check_token(TokenEnum.FIMSE):
        self.statement()

    self.expect_token(TokenEnum.FIMSE)

  def grammar_command_enquanto(self):
    self.expect_token(TokenEnum.ENQUANTO)
    self.grammar_logic_expression()
    
    if self.check_token(TokenEnum.FACA):
        self.expect_token(TokenEnum.FACA)
    
    while not self.check_token(TokenEnum.FIMENQUANTO):
      self.statement()

    self.expect_token(TokenEnum.FIMENQUANTO)

  def grammar_command_para(self):
    self.expect_token(TokenEnum.PARA)
    self.expect_token(TokenEnum.ID)
    
    # Sintaxe: PARA id DE inicio ATE fim [FACA]
    self.expect_token(TokenEnum.DE)
    self.grammar_arithmetic_term() # Inicio (valor ou id)
    
    self.expect_token(TokenEnum.ATE)
    self.grammar_arithmetic_term() # Fim definition
    
    # Passo opcional
    if self.check_token(TokenEnum.PASSO):
      self.expect_token(TokenEnum.PASSO)
      self.grammar_arithmetic_term() # Passo value

    if self.check_token(TokenEnum.FACA):
        self.expect_token(TokenEnum.FACA)

    while not self.check_token(TokenEnum.FIMPARA):
      self.statement()

    self.expect_token(TokenEnum.FIMPARA)

  #
  # Fundamental
  #
  def grammar_arithmetic_expression(self):
    self.grammar_arithmetic_term()
    
    while self.check_token_any([TokenEnum.OPMAIS, TokenEnum.OPMENOS, TokenEnum.OPMULTI, TokenEnum.OPDIVI]):
      self.pos += 1
      self.grammar_arithmetic_term()

  def grammar_arithmetic_term(self):
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
      
      # Aceita métodos/propriedades encadeados em expressões (ex: escreva(texto.upper()))
      while self.check_token(TokenEnum.PONTO):
          self.expect_token(TokenEnum.PONTO)
          self.expect_token(TokenEnum.ID)
          
      if self.check_token(TokenEnum.PARAB):
          # É uma chamada de método que retorna valor
          self.expect_token(TokenEnum.PARAB)
          if not self.check_token(TokenEnum.PARFE):
              self.grammar_arithmetic_expression()
              while self.check_token(TokenEnum.COMMA):
                  self.expect_token(TokenEnum.COMMA)
                  self.grammar_arithmetic_expression()
          self.expect_token(TokenEnum.PARFE)
      else:
          # É apenas uma variável/propriedade (ex: pessoa.idade)
          while self.check_token(TokenEnum.COLCHETEA):
              self.expect_token(TokenEnum.COLCHETEA)
              self.grammar_arithmetic_expression()
              self.expect_token(TokenEnum.COLCHETEF)

    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.STRING):
      self.expect_token(TokenEnum.STRING)
    elif self.check_token(TokenEnum.COLCHETEA):
      self.expect_token(TokenEnum.COLCHETEA)
      # Recursive list support
      if not self.check_token(TokenEnum.COLCHETEF):
          self.grammar_arithmetic_expression()
          while self.check_token(TokenEnum.COMMA):
              self.expect_token(TokenEnum.COMMA)
              self.grammar_arithmetic_expression()
      self.expect_token(TokenEnum.COLCHETEF)

    elif self.check_token(TokenEnum.CHAVEA):
      self.expect_token(TokenEnum.CHAVEA)
      
      # Verifica se não é um dicionário vazio {}
      if not self.check_token(TokenEnum.CHAVEF):
          # Lê o primeiro par -> Chave : Valor
          self.grammar_arithmetic_expression() # Chave
          self.expect_token(TokenEnum.COLON)   # :
          self.grammar_arithmetic_expression() # Valor
          
          # Lê os próximos pares se houver vírgula
          while self.check_token(TokenEnum.COMMA):
              self.expect_token(TokenEnum.COMMA)   # ,
              self.grammar_arithmetic_expression() # Chave
              self.expect_token(TokenEnum.COLON)   # :
              self.grammar_arithmetic_expression() # Valor
              
      self.expect_token(TokenEnum.CHAVEF)

    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_arithmetic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      code_index = self.current_code_index()
      raise SyntacticError(f'Esperado identificador ou valor na expressão, linha {code_index}')

  def grammar_logic_expression(self):
    self.grammar_logic_comparison()
    while self.check_token_any([TokenEnum.E, TokenEnum.OU]):
      self.pos += 1
      self.grammar_logic_comparison()

  def grammar_logic_comparison(self):
    if self.check_token(TokenEnum.NAO):
      self.expect_token(TokenEnum.NAO)
      self.grammar_logic_comparison()
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_logic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      self.grammar_logic_operand()
      if self.check_token_any([
        TokenEnum.LOGIGUAL, TokenEnum.LOGDIFF,
        TokenEnum.LOGMENOR, TokenEnum.LOGMENORIGUAL,
        TokenEnum.LOGMAIOR, TokenEnum.LOGMAIORIGUAL
      ]):
        self.pos += 1
        self.grammar_logic_operand()
      else:
        code_index = self.current_code_index()
        raise SyntacticError(f'Faltando operador de comparação na linha {code_index}')

  def grammar_logic_operand(self):
    if self.check_token_any([TokenEnum.ID, TokenEnum.NUMINT, TokenEnum.STRING, TokenEnum.PARAB]):
        self.grammar_arithmetic_term()
    else:
      code_index = self.current_code_index()
      raise SyntacticError(f'Operando lógico inválido na linha {code_index}')

  def grammar_function_declaration(self):
    self.expect_token(TokenEnum.FUNCAO)
    self.expect_token(TokenEnum.ID)     # Nome da função
    self.expect_token(TokenEnum.PARAB)  # (
    
    # Parâmetros opcionais (ex: a, b)
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)
        
    self.expect_token(TokenEnum.PARFE)  # )
    
    # Corpo da função
    while not self.check_token(TokenEnum.FIMFUNCAO):
      self.statement()
      
    self.expect_token(TokenEnum.FIMFUNCAO)

  def grammar_command_retorne(self):
    self.expect_token(TokenEnum.RETORNE)
    self.grammar_arithmetic_expression() # O que ele vai retornar