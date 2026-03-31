# src/telas/cliente.py
from datetime import datetime
from src.utils import GREEN, RED, YELLOW, RESET, BOLD, ITALIC

def rodar_menu_cliente(empresas):
    print("\n====== MODO CLIENTE ======")
    lojas_disponiveis = {nome: dados for nome, dados in empresas.items() if dados["produtos"] and dados.get("publicada", False)}

    if not lojas_disponiveis:
        print("Nenhuma loja disponível no momento.")
        return

    print("\nLojas disponíveis:")
    for i, (nome, dados) in enumerate(lojas_disponiveis.items(), 1):
        horario = dados.get("horario", {"abertura": "00:00", "fechamento": "23:59"})
        abertura, fechamento = horario.get("abertura"), horario.get("fechamento")
        hora_atual = datetime.now().strftime("%H:%M")
        status = f"{GREEN}Aberto{RESET}" if abertura <= hora_atual <= fechamento else f"{RED}Fechado{RESET}"
        
        print(f"{BOLD}{i} - {dados.get('logo', '')} {nome.upper()} ({dados.get('categoria', '')}) - {status}{RESET}")
        print(f"  {ITALIC}{dados.get('descricao', '')}{RESET}")
        print(f"  Horário: {abertura} - {fechamento}\n")

    while True:
        try:
            opcao_loja = int(input("\nEscolha uma loja: "))
            if 1 <= opcao_loja <= len(lojas_disponiveis): break
            print("Opção inválida.")
        except ValueError:
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
                if not (1 <= opcao_item <= len(cardapio)):
                    print("Opção inválida.")
                    continue
                item_escolhido = list(cardapio.keys())[opcao_item - 1]
                quantidade = int(input("Quantidade: "))
                if quantidade <= 0: continue
                
                carrinho.append((item_escolhido, quantidade))
                print(f"\nCarrinho atual:")
                for idx, (item, qtd) in enumerate(carrinho, 1):
                    print(f"{idx}. {item} x{qtd}")

                mais_item = input("\nDeseja escolher outro item? (S/N): ").lower()
                if mais_item == "n": break
            except ValueError:
                print("Entrada inválida.")

        total = 0
        print(f"\n{BOLD}====== RESUMO DO PEDIDO ======{RESET}")
        for item, qtd in carrinho:
            preco = cardapio[item]
            subtotal = preco * qtd
            total += subtotal
            print(f"{item} x{qtd} = {YELLOW}R${subtotal}{RESET}")
        print(f"\n{BOLD}TOTAL: {YELLOW}R${total}{RESET}")