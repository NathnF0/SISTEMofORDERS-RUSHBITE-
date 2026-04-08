import os
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar
from src.database import carregar_dados, carregar_clientes, salvar_clientes
from src.telas.cliente import menu_cliente
from src.telas.empresa import menu_empresa

def login():
    while True:
        exibir_cabecalho("BEM-VINDO AO RUSHBITE")
        print(f"{CYAN}[1]{RESET} Entrar como Cliente")
        print(f"{GREEN}[2]{RESET} Entrar como Empresa")
        print(f"{YELLOW}[3]{RESET} Criar Nova Conta")
        print("-" * 30)
        print(f"{RED}[0]{RESET} Sair do Programa")
        
        op = input(f"\n{BOLD}Escolha sua jornada: {RESET}")

        if op == "1":
            clis = carregar_clientes()
            user = input("Usuário: ").strip()
            senha = input("Senha: ")
            if user in clis and clis[user]['senha'] == senha:
                menu_cliente(user) # Chama a v0.2.6 do cliente
            else:
                print(f"{RED}Login inválido!{RESET}"); pausar()

        elif op == "2":
            dados = carregar_dados()
            loja = input("Nome da Loja: ").strip()
            senha = input("Senha: ")
            if loja in dados and dados[loja]['senha'] == senha:
                menu_empresa(loja) # Chama a v0.2.6 da empresa
            else:
                print(f"{RED}Empresa não encontrada ou senha incorreta!{RESET}"); pausar()

        elif op == "3":
            criar_conta()

        elif op == "0":
            print(f"\n{YELLOW}Obrigado por usar o RushBite! Até logo. 🍔{RESET}")
            break

def criar_conta():
    exibir_cabecalho("CRIAR NOVA CONTA")
    tipo = input("Você é [1] Cliente ou [2] Empresa? ")
    
    if tipo == "1":
        clis = carregar_clientes()
        user = input("Escolha um usuário: ").strip()
        if user in clis:
            print(f"{RED}Usuário já existe!{RESET}"); pausar()
        else:
            senha = input("Crie uma senha: ")
            clis[user] = {"senha": senha, "endereco": "", "telefone": ""}
            salvar_clientes(clis)
            print(f"{GREEN}✓ Conta cliente criada com sucesso!{RESET}"); pausar()
            
    elif tipo == "2":
        from src.database import salvar_dados
        dados = carregar_dados()
        loja = input("Nome da sua Loja: ").strip()
        if loja in dados:
            print(f"{RED}Essa loja já está cadastrada!{RESET}"); pausar()
        else:
            senha = input("Crie uma senha: ")
            dados[loja] = {
                "senha": senha, 
                "produtos": {}, 
                "logo": "🍔", 
                "descricao": "Nova loja no RushBite",
                "taxa_entrega": 5.0,
                "aceita_cupom_rush": True
            }
            salvar_dados(dados)
            print(f"{GREEN}✓ Empresa cadastrada com sucesso!{RESET}"); pausar()

if __name__ == "__main__":
    # Garante que as pastas e arquivos existam antes de começar
    if not os.path.exists("src/telas"):
        print(f"{RED}Erro crítico: Pasta 'src/telas' não encontrada!{RESET}")
    else:
        login()