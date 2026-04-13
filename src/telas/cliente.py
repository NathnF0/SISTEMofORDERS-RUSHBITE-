from gzip import WRITE
import os
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_dados, salvar_pedido, ler_todos_pedidos, gerar_id_pedido, carregar_clientes, salvar_clientes, atualizar_status_pedido
from datetime import datetime
import json

def verificar_notificacoes(user):
    pedidos = ler_todos_pedidos()
    alterado = False
    for p in pedidos:
        if p.get('cliente') == user and p.get('notificado') == False:
            print(f"\n{YELLOW}🔔 NOTIFICAÇÃO: Seu pedido {p['id']} agora está: {p['status']}!{RESET}")
            p['notificado'] = True
            alterado = True
    if alterado:
        with open("pedidos.json", "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=4, ensure_ascii=False)

def menu_cliente(user_logado):
    while True:
        exibir_cabecalho(f"RUSHBITE | {user_logado.upper()}")
        verificar_notificacoes(user_logado)
        
        clis = carregar_clientes()
        pts = clis.get(user_logado, {}).get('pontos', 0)
        
        # Dashboard de Fidelidade
        progresso = pts % 10
        print(f"{YELLOW}⭐ PONTOS:{RESET} {pts} | PRÓXIMO MIMO: [{'#' * progresso}{'-' * (10-progresso)}]")
        print("-" * 40)

        print(f" [{BOLD}1{RESET}] 🛒 Explorar Restaurantes")
        print(f" [{BOLD}2{RESET}] ✨ Promoções & Novidades")
        print(f" [{BOLD}3{RESET}] 📋 Meus Pedidos")
        print(f" [{BOLD}4{RESET}] 👤 Minha Conta")
        print("-" * 40)
        print(f" [{RED}0{RESET}] ⬅️  Logout")
        
        op = input(f"\n{BOLD}Escolha: {RESET}").strip()
        
        if op == "1": escolher_loja(user_logado)
        elif op == "2": exibir_promocoes(user_logado)
        elif op == "3": acompanhar_pedidos_v2(user_logado)
        elif op == "4": editar_perfil_cliente(user_logado)
        elif op == "0": break
 
def escolher_loja(user):
    dados = carregar_dados()
    lojas = list(dados.keys())
    if not lojas:
        print(f"{RED}Nenhuma loja aberta.{RESET}"); pausar(); return
    exibir_cabecalho("RESTAURANTES DISPONÍVEIS")
    for i, n in enumerate(lojas, 1):
        l = dados[n]
        print(f"{BOLD}[{i}]{RESET} {l.get('logo','🍔')} {n:<15} | {l.get('descricao','')}")
    esc = input(f"\n{RED}[0] Voltar{RESET} | Escolha: ")
    if esc == "0": return
    try:
        n_loja = lojas[int(esc)-1]
        fazer_pedido(n_loja, dados[n_loja], user)
    except: pass

def fazer_pedido(nome_loja, info, user):
    carrinho = []; total_p = 0
    while True:
        exibir_cabecalho(f"CARDÁPIO: {nome_loja.upper()}")
        prods = info.get('produtos', {})
        estoque_loja = info.get('estoque', {})
        
        # Garante estrutura de categorias
        if not any(isinstance(v, dict) for v in prods.values()): prods = {"Geral": prods}
        
        all_items = []
        idx = 1
        
        for cat, itens in prods.items():
            if not isinstance(itens, dict): continue
            
            # Só exibe a categoria se houver itens disponíveis nela
            tem_item_na_cat = False
            bloco_cat = f"\n{CYAN}📂 {cat.upper()}{RESET}\n"
            
            for p, v in itens.items():
                qtd = estoque_loja.get(p, "∞")
                
                # SEGREDO: Se for 0, o cliente nem vê o item
                if qtd != "∞" and qtd <= 0:
                    continue
                
                bloco_cat += f"  {BOLD}[{idx}]{RESET} {p:<25} | {GREEN}R$ {v:>6.2f}{RESET}\n"
                all_items.append((p, v))
                idx += 1
                tem_item_na_cat = True
            
            if tem_item_na_cat:
                print(bloco_cat)

        if not all_items:
            print(f"\n{RED}Ops! Esta loja está sem estoque no momento.{RESET}")
            pausar(); break

        print("-" * 40)
        print(f"{BOLD}[0] Finalizar Pedido{RESET} | Subtotal: {GREEN}R$ {total_p:.2f}{RESET}")
        op = input(f"\n{CYAN}Adicionar nº{RESET} (ou {RED}'c'{RESET} para sair): ").lower()
        
        if op == 'c': break
        if op == "0":
            if carrinho: 
                processar_checkout(nome_loja, info, carrinho, total_p, user)
                break
            else: 
                print(f"{RED}Seu carrinho está vazio!{RESET}"); pausar()
        
        try:
            escolha = int(op) - 1
            if 0 <= escolha < len(all_items):
                nome_it, valor_it = all_items[escolha]
                carrinho.append(nome_it)
                total_p += valor_it
                print(f"{GREEN}✓ {nome_it} no carrinho!{RESET}")
            else:
                print(f"{RED}Nº inválido!{RESET}"); pausar()
        except: pass

def processar_checkout(loja, info, itens, total_prod, user):
    exibir_cabecalho("CHECKOUT RUSHBITE")
    
    # Simulação de tempo de entrega baseado no volume de itens
    tempo_estimado = 20 + (len(itens) * 5) 
    
    print(f"📦 {BOLD}Itens:{RESET} {len(itens)}")
    print(f"⏳ {BOLD}Previsão:{RESET} {tempo_estimado}-{tempo_estimado+10} min")
    print("-" * 35)
    
    print(f"{BOLD}1.{RESET} Entrega 🚚 | {BOLD}2.{RESET} Retirada 🏪")
    tipo = "Entrega" if input("Opção: ") == "1" else "Retirada"
    taxa = info.get('taxa_entrega', 0) if tipo == "Entrega" else 0
    clientes = carregar_clientes()
    end_padrão = clientes.get(user, {}).get('endereco', 'Não informado')
    end_final = "Retirada na Loja"
    if tipo == "Entrega":
        print(f"\nEndereço: {CYAN}{end_padrão}{RESET}")
        if input("Usar este? (S/N): ").lower() != 's':
            end_final = input("Novo endereço: ")
            if input("Salvar como padrão? (S/N): ").lower() == 's':
                clientes[user]['endereco'] = end_final
                salvar_clientes(clientes)
        else: end_final = end_padrão
    subtotal = total_prod + taxa
    exibir_cabecalho("PAGAMENTO")
    print(f"Total: {GREEN}R$ {subtotal:.2f}{RESET}")
    cupom = input("\nCupom: ").upper().strip()
    desconto = 0
    if cupom in ["RUSH10", "RUSHFREE"] and info.get('aceita_cupom_rush', True):
        desconto = subtotal * 0.10 if cupom == "RUSH10" else taxa
        print(f"{GREEN}✓ Cupom Rush aplicado!{RESET}")
    elif cupom == info.get('cupom_id'):
        desconto = subtotal * (info.get('cupom_desc', 0) / 100)
        print(f"{GREEN}✓ Cupom Loja aplicado!{RESET}")

    # Atualização de estoque segura
    dados_globais = carregar_dados()
    if loja in dados_globais:
        estoque_loja = dados_globais[loja].get('estoque', {})
        for item in itens:
            if item in estoque_loja and estoque_loja[item] != "∞":
                try:
                    v = int(estoque_loja[item])
                    if v > 0: estoque_loja[item] = v - 1
                except: pass
        dados_globais[loja]['estoque'] = estoque_loja
        salvar_dados(dados_globais)

    pedido = {
        "id": gerar_id_pedido(), "cliente": user, "data": datetime.now().strftime("%H:%M"),
        "loja": loja, "itens": itens, "total": subtotal - desconto, "tipo_entrega": tipo,
        "endereco": end_final, "status": "Pendente", "notificado": True,
        "historico_chat": ["Sistema: Pedido enviado!"]
    }
    salvar_pedido(pedido); print(f"\n{GREEN}🚀 SUCESSO!{RESET}"); pausar()

def acompanhar_pedidos_v2(user):
    while True:
        exibir_cabecalho("MEUS PEDIDOS")
        pedidos = [p for p in ler_todos_pedidos() if p.get('cliente') == user]
        if not pedidos: print(f"{YELLOW}Nenhum pedido.{RESET}"); pausar(); break
        meus = list(reversed(pedidos))[:5]
        for i, p in enumerate(meus, 1):
            st = p.get('status', 'Pendente')
            cor = GREEN if st in ["Entregue", "Finalizado"] else YELLOW
            print(f"[{i}] {p['id']} | {p['loja'][:12]:<12} | {cor}{st}{RESET}")
        esc = input(f"\n{CYAN}[nº]{RESET} Detalhes | {RED}[0]{RESET} Voltar: ")
        if esc == "0": break
        try: detalhar_pedido_cliente(meus[int(esc)-1])
        except: pass

def detalhar_pedido_cliente(p):
    while True:
        exibir_cabecalho(f"PEDIDO: {p['id']}")
        print(f"Loja: {p['loja']} | Status: {p['status']}")
        print(f"Itens: {', '.join(p['itens'])}")
        print(f"Total: R$ {p['total']:.2f}")
        print("-" * 30)
        for msg in p.get('historico_chat', []): print(f" > {msg}")
        acao = input(f"\n{CYAN}[C]{RESET} Mensagem | {RED}[0]{RESET} Voltar: ").lower()
        if acao == "0": break
        elif acao == "c":
            msg = input("Sua mensagem: ")
            if atualizar_status_pedido(p['id'], p['status'], f"Cliente: {msg}"):
                p.setdefault('historico_chat', []).append(f"Cliente: {msg}")

def editar_perfil_cliente(user):
    while True:
        clis = carregar_clientes()
        if user not in clis: break
        c = clis[user]
        end = c.get('endereco', {})
        
        exibir_cabecalho("👤 MINHA CONTA / ENDEREÇO")
        print(f"{BOLD}Nome:{RESET} {user}")
        print(f"{BOLD}Telefone:{RESET} {c.get('telefone','(não informado)')}")
        print("-" * 30)
        
        print(f"{CYAN}📝 ENDEREÇO ATUAL:{RESET}")
        # SEGREDO: Se o endereço for um dicionário (estruturado), exibe campo por campo
        if isinstance(end, dict) and end:
            print(f" Rua: {end.get('rua','')}, Nº {end.get('numero','')}")
            print(f" Bairro: {end.get('bairro','')}")
            if end.get('cep'): print(f" CEP: {end.get('cep','')}")
            if end.get('complemento'): print(f" Ref: {end.get('complemento','')}")
        else:
            print(f" Endereço: {end if end else '(não informado)'}")
            if end: print(f"{RED}(* Recomendamos atualizar para o formato novo){RESET}")
        
        print(f"\n[{BOLD}1{RESET}] Atualizar Telefone")
        print(f"[{BOLD}2{RESET}] 🏠 Atualizar Endereço")
        print(f"[{RED}0{RESET}] Voltar")
        
        op = input(f"\n{BOLD}Escolha: {RESET}")
        
        if op == "0": break
        elif op == "1":
            c['telefone'] = input("Novo Telefone: ")
            salvar_clientes(clis); print(f"\n{GREEN}✓ Telefone atualizado!{RESET}"); pausar()
        elif op == "2":
            # --- PASSO A PASSO ESTRUTURADO DO ENDEREÇO ---
            print(f"\n{CYAN}--- CADASTRO DE ENDEREÇO ---{RESET}")
            novo_end = {}
            novo_end['rua'] = input(f"{BOLD}Nome da Rua:{RESET} ").strip()
            if not novo_end['rua']: print(f"{RED}Rua é obrigatória!{RESET}"); pausar(); continue
            
            novo_end['numero'] = input(f"{BOLD}Número:{RESET} ").strip()
            novo_end['bairro'] = input(f"{BOLD}Bairro:{RESET} ").strip()
            
            if input("Você sabe o seu CEP? (S/N): ").lower() == 's':
                novo_end['cep'] = input("Digite o CEP: ").strip()
            
            novo_end['complemento'] = input("Referência ou Complemento (opcional): ").strip()
            
            # Salva como um dicionário estruturado
            c['endereco'] = novo_end
            salvar_clientes(clis)
            print(f"\n{GREEN}🏠 ✨ Endereço salvo e estruturado!{RESET}")
            pausar()

def exibir_promocoes(user):
    dados = carregar_dados()
    exibir_cabecalho("✨ PROMOÇÕES & NOVIDADES ✨")
    
    tem_promo = False
    
    # 1. Checar lojas com cupons próprios ativos
    print(f"{YELLOW}🎫 CUPONS DE LOJAS DISPONÍVEIS:{RESET}")
    for nome_loja, info in dados.items():
        if info.get('cupom_ativo') and info.get('cupom_id'):
            print(f" • {BOLD}{nome_loja:<15}{RESET} -> Cupom: {GREEN}{info['cupom_id']}{RESET} ({info['cupom_desc']}% OFF)")
            tem_promo = True
            
    # 2. Checar lojas que aceitam cupons da plataforma (Parceiras)
    print(f"\n{CYAN}🤝 PARCEIROS RUSHBITE (Aceitam RUSH10):{RESET}")
    parceiros = [nome for nome, info in dados.items() if info.get('aceita_cupom_rush')]
    
    if parceiros:
        for p in parceiros:
            print(f" • {p} {YELLOW}★{RESET}")
        tem_promo = True
    else:
        print(" Nenhuma loja parceira no momento.")

    if not tem_promo:
        print(f"\n{RED}Nenhuma promoção ativa hoje. Fique de olho!{RESET}")
    
    print(f"\n{BOLD}[1]{RESET} Ir para Restaurantes | {RED}[0]{RESET} Voltar")
    op = input("\nEscolha: ")
    if op == "1": escolher_loja(user)            
