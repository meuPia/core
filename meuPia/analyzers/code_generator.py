from typing import Dict, List
from ..utils.token_enum import TokenEnum

class CodeGenerator:
    def __init__(self, lexemePairs: List[Dict[str, str]]):
        self.lexeme_pairs = lexemePairs
        self.pos = 0
        self.python_code = []
        self.indent_level = 0
        self.var_types = {}

    def add_line(self, line):
        indent = "    " * self.indent_level
        self.python_code.append(f"{indent}{line}")

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
            "ia": "from meupia_ia.plugin_ia import *",       # Caminho explícito para o novo padrão
            "maker": "from meupia_maker.plugin_iot import *", # (Ajuste se necessário, ou mantenha genérico)
            "espacial": "from meupia_espacial.plugin_ksp import *"
        }

        for plugin in self.imports:
            # Tenta pegar do mapa, se não existir, usa o padrão 'meupia_{plugin}'
            import_stmt = PLUGIN_IMPORT_MAP.get(plugin, f"from meupia_{plugin} import *")
            
            self.add_line(f"try:")
            self.indent_level += 1
            self.add_line(f"{import_stmt}")
            self.indent_level -= 1
            self.add_line(f"except ImportError:")
            self.indent_level += 1
            # Usando 'mpgp instale' conforme nomenclatura do mpgp.py
            self.add_line(f"print(\"Erro: O plugin '{plugin}' não está instalado. Execute: mpgp instale {plugin}\")")
            self.add_line(f"sys.exit(1)")
            self.indent_level -= 1
            
        self.add_line("")
        
        if self.check_token(TokenEnum.VAR):
            self.gen_variables()

        if self.check_token(TokenEnum.INICIO):
            self.advance() # INICIO
        
        self.add_line("def main():")
        self.indent_level += 1
        
        while not self.check_token(TokenEnum.FIMALGORITMO) and not self.check_token(TokenEnum.END_OF_FILE):
            self.gen_statement()

        self.indent_level -= 1
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
            
            val_inicial = "0" if tipo == "inteiro" else "''"
            for var_name in ids:
                self.var_types[var_name] = tipo
                self.add_line(f"{var_name} = {val_inicial}")

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

        else:
            self.advance() 

    def gen_enquanto(self):
        self.advance() # ENQUANTO
        cond = self.gen_expression()
        
        if self.check_token(TokenEnum.FACA):
            self.advance()

        self.add_line(f"while {cond}:")
        self.indent_level += 1
        
        while not self.check_token(TokenEnum.FIMENQUANTO):
            self.gen_statement()

        self.indent_level -= 1
        self.advance() # FIMENQUANTO

    def gen_assignment_or_call(self):
        lexeme = self.current_lexeme()
        self.advance()

        while self.check_token(TokenEnum.PONTO):
            lexeme += "."
            self.advance() # PONTO
            lexeme += self.current_lexeme()
            self.advance() # ID
        
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
        expr = self.gen_expression()
        # O python print adiciona newline por padrao, portugol as vezes nao.
        # Mas vamos manter simples: print()
        self.add_line(f"print({expr})")
        self.advance() # )

    def gen_leia(self):
        self.advance() # LEIA
        self.advance() # (
        var_name = self.current_lexeme()
        self.advance() # ID
        
        is_int = self.var_types.get(var_name) == 'inteiro'
        
        if is_int:
            self.add_line(f"{var_name} = int(input())") 
        else:
            self.add_line(f"{var_name} = input()")

        self.advance() # )

    def gen_se(self):
        self.advance() # SE
        cond = self.gen_expression()
        self.advance() # ENTAO
        
        self.add_line(f"if {cond}:")
        self.indent_level += 1
        
        # Processa bloco
        while not (self.check_token(TokenEnum.SENAO) or self.check_token(TokenEnum.FIMSE) or self.check_token(TokenEnum.FIMALGORITMO)):
            self.gen_statement()
        
        self.indent_level -= 1
        
        if self.check_token(TokenEnum.SENAO):
            self.advance() # SENAO
            self.add_line("else:")
            self.indent_level += 1
            while not (self.check_token(TokenEnum.FIMSE) or self.check_token(TokenEnum.FIMALGORITMO)):
                self.gen_statement()
            self.indent_level -= 1
            
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
            
        self.add_line(f"for {var_controle} in range({inicio_val}, {fim_val} + 1, {passo_val}):") # Range inclusivo
        
        self.indent_level += 1
        while not self.check_token(TokenEnum.FIMPARA):
            self.gen_statement()
        self.indent_level -= 1
        self.advance() # FIMPARA
    
    def gen_expression(self):
        expr_parts = []
        paren_balance = 0
        last_token_type = None
        
        while True:
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
            if t == TokenEnum.LOGIGUAL.name: l = "=="
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
            elif t == TokenEnum.ATR.name: break 
            
            # Valid tokens
            valid_expr_tokens = [
                TokenEnum.ID.name, TokenEnum.NUMINT.name, TokenEnum.STRING.name, 
                TokenEnum.OPMAIS.name, TokenEnum.OPMENOS.name, TokenEnum.OPMULTI.name, TokenEnum.OPDIVI.name,
                TokenEnum.PARAB.name, TokenEnum.PARFE.name,
                TokenEnum.COLCHETEA.name, TokenEnum.COLCHETEF.name, TokenEnum.COMMA.name, 
                TokenEnum.LOGIGUAL.name, TokenEnum.LOGDIFF.name, TokenEnum.LOGMENOR.name, TokenEnum.LOGMAIOR.name,
                TokenEnum.LOGMENORIGUAL.name, TokenEnum.LOGMAIORIGUAL.name,
                TokenEnum.E.name, TokenEnum.OU.name, TokenEnum.NAO.name,
                TokenEnum.PONTO.name, TokenEnum.CHAVEA.name, TokenEnum.CHAVEF.name, TokenEnum.COLON.name
            ]
            
            # If strictly not in valid tokens, break (safety)
            if t not in valid_expr_tokens and paren_balance == 0:
                break

            # Adjacency check for implicit break (e.g. "20 ia_treinar")
            operands_end = [TokenEnum.ID.name, TokenEnum.NUMINT.name, TokenEnum.STRING.name, TokenEnum.PARFE.name, TokenEnum.COLCHETEF.name, TokenEnum.CHAVEF.name] # Adicionado CHAVEF aqui por segurança
            operands_start = [TokenEnum.ID.name, TokenEnum.NUMINT.name, TokenEnum.STRING.name, TokenEnum.PARAB.name, TokenEnum.NAO.name, TokenEnum.COLCHETEA.name, TokenEnum.CHAVEA.name] # Adicionado CHAVEA aqui
            
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