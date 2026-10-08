from typing import Dict, List

from ..utils.builtins import TIPOS_CONTEXTUAIS
from ..utils.erros import ErroCompilacao, descrever_token, posicao
from ..utils.token_enum import TokenEnum

class SyntacticError(ErroCompilacao):
  etapa = 'sintático'

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
  
  def erro(self, descricao: str) -> SyntacticError:
    linha, coluna = posicao(self.lexeme_pairs, self.pos)
    return SyntacticError(descricao, linha, coluna)

  def descrever_atual(self) -> str:
    if self.pos >= len(self.lexeme_pairs):
      return descrever_token(TokenEnum.END_OF_FILE)
    return f'"{self.current_lexeme()}"'

  def peek_next_token(self) -> str:
    if self.pos + 1 < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos + 1]['token']
    return ''

  def expect_token(self, expected: TokenEnum):
    if self.current_token() == expected.name:
      self.pos += 1
      return
    
    raise self.erro(f'esperado {descrever_token(expected)}, encontrado {self.descrever_atual()}')
  
  def check_token(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name
  
  def is_equal_sign(self) -> bool:
    # '=' e tokenizado como ATR; dentro de expressoes significa comparacao
    return self.check_token(TokenEnum.ATR) and self.current_lexeme() == '='

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

    while self.check_token_any([TokenEnum.FUNCAO, TokenEnum.VAR, TokenEnum.CLASSE]):
      if self.check_token(TokenEnum.FUNCAO):
          self.grammar_function_declaration()
      elif self.check_token(TokenEnum.VAR):
          self.grammar_variable_block()
      elif self.check_token(TokenEnum.CLASSE):
          self.grammar_class_declaration()

    self.expect_token(TokenEnum.INICIO)

    while not self.check_token_any([TokenEnum.FIMALGORITMO, TokenEnum.END_OF_FILE]):
      self.statement()

    self.expect_token(TokenEnum.FIMALGORITMO)

    if self.pos < len(self.lexeme_pairs):
      raise self.erro(f'código inesperado depois de "fim_algoritmo": {self.descrever_atual()}')

  def statement(self):
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
    elif self.check_token(TokenEnum.CONTINUE):
      self.expect_token(TokenEnum.CONTINUE)
    elif self.check_token(TokenEnum.INTERROMPA):
      self.expect_token(TokenEnum.INTERROMPA)
    else:
      raise self.erro(f'comando inesperado: {self.descrever_atual()}')

  def grammar_id_statement(self):
    self.expect_token(TokenEnum.ID)
    
    while self.check_token(TokenEnum.PONTO):
      self.expect_token(TokenEnum.PONTO)
      self.expect_token(TokenEnum.ID)

    while self.check_token(TokenEnum.COLCHETEA):
      self.expect_token(TokenEnum.COLCHETEA)
      self.grammar_expression()
      self.expect_token(TokenEnum.COLCHETEF)
      
    if self.check_token(TokenEnum.ATR):
      self.expect_token(TokenEnum.ATR)
      self.grammar_expression()
      
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      if not self.check_token(TokenEnum.PARFE):
          self.grammar_expression()
          while self.check_token(TokenEnum.COMMA):
              self.expect_token(TokenEnum.COMMA)
              self.grammar_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      raise self.erro(f'depois de um nome é preciso "<-" para atribuir ou "(" para chamar, encontrado {self.descrever_atual()}')

  # ----------------
  # Gramáticas
  # ----------------

  def grammar_variable_block(self):
    self.expect_token(TokenEnum.VAR)

    while self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)

      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)

      self.expect_token(TokenEnum.COLON)
      if self.check_token(TokenEnum.ID) and self.current_lexeme() in TIPOS_CONTEXTUAIS:
        self.expect_token(TokenEnum.ID)
      else:
        self.expect_token(TokenEnum.TIPO)

  def grammar_command_escreva(self):
    self.expect_token(TokenEnum.ESCREVA)
    self.grammar_arguments(TokenEnum.PARAB, TokenEnum.PARFE)

  def grammar_command_leia(self):
    self.expect_token(TokenEnum.LEIA)
    self.expect_token(TokenEnum.PARAB)

    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    else:
      raise self.erro(f'o comando leia precisa de uma variável, encontrado {self.descrever_atual()}')

    self.expect_token(TokenEnum.PARFE)
  
  def grammar_command_se(self):
    self.expect_token(TokenEnum.SE)
    self.grammar_expression()

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
    self.grammar_expression()
    
    if self.check_token(TokenEnum.FACA):
        self.expect_token(TokenEnum.FACA)
    
    while not self.check_token(TokenEnum.FIMENQUANTO):
      self.statement()

    self.expect_token(TokenEnum.FIMENQUANTO)

  def grammar_command_para(self):
    self.expect_token(TokenEnum.PARA)
    self.expect_token(TokenEnum.ID)
    
    self.expect_token(TokenEnum.DE)
    self.grammar_expression()
    
    self.expect_token(TokenEnum.ATE)
    self.grammar_expression() 
    
    if self.check_token(TokenEnum.PASSO):
      self.expect_token(TokenEnum.PASSO)
      self.grammar_expression() 

    if self.check_token(TokenEnum.FACA):
        self.expect_token(TokenEnum.FACA)

    while not self.check_token(TokenEnum.FIMPARA):
      self.statement()

    self.expect_token(TokenEnum.FIMPARA)

  #
  # Expressoes (do menor para o maior nivel de precedencia)
  #   expressao  := ou
  #   ou         := e ("ou" e)*
  #   e          := nao ("e" nao)*
  #   nao        := "nao" nao | relacional
  #   relacional := aditiva (op_relacional aditiva)?
  #   aditiva    := mult (("+" | "-") mult)*
  #   mult       := unario (("*" | "/" | "%" | "mod") unario)*
  #   unario     := "-" unario | primario
  #
  RELACIONAIS = [
    TokenEnum.LOGIGUAL, TokenEnum.LOGDIFF,
    TokenEnum.LOGMENOR, TokenEnum.LOGMENORIGUAL,
    TokenEnum.LOGMAIOR, TokenEnum.LOGMAIORIGUAL
  ]

  def grammar_expression(self):
    self.grammar_ou()

  def grammar_ou(self):
    self.grammar_e()
    while self.check_token(TokenEnum.OU):
      self.expect_token(TokenEnum.OU)
      self.grammar_e()

  def grammar_e(self):
    self.grammar_nao()
    while self.check_token(TokenEnum.E):
      self.expect_token(TokenEnum.E)
      self.grammar_nao()

  def grammar_nao(self):
    if self.check_token(TokenEnum.NAO):
      self.expect_token(TokenEnum.NAO)
      self.grammar_nao()
    else:
      self.grammar_relacional()

  def grammar_relacional(self):
    self.grammar_aditiva()

    if self.check_token_any(self.RELACIONAIS) or self.is_equal_sign():
      self.pos += 1
      self.grammar_aditiva()
    elif self.check_token(TokenEnum.ATR):
      # '<-' nunca aparece dentro de uma expressao
      raise self.erro('"<-" serve para atribuir; para comparar use "=" ou "=="')

  def grammar_aditiva(self):
    self.grammar_mult()
    while self.check_token_any([TokenEnum.OPMAIS, TokenEnum.OPMENOS]):
      self.pos += 1
      self.grammar_mult()

  def grammar_mult(self):
    self.grammar_unario()
    while self.check_token_any([TokenEnum.OPMULTI, TokenEnum.OPDIVI, TokenEnum.OPMOD]):
      self.pos += 1
      self.grammar_unario()

  def grammar_unario(self):
    if self.check_token(TokenEnum.OPMENOS):
      self.expect_token(TokenEnum.OPMENOS)
      self.grammar_unario()
    else:
      self.grammar_primario()

  def grammar_arguments(self, abre: TokenEnum, fecha: TokenEnum):
    # Lista de expressoes separadas por virgula, possivelmente vazia
    self.expect_token(abre)
    if not self.check_token(fecha):
      self.grammar_expression()
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.grammar_expression()
    self.expect_token(fecha)

  def grammar_cauda(self):
    # Membros, chamadas e indices encadeados: a.b(1)[2].c
    while self.check_token_any([TokenEnum.PONTO, TokenEnum.PARAB, TokenEnum.COLCHETEA]):
      if self.check_token(TokenEnum.PONTO):
        self.expect_token(TokenEnum.PONTO)
        self.expect_token(TokenEnum.ID)
      elif self.check_token(TokenEnum.PARAB):
        self.grammar_arguments(TokenEnum.PARAB, TokenEnum.PARFE)
      else:
        self.expect_token(TokenEnum.COLCHETEA)
        self.grammar_expression()
        self.expect_token(TokenEnum.COLCHETEF)

  def grammar_primario(self):
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
      self.grammar_cauda()

    elif self.check_token(TokenEnum.NOVO):
      self.expect_token(TokenEnum.NOVO)
      
      if self.check_token(TokenEnum.TIPO):
          self.expect_token(TokenEnum.TIPO)
      else:
          self.expect_token(TokenEnum.ID)
          
      self.grammar_arguments(TokenEnum.PARAB, TokenEnum.PARFE)

    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.STRING):
      self.expect_token(TokenEnum.STRING)
    elif self.check_token(TokenEnum.COLCHETEA):
      self.grammar_arguments(TokenEnum.COLCHETEA, TokenEnum.COLCHETEF)
      self.grammar_cauda()

    elif self.check_token(TokenEnum.CHAVEA):
      self.expect_token(TokenEnum.CHAVEA)
      
      if not self.check_token(TokenEnum.CHAVEF):
          self.grammar_expression() # Chave
          self.expect_token(TokenEnum.COLON)   # :
          self.grammar_expression() # Valor
          
          while self.check_token(TokenEnum.COMMA):
              self.expect_token(TokenEnum.COMMA)   # ,
              self.grammar_expression() # Chave
              self.expect_token(TokenEnum.COLON)   # :
              self.grammar_expression() # Valor
              
      self.expect_token(TokenEnum.CHAVEF)

    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_expression()
      self.expect_token(TokenEnum.PARFE)
      self.grammar_cauda()
    else:
      raise self.erro(f'esperado um valor ou expressão, encontrado {self.descrever_atual()}')

  def grammar_function_declaration(self):
    self.expect_token(TokenEnum.FUNCAO)
    self.expect_token(TokenEnum.ID)     
    self.expect_token(TokenEnum.PARAB)  # (
    
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)
        
    self.expect_token(TokenEnum.PARFE)  # )
    
    while not self.check_token(TokenEnum.FIMFUNCAO):
      self.statement()
      
    self.expect_token(TokenEnum.FIMFUNCAO)

  def grammar_command_retorne(self):
    self.expect_token(TokenEnum.RETORNE)
    self.grammar_expression() # O que ele vai retornar
  
  def grammar_class_declaration(self):
    self.expect_token(TokenEnum.CLASSE)
    self.expect_token(TokenEnum.ID) # Nome da classe
    while self.check_token(TokenEnum.METODO):
      self.grammar_method_declaration()

    self.expect_token(TokenEnum.FIMCLASSE)

  def grammar_method_declaration(self):
    self.expect_token(TokenEnum.METODO)
    self.expect_token(TokenEnum.ID)     # Nome do método
    self.expect_token(TokenEnum.PARAB)  # (
    
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)
        
    self.expect_token(TokenEnum.PARFE)  # )
    
    while not self.check_token(TokenEnum.FIMFUNCAO):
      self.statement()
      
    self.expect_token(TokenEnum.FIMFUNCAO)