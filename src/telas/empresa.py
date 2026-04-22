import os
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_dados, ler_todos_pedidos, atualizar_status_pedido, carregar_config_loja, salvar_config_loja
import os

def limpar_terminal():
    # Se for Windows usa 'cls', se for Linux/Mac usa 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')
def menu_empresa(loja_dados):
    while True:
        limpar_terminal()
        dados = carregar_dados()

        # Descobrimos o nome da loja, não importa se veio como texto ou dicionário
        if isinstance(loja_dados, dict):
            nome_loja = loja_dados.get('nome')
        else:
            nome_loja = loja_dados
            
        loja = dados.get(nome_loja)

        # Se mesmo assim não carregar, vamos debugar
        if not loja:
            print(f"{RED}Erro: Não encontrei a loja '{nome_loja}' no banco de dados.{RESET}")
            pausar()
            break 
        
        # 3. Pega o status atualizado do arquivo
        status_atual = loja.get('status', 'Fechado')
        is_aberta = (status_atual == "Aberto")
        cor_status = GREEN if is_aberta else RED

        # --- RESUMO DE STATUS ---
        pedidos_todos = ler_todos_pedidos()
        # Filtra garantindo que nome_loja é o texto (ex: "TestHive")
        pedidos_loja = [p for p in pedidos_todos if p.get('loja') == nome_loja]
        
        pendentes = [p for p in pedidos_loja if p.get('status') == "Pendente"]
        em_preparo = [p for p in pedidos_loja if p.get('status') == "Preparando"]

        exibir_cabecalho(f"PAINEL: {str(nome_loja).upper()}")
        

        # Alerta visual se houver trabalho
        if pendentes:
            print(f" {RED}🔔 {len(pendentes)} PEDIDOS AGUARDANDO ACEITAÇÃO!{RESET}")
        if em_preparo:
            print(f" {YELLOW}⏳ {len(em_preparo)} pedidos em preparo...{RESET}")
        if not pendentes and not em_preparo:
            print(f" {GREEN}✅ Tudo em dia por aqui!{RESET}")
        
        print("-" * 35)

# --- BLOCO 1: OPERAÇÃO ---
        status_loja = f"{GREEN}ABERTA{RESET}" if loja.get('aberta', True) else f"{RED}FECHADA{RESET}"
        print(f"{CYAN}📂 OPERAÇÃO{RESET} | Status: {status_loja}")
        print(f" [{BOLD}1{RESET}] 🍴 Cardápio & Estoque")
        print(f" [{BOLD}2{RESET}] 📦 Fila de Pedidos")
        print(f" [{BOLD}3{RESET}] {'🔴 Fechar' if loja.get('aberta', True) else '🟢 Abrir'} Loja")
        print("-" * 35)

        # --- BLOCO 2: INTELIGÊNCIA & LUCRO ---
        print(f"{CYAN}📊 ESTATÍSTICAS{RESET}")
        print(f" [{BOLD}4{RESET}] 🏆 Performance & Ranking")
        print(f" [{BOLD}5{RESET}] 💰 Financeiro (Lucros)")
        print("-" * 35)

        # --- BLOCO 3: IDENTIDADE & CONFIGS ---
        print(f"{CYAN}✨ PERSONALIZAÇÃO{RESET}")
        print(f" [{BOLD}6{RESET}] 🛠️  Configurar Loja")
        print(f" [{BOLD}7{RESET}] 🕒 Ajustar Horários & Relógio")
        print("-" * 35)

        # --- BLOCO 4: PARCERIA & MARKETING ---
        status_parceria = f"{GREEN}ATIVADA{RESET}" if loja.get('aceita_cupom_rush', True) else f"{RED}DESATIVADA{RESET}"
        print(f"{CYAN}🤝 RUSHBITE PARTNER{RESET}")
        print(f" [{BOLD}8{RESET}] 🎟️  Meus Cupons") # <--- OS CUPONS VOLTARAM!
        print(f" [{BOLD}9{RESET}] Parceria RushBite: {status_parceria}")
        print("-" * 35)

        print(f" [{RED}0{RESET}] ⬅️  Sair para o Menu Principal")
        
        op = input(f"\n{BOLD}Escolha: {RESET}").strip()
        
