from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_dados, ler_todos_pedidos, atualizar_status_pedido

def menu_empresa(nome_loja):
    while True:
        dados = carregar_dados()
        loja = dados[nome_loja]
        
        if 'aceita_cupom_rush' not in loja:
            loja['aceita_cupom_rush'] = True
            salvar_dados(dados)

        exibir_cabecalho(f"PAINEL ADMINISTRATIVO: {nome_loja}")
        
        # --- SEÇÃO GESTÃO ---
        print(f"{CYAN}{BOLD}📂 GESTÃO DE OPERAÇÕES{RESET}")
        print(f"  [1] 🍴 Gerenciar Cardápio & Estoque")
        print(f"  [2] 📦 Pedidos Recebidos (Fila)")
        print("-" * 40)
        
        # --- SEÇÃO FINANCEIRA ---
        print(f"{GREEN}{BOLD}💰 INTELIGÊNCIA FINANCEIRA{RESET}")
        print(f"  [3] 📊 Dashboard de Faturamento")
        print(f"  [4] 🎟️  Meus Cupons Próprios")
        
        status_rush = f"{GREEN}ATIVO{RESET}" if loja.get('aceita_cupom_rush') else f"{RED}INATIVO{RESET}"
        print(f"  [5] 🌐 Parceria RushBite: {status_rush}")
        print("-" * 40)
        
        # --- SEÇÃO CONFIGURAÇÃO ---
        print(f"{YELLOW}{BOLD}⚙️  CONFIGURAÇÕES DA LOJA{RESET}")
        print(f"  [6] 🎨 Personalizar Perfil Visual")
        print(f"  [7] 📞 Contato e Chave PIX")
        print("-" * 40)
        
        print(f"{RED}[0] ⬅️  Sair do Sistema{RESET}")
        
        op = input(f"\n{BOLD}Selecione uma opção: {RESET}")
        
        if op == "1": gerenciar_cardapio(nome_loja, dados)
        elif op == "2": gerenciar_pedidos_v2(nome_loja)
        elif op == "3": exibir_financeiro_detalhado(nome_loja)
        elif op == "4": gerenciar_marketing(nome_loja, dados)
        elif op == "5": 
            loja['aceita_cupom_rush'] = not loja.get('aceita_cupom_rush')
            salvar_dados(dados)
            print(f"\n{GREEN}✓ Status de parceria atualizado!{RESET}")
            pausar()
        elif op == "6": personalizar_loja_inteligente(nome_loja, dados)
        elif op == "7": configurar_contato_pagamento(nome_loja, dados)
        elif op == "0": break

def gerenciar_pedidos_v2(nome_loja):
    while True:
        exibir_cabecalho(f"FILA DE PEDIDOS - {nome_loja}")
        pedidos_totais = ler_todos_pedidos()
        meus = [p for p in pedidos_totais if p['loja'] == nome_loja]
        
        if not meus:
            print(f"{YELLOW}Nenhum pedido na fila no momento.{RESET}")
            pausar(); break
            
        print(f"{BOLD}{'ID':<7} | {'CLIENTE':<15} | {'STATUS':<15}{RESET}")
        print("-" * 40)
        for i, p in enumerate(meus, 1):
            cor = GREEN if p['status'] in ["Entregue", "Finalizado"] else YELLOW
            print(f"{i}. {p['id']} | {p.get('cliente')[:15]:<15} | {cor}{p['status']:<15}{RESET}")
        
        print(f"\n{CYAN}[nº]{RESET} Ver Detalhes | {CYAN}[c + nº]{RESET} Chat Rápido | {RED}[0]{RESET} Voltar")
        esc = input("\nAção: ")
        
        if esc == "0": break
        
        if esc.startswith('c'):
            try:
                idx = int(esc[1:]) - 1
                p = meus[idx]
                msg = input(f"\n{BOLD}Mensagem para {p['cliente']}:{RESET} ")
                atualizar_status_pedido(p['id'], p['status'], f"Loja: {msg}")
                print(f"{GREEN}✓ Mensagem enviada ao chat!{RESET}"); pausar()
                continue
            except: pass

        try:
            p = meus[int(esc)-1]
            detalhar_pedido_empresa(p)
        except: pass

