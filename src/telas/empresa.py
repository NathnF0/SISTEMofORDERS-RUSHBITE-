from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_dados, ler_todos_pedidos, atualizar_status_pedido

def menu_empresa(nome_loja):
    while True:
        dados = carregar_dados()
        loja = dados[nome_loja]
        
        exibir_cabecalho(f"Painel Administrativo: {nome_loja}")
        print(f"{CYAN}--- GESTÃO ---{RESET}")
        print("1. Gerenciar Cardápio")
        print("2. Ver Pedidos Recebidos")
        print("3. Relatório de Faturamento")
        print(f"\n{CYAN}--- CONFIGURAÇÕES ---{RESET}")
        print("4. Editar Perfil (Logo, Descrição, Horário)")
        print("5. Configurar Entrega e PIX")
        print(f"\n{RED}0. Sair do Painel{RESET}")
        
        op = input("\nEscolha uma opção: ")

        if op == "1":
            gerenciar_cardapio(nome_loja, dados)
        elif op == "2":
            gerenciar_pedidos(nome_loja)
        elif op == "3":
            exibir_faturamento(nome_loja)
        elif op == "4":
            personalizar_loja(nome_loja, dados)
        elif op == "5":
            configurar_pagamento(nome_loja, dados)
        elif op == "0":
            break

def personalizar_loja(nome, dados):
    loja = dados[nome]
    exibir_cabecalho(f"Personalizar: {nome}")
    print(f"Logo atual: {loja.get('logo', 'Sem logo')}")
    print(f"Descrição: {loja.get('descricao', 'Sem descrição')}")
    print(f"Horário: {loja.get('horario', 'Não definido')}")
    print("-" * 20)
    
    loja['logo'] = input("Nova Logo (Ex: 🍕): ")
    loja['descricao'] = input("Descrição da Loja: ")
    loja['horario'] = input("Horário de Funcionamento (Ex: 18h às 23h): ")
    
    salvar_dados(dados)
    print(f"\n{GREEN}✅ Perfil atualizado com sucesso!{RESET}")
    pausar()

def gerenciar_cardapio(nome, dados):
    loja = dados[nome]
    exibir_cabecalho("Gerenciar Cardápio")
    print("1. Adicionar/Editar Produto")
    print("2. Listar Produtos")
    print("0. Voltar")
    esc = input("\nOpção: ")
    if esc == "1":
        n = input("Nome do Produto: ")
        p = ler_float("Preço: R$ ")
        loja['produtos'][n] = p
        salvar_dados(dados)
        print(f"✅ {n} atualizado!")
    elif esc == "2":
        for p, v in loja['produtos'].items():
            print(f"- {p}: R$ {v:.2f}")
    pausar()

def configurar_pagamento(nome, dados):
    loja = dados[nome]
    exibir_cabecalho("Configurações de Venda")
    loja['taxa_entrega'] = ler_float("Taxa de Entrega: R$ ")
    loja['chave_pix'] = input("Sua Chave PIX: ")
    salvar_dados(dados)
    print(f"{GREEN}✅ Dados salvos!{RESET}")
    pausar()

def exibir_faturamento(nome_loja):
    pedidos = [p for p in ler_todos_pedidos() if p['loja'] == nome_loja and p['status'] == "Entregue"]
    total = sum(p['total'] for p in pedidos)
    exibir_cabecalho("Financeiro")
    print(f"Vendas Concluídas: {len(pedidos)}")
    print(f"Total Faturado: {GREEN}R$ {total:.2f}{RESET}")
    pausar()

def gerenciar_pedidos(nome_loja):
    while True:
        exibir_cabecalho(f"Pedidos de {nome_loja}")
        meus = [p for p in ler_todos_pedidos() if p['loja'] == nome_loja]
        
        if not meus:
            print("Nenhum pedido hoje."); pausar(); break
            
        for i, p in enumerate(meus, 1):
            cor = GREEN if p['status'] == "Entregue" else YELLOW
            print(f"{i}. {p['id']} | Status: {cor}{p['status']}{RESET} | R$ {p['total']:.2f}")
        
        esc = input("\nVer detalhes (nº) ou 0 para sair: ")
        if esc == "0": break
        try:
            p = meus[int(esc)-1]
            exibir_cabecalho(f"Detalhes: {p['id']}")
            print(f"Itens: {', '.join(p['itens'])}")
            print(f"Pagamento: {p['pagamento']}")
            print(f"Tipo: {p['tipo_entrega']}")
            print(f"Endereço: {p['endereco']}")
            print("\n1-Preparando 2-Saiu para Entrega 3-Entregue 4-Cancelar")
            acao = input("Mudar status: ")
            m = {"1":"Preparando", "2":"Saiu para Entrega", "3":"Entregue", "4":"Cancelado"}
            if acao in m: atualizar_status_pedido(p['id'], m[acao])
        except: pass