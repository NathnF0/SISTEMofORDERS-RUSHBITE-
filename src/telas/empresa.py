# src/telas/empresa.py
from src.utils import GREEN, RED, YELLOW, RESET, BOLD, ler_float
from src.database import salvar_empresas

def rodar_menu_empresa(empresas):
    print("\n====== MODO EMPRESA ======")
    while True:
        print("\n1 - Login\n2 - Criar loja\n3 - Sair")
        escolha = input("Escolha: ")

        if escolha == "1":
            nome = input("Nome da empresa: ")
            senha = input("Senha: ")
            if nome in empresas and empresas[nome]["senha"] == senha:
                print(f"{GREEN}Login realizado!{RESET}")
                while True:
                    print("\n=== PAINEL DA EMPRESA ===")
                    print("1 - Adicionar produto\n2 - Ver produtos\n3 - Personalizar loja\n4 - Publicar\n5 - Sair")
                    op = input("Escolha: ")
                    if op == "1":
                        p = input("Produto: "); v = ler_float("Preço: ")
                        empresas[nome]["produtos"][p] = v
                        salvar_empresas(empresas)
                    elif op == "2":
                        for p, v in empresas[nome]["produtos"].items():
                            print(f"{p} - R${v}")
                    elif op == "3":
                        d = empresas[nome]
                        empresas[nome]["categoria"] = input(f"Categoria: ") or d["categoria"]
                        empresas[nome]["logo"] = input(f"Logo: ") or d["logo"]
                        salvar_empresas(empresas)
                    elif op == "4":
                        empresas[nome]["publicada"] = True
                        salvar_empresas(empresas)
                        print("Publicado!")
                    elif op == "5": break
            else: print("Erro de login.")
        elif escolha == "2":
            nome = input("Nome: ")
            if nome in empresas: continue
            senha = input("Senha: ")
            empresas[nome] = {"senha": senha, "produtos": {}, "publicada": False}
            salvar_empresas(empresas)
        elif escolha == "3": break