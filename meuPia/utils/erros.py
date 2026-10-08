from typing import Dict, List, Tuple

from .token_enum import TokenEnum


class ErroCompilacao(Exception):
  """Erro de compilacao com mensagem padronizada: 'Erro <etapa> na linha L, coluna C: <descricao>'."""
  etapa = 'de compilação'

  def __init__(self, descricao: str, linha: int = 1, coluna: int = 1):
    self.descricao = descricao
    self.linha = linha
    self.coluna = coluna
    super().__init__(str(self))

  def __str__(self) -> str:
    return f'Erro {self.etapa} na linha {self.linha}, coluna {self.coluna}: {self.descricao}'


def posicao(lexeme_pairs: List[Dict[str, str]], pos: int) -> Tuple[int, int]:
  """Retorna (linha, coluna) do token em 'pos'; no fim do arquivo usa o ultimo token, e 1:1 se nao houver tokens."""
  if not lexeme_pairs:
    return (1, 1)

  indice = min(pos, len(lexeme_pairs) - 1)
  linha, coluna = lexeme_pairs[indice]['code_index'].split(':')
  return (int(linha), int(coluna))


# Como cada token aparece para o aluno nas mensagens de erro
DESCRICAO_TOKEN = {
  TokenEnum.ATE: '"ate"',
  TokenEnum.ATR: '"<-"',
  TokenEnum.COLCHETEA: '"["',
  TokenEnum.COLCHETEF: '"]"',
  TokenEnum.CHAVEA: '"{"',
  TokenEnum.CHAVEF: '"}"',
  TokenEnum.DE: '"de"',
  TokenEnum.E: '"e"',
  TokenEnum.FUNCAO: '"funcao"',
  TokenEnum.RETORNE: '"retorne"',
  TokenEnum.FIMFUNCAO: '"fim_funcao"',
  TokenEnum.ENQUANTO: '"enquanto"',
  TokenEnum.ENTAO: '"entao"',
  TokenEnum.ESCREVA: '"escreva"',
  TokenEnum.FACA: '"faca"',
  TokenEnum.FIMPARA: '"fim_para"',
  TokenEnum.FIMSE: '"fim_se"',
  TokenEnum.FIMENQUANTO: '"fim_enquanto"',
  TokenEnum.ID: 'um nome (variável ou função)',
  TokenEnum.LEIA: '"leia"',
  TokenEnum.LOGDIFF: '"<>"',
  TokenEnum.LOGIGUAL: '"=="',
  TokenEnum.LOGMAIOR: '">"',
  TokenEnum.LOGMAIORIGUAL: '">="',
  TokenEnum.LOGMENOR: '"<"',
  TokenEnum.LOGMENORIGUAL: '"<="',
  TokenEnum.NAO: '"nao"',
  TokenEnum.NUMINT: 'um número',
  TokenEnum.OPDIVI: '"/"',
  TokenEnum.OPMAIS: '"+"',
  TokenEnum.OPMENOS: '"-"',
  TokenEnum.OPMULTI: '"*"',
  TokenEnum.OU: '"ou"',
  TokenEnum.PARA: '"para"',
  TokenEnum.PARAB: '"("',
  TokenEnum.PARFE: '")"',
  TokenEnum.PASSO: '"passo"',
  TokenEnum.SE: '"se"',
  TokenEnum.SENAO: '"senao"',
  TokenEnum.STRING: 'um texto entre aspas',
  TokenEnum.TIPO: 'um tipo (inteiro, real, cadeia, logico, lista...)',
  TokenEnum.ALGORITMO: '"algoritmo"',
  TokenEnum.VAR: '"var"',
  TokenEnum.COMMA: '","',
  TokenEnum.COLON: '":"',
  TokenEnum.PONTO: '"."',
  TokenEnum.INICIO: '"inicio"',
  TokenEnum.FIMALGORITMO: '"fim_algoritmo"',
  TokenEnum.USAR: '"usar"',
  TokenEnum.END_OF_FILE: 'o fim do arquivo',
  TokenEnum.CONTINUE: '"continue"',
  TokenEnum.INTERROMPA: '"interrompa"',
  TokenEnum.CLASSE: '"classe"',
  TokenEnum.METODO: '"metodo"',
  TokenEnum.NOVO: '"novo"',
  TokenEnum.FIMCLASSE: '"fim_classe"',
}


def descrever_token(token: TokenEnum) -> str:
  return DESCRICAO_TOKEN.get(token, f'"{token.value}"')
