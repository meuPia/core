import argparse
import sys
import subprocess
import pkg_resources

PLUGIN_REGISTRY = {
    "maker": "git+https://github.com/meuPia/maker.git",
    "espacial": "git+https://github.com/meuPia/espacial.git",
    "ia": "git+https://github.com/meuPia/ia.git",
    "testes": "git+https://github.com/meuPia/testes.git",
}

def install_plugin(plugin_name):
    url = PLUGIN_REGISTRY.get(plugin_name)
    if not url:
        print(f"Erro: Plugin '{plugin_name}' não encontrado no registro.")
        return

    print(f"Instalando '{plugin_name}' de {url}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", url])
        print(f"Sucesso! '{plugin_name}' instalado corretamente.")
    except subprocess.CalledProcessError as e:
        print(f"Falha na instalação: {e}")
    except OSError as e:
        print(f"Erro de sistema (git/pip ausente?): {e}")

def list_plugins():
    print("Plugins disponíveis no ecossistema meuPia:")
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    
    for name, url in PLUGIN_REGISTRY.items():
        # Heurística simples: assume que o nome do pacote instalado contém o nome do plugin
        # O ideal seria ter o nome exato do pacote no registro, mas vamos verificar se 'meupia-<nome>' está instalado
        package_name = f"meupia-{name}"
        status = "[instalado]" if package_name.lower() in installed_packages else ""
        print(f" - {name:10} {status} ({url})")

def main():
    parser = argparse.ArgumentParser(description="MPGP - meuPiá Gerenciador de Pacotes")
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")

    # Comando 'instale'
    parser_install = subparsers.add_parser("instale", help="Instala uma extensão do meuPia")
    parser_install.add_argument("nome", help="Nome do plugin (ex: maker, espacial)")

    # Comando 'list'
    parser_list = subparsers.add_parser("list", help="Lista plugins disponíveis")

    args = parser.parse_args()

    if args.command == "instale":
        install_plugin(args.nome)
    elif args.command == "list":
        list_plugins()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
