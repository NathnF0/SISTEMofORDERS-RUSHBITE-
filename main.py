from src.utils import exibir_cabecalho, GREEN, RED, RESET, pausar
from src.database import carregar_dados, salvar_dados, carregar_clientes, salvar_clientes
from src.telas.empresa import menu_empresa # <-- ESTE IMPORT DEVE FUNCIONAR AGORA
from src.telas.cliente import menu_cliente

def main():
    while True:
        exibir_cabecalho("RushBite")
        print("1. 🛍️  Área do Cliente")
        print("2. 🏢 Área da Empresa")
        print("0. ❌ Sair")
        
        op = input("\nEscolha: ")
        if op == "1": portal_cliente()
        elif op == "2": portal_empresa()
        elif op == "0": break

def portal_cliente():
    exibir_cabecalho("Portal Cliente")
    print("1. Login | 2. Cadastro | 0. Voltar")
    op = input("Opção: ")
    clis = carregar_clientes()
    if op == "1":
        u = input("User: "); s = input("Senha: ")
        if u in clis and clis[u]['senha'] == s: menu_cliente(u)
        else: print(f"{RED}Erro login!{RESET}"); pausar()
    elif op == "2":
        u = input("User: "); s = input("Senha: "); t = input("Tel: ")
        clis[u] = {"senha": s, "endereco": "", "telefone": t}; salvar_clientes(clis); print("Cadastrado!")
        pausar()

def portal_empresa():
    exibir_cabecalho("Portal Empresa")
    print("1. Login | 2. Cadastro | 0. Voltar")
    op = input("Opção: ")
    dados = carregar_dados()
    if op == "1":
        n = input("Loja: "); s = input("Senha: ")
        if n in dados and dados[n]['senha'] == s: menu_empresa(n)
        else: print(f"{RED}Erro login!{RESET}"); pausar()
    elif op == "2":
        n = input("Nome Loja: "); c = input("Categoria: "); s = input("Senha: ")
        dados[n] = {"categoria": c, "senha": s, "produtos": {}, "taxa_entrega": 0, "logo": "🍔"}
        salvar_dados(dados); print("Cadastrada!"); pausar()

if __name__ == "__main__":
    main()