# --- LÓGICA DE EXECUÇÃO (SINCRONIZADA COM O MENU) ---
        if op == "1": 
            gerenciar_cardapio(nome_loja, dados)
        
        elif op == "2": 
            gerenciar_pedidos_v2(nome_loja)
        
        elif op == "3": 
            # Lógica invertida: Se está Aberto, vira Fechado. Se não, vira Aberto.
            novo_status = "Fechado" if status_atual == "Aberto" else "Aberto"
            
            # Atualiza no dicionário principal e salva
            dados[nome_loja]['status'] = novo_status
            
            # CRUCIAL: Atualiza também a chave 'aberta' para manter compatibilidade com o resto do sistema
            dados[nome_loja]['aberta'] = (novo_status == "Aberto")
            
            salvar_dados(dados)
            
            print(f"\n{cor_status}Status alterado para: {novo_status}{RESET}")
            pausar()
            continue
            
        elif op == "4": 
            exibir_performance_ranking(nome_loja)
            
        elif op == "5": 
            exibir_financeiro_lucro(nome_loja)
            
        elif op == "6": 
            menu_personalizacao_loja(nome_loja, dados)
            
        elif op == "7": 
            ajustar_horarios_loja(nome_loja, dados)
            
        elif op == "8":
            # Aqui você chama a função que exibe os cupons da loja
            gerenciar_marketing(nome_loja, dados) 
            
        elif op == "9":
            # Aqui chama a tela de contrato/parceria RushBite
            gerenciar_marketing(nome_loja, dados)

        elif op == "0": 
            break

def gerenciar_cardapio(nome, dados):
    while True:
        exibir_cabecalho("CARDÁPIO & ESTOQUE")
        loja = dados[nome]
        prods = loja.setdefault('produtos', {})
        estoque = loja.setdefault('estoque', {})

        for cat, itens in prods.items():
            print(f"\n{CYAN}📂 {cat.upper()}{RESET}")
            for p, v in itens.items():
                qtd = estoque.get(p, "∞")
                print(f"  • {p:<20} | R$ {v:>6.2f} | Est: {qtd}")
        
        print("\n[1] Add Item [2] Remover [3] Ajustar Estoque [0] Voltar")
        op = input("Ação: ")
        if op == "1":
            cat = input("Categoria: ").capitalize() or "Geral"
            n = input("Nome: ")
            v = ler_float("Preço: ")
            prods.setdefault(cat, {})[n] = v
            if n not in estoque: estoque[n] = "∞"
            salvar_dados(dados); pausar()
        elif op == "2":
            cat = input("Categoria: ").capitalize()
            n = input("Nome: ")
            if cat in prods and n in prods[cat]:
                del prods[cat][n]
                estoque.pop(n, None)
                salvar_dados(dados)
        elif op == "3":
            n = input("Nome do item: ")
            qtd = input("Quantidade (vazio = ∞): ")
            estoque[n] = int(qtd) if qtd.isdigit() else "∞"
            salvar_dados(dados)
        elif op == "0": break