def detalhar_pedido_empresa(p):
    exibir_cabecalho(f"DETALHES: {p['id']}")
    tipo = p.get('tipo_entrega', 'Entrega')
    print(f"{BOLD}Cliente:{RESET} {p['cliente']}")
    print(f"{BOLD}Endereço:{RESET} {p['endereco']}")
    print(f"{BOLD}Itens:{RESET} {YELLOW}{', '.join(p['itens'])}{RESET}")
    print(f"{BOLD}Total:{RESET} {GREEN}R$ {p['total']:.2f}{RESET}")
    print("-" * 30)
    
    print(f"{CYAN}ATUALIZAR STATUS:{RESET}")
    if tipo == "Entrega":
        opcoes = {"1":"Preparando", "2":"Saiu para Entrega", "3":"Entregue", "4":"Cancelado"}
        for k, v in opcoes.items(): print(f"[{k}] {v}")
    else:
        opcoes = {"1":"Preparando", "2":"Pronto p/ Retirada", "3":"Finalizado", "4":"Cancelado"}
        for k, v in opcoes.items(): print(f"[{k}] {v}")
    
    st = input("\nNova fase: ")
    if st in opcoes:
        atualizar_status_pedido(p['id'], opcoes[st], f"Sistema: Pedido movido para {opcoes[st]}")
        print(f"{GREEN}✓ Status atualizado!{RESET}"); pausar()

# ... (Funções de Financeiro, Cardápio e Perfil continuam as mesmas, mas agora com menus verticais)
def gerenciar_cardapio(nome, dados):
    while True:
        exibir_cabecalho("GERENCIAR CARDÁPIO")
        prods = dados[nome]['produtos']
        for i, (p, v) in enumerate(prods.items(), 1):
            print(f"{i}. {p:<20} | R$ {v:>6.2f}")
        
        print("\n" + "-"*30)
        print(f"{GREEN}[1] Adicionar / Editar{RESET}")
        print(f"{RED}[2] Remover Produto{RESET}")
        print(f"{YELLOW}[0] Voltar{RESET}")
        
        op = input("\nEscolha: ")
        if op == "1":
            n = input("Nome do Item: ")
            v = ler_float("Preço: R$ ")
            dados[nome]['produtos'][n] = v
            salvar_dados(dados)
        elif op == "2":
            n = input("Nome para deletar: ")
            if n in prods: del dados[nome]['produtos'][n]; salvar_dados(dados)
        elif op == "0": break

def exibir_financeiro_detalhado(nome_loja):
    pedidos = [p for p in ler_todos_pedidos() if p['loja'] == nome_loja and p['status'] in ["Entregue", "Finalizado"]]
    total = sum(p['total'] for p in pedidos)
    exibir_cabecalho("DASHBOARD FINANCEIRO")
    print(f"💵 Faturamento Líquido: {GREEN}R$ {total:.2f}{RESET}")
    print(f"📦 Pedidos Finalizados: {len(pedidos)}")
    print(f"📈 Ticket Médio: R$ {(total/len(pedidos) if pedidos else 0):.2f}")
    pausar()

def gerenciar_marketing(nome_loja, dados):
    loja = dados[nome_loja]
    exibir_cabecalho("MARKETING: MEUS CUPONS")
    print(f"Código Atual: {BOLD}{loja.get('cupom_id', 'NENHUM')}{RESET}")
    print(f"Desconto: {GREEN}{loja.get('cupom_desc', 0)}%{RESET}")
    print("\n[1] Criar/Alterar Cupom\n[2] Desativar Cupom\n[0] Voltar")
    op = input("\nOpção: ")
    if op == "1":
        loja['cupom_id'] = input("Código: ").upper().strip()
        loja['cupom_desc'] = ler_float("Desconto %: ")
        salvar_dados(dados)
    elif op == "2":
        loja['cupom_id'] = None; loja['cupom_desc'] = 0
        salvar_dados(dados)
    pausar()

def personalizar_loja_inteligente(nome, dados):
    l = dados[nome]
    exibir_cabecalho("PERFIL VISUAL")
    n_logo = input(f"Logo/Emoji [{l.get('logo','🍔')}]: "); l['logo'] = n_logo if n_logo else l['logo']
    n_desc = input(f"Descrição [{l.get('descricao','')}]: "); l['descricao'] = n_desc if n_desc else l['descricao']
    salvar_dados(dados); print("✓ Salvo!"); pausar()

def configurar_contato_pagamento(nome, dados):
    l = dados[nome]
    exibir_cabecalho("CONTATO E PAGAMENTO")
    n_tel = input(f"Tel SAC [{l.get('telefone_suporte','N/A')}]: "); l['telefone_suporte'] = n_tel if n_tel else l['telefone_suporte']
    n_taxa = input(f"Taxa de Entrega [{l.get('taxa_entrega',0)}]: ")
    if n_taxa: l['taxa_entrega'] = float(n_taxa)
    n_pix = input(f"Chave PIX [{l.get('chave_pix','N/A')}]: "); l['chave_pix'] = n_pix if n_pix else l['chave_pix']
    salvar_dados(dados); print("✓ Configurações salvas!"); pausar()