# main.py
from src.database import carregar_empresas
from src.telas.cliente import rodar_menu_cliente
from src.telas.empresa import rodar_menu_empresa

def main():
    empresas = carregar_empresas()
    while True:
        print("\n=== RUSHBITE ===")
        print("1 - Cliente\n2 - Empresa\n3 - Sair")
        opcao = input("Opção: ")
        if opcao == "1": rodar_menu_cliente(empresas)
        elif opcao == "2": rodar_menu_empresa(empresas)
        elif opcao == "3": break
        else: print("Opção inválida.")

if __name__ == "__main__":
    main()