def gerenciar_pedidos_v2(nome_loja):
    while True:
        exibir_cabecalho("PEDIDOS RECEBIDOS")
        # Busca todos os pedidos e filtra os desta loja
        todos = ler_todos_pedidos()
        pedidos = [p for p in todos if p.get('loja') == nome_loja]
        
        if not pedidos:
            print(f"\n{YELLOW}Nenhum pedido na fila no momento.{RESET}")
            pausar(); break
            
        # Mostra os 10 mais recentes (do último para o primeiro)
        meus = list(reversed(pedidos))[:10]
        for i, p in enumerate(meus, 1):
            st = p.get('status', 'Pendente')
            cor = GREEN if st in ["Entregue", "Finalizado"] else YELLOW
            # Proteção caso o ID ou Cliente não existam no dicionário
            p_id = p.get('id', 'N/A')
            p_cli = p.get('cliente', 'Desconhecido')[:10]
            print(f"{BOLD}[{i}]{RESET} {p_id} | {p_cli:<10} | {cor}{st}{RESET}")
            
        esc = input(f"\n{CYAN}[nº]{RESET} Detalhes | {RED}[0]{RESET} Voltar: ").strip()
        if esc == "0": break
        
        # Validação robusta da escolha
        if esc.isdigit():
            idx = int(esc) - 1
            if 0 <= idx < len(meus):
                detalhar_pedido_empresa(meus[idx])
            else:
                print(f"{RED}Número fora da lista!{RESET}"); pausar()
        else:
            print(f"{RED}Digite apenas números!{RESET}"); pausar()

def detalhar_pedido_empresa(p):
    while True:
        exibir_cabecalho(f"DETALHES: {p.get('id', 'S/ID')}")
        print(f"Cliente: {p.get('cliente', 'N/A')} | Status: {YELLOW}{p.get('status', 'Pendente')}{RESET}")
        print(f"Endereço: {p.get('endereco', 'N/A')}")
        
        # Garante que itens seja uma lista para o join não quebrar
        itens = p.get('itens', [])
        print(f"Itens: {', '.join(itens) if itens else 'Nenhum item'}")
        print("-" * 35)
        
        acao = input(f"{CYAN}[S]{RESET} Mudar Status | {CYAN}[C]{RESET} Chat | {RED}[0]{RESET} Voltar: ").lower().strip()
        
        if acao == "0": break
        elif acao == "c":
            msg = input("Resposta para o cliente: ")
            if msg:
                if atualizar_status_pedido(p['id'], p['status'], f"Loja: {msg}"):
                    p.setdefault('historico_chat', []).append(f"Loja: {msg}")
                    print(f"{GREEN}Mensagem enviada!{RESET}")
        elif acao == "s":
            print(f"\n{BOLD}Novos Status:{RESET}")
            print("1. Preparando | 2. Em trânsito/Pronto | 3. Finalizado | 4. Cancelado")
            st_map = {"1":"Preparando", "2":"Em trânsito/Pronto", "3":"Finalizado", "4":"Cancelado"}
            op_st = input("Escolha o novo status: ")
            novo = st_map.get(op_st)
            
            if novo:
                if atualizar_status_pedido(p['id'], novo, f"Sistema: Pedido alterado para {novo}"):
                    p['status'] = novo # Atualiza no objeto local para o menu mostrar certo
                    print(f"{GREEN}Status atualizado para {novo}!{RESET}")
                    pausar(); break

def menu_personalizacao_loja(nome_loja, dados):
    # Ajuste da gaveta (conforme o erro anterior)
    loja = dados['lojas'][nome_loja] if 'lojas' in dados else dados[nome_loja]
    
    while True:
        limpar_terminal() # Importante para atualizar o que você acabou de digitar!
        exibir_cabecalho(f"🛠️  PERSONALIZAR: {loja.get('nome', nome_loja).upper()}")
        
        print(f" 1. Logo/Emoji:   {loja.get('logo', '🥗')}")
        print(f" 2. Nome:         {loja.get('nome', nome_loja)}")
        print(f" 3. Descrição:    {loja.get('descricao', 'Sem descrição')}")
        print(f" 4. Taxa Entrega: R$ {loja.get('taxa_entrega', 0.0):.2f}")
        print(f"\n [{RED}0{RESET}] Salvar e Voltar")

        op = input(f"\n{BOLD}O que deseja alterar? {RESET}").strip()

        if op == "1":
            loja['logo'] = input("Novo Emoji/Logo (ex: 🥗): ")
        elif op == "2":
            loja['nome'] = input("Novo Nome da Loja: ")
        elif op == "3":
            # Aqui estava o erro: ele mudava mas não mostrava
            nova_desc = input("Nova Descrição: ")
            loja['descricao'] = nova_desc
            print(f"{GREEN}Descrição atualizada internamente!{RESET}")
        elif op == "4":
            try:
                valor = input("Nova Taxa (ex: 7.50): ").replace(',', '.')
                loja['taxa_entrega'] = float(valor)
            except:
                print(f"{RED}Valor inválido!{RESET}"); pausar()
        elif op == "0":
            salvar_dados(dados) # O COMANDO MAIS IMPORTANTE
            print(f"\n{GREEN}✅ Tudo pronto! Dados gravados no banco.{RESET}")
            pausar()
            break 
        else:
            print(f"{RED}Opção inválida!{RESET}"); pausar()



