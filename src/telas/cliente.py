from src.utils import exibir_cabecalho, GREEN, RED, RESET, BOLD, YELLOW, CYAN, pausar, ler_float
from src.database import carregar_dados, salvar_pedido, ler_todos_pedidos, gerar_id_pedido
from datetime import datetime

def menu_cliente():
    while True:
        exibir_cabecalho("RushBite - Área do Cliente")
        print("1. 🛍️  Fazer Pedido")
        print("2. 🕒 Acompanhar Pedidos")
        print("0. ⬅️  Voltar")
        op = input("\nEscolha: ")
        if op == "1": escolher_loja()
        elif op == "2": acompanhar_pedidos()
        elif op == "0": break

def escolher_loja():
    dados = carregar_dados()
    lojas = list(dados.keys())
    if not lojas:
        print("Nenhuma loja aberta."); pausar(); return
    
    exibir_cabecalho("Lojas Disponíveis")
    for i, nome in enumerate(lojas, 1):
        loja = dados[nome]
        print(f"{i}. {loja.get('logo', '🍔')} {BOLD}{nome}{RESET}")
        print(f"   ↳ {loja.get('descricao', 'Melhor comida da região')}")
        print(f"   ↳ Taxa: R$ {loja.get('taxa_entrega', 0):.2f}\n")
    
    esc = input("Selecione uma loja (nº): ")
    try:
        nome_loja = lojas[int(esc)-1]
        fazer_pedido(nome_loja, dados[nome_loja])
    except: pass

def acompanhar_pedidos():
    exibir_cabecalho("Meus Pedidos Recentes")
    pedidos = ler_todos_pedidos()
    if not pedidos:
        print("Você ainda não pediu nada.")
    else:
        for p in pedidos[-5:]:
            status_cor = GREEN if p['status'] == "Entregue" else YELLOW
            print(f"{p['id']} | {p['loja']} | Status: {status_cor}{p['status']}{RESET}")
    pausar()

def fazer_pedido(nome_loja, info):
    carrinho = []; total_p = 0
    while True:
        exibir_cabecalho(f"{info.get('logo', '🍕')} {nome_loja}")
        print(f"{CYAN}Horário: {info.get('horario', 'Aberto')}{RESET}")
        print(f"Descrição: {info.get('descricao', '')}\n")
        
        prods = info['produtos']
        for i, (p, v) in enumerate(prods.items(), 1):
            print(f"{i}. {p} - R$ {v:.2f}")
        print("\n0. Finalizar Pedido")
        print("C. Cancelar e Voltar")

        op = input("\nAdicionar ao Carrinho: ")
        if op.lower() == 'c': return
        if op == "0":
            if not carrinho: return
            processar_checkout(nome_loja, info, carrinho, total_p)
            break
        try:
            lista_nomes = list(prods.keys())
            escolhido = lista_nomes[int(op)-1]
            carrinho.append(escolhido)
            total_p += prods[escolhido]
            print(f"{GREEN}✓ {escolhido} adicionado!{RESET}")
        except: pass

def processar_checkout(loja, info, itens, total_prod):
    exibir_cabecalho("Checkout Final")
    print("1. Entrega (+ Taxa)")
    print("2. Retirada na Loja (Grátis)")
    t_op = input("\nComo deseja receber? ")
    
    tipo = "Entrega" if t_op == "1" else "Retirada"
    taxa = info.get('taxa_entrega', 0) if tipo == "Entrega" else 0
    end = "Retirada Presencial"
    
    if tipo == "Entrega":
        end = input("Digite seu Endereço Completo: ")

    subtotal = total_prod + taxa
    exibir_cabecalho(f"Pagamento | Total: R$ {subtotal:.2f}")
    print("1. Cartão")
    print("2. PIX")
    print("3. Dinheiro")
    p_op = input("\nForma de Pagamento: ")
    
    f_pag = "Cartão"; troco = 0
    if p_op == "2":
        print(f"\n{YELLOW}CHAVE PIX: {info.get('chave_pix', 'Não cadastrada')}{RESET}")
        pausar(); f_pag = "PIX"
    elif p_op == "3":
        f_pag = "Dinheiro"
        valor_troco = ler_float("Precisa de troco para quanto? R$ ")
        if valor_troco > subtotal: troco = valor_troco

    cupom = input("\nCupom de Desconto: ").upper()
    desc = subtotal * 0.10 if cupom == "RUSH10" else 0
    
    pedido = {
        "id": gerar_id_pedido(),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "loja": loja,
        "itens": itens,
        "total": subtotal - desc,
        "tipo_entrega": tipo,
        "endereco": end,
        "pagamento": f_pag,
        "troco_para": troco,
        "status": "Pendente"
    }
    salvar_pedido(pedido)
    print(f"\n{GREEN}🚀 Pedido enviado! Acompanhe no menu inicial.{RESET}")
    pausar()