import json
import os
from datetime import datetime

# ANSI colors para terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"

print("Bem-vindo ao RushBite!")
print("=======================")
print("1 - Cliente")
print("2 - Empresa")

modo = int(input("\nEscolha uma opção: "))

# ================= FUNÇÃO PARA CARREGAR EMPRESAS =================
def carregar_empresas():
    if os.path.exists("empresas.json"):
        with open("empresas.json", "r") as f:
            try:
                empresas = json.load(f)
            except:
                empresas = {}
    else:
        empresas = {}

    # criar empresas fake de demonstração se JSON estiver vazio
    if not empresas:
        empresas = {
            "Pizza do Tony": {
                "senha": "123",
                "categoria": "Pizza",
                "descricao": "Melhor pizza da cidade",
                "produtos": {"Mussarela": 18, "Calabresa": 20},
                "publicada": True,
                "horario": {"abertura": "10:00", "fechamento": "23:00"},
                "logo": "🍕"
            },
            "Brasa Lanches": {
                "senha": "abc",
                "categoria": "Hamburguer",
                "descricao": "Hamburguer artesanal delicioso",
                "produtos": {"X-Burguer": 10, "X-Tudo": 15},
                "publicada": True,
                "horario": {"abertura": "09:00", "fechamento": "22:00"},
                "logo": "🍔"
            }
        }

    # corrigir formato antigo
    for nome, dados in list(empresas.items()):
        if isinstance(dados, str):
            empresas[nome] = {
                "senha": dados,
                "categoria": "",
                "descricao": "",
                "produtos": {},
                "publicada": False,
                "horario": {"abertura": "00:00", "fechamento": "23:59"},
                "logo": ""
            }
        else:
            if "produtos" not in dados: dados["produtos"] = {}
            if "categoria" not in dados: dados["categoria"] = ""
            if "descricao" not in dados: dados["descricao"] = ""
            if "publicada" not in dados: dados["publicada"] = False
            if "horario" not in dados: dados["horario"] = {"abertura": "00:00", "fechamento": "23:59"}
            if "logo" not in dados: dados["logo"] = ""
    return empresas

# ================= CLIENTE =================
if modo == 1:
    print("\n====== MODO CLIENTE ======")
    empresas = carregar_empresas()

    # só empresas publicadas
    lojas_disponiveis = {nome: dados for nome, dados in empresas.items() if dados["produtos"] and dados.get("publicada", False)}

    if not lojas_disponiveis:
        print("Nenhuma loja disponível no momento.")
    else:
        print("\nLojas disponíveis:")
        for i, (nome, dados) in enumerate(lojas_disponiveis.items(), 1):
            descricao = dados.get("descricao", "")
            categoria = dados.get("categoria", "")
            horario = dados.get("horario", {"abertura": "00:00", "fechamento": "23:59"})
            abertura, fechamento = horario.get("abertura"), horario.get("fechamento")
            hora_atual = datetime.now().strftime("%H:%M")
            status = f"{GREEN}Aberto{RESET}" if abertura <= hora_atual <= fechamento else f"{RED}Fechado{RESET}"
            logo = dados.get("logo", "")

            print(f"{BOLD}{i} - {logo} {nome.upper()} ({categoria}) - {status}{RESET}")
            print(f"  {ITALIC}{descricao}{RESET}")
            print(f"  Horário: {abertura} - {fechamento}\n")

        while True:
            try:
                opcao_loja = int(input("\nEscolha uma loja: "))
                if opcao_loja < 1 or opcao_loja > len(lojas_disponiveis):
                    print("Opção inválida.")
                    continue
                break
            except:
                print("Digite um número válido.")

        loja_escolhida = list(lojas_disponiveis.keys())[opcao_loja - 1]
        cardapio = lojas_disponiveis[loja_escolhida]["produtos"]

        if not cardapio:
            print("Esta loja ainda não tem produtos cadastrados.")
        else:
            print(f"\n{BOLD}=== CARDÁPIO DE {loja_escolhida.upper()} ==={RESET}")
            for i, (produto, preco) in enumerate(cardapio.items(), 1):
                print(f"{i}. {produto} - {YELLOW}R${preco}{RESET}")

            carrinho = []
            while True:
                try:
                    opcao_item = int(input("\nEscolha o item: "))
                    if opcao_item < 1 or opcao_item > len(cardapio):
                        print("Opção inválida.")
                        continue
                    item_escolhido = list(cardapio.keys())[opcao_item - 1]
                except:
                    print("Digite um número válido.")
                    continue

                try:
                    quantidade = int(input("Quantidade: "))
                except:
                    print("Quantidade inválida.")
                    continue

                carrinho.append((item_escolhido, quantidade))

                print("\nCarrinho atual:")
                for idx, (item, qtd) in enumerate(carrinho, 1):
                    print(f"{idx}. {item} x{qtd}")

                while True:
                    mais_item = input("\nDeseja escolher outro item? (S/N): ").lower()
                    if mais_item in ["s", "n"]:
                        break
                    else:
                        print("Digite apenas S ou N")
                if mais_item == "n":
                    break

            total = 0
            print(f"\n{BOLD}====== RESUMO DO PEDIDO ======{RESET}")
            print(f"Loja: {loja_escolhida}")

            for item, qtd in carrinho:
                preco = cardapio[item]
                subtotal = preco * qtd
                total += subtotal
                print(f"{item} x{qtd} = {YELLOW}R${subtotal}{RESET}")

            print(f"\n{BOLD}TOTAL: {YELLOW}R${total}{RESET}")

