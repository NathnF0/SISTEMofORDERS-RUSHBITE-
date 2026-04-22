import os
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar
from src.database import carregar_dados, salvar_dados, carregar_clientes, salvar_clientes, carregar_config_loja
from src.telas.cliente import menu_cliente
from src.telas.empresa import menu_empresa
from datetime import datetime

def esta_no_horario_comercial(nome_loja, dados):
    # Em vez de carregar_config_loja(), pegamos direto dos dados que já temos
    loja = dados['lojas'][nome_loja]
    
    if not loja.get('aberta', True):
        return False, "A loja foi fechada manualmente pelo administrador."

    agora = datetime.now().time()
    # Pega o horário da loja ou usa um padrão caso esteja vazio
    abertura = datetime.strptime(loja.get('horario_abertura', '18:00'), "%H:%M").time()
    fechamento = datetime.strptime(loja.get('horario_fechamento', '23:00'), "%H:%M").time()

    if abertura <= agora <= fechamento:
        return True, "Ok"
    else:
        return False, f"Loja Fechada! Nosso horário: {loja.get('horario_abertura', '18:00')} às {loja.get('horario_fechamento', '23:00')}"
     
def login():
    while True:
        exibir_cabecalho("BEM-VINDO AO RUSHBITE")
        print(f"{CYAN}[1]{RESET} Entrar como Cliente")
        print(f"{GREEN}[2]{RESET} Entrar como Empresa")
        print(f"{YELLOW}[3]{RESET} Criar Nova Conta")
        print("-" * 30)
        print(f"{RED}[0]{RESET} Sair do Programa")
        
        op = input(f"\n{BOLD}Escolha sua jornada: {RESET}").strip()

        if op == "1":
            clis = carregar_clientes()
            login_digitado = input("Usuário: ").strip() 
            senha = input("Senha: ")
            
            if login_digitado in clis and clis[login_digitado]['senha'] == senha:
                # Pegamos o dicionário de dados do cliente
                user_logado = clis[login_digitado]
                user_logado['nome'] = login_digitado 
                
                menu_cliente(user_logado) 
            else:
                print(f"{RED}Login inválido!{RESET}"); pausar()

        elif op == "2":
            dados = carregar_dados()
            loja_nome = input("Nome da Loja: ").strip()
            senha = input("Senha: ")
            if loja_nome in dados and dados[loja_nome]['senha'] == senha:
                # Criamos o dicionário completo e injetamos o nome nele
                loja_dados = dados[loja_nome]
                loja_dados['nome'] = loja_nome  
                menu_empresa(loja_dados)
            else:
                print(f"{RED}Empresa não encontrada ou senha incorreta!{RESET}"); pausar()

        elif op == "3":
            criar_conta()

        elif op == "0":
            print(f"\n{YELLOW}Obrigado por usar o RushBite! Até logo. 🍔{RESET}")
            break

def criar_conta():
    exibir_cabecalho("CRIAR NOVA CONTA")
    print(f"[{BOLD}1{RESET}] Cliente")
    print(f"[{BOLD}2{RESET}] Empresa")
    tipo = input("\nEscolha o tipo de conta: ").strip()
    
    if tipo == "1":
        clis = carregar_clientes()
        user = input("Escolha um usuário: ").strip()
        if user in clis:
            print(f"{RED}Usuário já existe!{RESET}"); pausar()
        else:
            senha = input("Crie uma senha: ")
            # Agora criamos com a chave de pontos zerada
            clis[user] = {
             "senha": senha, 
             "endereco": {}, 
             "telefone": "", 
             "pontos": 0,
             "xp": 0,         
             "level": "Bronze" # Bronze, Prata, Ouro, Rush
            }
            salvar_clientes(clis)
            print(f"{GREEN}✓ Conta cliente criada com sucesso!{RESET}"); pausar()
            
    elif tipo == "2":
        dados = carregar_dados()
        loja = input("Nome da sua Loja: ").strip()
        if loja in dados:
            print(f"{RED}Essa loja já está cadastrada!{RESET}"); pausar()
        else:
            senha = input("Crie uma senha: ")
            # Inicializa a loja com TODAS as funções da v0.2.8
            dados[loja] = {
                "senha": senha, 
                "produtos": {},
                "estoque": {},
                "logo": "🍔", 
                "descricao": "Nova loja no RushBite",
                "taxa_entrega": 5.0,
                "aberta": True,           # Status de funcionamento
                "aceita_cupom_rush": False, # Começa como False até assinar o contrato
                "cupom_id": "",
                "cupom_desc": 0,
                "cupom_ativo": False
            }
            salvar_dados(dados)
            print(f"{GREEN}✓ Empresa cadastrada com sucesso!{RESET}"); pausar()

if __name__ == "__main__":
    # Verifica integridade das pastas
    if not os.path.exists("src/telas"):
        os.makedirs("src/telas", exist_ok=True)
        print(f"{YELLOW}Aviso: Pastas de telas criadas agora.{RESET}")
    
    login()

