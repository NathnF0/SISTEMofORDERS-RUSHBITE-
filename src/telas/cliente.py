import os
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_pedido, ler_todos_pedidos, gerar_id_pedido, carregar_clientes, salvar_clientes, atualizar_status_pedido
from datetime import datetime

def menu_cliente(user_logado):
    while True:
        exibir_cabecalho(f"RUSHBITE | OLÁ, {user_logado.upper()}!")
        
        print(f"{CYAN}[1] 🛒 Fazer Novo Pedido{RESET}")
        print(f"{YELLOW}[2] 📋 Acompanhar Meus Pedidos{RESET}")
        print(f"{GREEN}[3] 👤 Minha Conta (Perfil){RESET}")
        print("-" * 35)
        print(f"{RED}[0] ⬅️ Sair / Logout{RESET}")
        
        op = input(f"\n{BOLD}O que deseja fazer? {RESET}")
        if op == "1": escolher_loja(user_logado)
        elif op == "2": acompanhar_pedidos_v2(user_logado)
        elif op == "3": editar_perfil_cliente(user_logado)
        elif op == "0": break

def acompanhar_pedidos_v2(user):
    while True:
        exibir_cabecalho("MEUS PEDIDOS")
        pedidos = [p for p in ler_todos_pedidos() if p.get('cliente') == user]
        
        if not pedidos:
            print(f"{YELLOW}Você ainda não fez nenhum pedido.{RESET}")
            pausar(); break
        
        print(f"{BOLD}{'Nº':<3} | {'ID':<7} | {'LOJA':<15} | {'STATUS':<15}{RESET}")
        print("-" * 45)
        
        meus_recentes = list(reversed(pedidos))[:5]
        
        for i, p in enumerate(meus_recentes, 1):
            st = p.get('status', 'Pendente')
            cor_status = GREEN if st in ["Entregue", "Finalizado", "Pronto p/ Retirada"] else YELLOW
            print(f"{i:<3} | {p['id']:<7} | {p['loja'][:15]:<15} | {cor_status}{st:<15}{RESET}")
        
        print(f"\n{CYAN}[nº]{RESET} Ver Detalhes e Chat | {RED}[0]{RESET} Voltar")
        esc = input("\nEscolha: ")
        
        if esc == "0": break
        
        try:
            p_selecionado = meus_recentes[int(esc)-1]
            detalhar_pedido_cliente(p_selecionado)
        except:
            print(f"{RED}Opção inválida!{RESET}"); pausar()

def detalhar_pedido_cliente(p):
    while True:
        exibir_cabecalho(f"DETALHES DO PEDIDO: {p['id']}")
        print(f"{BOLD}Loja:{RESET} {p['loja']}")
        st = p.get('status', 'Pendente')
        cor = GREEN if st in ["Entregue", "Finalizado"] else YELLOW
        print(f"{BOLD}Status:{RESET} {cor}{st}{RESET}")
        print(f"{BOLD}Itens:{RESET} {', '.join(p.get('itens', []))}")
        print(f"{BOLD}Total:{RESET} {GREEN}R$ {p.get('total', 0):.2f}{RESET}")
        print("-" * 40)
        
        print(f"{CYAN}💬 HISTÓRICO DE CHAT:{RESET}")
        historico = p.get('historico_chat', ["Pedido realizado com sucesso!"])
        for msg in historico:
            print(f" > {msg}")
        print("-" * 40)

        pode_avaliar = st in ["Entregue", "Finalizado"] and 'avaliacao' not in p
        
        if pode_avaliar:
            print(f"{YELLOW}[A] Avaliar este Pedido ⭐{RESET}")
        
        print(f"{CYAN}[C] Enviar Mensagem à Loja{RESET}")
        print(f"{RED}[0] Voltar{RESET}")
        
        acao = input("\nAção: ").lower().strip()
        
        if acao == "0": break
        
        elif acao == "a" and pode_avaliar:
            try:
                nota = int(input("Nota (1 a 5 estrelas): "))
                if 1 <= nota <= 5:
                    p['avaliacao'] = nota
                    atualizar_status_pedido(p['id'], st, f"Cliente avaliou com {nota}⭐")
                    print(f"\n{GREEN}✓ Obrigado pela avaliação!{RESET}")
                    pausar(); break
                else: print(f"{RED}Nota inválida!{RESET}"); pausar()
            except: print(f"{RED}Digite um número!{RESET}"); pausar()
            
        elif acao == "c":
            msg = input(f"\n{BOLD}Mensagem para {p['loja']}:{RESET} ")
            if msg:
                atualizar_status_pedido(p['id'], st, f"Cliente: {msg}")
                p.setdefault('historico_chat', []).append(f"Cliente: {msg}")
                print(f"{GREEN}✓ Mensagem enviada!{RESET}"); pausar()

def escolher_loja(user):
    dados = carregar_dados()
    lojas = list(dados.keys())
    if not lojas:
        print(f"{RED}Nenhuma loja aberta no momento.{RESET}"); pausar(); return
    
    exibir_cabecalho("RESTAURANTES DISPONÍVEIS")
    for i, n in enumerate(lojas, 1):
        l = dados[n]
        print(f"{BOLD}[{i}]{RESET} {l.get('logo','🍔')} {n:<15} | {l.get('descricao','')}")
    
    print(f"\n{RED}[0] Voltar{RESET}")
    esc = input("\nEscolha a loja: ")
    if esc == "0": return
    try:
        n_loja = lojas[int(esc)-1]
        fazer_pedido(n_loja, dados[n_loja], user)
    except: pass