# ================= EMPRESA =================
elif modo == 2:
    empresas = carregar_empresas()
    print("\n====== MODO EMPRESA ======")

    while True:
        print("\n1 - Login")
        print("2 - Criar loja")
        print("3 - Sair")

        escolha = input("Escolha: ")

        if escolha == "1":
            nome = input("Nome da empresa: ")
            senha = input("Senha: ")

            if nome in empresas and empresas[nome]["senha"] == senha:
                print("Login realizado!")
                while True:
                    print("\n=== PAINEL DA EMPRESA ===")
                    print("1 - Adicionar produto")
                    print("2 - Ver produtos")
                    print("3 - Personalizar loja")
                    print("4 - Publicar em RushBite")
                    print("5 - Sair")

                    op = input("Escolha: ")

                    if op == "1":
                        produto = input("Nome do produto: ")
                        preco = float(input("Preço: "))
                        empresas[nome]["produtos"][produto] = preco
                        with open("empresas.json", "w") as f:
                            json.dump(empresas, f)
                        print("Produto adicionado!")

                    elif op == "2":
                        print("\nSeus produtos:")
                        for p, v in empresas[nome]["produtos"].items():
                            print(f"{p} - {YELLOW}R${v}{RESET}")

                    elif op == "3":
                        # mostra valores atuais e permite manter ou mudar
                        dados = empresas[nome]
                        print("\n=== Personalização da Loja ===")
                        categoria = input(f"Categoria ({dados.get('categoria','')}): ") or dados.get("categoria","")
                        descricao = input(f"Descrição ({dados.get('descricao','')}): ") or dados.get("descricao","")
                        abertura = input(f"Hora de abertura ({dados.get('horario',{}).get('abertura','09:00')}): ") or dados.get('horario',{}).get('abertura','09:00')
                        fechamento = input(f"Hora de fechamento ({dados.get('horario',{}).get('fechamento','22:00')}): ") or dados.get('horario',{}).get('fechamento','22:00')
                        logo = input(f"Logo da loja ({dados.get('logo','')}): ") or dados.get('logo','')

                        empresas[nome]["categoria"] = categoria
                        empresas[nome]["descricao"] = descricao
                        empresas[nome]["horario"] = {"abertura": abertura, "fechamento": fechamento}
                        empresas[nome]["logo"] = logo

                        with open("empresas.json", "w") as f:
                            json.dump(empresas, f)
                        print("Loja personalizada!")

                    elif op == "4":
                        print("\nPublicar em RushBite torna sua loja visível para todos os clientes.")
                        print("Certifique-se de que produtos e personalização estão completos.")
                        confirmar = input("Deseja publicar agora? (S/N): ").lower()
                        if confirmar == "s":
                            empresas[nome]["publicada"] = True
                            with open("empresas.json", "w") as f:
                                json.dump(empresas, f)
                            print(f"{GREEN}Empresa {nome} publicada com sucesso!{RESET}")
                        else:
                            print("Publicação cancelada.")

                    elif op == "5":
                        break
            else:
                print("Login inválido.")

        elif escolha == "2":
            nome = input("Nome da empresa: ")

            if nome in empresas:
                print("Empresa já existe.")
                continue

            senha = input("Senha: ")
            empresas[nome] = {
                "senha": senha,
                "categoria": "",
                "descricao": "",
                "produtos": {},
                "publicada": False,
                "horario": {"abertura": "00:00", "fechamento": "23:59"},
                "logo": ""
            }
            with open("empresas.json", "w") as f:
                json.dump(empresas, f)
            print("Empresa criada! Lembre-se de personalizar e publicar depois.")

        elif escolha == "3":
            break

        else:
            print("Opção inválida.")