def exibir_performance_ranking(nome_loja):
    pedidos = [p for p in ler_todos_pedidos() if p.get('loja') == nome_loja and p.get('status') in ["Entregue", "Finalizado"]]
    
    # Ranking de Produtos
    contagem_itens = {}
    # Ranking de Clientes
    contagem_clientes = {}
    
    for p in pedidos:
        # Conta produtos
        for item in p.get('itens', []):
            contagem_itens[item] = contagem_itens.get(item, 0) + 1
        # Conta clientes
        cliente = p.get('cliente', 'Desconhecido')
        contagem_clientes[cliente] = contagem_clientes.get(cliente, 0) + 1

    rank_itens = sorted(contagem_itens.items(), key=lambda x: x[1], reverse=True)
    rank_clientes = sorted(contagem_clientes.items(), key=lambda x: x[1], reverse=True)

    exibir_cabecalho("🏆 PERFORMANCE & RANKING")
    
    print(f"{YELLOW}🔥 LANCHES MAIS PEDIDOS:{RESET}")
    if not rank_itens: print("  Sem dados de vendas ainda.")
    for i, (item, qtd) in enumerate(rank_itens[:5], 1):
        print(f"  {i}º {item:<18} | {qtd}x")
    
    print(f"\n{CYAN}👤 CLIENTES QUE MAIS COMPRAM:{RESET}")
    if not rank_clientes: print("  Nenhum cliente registrado.")
    for i, (cli, qtd) in enumerate(rank_clientes[:3], 1):
        print(f"  {i}º {cli:<18} | {qtd} pedidos")
        
    pausar()