def fazer_pedido(nome_loja, info, user):
    carrinho = []; total_p = 0
    while True:
        exibir_cabecalho(f"CARDÁPIO: {nome_loja}")
        prods = info.get('produtos', {})
        
        for i, (p, v) in enumerate(prods.items(), 1):
            print(f"{BOLD}[{i}]{RESET} {p:<20} | R$ {v:>6.2f}")
        
        print("-" * 30)
        print(f"{GREEN}[0] Finalizar e Ir p/ Checkout{RESET}")
        print(f"{RED}[C] Cancelar Pedido{RESET}")
        print(f"\nSubtotal: {BOLD}R$ {total_p:.2f}{RESET}")
        
        op = input("\nAdicionar item (nº): ")
        if op.lower() == 'c': return
        if op == "0":
            if carrinho: processar_checkout(nome_loja, info, carrinho, total_p, user); break
            else: print(f"{RED}Carrinho vazio!{RESET}"); pausar()
        try:
            indices = list(prods.keys())
            item_nome = indices[int(op)-1]
            carrinho.append(item_nome)
            total_p += prods[item_nome]
            print(f"{GREEN}✓ {item_nome} adicionado!{RESET}")
        except: pass

def processar_checkout(loja, info, itens, total_prod, user):
    exibir_cabecalho("CHECKOUT RUSHBITE")
    print(f"{BOLD}1.{RESET} Entrega em Casa 🚚")
    print(f"{BOLD}2.{RESET} Retirada na Loja 🏪")
    tipo = "Entrega" if input("\nOpção: ") == "1" else "Retirada"
    
    taxa = info.get('taxa_entrega', 0) if tipo == "Entrega" else 0
    clientes = carregar_clientes()
    end_salvo = clientes.get(user, {}).get('endereco', 'Não informado')
    
    # --- LÓGICA DE ENDEREÇO CORRIGIDA ---
    end_final = "Retirada na Loja"
    if tipo == "Entrega":
        print(f"\nEndereço atual: {CYAN}{end_salvo}{RESET}")
        escolha_end = input(f"{BOLD}Deseja usar este endereço? (S/N): {RESET}").lower()
        
        if escolha_end == 's' and end_salvo != 'Não informado':
            end_final = end_salvo
        else:
            end_final = input(f"{YELLOW}Digite o novo endereço de entrega: {RESET}")
            salvar = input("Deseja salvar este como seu endereço padrão? (S/N): ").lower()
            if salvar == 's':
                clientes[user]['endereco'] = end_final
                salvar_clientes(clientes)

    subtotal = total_prod + taxa
    exibir_cabecalho("PAGAMENTO")
    print(f"Total: {GREEN}R$ {subtotal:.2f}{RESET} (Taxa: R$ {taxa:.2f})")
    
    cupom = input(f"\n{CYAN}Possui um cupom?{RESET} ").upper().strip()
    desconto = 0
    mes_atual = datetime.now().month
    
    if cupom in ["RUSH10", "PASCOABITE", "NATALBITE", "RUSHFREE"]:
        if not info.get('aceita_cupom_rush', True):
            print(f"{RED}Loja não aceita cupons globais.{RESET}")
        else:
            if cupom == "PASCOABITE" and mes_atual not in [3,4]: print("Fora de época!")
            elif cupom == "NATALBITE" and mes_atual != 12: print("Fora de época!")
            else:
                if cupom == "RUSH10": desconto = subtotal * 0.10
                elif cupom == "RUSHFREE": desconto = taxa
                elif cupom == "PASCOABITE": desconto = subtotal * 0.15
                elif cupom == "NATALBITE": desconto = subtotal * 0.20
                print(f"{GREEN}✓ Cupom {cupom} aplicado!{RESET}")
    
    elif cupom == info.get('cupom_id'):
        desconto = subtotal * (info.get('cupom_desc', 0) / 100)
        print(f"{GREEN}✓ Cupom da Loja aplicado!{RESET}")

    pedido = {
        "id": gerar_id_pedido(), "cliente": user, "data": datetime.now().strftime("%H:%M"),
        "loja": loja, "itens": itens, "total": subtotal - desconto, "tipo_entrega": tipo,
        "endereco": end_final, "status": "Pendente", "historico_chat": ["Sistema: Pedido enviado!"]
    }
    salvar_pedido(pedido); print(f"\n{GREEN}🚀 PEDIDO REALIZADO COM SUCESSO!{RESET}"); pausar()

def editar_perfil_cliente(user):
    while True:
        clis = carregar_clientes(); c = clis[user]
        exibir_cabecalho("MINHA CONTA")
        print(f"{BOLD}1.{RESET} Endereço: {CYAN}{c.get('endereco','N/A')}{RESET}")
        print(f"{BOLD}2.{RESET} Telefone: {CYAN}{c.get('telefone','N/A')}{RESET}")
        print(f"{BOLD}3.{RESET} Alterar Senha")
        print(f"{RED}[0] Voltar{RESET}")
        
        op = input("\nEditar o que? ")
        if op == "1": c['endereco'] = input("Novo Endereço: ")
        elif op == "2": c['telefone'] = input("Novo Telefone: ")
        elif op == "3": c['senha'] = input("Nova Senha: ")
        elif op == "0": break
        salvar_clientes(clis); print("✓ Perfil atualizado!"); pausar()