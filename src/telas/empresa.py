import os
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_dados, ler_todos_pedidos, atualizar_status_pedido

def menu_empresa(nome_loja):
    while True:
        dados = carregar_dados()
        if nome_loja not in dados:
            print(f"{RED}Erro: Loja não encontrada!{RESET}")
            break
            
        loja = dados[nome_loja]
        
        # Garantia de campos obrigatórios
        if 'aceita_cupom_rush' not in loja:
            loja['aceita_cupom_rush'] = True
            salvar_dados(dados)

        exibir_cabecalho(f"PAINEL ADMINISTRATIVO: {nome_loja}")
        
        print(f"{CYAN}{BOLD}📂 GESTÃO DE OPERAÇÕES{RESET}")
        print(f"  [1] 🍴 Gerenciar Cardápio & Estoque")
        print(f"  [2] 📦 Pedidos Recebidos (Fila)")
        print("-" * 40)
        
        print(f"{GREEN}{BOLD}💰 INTELIGÊNCIA FINANCEIRA{RESET}")
        print(f"  [3] 📊 Dashboard de Faturamento")
        print(f"  [4] 🎟️  Meus Cupons Próprios")
        
        status_rush = f"{GREEN}ATIVO{RESET}" if loja.get('aceita_cupom_rush') else f"{RED}INATIVO{RESET}"
        print(f"  [5] 🌐 Parceria RushBite: {status_rush}")
        print("-" * 40)
        
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
        
        meus = [p for p in pedidos_totais if p.get('loja') == nome_loja]
        
        if not meus:
            print(f"{YELLOW}Nenhum pedido na fila no momento.{RESET}")
            pausar(); break
            
        print(f"{BOLD}{'Nº':<3} | {'ID':<7} | {'CLIENTE':<15} | {'STATUS':<15}{RESET}")
        print("-" * 45)
        
        for i, p in enumerate(meus, 1):
            st = p.get('status', 'Pendente')
            cor = GREEN if st in ["Entregue", "Finalizado", "Pronto p/ Retirada"] else YELLOW
            nome_c = str(p.get('cliente', 'S/N'))[:15]
            print(f"{i:<3} | {p.get('id', '???'):<7} | {nome_c:<15} | {cor}{st:<15}{RESET}")
        
        print(f"\n{CYAN}[nº]{RESET} Ver Detalhes | {CYAN}[c + nº]{RESET} Chat Rápido | {RED}[0]{RESET} Voltar")
        esc = input("\nAção: ").lower().strip()
        
        if esc == "0" or not esc: break
        
        if esc.startswith('c'):
            try:
                idx = int(esc[1:]) - 1
                p = meus[idx]
                msg = input(f"\n{BOLD}Mensagem para {p.get('cliente')}:{RESET} ")
                if msg:
                    atualizar_status_pedido(p['id'], p.get('status'), f"Loja: {msg}")
                    print(f"{GREEN}✓ Mensagem enviada!{RESET}"); pausar()
                continue
            except: 
                print(f"{RED}Erro ao abrir chat.{RESET}"); pausar(); continue

        try:
            p = meus[int(esc)-1]
            detalhar_pedido_empresa(p)
        except:
            print(f"{RED}Opção inválida.{RESET}"); pausar()

def detalhar_pedido_empresa(p):
    while True:
        exibir_cabecalho(f"DETALHES DO PEDIDO: {p.get('id')}")
        print(f"{BOLD}Cliente:{RESET} {p.get('cliente')}")
        print(f"{BOLD}Endereço:{RESET} {YELLOW}{p.get('endereco', 'Não informado')}{RESET}")
        print(f"{BOLD}Itens:{RESET} {YELLOW}{', '.join(p.get('itens', []))}{RESET}")
        print(f"{BOLD}Total:{RESET} {GREEN}R$ {p.get('total', 0):.2f}{RESET}")
        print(f"{BOLD}Tipo:{RESET} {p.get('tipo_entrega', 'Entrega')}")
        print("-" * 40)
        
        # --- NOVO: VISUALIZAÇÃO DO CHAT NOS DETALHES ---
        print(f"{CYAN}💬 HISTÓRICO DE CHAT:{RESET}")
        historico = p.get('historico_chat', [])
        if not historico:
            print(" > Nenhuma mensagem registrada.")
        for msg in historico:
            print(f" > {msg}")
        print("-" * 40)
        
        print(f"{CYAN}[S]{RESET} Mudar Status | {CYAN}[C]{RESET} Responder Chat | {CYAN}[I]{RESET} Comanda | {RED}[0]{RESET} Voltar")
        acao = input("\nAção: ").lower()

        if acao == "0": break
        
        elif acao == "c":
            msg = input(f"\n{BOLD}Resposta para {p.get('cliente')}:{RESET} ")
            if msg:
                atualizar_status_pedido(p['id'], p.get('status'), f"Loja: {msg}")
                # Atualiza localmente para a empresa ver na tela atual
                p.setdefault('historico_chat', []).append(f"Loja: {msg}")
                print(f"{GREEN}✓ Mensagem enviada!{RESET}"); pausar()

        elif acao == "i":
            gerar_comanda_txt(p)

        elif acao == "s":
            tipo = p.get('tipo_entrega', 'Entrega')
            if tipo == "Entrega":
                opcoes = {"1":"Preparando", "2":"Saiu para Entrega", "3":"Entregue", "4":"Cancelado"}
            else:
                opcoes = {"1":"Preparando", "2":"Pronto p/ Retirada", "3":"Finalizado", "4":"Cancelado"}
            
            print(f"\n{BOLD}SELECIONE O NOVO STATUS:{RESET}")
            for k, v in opcoes.items(): print(f"[{k}] {v}")
            
            st_esc = input("\nEscolha: ")
            if st_esc in opcoes:
                novo_st = opcoes[st_esc]
                atualizar_status_pedido(p['id'], novo_st, f"Sistema: Pedido atualizado para {novo_st}")
                p['status'] = novo_st 
                print(f"{GREEN}✓ Status atualizado!{RESET}"); pausar()
                break

