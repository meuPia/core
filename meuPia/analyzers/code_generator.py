from typing import Dict, List
from ..utils.builtins import CONSTANTES_BUILTIN, FUNCOES_BUILTIN, METODOS, TIPOS_CONTEXTUAIS
from ..utils.token_enum import TokenEnum
from .syntax_analyzer import Parser

class CodeGenerator:
    def __init__(self, lexemePairs: List[Dict[str, str]]):
        self.lexeme_pairs = lexemePairs
        self.pos = 0
        self.python_code = []
        self.indent_level = 0
        self.var_types = {}
        self.local_types = {} # tipos das variaveis locais do def atual (funcao, metodo ou main)
        self.user_names = self.collect_user_names()

    def add_line(self, line):
        indent = "    " * self.indent_level
        self.python_code.append(f"{indent}{line}")

    def collect_user_names(self) -> set:
        # Nomes declarados pelo usuario (var, funcao, classe, parametros) tem prioridade sobre builtins
        names = set()
        pairs = self.lexeme_pairs
        in_var_block = False
        in_body = False # dentro de funcao, metodo ou inicio, 'var' e declaracao local
        i = 0
        while i < len(pairs):
            token = pairs[i]['token']
            if token == TokenEnum.VAR.name and in_body:
                linhas, i = Parser.ler_declaracao_local(pairs, i)
                for linha in linhas:
                    names.update(nome for nome, _ in linha['nomes'])
                continue
            elif token == TokenEnum.VAR.name:
                in_var_block = True
            elif token == TokenEnum.FIMFUNCAO.name:
                in_body = False
            elif token in (TokenEnum.FUNCAO.name, TokenEnum.CLASSE.name, TokenEnum.METODO.name, TokenEnum.INICIO.name):
                in_var_block = False
                in_body = token != TokenEnum.CLASSE.name
                if token in (TokenEnum.FUNCAO.name, TokenEnum.CLASSE.name) and i + 1 < len(pairs):
                    names.add(pairs[i + 1]['lexeme'])
                if token in (TokenEnum.FUNCAO.name, TokenEnum.METODO.name):
                    # Parametros: IDs entre '(' e ')' logo apos o nome
                    j = i + 3
                    while j < len(pairs) and pairs[j]['token'] != TokenEnum.PARFE.name:
                        if pairs[j]['token'] == TokenEnum.ID.name:
                            names.add(pairs[j]['lexeme'])
                        j += 1
            elif in_var_block and token == TokenEnum.ID.name:
                is_type = i > 0 and pairs[i - 1]['token'] == TokenEnum.COLON.name
                if not is_type:
                    names.add(pairs[i]['lexeme'])
            i += 1
        return names

    def map_identifier(self, name: str, after_dot: bool) -> str:
        if after_dot:
            return METODOS.get(name, name)
        if name in self.user_names:
            return name
        if name in FUNCOES_BUILTIN:
            return FUNCOES_BUILTIN[name]
        return CONSTANTES_BUILTIN.get(name, name)

    def begin_block(self) -> int:
        # Marca o inicio do corpo de um bloco ja indentado
        return len(self.python_code)

    def end_block(self, start: int):
        # Bloco sem nenhuma linha de corpo vira 'pass' para gerar Python valido
        if len(self.python_code) == start:
            self.add_line("pass")
        self.indent_level -= 1

    def current_token(self) -> str:
        if self.pos < len(self.lexeme_pairs):
            return self.lexeme_pairs[self.pos]['token']
        return TokenEnum.END_OF_FILE.name
    
    def current_lexeme(self) -> str:
        if self.pos < len(self.lexeme_pairs):
            return self.lexeme_pairs[self.pos]['lexeme']
        return ''

    def advance(self):
        self.pos += 1

    def check_token(self, expected: TokenEnum) -> bool:
        return self.current_token() == expected.name

    def generate(self):
        # Cabeçalho com Wrappers do meuPiá
        self.add_line("# -*- coding: utf-8 -*-")
        self.add_line("import sys")
        self.add_line("import math")
        self.add_line("import heapq")
        self.add_line("class _S(str):")
        self.add_line("    def __add__(self, other):")
        self.add_line("        if other is True: other = 'verdadeiro'")
        self.add_line("        elif other is False: other = 'falso'")
        self.add_line("        return _S(str(self) + str(other))")
        self.add_line("    def __radd__(self, other):")
        self.add_line("        if other is True: other = 'verdadeiro'")
        self.add_line("        elif other is False: other = 'falso'")
        self.add_line("        return _S(str(other) + str(self))")
        self.add_line("def _texto(valor):")
        self.add_line("    if valor is True: return 'verdadeiro'")
        self.add_line("    if valor is False: return 'falso'")
        self.add_line("    return str(valor)")
        self.add_line("def _escreva(*valores):")
        self.add_line("    print(''.join(_texto(v) for v in valores))")
        self.add_line("def _faixa(inicio, fim, passo):")
        self.add_line("    # Intervalo do laco 'para': inclui o fim nos dois sentidos")
        self.add_line("    if passo == 0: raise ValueError('passo do laço para não pode ser zero')")
        self.add_line("    return range(inicio, fim + 1, passo) if passo > 0 else range(inicio, fim - 1, passo)")
        self.add_line("from collections import deque")
        self.add_line("class FilaPrioridade:")
        self.add_line("    def __init__(self):")
        self.add_line("        self.heap = []")
        self.add_line("    def inserir(self, item):")
        self.add_line("        heapq.heappush(self.heap, item)")
        self.add_line("    def remover(self):")
        self.add_line("        return heapq.heappop(self.heap)")
        self.add_line("    def espiar(self):")
        self.add_line("        return self.heap[0] if self.heap else None")
        self.add_line("    def len(self):")
        self.add_line("        return len(self.heap)")
        self.add_line("    def __len__(self):")
        self.add_line("        return len(self.heap)")
        self.add_line("")

        self.imports = []

        # Pular algoritmo e nome se existirem
        if self.check_token(TokenEnum.ALGORITMO):
            self.advance() # ALGORITMO
            self.advance() # "NOME"
        
        # Processar imports
        while self.check_token(TokenEnum.USAR):
            self.advance() # USAR
            plugin_name = self.current_lexeme().strip('"')
            self.imports.append(plugin_name)
            self.advance() # "NOME_DO_PLUGIN"
        
        # Mapeamento: "comando usar" -> "linha de import python"
        PLUGIN_IMPORT_MAP = {
            "ia": "from meupia_ia.plugin_ia import *",
            "maker": "from meupia_maker.plugin_iot import *",
            "espacial": "from meupia_espacial.plugin_ksp import *",
            "testes": "from meupia_testes.plugin_testes import *",
            "grid": "from meupia_grid.plugin_grid import *"
        }

        for plugin in self.imports:
            if plugin in PLUGIN_IMPORT_MAP:
                import_stmt = PLUGIN_IMPORT_MAP[plugin]
                
                self.add_line(f"try:")
                self.indent_level += 1
                self.add_line(f"{import_stmt}")
                self.indent_level -= 1
                self.add_line(f"except ImportError:")
                self.indent_level += 1
                self.add_line(f"print(\"Erro: O plugin '{plugin}' não está instalado. Execute: mpgp instale {plugin}\")")
                self.add_line(f"sys.exit(1)")
                self.indent_level -= 1
            
            else:
                self.add_line(f"try:")
                self.indent_level += 1
                self.add_line(f"from {plugin} import *")
                self.indent_level -= 1
                self.add_line(f"except ImportError:")
                self.indent_level += 1
                self.add_line(f"print(\"Erro: O arquivo local '{plugin}' não foi encontrado.\")")
                self.add_line(f"sys.exit(1)")
                self.indent_level -= 1

        self.add_line("")
        
        while self.check_token(TokenEnum.VAR) or self.check_token(TokenEnum.FUNCAO) or self.check_token(TokenEnum.CLASSE):
            if self.check_token(TokenEnum.VAR):
                self.gen_variables()
            elif self.check_token(TokenEnum.FUNCAO):
                self.gen_function_definition()
            elif self.check_token(TokenEnum.CLASSE):
                self.gen_class_definition()

        if self.check_token(TokenEnum.INICIO):
            self.advance() # INICIO
        
        self.add_line("def main():")
        self.local_types = {}
        self.indent_level += 1
        if self.var_types:
            self.add_line(f"global {', '.join(self.var_types.keys())}")
        start = self.begin_block()
        
        while not self.check_token(TokenEnum.FIMALGORITMO) and not self.check_token(TokenEnum.END_OF_FILE):
            self.gen_statement()

        self.end_block(start)
        self.add_line("")
        self.add_line("if __name__ == '__main__':")
        self.add_line("    main()")
        
        return "\n".join(self.python_code)

    def gen_variables(self):
        self.advance() # VAR
        while self.check_token(TokenEnum.ID):
            ids = []
            ids.append(self.current_lexeme())
            self.advance()
            
            while self.check_token(TokenEnum.COMMA):
                self.advance() # ,
                ids.append(self.current_lexeme())
                self.advance() # ID
                
            self.advance() # :
            tipo = self.current_lexeme()
            self.advance() # TIPO
            
            for var_name in ids:
                self.var_types[var_name] = tipo
                self.add_line(f"{var_name} = {self.valor_inicial(tipo)}")

    def valor_inicial(self, tipo: str) -> str:
        # Valor com que toda variavel declarada (global ou local) comeca
        if tipo == "inteiro":
            return "0"
        elif tipo == "real" or tipo == "float":
            return "0.0"
        elif tipo == "dicionario": 
            return "{}"
        elif tipo == "logico":
            return "False"
        elif tipo == "lista":
            return "[]"
        elif tipo.lower() == "filaprioridade": 
            return "FilaPrioridade()"
        return "_S('')"

    def gen_statement(self):
        if self.check_token(TokenEnum.ID):
            self.gen_assignment_or_call()

        elif self.check_token(TokenEnum.ESCREVA):
            self.gen_escreva()
        
        elif self.check_token(TokenEnum.LEIA):
            self.gen_leia()

        elif self.check_token(TokenEnum.SE):
            self.gen_se()

        elif self.check_token(TokenEnum.ENQUANTO):
            self.gen_enquanto()

        elif self.check_token(TokenEnum.PARA):
            self.gen_para()

        elif self.check_token(TokenEnum.RETORNE):
            self.gen_retorne()

        elif self.check_token(TokenEnum.CONTINUE):
            self.advance()
            self.add_line("continue")

        elif self.check_token(TokenEnum.INTERROMPA):
            self.advance()
            self.add_line("break")

        elif self.check_token(TokenEnum.VAR):
            self.gen_local_declaration()

        else:
            self.advance()

    def gen_local_declaration(self):
        # Locais viram atribuicoes comuns: o Python ja as trata como locais do def (nao estao no 'global')
        linhas, fim = Parser.ler_declaracao_local(self.lexeme_pairs, self.pos)
        for linha in linhas:
            if linha['expressao']:
                self.pos, fim_expr = linha['expressao']
                valor = self.gen_expression(fim=fim_expr)
            else:
                valor = self.valor_inicial(linha['tipo'])
            for nome, _ in linha['nomes']:
                self.local_types[nome] = linha['tipo']
                self.add_line(f"{nome} = {valor}")
        self.pos = fim

    def gen_enquanto(self):
        self.advance() # ENQUANTO
        cond = self.gen_expression()
        
        if self.check_token(TokenEnum.FACA):
            self.advance()

        self.add_line(f"while {cond}:")
        self.indent_level += 1
        start = self.begin_block()
        
        while not self.check_token(TokenEnum.FIMENQUANTO):
            self.gen_statement()

        self.end_block(start)
        self.advance() # FIMENQUANTO

    def gen_assignment_or_call(self):
        lexeme = self.current_lexeme()
        self.advance()

        while self.check_token(TokenEnum.PONTO):
            lexeme += "."
            self.advance() # PONTO

            lexeme += self.map_identifier(self.current_lexeme(), after_dot=True)

            self.advance() # ID
        
        while self.check_token(TokenEnum.COLCHETEA):
            lexeme += "["
            self.advance() # Consome '['
            lexeme += self.gen_expression() # Gera o índice (ex: 0 ou variável)
            lexeme += "]"
            self.advance() # Consome ']' (o gen_expression para antes dele)
        
        if self.check_token(TokenEnum.ATR):
            self.advance() # <-
            expr = self.gen_expression()
            self.add_line(f"{lexeme} = {expr}")
            
        elif self.check_token(TokenEnum.PARAB):
            self.advance() # (
            args = []
            if not self.check_token(TokenEnum.PARFE):
                args.append(self.gen_expression())
                while self.check_token(TokenEnum.COMMA):
                    self.advance()
                    args.append(self.gen_expression())
            self.advance() # )
            self.add_line(f"{lexeme}({', '.join(args)})")

    def gen_escreva(self):
        self.advance() # ESCREVA
        self.advance() # (
        args = []
        if not self.check_token(TokenEnum.PARFE):
            args.append(self.gen_expression())
            while self.check_token(TokenEnum.COMMA):
                self.advance() # ,
                args.append(self.gen_expression())
        # Concatena sem separador (estilo VisuAlg) e mostra logicos como verdadeiro/falso
        self.add_line(f"_escreva({', '.join(args)})")
        self.advance() # )

    def gen_leia(self):
        self.advance() # LEIA
        self.advance() # (
        var_name = self.current_lexeme()
        self.advance() # ID
        
        tipo_var = self.local_types.get(var_name, self.var_types.get(var_name))
        
        if tipo_var == 'inteiro':
            self.add_line(f"{var_name} = int(input())") 
        elif tipo_var in ['real', 'float']:
            self.add_line(f"{var_name} = float(input())") 
        elif tipo_var == 'logico':
            self.add_line(f"{var_name} = input().strip().lower() == 'verdadeiro'")
        else:
            self.add_line(f"{var_name} = _S(input())")

        self.advance() # )

    def gen_se(self):
        self.advance() # SE
        cond = self.gen_expression()
        self.advance() # ENTAO
        
        self.add_line(f"if {cond}:")
        self.indent_level += 1
        start = self.begin_block()
        
        # Processa bloco
        while not (self.check_token(TokenEnum.SENAO) or self.check_token(TokenEnum.FIMSE) or self.check_token(TokenEnum.FIMALGORITMO)):
            self.gen_statement()
        
        self.end_block(start)
        
        if self.check_token(TokenEnum.SENAO):
            self.advance() # SENAO
            self.add_line("else:")
            self.indent_level += 1
            start = self.begin_block()
            while not (self.check_token(TokenEnum.FIMSE) or self.check_token(TokenEnum.FIMALGORITMO)):
                self.gen_statement()
            self.end_block(start)
            
        self.advance() # FIMSE

    def gen_para(self):
        self.advance() # PARA
        var_controle = self.current_lexeme()
        self.advance() # ID
        
        self.advance() # DE
        inicio_val = self.gen_expression() # A expressão pode ser complexa? gen_expression lida com tudo até achar token invalido (ate)
        # Note: gen_expression para em 'ate' se não tiver em valid_tokens. 'ate' nao esta na lista. OK.
        
        self.advance() # ATE
        fim_val = self.gen_expression()
        
        passo_val = "1"
        if self.check_token(TokenEnum.PASSO):
            self.advance()
            passo_val = self.gen_expression() # Allow expression for step too
            
        if self.check_token(TokenEnum.FACA):
            self.advance()
            
        self.add_line(f"for {var_controle} in _faixa({inicio_val}, {fim_val}, {passo_val}):") # Range inclusivo
        
        self.indent_level += 1
        start = self.begin_block()
        while not self.check_token(TokenEnum.FIMPARA):
            self.gen_statement()
        self.end_block(start)
        self.advance() # FIMPARA
    
    def gen_expression(self, fim=None):
        expr_parts = []
        paren_balance = 0
        last_token_type = None
        
        while True:
            if fim is not None and self.pos >= fim:
                break # Limite da expressao ja conhecido pela gramatica
            t = self.current_token()
            l = self.current_lexeme()
            
            # Break conditions based on balance
            if t == TokenEnum.PARFE.name:
                if paren_balance == 0:
                    break
                else:
                    paren_balance -= 1
            elif t == TokenEnum.COMMA.name:
                if paren_balance == 0:
                    break
            elif t == TokenEnum.PARAB.name:
                paren_balance += 1
            elif t == TokenEnum.COLCHETEA.name:
                paren_balance += 1 
            elif t == TokenEnum.COLCHETEF.name:
                if paren_balance == 0:
                    break
                else:
                    paren_balance -= 1
            elif t == TokenEnum.CHAVEA.name:
                paren_balance += 1 
            elif t == TokenEnum.CHAVEF.name:
                if paren_balance == 0:
                    break
                else:
                    paren_balance -= 1
            
            # Stop on keywords or unrelated tokens
            if t in [TokenEnum.FIMALGORITMO.name, TokenEnum.FIMSE.name, TokenEnum.FIMPARA.name, TokenEnum.FIMENQUANTO.name, TokenEnum.ENTAO.name]:
                break
            
            # Lexeme mapping
            if t == TokenEnum.ID.name and last_token_type == TokenEnum.NOVO.name and l == "lista":
                l = "list"
            elif t == TokenEnum.ID.name:
                l = self.map_identifier(l, after_dot=(last_token_type == TokenEnum.PONTO.name))
            elif t == TokenEnum.TIPO.name:
                if l.lower() == "filaprioridade": l = "FilaPrioridade"
                elif l == "dicionario": l = "dict"
            elif t == TokenEnum.LOGIGUAL.name: l = "=="
            elif t == TokenEnum.OPMOD.name: l = "%"
            elif t == TokenEnum.LOGDIFF.name: l = "!="
            elif t == TokenEnum.LOGMENOR.name: l = "<"
            elif t == TokenEnum.LOGMAIOR.name: l = ">"
            elif t == TokenEnum.LOGMENORIGUAL.name: l = "<="
            elif t == TokenEnum.LOGMAIORIGUAL.name: l = ">="
            elif t == TokenEnum.E.name: l = " and "
            elif t == TokenEnum.OU.name: l = " or "
            elif t == TokenEnum.NAO.name: l = " not "
            elif t == TokenEnum.COLCHETEA.name: l = "["
            elif t == TokenEnum.COLCHETEF.name: l = "]"
            elif t == TokenEnum.COMMA.name: l = ", "
            elif t == TokenEnum.PONTO.name: l = "."
            elif t == TokenEnum.CHAVEA.name: l = "{"
            elif t == TokenEnum.CHAVEF.name: l = "}"
            elif t == TokenEnum.COLON.name: l = ": "
            elif t == TokenEnum.ATR.name:
                if l != '=': break # '<-' nunca faz parte de uma expressao
                l = "=="
                t = TokenEnum.LOGIGUAL.name
            elif t == TokenEnum.NOVO.name: l = "" 
            elif t == TokenEnum.STRING.name: l = f"_S({l})"
            
            # Valid tokens
            valid_expr_tokens = [
                TokenEnum.ID.name, TokenEnum.NUMINT.name, TokenEnum.STRING.name, TokenEnum.TIPO.name,
                TokenEnum.OPMAIS.name, TokenEnum.OPMENOS.name, TokenEnum.OPMULTI.name, TokenEnum.OPDIVI.name, TokenEnum.OPMOD.name,
                TokenEnum.PARAB.name, TokenEnum.PARFE.name,
                TokenEnum.COLCHETEA.name, TokenEnum.COLCHETEF.name, TokenEnum.COMMA.name, 
                TokenEnum.LOGIGUAL.name, TokenEnum.LOGDIFF.name, TokenEnum.LOGMENOR.name, TokenEnum.LOGMAIOR.name,
                TokenEnum.LOGMENORIGUAL.name, TokenEnum.LOGMAIORIGUAL.name,
                TokenEnum.E.name, TokenEnum.OU.name, TokenEnum.NAO.name,
                TokenEnum.PONTO.name, TokenEnum.CHAVEA.name, TokenEnum.CHAVEF.name, TokenEnum.COLON.name,
                TokenEnum.NOVO.name
            ]
            
            # If strictly not in valid tokens, break (safety)
            if t not in valid_expr_tokens and paren_balance == 0:
                break

            # Adjacency check for implicit break (e.g. "20 ia_treinar")
            operands_end = [TokenEnum.ID.name, TokenEnum.NUMINT.name, TokenEnum.STRING.name, TokenEnum.PARFE.name, TokenEnum.COLCHETEF.name, TokenEnum.CHAVEF.name] 
            operands_start = [TokenEnum.ID.name, TokenEnum.NUMINT.name, TokenEnum.STRING.name, TokenEnum.TIPO.name, TokenEnum.PARAB.name, TokenEnum.NAO.name, TokenEnum.COLCHETEA.name, TokenEnum.CHAVEA.name, TokenEnum.NOVO.name]
            
            if len(expr_parts) > 0:
                pass

            if last_token_type in operands_end and t in operands_start:
                # Special case: Function call ID + ( is allowed.
                if (last_token_type == TokenEnum.ID.name and t == TokenEnum.PARAB.name) or \
                    (last_token_type == TokenEnum.ID.name and t == TokenEnum.COLCHETEA.name) or \
                    (last_token_type == TokenEnum.COLCHETEF.name and t == TokenEnum.COLCHETEA.name):
                    pass
                else:
                    # Break if operand follows operand (missing operator)
                    if paren_balance == 0:
                        break

            expr_parts.append(l)
            last_token_type = t
            self.advance()
            
        return "".join(expr_parts)

    def gen_function_definition(self):
        self.local_types = {}
        self.advance() # FUNCAO
        func_name = self.current_lexeme()
        self.advance() # ID
        
        self.advance() # (
        
        params = []
        if self.check_token(TokenEnum.ID):
            params.append(self.current_lexeme())
            self.advance() # ID
            while self.check_token(TokenEnum.COMMA):
                self.advance() # ,
                params.append(self.current_lexeme())
                self.advance() # ID
                
        self.advance() # )
        
        self.add_line(f"def {func_name}({', '.join(params)}):")
        self.indent_level += 1 
        if self.var_types:
            global_vars = [v for v in self.var_types.keys() if v not in params]
            if global_vars:
                self.add_line(f"global {', '.join(global_vars)}")
        start = self.begin_block()
        
        while not self.check_token(TokenEnum.FIMFUNCAO):
            self.gen_statement()
            
        self.end_block(start)
        self.advance() # FIMFUNCAO
        self.add_line("") # Pula uma linha para deixar o Python bonito e legível

    def gen_retorne(self):
        self.advance() # RETORNE
        expr = self.gen_expression()
        self.add_line(f"return {expr}")

    def gen_class_definition(self):
        self.advance() # CLASSE
        class_name = self.current_lexeme()
        self.advance() # ID
        
        self.add_line(f"class {class_name}:")
        self.indent_level += 1
        
        has_methods = False
        while self.check_token(TokenEnum.METODO):
            has_methods = True
            self.gen_method_definition()
            
        if not has_methods:
            self.add_line("pass")
            
        self.indent_level -= 1
        self.advance() # FIMCLASSE
        self.add_line("")

    def gen_method_definition(self):
        self.local_types = {}
        self.advance() # METODO
        func_name = self.current_lexeme()
        self.advance() # ID
        
        self.advance() # (
        
        # MÁGICA PEDAGÓGICA: Injeta o 'self' silenciosamente no Python
        params = ["self"]
        if self.check_token(TokenEnum.ID):
            params.append(self.current_lexeme())
            self.advance() # ID
            while self.check_token(TokenEnum.COMMA):
                self.advance() # ,
                params.append(self.current_lexeme())
                self.advance() # ID
                
        self.advance() # )
        
        # Mapeia 'construtor' para o padrão Python
        if func_name == "construtor":
            func_name = "__init__"
            
        self.add_line(f"def {func_name}({', '.join(params)}):")
        self.indent_level += 1 
        if self.var_types:
            global_vars = [v for v in self.var_types.keys() if v not in params]
            if global_vars:
                self.add_line(f"global {', '.join(global_vars)}")
        start = self.begin_block()
        
        while not self.check_token(TokenEnum.FIMFUNCAO):
            self.gen_statement()
            
        self.end_block(start)
        self.advance() # FIMFUNCAO
        self.add_line("")