import sys
from cli.interface import main as cli_main
from web.server import app as web_app

def main():
    if len(sys.argv) > 1:
        cli_main()
    else:
        print("Selecione o modo:")
        print("1. Interface CLI")
        print("2. Servidor Web")
        choice = input("Opção: ").strip()
        
        if choice == '1':
            cli_main()
        elif choice == '2':
            web_app.run(host='0.0.0.0', port=5000)
        else:
            print("Opção Inválida")

if __name__ == '__main__':
    main()