def gerar_comanda_txt(p):
    nome_arquivo = f"comanda_{p['id'].replace('#','')}.txt"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("="*30 + "\n")
            f.write(f"      COMANDA RUSHBITE\n")
            f.write("="*30 + "\n")
            f.write(f"PEDIDO: {p['id']}\n")
            f.write(f"CLIENTE: {p['cliente']}\n")
            f.write(f"TIPO: {p['tipo_entrega']}\n")
            f.write("-" * 30 + "\n")
            f.write("ITENS:\n")
            for item in p['itens']:
                f.write(f" - {item}\n")
            f.write("-" * 30 + "\n")
            f.write(f"TOTAL: R$ {p['total']:.2f}\n")
            f.write("="*30 + "\n")
            f.write(f"Endereço: {p.get('endereco', 'N/A')}\n")
        
        print(f"\n{GREEN}✓ Comanda gerada: {nome_arquivo}{RESET}")
    except Exception as e:
        print(f"{RED}Erro ao gerar comanda: {e}{RESET}")
    pausar()

def exibir_financeiro_detalhado(nome_loja):
    pedidos = [p for p in ler_todos_pedidos() if p.get('loja') == nome_loja and p.get('status') in ["Entregue", "Finalizado"]]
    total = sum(p.get('total', 0) for p in pedidos)
    exibir_cabecalho("DASHBOARD FINANCEIRO")
    print(f"💵 Faturamento Líquido: {GREEN}R$ {total:.2f}{RESET}")
    print(f"📦 Pedidos Finalizados: {len(pedidos)}")
    ticket = total/len(pedidos) if pedidos else 0
    print(f"📈 Ticket Médio: R$ {ticket:.2f}")
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
        print(f"{GREEN}✓ Cupom ativado!{RESET}")
    elif op == "2":
        loja['cupom_id'] = None; loja['cupom_desc'] = 0
        salvar_dados(dados)
        print(f"{YELLOW}✓ Cupom desativado!{RESET}")
    pausar()

def personalizar_loja_inteligente(nome, dados):
    l = dados[nome]
    exibir_cabecalho("PERFIL VISUAL")
    n_logo = input(f"Logo/Emoji atual [{l.get('logo','🍔')}]: "); l['logo'] = n_logo if n_logo else l['logo']
    n_desc = input(f"Descrição atual [{l.get('descricao','')}]: "); l['descricao'] = n_desc if n_desc else l['descricao']
    salvar_dados(dados); print(f"{GREEN}✓ Perfil atualizado!{RESET}"); pausar()

def configurar_contato_pagamento(nome, dados):
    l = dados[nome]
    exibir_cabecalho("CONTATO E PAGAMENTO")
    n_tel = input(f"Tel SAC [{l.get('telefone_suporte','N/A')}]: "); l['telefone_suporte'] = n_tel if n_tel else l['telefone_suporte']
    n_taxa = input(f"Taxa de Entrega atual [{l.get('taxa_entrega',0)}]: ")
    if n_taxa: l['taxa_entrega'] = float(n_taxa)
    n_pix = input(f"Chave PIX atual [{l.get('chave_pix','N/A')}]: "); l['chave_pix'] = n_pix if n_pix else l['chave_pix']
    salvar_dados(dados); print(f"{GREEN}✓ Configurações salvas!{RESET}"); pausar()

def gerenciar_cardapio(nome, dados):
    while True:
        exibir_cabecalho("GERENCIAR CARDÁPIO")
        prods = dados[nome].get('produtos', {})
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
            if 'produtos' not in dados[nome]: dados[nome]['produtos'] = {}
            dados[nome]['produtos'][n] = v
            salvar_dados(dados)
        elif op == "2":
            n = input("Nome exato para deletar: ")
            if n in prods: 
                del dados[nome]['produtos'][n]
                salvar_dados(dados)
                print(f"{GREEN}✓ Removido!{RESET}")
        elif op == "0": break