def exibir_financeiro_lucro(nome_loja):
    # --- 1. FILTRAGEM DOS DADOS ---
    # Pegamos apenas pedidos dessa loja que já foram finalizados
    pedidos = [p for p in ler_todos_pedidos() if p.get('loja') == nome_loja and p.get('status') in ["Entregue", "Finalizado"]]
    
    # Filtro opcional: Se quiser ver apenas o financeiro de HOJE (comentado se quiser ver o total acumulado)
    # hoje = datetime.now().strftime("%d/%m/%Y")
    # pedidos = [p for p in pedidos if p.get('data') == hoje]

    if not pedidos:
        exibir_cabecalho("💰 FINANCEIRO & LUCROS")
        print(f"{RED}Nenhuma venda finalizada para processar o financeiro.{RESET}")
        pausar(); return

    # --- 2. CÁLCULOS TÉCNICOS ---
    faturamento_bruto = sum(p.get('total', 0) for p in pedidos)
    qtd_pedidos = len(pedidos)
    ticket_medio = faturamento_bruto / qtd_pedidos
    
    # Separação por método de pagamento (Pix, Cartão, Dinheiro)
    pix = sum(p.get('total', 0) for p in pedidos if p.get('metodo_pagamento') == 'Pix')
    cartao = sum(p.get('total', 0) for p in pedidos if p.get('metodo_pagamento') == 'Cartão')
    dinheiro = sum(p.get('total', 0) for p in pedidos if p.get('metodo_pagamento') == 'Dinheiro')

    # Meta Diária (Vamos deixar 500 como padrão conforme a reunião)
    meta = 500.00
    progresso = (faturamento_bruto / meta) * 100
    if progresso > 100: progresso = 100 # Trava visual da barra

    # --- 3. INTERFACE "BATER O OLHO E ENTENDER" ---
    exibir_cabecalho("💰 FINANCEIRO & LUCROS")
    
    print(f"📊 {BOLD}RESUMO GERAL{RESET}")
    print(f"Vendas Concluídas: {BOLD}{qtd_pedidos}{RESET}")
    print(f"Faturamento Bruto: {GREEN}R$ {faturamento_bruto:.2f}{RESET}")
    print(f"Ticket Médio:      {CYAN}R$ {ticket_medio:.2f}{RESET}")
    print("-" * 35)
    
    print(f"💳 {BOLD}ENTRADAS POR TIPO{RESET}")
    print(f"📱 Pix:      R$ {pix:.2f}")
    print(f"💳 Cartão:   R$ {cartao:.2f}")
    print(f"💵 Dinheiro: R$ {dinheiro:.2f}")
    print("-" * 35)

    # --- 4. BARRA DE META (O DIFERENCIAL) ---
    print(f"🎯 {BOLD}META DIÁRIA (R$ {meta:.2f}){RESET}")
    blocos = int(progresso // 10)
    barra = "█" * blocos + "░" * (10 - blocos)
    
    cor_meta = GREEN if faturamento_bruto >= meta else YELLOW
    print(f"{cor_meta}[{barra}] {progresso:.1f}%{RESET}")
    
    if faturamento_bruto >= meta:
        print(f"\n{GREEN}{BOLD}🔥 EXCELENTE! META BATIDA.{RESET}")
    
    # Simulação de lucro líquido (15% de taxas conforme você tinha)
    lucro_estimado = faturamento_bruto * 0.85
    print(f"\n{BOLD}Lucro Estimado (Líquido):{RESET} {GREEN}R$ {lucro_estimado:.2f}{RESET}")
    print(f"{RED}* Descontando taxas de 15% (Insumos/App){RESET}")
    
    pausar()

def gerenciar_marketing(nome_loja, dados):
    while True:
        l = dados[nome_loja]
        exibir_cabecalho("GERENCIAMENTO DE CUPONS")
        
        # Exibe Cupons da Plataforma se for parceiro
        if l.get('aceita_cupom_rush', False):
            print(f"{CYAN}🎟️  CUPONS RUSHBITE (ATIVOS PELA PARCERIA):{RESET}")
            print(f" • [BITE] - 15% OFF")
            print(f" • [RUSH10]     - 10% OFF")
            print("-" * 35)

        # Cupom Próprio da Loja
        cupom_id = l.get('cupom_id', 'NENHUM')
        status_c = f"{GREEN}ATIVO{RESET}" if l.get('cupom_ativo', True) else f"{RED}INATIVO{RESET}"
        print(f"{YELLOW}🎫 MEU CUPOM ATUAL:{RESET} {BOLD}{cupom_id}{RESET} ({status_c})")
        print(f" Desconto: {l.get('cupom_desc', 0)}% | Limite: {l.get('cupom_limite', '∞')}")
        
        print(f"\n{BOLD}[1]{RESET} Criar/Editar Cupom")
        print(f"{BOLD}[2]{RESET} Alternar Ativar/Desativar")
        print(f"{RED}[0] Voltar{RESET}")
        
        op = input(f"\n{BOLD}Ação: {RESET}")
        
        if op == "0": break
        elif op == "2":
            l['cupom_ativo'] = not l.get('cupom_ativo', True)
            salvar_dados(dados)
            print("✓ Status alterado!"); pausar()
        elif op == "1":
            print(f"\n{CYAN}--- NOVO CUPOM (Digite 'c' para cancelar) ---{RESET}")
            novo_id = input("Código do Cupom: ").upper()
            if novo_id.lower() == 'c': continue
            
            try:
                desc = ler_float("Porcentagem de Desconto: ")
                limite = input("Quantidade de usos (vazio para ilimitado): ")
                
                l['cupom_id'] = novo_id
                l['cupom_desc'] = desc
                l['cupom_limite'] = int(limite) if limite.isdigit() else "∞"
                l['cupom_ativo'] = True
                
                salvar_dados(dados)
                print(f"{GREEN}✓ Cupom {novo_id} criado com sucesso!{RESET}"); pausar()
            except:
                print(f"{RED}Erro na criação. Operação cancelada.{RESET}"); pausar()

def exibir_contrato_parceria(nome_loja, dados):
    exibir_cabecalho("TERMOS DE ADESÃO: RUSHBITE PARTNER")
    print(f"{BOLD}CONTRATO DE COOPERAÇÃO COMERCIAL{RESET}\n")
    print("Ao ativar esta parceria, sua loja concorda em:")
    print(f"1. {CYAN}ACEITE DE CUPONS GLOBAIS:{RESET} Permitir o uso de cupons gerados")
    print("   pela plataforma (ex: BITE, RUSH10) em seu estabelecimento.")
    print(f"2. {CYAN}RESPONSABILIDADE FINANCEIRA:{RESET} O valor do desconto oferecido")
    print("   pelos cupons da plataforma será custeado integralmente pela loja.")
    print(f"3. {CYAN}VISIBILIDADE PRIORITÁRIA:{RESET} Em troca, sua loja terá selo de")
    print("   parceiro e prioridade nos algoritmos de busca do cliente.")
    print(f"4. {CYAN}FIDELIDADE:{RESET} Participação automática em eventos sazonais.")
    
    print(f"\n{YELLOW}⚠️  IMPORTANTE: O desconto é subtraído do seu faturamento bruto.{RESET}")
    confirma = input(f"\n{GREEN}VOCÊ ACEITA OS TERMOS? (S/N): {RESET}").lower()
    
    if confirma == 's':
        dados[nome_loja]['aceita_cupom_rush'] = True
        salvar_dados(dados)
        print(f"\n{GREEN}✨ PARABÉNS! Agora você é um Parceiro Oficial RushBite.{RESET}")
    else:
        print(f"\n{RED}Adesão cancelada. Sua loja continuará no plano padrão.{RESET}")
    pausar()    

def ajustar_horarios_loja(nome_loja, dados):
    # Vacina contra o KeyError: se não achar 'lojas', busca na raiz
    loja = dados['lojas'][nome_loja] if 'lojas' in dados else dados[nome_loja]
    
    while True:
        limpar_terminal()
        exibir_cabecalho("🕒 CONFIGURAÇÃO DE HORÁRIOS")
        
        # Mostra o que está salvo atualmente
        abertura_atual = loja.get('horario_abertura', '18:00')
        fechamento_atual = loja.get('horario_fechamento', '23:00')
        
        print(f" Horário Atual: {BOLD}{abertura_atual} às {fechamento_atual}{RESET}")
        print("-" * 35)
        print(" [1] Alterar Horário de Abertura")
        print(" [2] Alterar Horário de Fechamento")
        print(f"\n [{RED}0{RESET}] Salvar e Voltar")
        
        op = input(f"\n{BOLD}Escolha: {RESET}").strip()
        
        if op == "1":
            nova = input("Nova abertura (ex: 18:00): ").strip()
            if ":" in nova:
                loja['horario_abertura'] = nova
            else:
                print(f"{RED}Formato inválido!{RESET}"); pausar()
                
        elif op == "2":
            novo = input("Novo fechamento (ex: 23:30): ").strip()
            if ":" in novo:
                loja['horario_fechamento'] = novo
            else:
                print(f"{RED}Formato inválido!{RESET}"); pausar()
                
        elif op == "0":
            salvar_dados(dados) # Salva no banco de dados
            print(f"\n{GREEN}✅ Horários atualizados e salvos!{RESET}")
            pausar()
            break
