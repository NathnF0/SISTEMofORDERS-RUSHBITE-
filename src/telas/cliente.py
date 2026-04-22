import os
import json      
import random   
import time      
from datetime import datetime
from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import (carregar_dados, salvar_dados, salvar_pedido, ler_todos_pedidos, gerar_id_pedido, carregar_clientes, salvar_clientes, atualizar_status_pedido, obter_status_nivel)
from src.telas.empresa import limpar_terminal

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
        limpar_terminal()

        nome_cliente = user_logado.get('nome', 'Cliente').upper()
        exibir_cabecalho(f"RUSHBITE - CLIENTE | {nome_cliente}")
        
        verificar_notificacoes(user_logado)

    # --- Dashboard de Level (v0.3.0) ---
        nivel = user_logado.get('level', 'Bronze')
        xp = user_logado.get('xp', 0)
        
        print(f"{YELLOW}⭐ LEVEL: {nivel} ({xp} XP){RESET}")
        
        # Barra de progresso: garante que o desenho seja sempre de 10 caracteres
        progresso = min(xp // 10, 10) 
        barra = f"[{'#' * progresso}{'-' * (10 - progresso)}]"
        
        print(barra)
        print("-" * 40)

        print(f" [{BOLD}1{RESET}] 🛒 Explorar Cardápios")
        print(f" [{BOLD}2{RESET}] 🎰 ROLETA DA FOME (Surpresa!)")
        print(f" [{BOLD}3{RESET}] ✨ Promoções da Semana")
        print(f" [{BOLD}4{RESET}] 📋 Meus Pedidos")
        print(f" [{BOLD}5{RESET}] 👤 Meu Perfil Rush")
        print("-" * 40)
        print(f" [{RED}0{RESET}] ⬅️  Sair")
        
        op = input(f"\n{BOLD}Escolha: {RESET}").strip()
        
        if op == "1": escolher_loja(user_logado)
        elif op == "2": roleta_da_fome(user_logado)
        elif op == "3": exibir_promocoes(user_logado)
        elif op == "4": acompanhar_pedidos_v2(user_logado)
        elif op == "5": tela_meu_perfil(user_logado)
        elif op == "0": break
 
def escolher_loja(user):
    dados = carregar_dados()
    lojas = list(dados.keys())
    
    if not lojas:
        print(f"{RED}Nenhuma loja cadastrada.{RESET}"); pausar(); return
        
    exibir_cabecalho("RESTAURANTES DISPONÍVEIS")
    
    for i, n in enumerate(lojas, 1):
        l = dados[n]
        status = l.get('status', 'Aberto').strip().capitalize()
    # Se o status for qualquer coisa diferente de "Aberto", ele assume como Fechado
        if status == "Aberto":
            cor_status = GREEN
        else:
            cor_status = RED
            status = "Fechado" # Padroniza a exibição
        
        print(f"{BOLD}[{i}]{RESET} {l.get('logo','🍔')} {n:<15} | {cor_status}[{status}]{RESET} | {l.get('descricao','')}")

    esc = input(f"\n{RED}[0] Voltar{RESET} | Escolha: ")
    if esc == "0": return
    
    try:
        n_loja = lojas[int(esc)-1]
        info_loja = dados[n_loja]

        # --- A TRAVA DE SEGURANÇA ---
        if info_loja.get('status') == "Fechado":
            print(f"\n{RED}❌ DESCULPE! A loja {n_loja} está fechada.{RESET}")
            pausar()
            return # Aqui ele barra a entrada na função fazer_pedido
            
        fazer_pedido(n_loja, info_loja, user)
    except: 
        pass

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

def selecionar_metodo_pagamento(total, user): # <-- ADICIONEI O 'user' AQUI
    """Simulador de Gateway de Pagamento para a v0.3.0"""
    exibir_cabecalho("PAGAMENTO")
    
    # Agora o Python sabe quem é o user e não vai travar!
    print(f"Total a pagar: {GREEN}R$ {total:.2f}{RESET}")
    print(f"Cliente: {BOLD}{user.get('nome', 'Não identificado')}{RESET}")
    
    print(f"\n[{BOLD}1{RESET}] Pix (Instantâneo)")
    print(f"[{BOLD}2{RESET}] Cartão de Crédito")
    print(f"[{BOLD}3{RESET}] Pagar na Entrega")
    print("-" * 35)
    print(f"[{RED}0{RESET}] Cancelar Checkout")
    
    op = input(f"\n{BOLD}Escolha: {RESET}").strip()
    
    if op in ["1", "2"]:
        metodo = "Pix" if op == "1" else "Cartão"
        print(f"\n{CYAN}💳 Conectando ao Gateway...{RESET}")
        time.sleep(1.5)
        
        if metodo == "Pix":
            # Usando random e time que você já tem no sistema
            print(f"Chave Pix: {YELLOW}RUSH-{random.randint(100,999)}-PAY{RESET}")
            time.sleep(2)
        
        print(f"{GREEN}✅ Transação Aprovada!{RESET}")
        return metodo
    
    elif op == "3":
        print(f"{YELLOW}Aviso: O pagamento será feito ao entregador.{RESET}")
        return "Entrega"
    
    return False


def processar_checkout(loja, info, itens, total_prod, user):
    """Fluxo de finalização de pedido v0.3.5 - Com Trava de Cupons Reais"""
    exibir_cabecalho("CHECKOUT RUSHBITE")
    
    # --- 1. PREVISÃO E LOGÍSTICA ---
    tempo_estimado = 20 + (len(itens) * 5) 
    print(f"📦 {BOLD}Itens:{RESET} {len(itens)} | ⏳ {BOLD}Previsão:{RESET} {tempo_estimado} min")
    
    print(f"\n{BOLD}1.{RESET} Entrega 🚚 | {BOLD}2.{RESET} Retirada 🏪")
    tipo = "Entrega" if input("Opção: ") == "1" else "Retirada"
    taxa = info.get('taxa_entrega', 0) if tipo == "Entrega" else 0
    
    # --- 2. ENDEREÇO ---
    clientes = carregar_clientes()
    end_padrao = user.get('endereco', 'Não informado')
    
    if tipo == "Entrega":
        rua = end_padrao.get('rua', 'Sem Rua') if isinstance(end_padrao, dict) else end_padrao
        print(f"\nEnviar para: {CYAN}{rua}{RESET}")
        if input("Confirmar? (S/N): ").lower() != 's':
            end_final = input("Digite o novo endereço completo: ")
        else:
            end_final = end_padrao
    else:
        end_final = "Retirada na Loja"

    # --- 3. DESCONTOS (O CORAÇÃO DA v0.3.5) ---
    subtotal = total_prod + taxa
    
   # Pegamos o XP direto do objeto 'user' para evitar o erro de 'unhashable type'
    xp_usuario = user.get('xp', 0)
    nivel, desc_nivel = obter_status_nivel(xp_usuario)
    
    # Mantendo o cálculo original com o subtotal
    valor_desc_nivel = subtotal * desc_nivel
    if desc_nivel > 0:
        print(f"{YELLOW}⭐ Vantagem {nivel}: -R$ {valor_desc_nivel:.2f} ({desc_nivel*100:.0f}% OFF){RESET}")
    
    total_com_nivel = subtotal - valor_desc_nivel
    print(f"Total Parcial: {GREEN}R$ {total_com_nivel:.2f}{RESET}")
    
    # B) Sistema de Cupons Reais (Carteira do Usuário)
    cupons_disponiveis = user.get('cupons_ativos', [])
    if cupons_disponiveis:
        print(f"\n{CYAN}🎟️ Seus Cupons:{RESET}")
        for cp in cupons_disponiveis:
            print(f" - {BOLD}{cp['codigo']}{RESET} (R$ {cp['valor']} OFF | Mínimo: R$ {cp['minimo']})")
    
    cupom_digitado = input("\nDigite o cupom (ou Enter para pular): ").upper().strip()
    desconto_cupom = 0
    
    if cupom_digitado:
        cupom_valido = None
        # Procura o cupom na carteira do usuário
        for cp in cupons_disponiveis:
            if cp['codigo'] == cupom_digitado:
                cupom_valido = cp
                break
        
        if cupom_valido:
            # TRAVA DE VALOR MÍNIMO
            if total_com_nivel >= cupom_valido['minimo']:
                desconto_cupom = cupom_valido['valor']
                print(f"{GREEN}✓ Cupom Aplicado: -R$ {desconto_cupom:.2f}{RESET}")
                
                # REMOVE O CUPOM DA CARTEIRA
                cupons_disponiveis.remove(cupom_valido)
                
                # CORREÇÃO AQUI: Pegamos o login/nome para não quebrar o dicionário
                id_usuario = user.get('login') or user.get('nome')
                if id_usuario in clientes:
                    clientes[id_usuario]['cupons_ativos'] = cupons_disponiveis
                    # Importante: O objeto 'user' na memória também precisa ser atualizado
                    user['cupons_ativos'] = cupons_disponiveis
            else:
                print(f"{RED}❌ Pedido abaixo do mínimo de R$ {cupom_valido['minimo']:.2f}{RESET}")
        else:
            # Se não for cupom da loja, checa os cupons globais/fixos
            if cupom_digitado == "RUSH10":
                desconto_cupom = total_com_nivel * 0.10 # Use o total com nível para o cálculo
                print(f"{GREEN}✓ Cupom Global aplicado!{RESET}")
            else:
                print(f"{RED}❌ Cupom inválido ou não pertence a você!{RESET}")
        
        pausar() # Dá tempo do usuário ler o que aconteceu com o cupom

    # --- 4. PAGAMENTO ---
    total_final = max(0, total_com_nivel - desconto_cupom)

    metodo_pago = selecionar_metodo_pagamento(total_final, user) # Adicionei o user aqui
    
    if not metodo_pago:
        print(f"\n{RED}❌ Pedido cancelado no pagamento.{RESET}")
        pausar()
        return

    # --- DENTRO DA FUNÇÃO processar_checkout ---

    # 1. Extraímos o nome do cliente de forma segura (usando a variável 'user')
    nome_cliente = user.get('nome') if isinstance(user, dict) else user

    novo_pedido = {
    "id": f"#{gerar_id_pedido()}",
    "cliente": nome_cliente, # Agora o sistema sabe QUEM pediu
    "loja": loja,            # Agora o sistema sabe PARA ONDE vai o pedido
    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "itens": itens,
    "total": total_final,     # Certifique-se que 'total_final' é o valor com descontos
    "status": "Pendente",
    "historico_chat": [f"Sistema: Pedido realizado em {loja}"]
    }

    # 2. Salva no arquivo correto
    salvar_pedido(novo_pedido)

    print(f"\n{GREEN}✔ Pedido enviado com sucesso para {loja}!{RESET}")
    pausar()

# --- 5. SUCESSO E SALVAMENTO ---
    xp_ganho = 20
    
    # 1. Pegamos o login (String) para usar como chave no dicionário 'clientes'
    id_usuario = user.get('login') or user.get('nome')
    
    # 2. Atualizamos o XP no dicionário que será salvo no JSON
    # Pegamos o XP que já estava no arquivo e somamos o ganho
    clientes[id_usuario]['xp'] = clientes[id_usuario].get('xp', 0) + xp_ganho
    
    # 3. MUITO IMPORTANTE: Atualizamos o objeto 'user' que está na memória
    # Se não fizer isso, o menu vai mostrar o XP antigo até o cara deslogar
    user['xp'] = clientes[id_usuario]['xp']

    # 4. Salvamos tudo no arquivo
    salvar_clientes(clientes)
    
    print(f"\n{GREEN}✅ Pedido finalizado com sucesso!{RESET}")
    print(f"{YELLOW}⭐ Você ganhou {xp_ganho} XP!{RESET}")
    pausar()
    
def acompanhar_pedidos_v2(user):
    # 1. Extraímos a string do nome
    nome_usuario = user.get('nome') if isinstance(user, dict) else user

    while True:
        limpar_terminal()
        exibir_cabecalho("MEUS PEDIDOS")
        
        # 2. CARREGAR OS DADOS ATUALIZADOS DO ARQUIVO
        todos_pedidos = ler_todos_pedidos()
        
        # 3. FILTRO CORRIGIDO: Agora usamos 'nome_usuario'
        pedidos = [p for p in todos_pedidos if p.get('cliente') == nome_usuario]
        
        if not pedidos: 
            print(f"{YELLOW}Nenhum pedido encontrado para {nome_usuario}.{RESET}")
            pausar()
            break
            
        meus = list(reversed(pedidos))[:5]
        
        for i, p in enumerate(meus, 1):
            st = p.get('status', 'Pendente')
            # Diferenciando cores por status (v0.3.0)
            cor = GREEN if st in ["Entregue", "Finalizado"] else (RED if st == "Cancelado" else YELLOW)
            
            # Usamos .get() para garantir que, se não existir 'id', o programa não dê erro
            id_pedido = p.get('id', '#????')
            nome_loja = p.get('loja', 'Desconhecida')[:12]

            print(f"[{i}] {id_pedido} | {nome_loja:<12} | {cor}{st}{RESET}")
            
        esc = input(f"\n{CYAN}[nº]{RESET} Detalhes | {RED}[0]{RESET} Voltar: ").strip()
        
        if esc == "0": 
            break
            
        try:
            indice = int(esc) - 1
            if 0 <= indice < len(meus):
                detalhar_pedido_cliente(meus[indice])
            else:
                print(f"{RED}Opção inválida!{RESET}")
                pausar()
        except ValueError:
            print(f"{RED}Digite um número válido!{RESET}")
            pausar()

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
    # --- AJUSTE DE IDENTIDADE (v0.3.0) ---
    # Se 'user' for o dicionário completo, pegamos o nome. Se for string, usamos ela.
    nome_usuario = user.get('nome') if isinstance(user, dict) else user
    
    while True:
        clis = carregar_clientes()
        if nome_usuario not in clis: 
            print(f"{RED}Erro: Usuário '{nome_usuario}' não encontrado!{RESET}")
            pausar()
            break
        c = clis[nome_usuario]
        end = c.get('endereco', {})
        
        limpar_terminal()
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

import random

def roleta_da_fome(user):
    exibir_cabecalho("🎰 ROLETA DA FOME")
    print(f"{YELLOW}Não sabe o que comer? Deixe o RushBite decidir!{RESET}")
    print(f"Sugeriremos um item aleatório com {BOLD}15% de Desconto{RESET}!")
    
    pausar()
    
    dados = carregar_dados()
    todas_opcoes = []
    
    # Coleta as opções de todas as lojas abertas
    for loja_nome, info in dados.items():
        # Ignora chaves que não são lojas (se houver)
        if isinstance(info, dict) and info.get('aberta', True):
            for cat, itens in info.get('produtos', {}).items():
                if isinstance(itens, dict):
                    for p, v in itens.items():
                        # Verifica estoque
                        if info.get('estoque', {}).get(p, 1) != 0:
                            todas_opcoes.append((loja_nome, p, v, info))

    if not todas_opcoes:
        print(f"{RED}Nenhuma loja aberta no momento para girar a roleta.{RESET}")
        pausar()
        return

    while True:
        loja_sorteada, prato, preco_original, info_loja = random.choice(todas_opcoes)
        preco_com_desconto = preco_original * 0.85

        limpar_terminal()
        exibir_cabecalho("🎰 RESULTADO")
        print(f"\n{CYAN}A ROLETA PAROU EM...{RESET}")
        print(f"🏪 Loja: {BOLD}{loja_sorteada}{RESET}")
        print(f"🍔 Prato: {BOLD}{prato}{RESET}")
        print(f"💰 De: R$ {preco_original:.2f} por {GREEN}R$ {preco_com_desconto:.2f}{RESET}")
        print("-" * 35)
        
        # Mostra o XP atual que está no dicionário do usuário
        print(f"Seu saldo: {YELLOW}{user.get('xp', 0)} XP{RESET}")
        print("-" * 35)
        print(f" [{BOLD}1{RESET}] ACEITO O DESAFIO! (Checkout)")
        print(f" [{BOLD}2{RESET}] Girar novamente (Gasta 5 XP)")
        print(f" [{RED}0{RESET}] Desistir e Voltar")
        
        op = input(f"\n{BOLD}Escolha: {RESET}").strip()

        if op == "1":
            # Criamos o dicionário do item para o checkout
            itens_roleta = {prato: preco_com_desconto}
            # Passamos o objeto 'user' completo para evitar o erro de AttributeError
            processar_checkout(loja_sorteada, info_loja, itens_roleta, preco_com_desconto, user)
            break 
            
        elif op == "2":
            # Pegamos o XP direto do objeto user que já está na memória
            if user.get('xp', 0) >= 5:
                user['xp'] -= 5
                # Sincronizamos com o arquivo de clientes
                clientes = carregar_clientes()
                # Usamos o login (nome) do user para salvar no lugar certo
                login_usuario = user.get('login') or user.get('nome')
                if login_usuario in clientes:
                    clientes[login_usuario]['xp'] = user['xp']
                    salvar_clientes(clientes)
                
                print(f"{YELLOW}🔄 Girando de novo... (-5 XP){RESET}")
                time.sleep(1)
                continue 
            else:
                print(f"{RED}❌ XP insuficiente para girar novamente!{RESET}")
                pausar()
        
        elif op == "0":
            break
        else:
            continue


def tela_meu_perfil(user_logado):
    limpar_terminal()
    exibir_cabecalho("MEU PERFIL RUSH")
    
    # 1. SEGURANÇA: Extrair o nome não importa como ele venha
    if isinstance(user_logado, dict):
        nome_busca = user_logado.get('nome')
    else:
        nome_busca = user_logado

    # 2. Carregar o banco de clientes
    clientes = carregar_clientes()
    
    # 3. Buscar os dados (c é o dicionário com XP, endereço, etc.)
    c = clientes.get(nome_busca)

    # Se não achar, vamos imprimir o que está acontecendo para debugar
    if not c:
        print(f"{RED}❌ Erro: '{nome_busca}' não encontrado no banco.{RESET}")
        print(f"{YELLOW}Nomes cadastrados: {list(clientes.keys())}{RESET}")
        pausar()
        return

    # 4. Se achou, extrai os dados
    xp = c.get('xp', 0)
    nivel, desconto = obter_status_nivel(xp)
    
    # Barra de progresso (v0.3.0)
    progresso = (xp % 100) // 10
    barra = "█" * progresso + "░" * (10 - progresso)

    # Primeiro, extraímos o nome de dentro do dicionário
    nome_usuario = user_logado.get('nome', 'Usuário')

    # Mostra os dados atuais
    print(f"👤 Usuário: {BOLD}{nome_usuario.upper()}{RESET}")
    print(f"⭐ Nível: {YELLOW}{nivel}{RESET}")
    print(f"📈 Progresso: {CYAN}[{barra}]{RESET} {xp} XP")
    print(f"💰 Benefício Atual: {GREEN}{desconto*100:.0f}% OFF fixo{RESET}")
    print("-" * 40)
    
    # Mostra os dados atuais
    print(f"📍 Endereço: {c.get('endereco', 'Não informado')}")
    print(f"📱 Telefone: {c.get('telefone', 'Não informado')}")
    print("-" * 40)

    # --- AQUI ENTRA A ESCOLHA (Onde era o seu Editar Perfil antigo) ---
    print(f" [{BOLD}1{RESET}] ✏️  Editar Meus Dados")
    print(f" [{BOLD}2{RESET}] 🛒  Trocar XP por Cupons")
    print(f" [{BOLD}0{RESET}] ⬅️  Voltar ao Menu")
    
    op = input(f"\n{BOLD}Escolha uma opção: {RESET}").strip()

    if op == "1":
        # Aqui você chama a função que já existia antes!
        editar_perfil_cliente(user_logado) 
        # Após editar, chama a tela de perfil de novo para atualizar os dados na visão do usuário
        tela_meu_perfil(user_logado) 
    elif op == "2":
        loja_de_cupons(user_logado)
        tela_meu_perfil(user_logado)    
    elif op == "0":
        return 
    else:
        print(f"{RED}Opção inválida!{RESET}")
        pausar()

def loja_de_cupons(user_logado):
    # 1. Extraímos o nome (string) para usar como chave no dicionário 'clientes'
    nome_usuario = user_logado.get('nome') if isinstance(user_logado, dict) else user_logado
    limpar_terminal()
    exibir_cabecalho("🎟️ LOJA DE CUPONS RUSH")
    
    clientes = carregar_clientes()

    dados_banco = clientes.get(nome_usuario, {})
    xp_atual = dados_banco.get('xp', 0)
    nivel, _ = obter_status_nivel(xp_atual)
    
    print(f"Seu Status: {YELLOW}{nivel}{RESET} | Seu Saldo: {CYAN}{xp_atual} XP{RESET}\n")

    # Definição dos Cupons e suas Travas
    opcoes = {
        "1": {"nome": "Cupom R$ 5",  "xp": 60,  "min": 35,  "nivel": "BRONZE", "valor": 5},
        "2": {"nome": "Cupom R$ 15", "xp": 150, "min": 80,  "nivel": "PRATA",  "valor": 15},
        "3": {"nome": "Cupom R$ 30", "xp": 350, "min": 150, "nivel": "OURO",   "valor": 30}
    }

    for k, v in opcoes.items():
        cor = GREEN if nivel in v['nivel'] or (v['nivel'] == "BRONZE") or (v['nivel'] == "PRATA" and nivel == "OURO") else RED
        status_trava = "✅ Liberado" if cor == GREEN else f"🔒 Bloqueado (Requer {v['nivel']})"
        
        print(f" [{BOLD}{k}{RESET}] {v['nome']}")
        print(f"     Custo: {v['xp']} XP | Pedido Mínimo: R$ {v['min']}")
        print(f"     Status: {cor}{status_trava}{RESET}\n")

    print(f" [{RED}0{RESET}] Sair da Loja")
    
    escolha = input(f"\n{BOLD}Qual cupom deseja resgatar? {RESET}").strip()
    if escolha == "0": 
        return
    
    if escolha in opcoes:
        item = opcoes[escolha]
        
        # 1. VALIDAÇÃO DE NÍVEL
        pode_comprar = False
        if item['nivel'] == "BRONZE": pode_comprar = True
        elif item['nivel'] == "PRATA" and any(n in nivel for n in ["PRATA", "OURO", "RUSH MASTER"]): pode_comprar = True
        elif item['nivel'] == "OURO" and any(n in nivel for n in ["OURO", "RUSH MASTER"]): pode_comprar = True

        # 2. CHECAGEM DE REQUISITOS
        if not pode_comprar:
            print(f"\n{RED}❌ Nível insuficiente!{RESET}")
            pausar()
        elif xp_atual < item['xp']:
            print(f"\n{RED}❌ XP insuficiente!{RESET}")
            pausar()
        else:
            # 3. SE CHEGOU AQUI, TUDO OK! EFETUA A COMPRA:
            print(f"\n{YELLOW}Gerando seu cupom...{RESET}")
            
            # Desconta o XP (no banco e na memória)
            clientes[nome_usuario]['xp'] -= item['xp']
            user_logado['xp'] -= item['xp'] 
            
            # Gerencia o cupom
            codigo = f"RUSH{item['valor']}-{random.randint(1000, 9999)}"
            
            if 'cupons_ativos' not in user_logado:
                user_logado['cupons_ativos'] = []
            
            novo_cupom = {"codigo": codigo, "valor": item['valor'], "minimo": item['min']}
            user_logado['cupons_ativos'].append(novo_cupom)
            clientes[nome_usuario]['cupons_ativos'] = user_logado['cupons_ativos']
            
            salvar_clientes(clientes)
            print(f"\n{GREEN}✅ RESGATADO: {BOLD}{codigo}{RESET}")
            pausar()
            
    else:
        print(f"{RED}Opção inválida!{RESET}")
        pausar()