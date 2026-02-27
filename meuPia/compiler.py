import os
import sys # <-- Adicione esta linha no topo
from .analyzers import lexical_analyzer
from .analyzers import syntax_analyzer
from .analyzers import semantic_analyzer
from .analyzers.code_generator import CodeGenerator

def main(input_file: str = None, output_path: str = None):
    try:
        if input_file is None:
            if len(sys.argv) > 1:
                input_file = sys.argv[1]
            else:
                print("Erro: Nenhum arquivo informado.")
                print("Uso correto: meupia <arquivo.por>")
                return # Sai do programa graciosamente
        
        full_path = input_file
        filename_only = os.path.basename(full_path)

        print(f'Compilando {full_path}...')
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Arquivo {full_path} não encontrado.")

        # Lexer
        # Pass output path to compile if needed, or handle it inside lexical_analyzer 
        # For now we just pass filename_only as before, but lexical_analyzer needs refactor too.
        # We will assume lexical_analyzer.compile will be updated to accept output_dir.
        lexeme_pairs = lexical_analyzer.compile(full_path, output_path=output_path)

        # Parser
        parser = syntax_analyzer.Parser(lexeme_pairs)
        parser.parse()
        print('✅ Syntax is valid.')

        # Semantic Analyzer
        semantic = semantic_analyzer.SemanticAnalyzer(lexeme_pairs)
        semantic.validate()
        print('✅ Semantic is valid.')

        # Code Generator (NEW)
        print('Generating Python code...')
        generator = CodeGenerator(lexeme_pairs)
        python_code = generator.generate()
        
        # Save Output
        if output_path:
            os.makedirs(output_path, exist_ok=True)
            out_dir = output_path
        else:
            out_dir = 'output'
            os.makedirs(out_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(full_path))[0]
        final_output_path = os.path.join(out_dir, f'{base_name}.py')
        
        with open(final_output_path, 'w', encoding='utf-8') as f:
            f.write(python_code)
            
        print(f'✅ Code generated successfully at {final_output_path}')
        print('[COMPILED SUCCESSFULLY]')

    except Exception as e:
        print(f'[COMPILATION ERROR]:\n\t{e}')


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()