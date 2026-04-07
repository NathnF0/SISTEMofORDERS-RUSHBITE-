from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_pedido, ler_todos_pedidos, gerar_id_pedido, carregar_clientes, salvar_clientes
from datetime import datetime

def menu_cliente(user_logado):
    while True:
        exibir_cabecalho(f"RUSHBITE | OLÁ, {user_logado}!")
        
        print(f"{CYAN}[1] 🛒 Fazer Novo Pedido{RESET}")
        print(f"{YELLOW}[2] 📋 Acompanhar Meus Pedidos{RESET}")
        print(f"{GREEN}[3] 👤 Minha Conta (Perfil){RESET}")
        print("-" * 30)
        print(f"{RED}[0] ⬅️ Sair / Logout{RESET}")
        
        op = input(f"\n{BOLD}O que deseja fazer? {RESET}")
        if op == "1": escolher_loja(user_logado)
        elif op == "2": acompanhar_pedidos(user_logado)
        elif op == "3": editar_perfil_cliente(user_logado)
        elif op == "0": break

def acompanhar_pedidos(user):
    exibir_cabecalho("MEUS PEDIDOS")
    pedidos = [p for p in ler_todos_pedidos() if p.get('cliente') == user]
    
    if not pedidos:
        print(f"{YELLOW}Você ainda não fez nenhum pedido.{RESET}"); pausar(); return
    
    for p in reversed(pedidos[-5:]):
        cor_status = GREEN if p['status'] in ["Entregue", "Finalizado"] else YELLOW
        print(f"{BOLD}ID: {p['id']}{RESET} | Loja: {p['loja']}")
        print(f"Status: {cor_status}{p['status']}{RESET} | Valor: R$ {p['total']:.2f}")
        
        if 'historico_chat' in p and p['historico_chat']:
            print(f"💬 {CYAN}Última msg: {p['historico_chat'][-1]}{RESET}")
        print("-" * 40)
    pausar()

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
        prods = info['produtos']
        
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
    end = clientes[user].get('endereco', 'Não informado')
    
    if tipo == "Entrega" and (not end or end == "Não informado"):
        end = input(f"{YELLOW}Endereço não cadastrado. Digite agora:{RESET} ")
        clientes[user]['endereco'] = end; salvar_clientes(clientes)

    subtotal = total_prod + taxa
    exibir_cabecalho("PAGAMENTO")
    print(f"Total: {GREEN}R$ {subtotal:.2f}{RESET} (Taxa: R$ {taxa:.2f})")
    
    # --- SISTEMA DE CUPONS ---
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
        "endereco": end, "status": "Pendente", "historico_chat": ["Sistema: Pedido enviado!"]
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