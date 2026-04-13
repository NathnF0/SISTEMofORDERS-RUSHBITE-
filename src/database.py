import json
import os
import random
import string

ARQUIVO_EMPRESAS = "empresas.json"
ARQUIVO_PEDIDOS = "pedidos.json"
ARQUIVO_CLIENTES = "clientes.json"

def gerar_id_pedido():
    return "#" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

def carregar_dados():
    if not os.path.exists(ARQUIVO_EMPRESAS): return {}
    with open(ARQUIVO_EMPRESAS, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def salvar_dados(dados):
    with open(ARQUIVO_EMPRESAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_clientes():
    if not os.path.exists(ARQUIVO_CLIENTES): return {}
    with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def salvar_clientes(clientes):
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

def ler_todos_pedidos():
    if not os.path.exists(ARQUIVO_PEDIDOS): return []
    with open(ARQUIVO_PEDIDOS, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return []

def salvar_pedido(pedido):
    pedidos = ler_todos_pedidos()
    pedidos.append(pedido)
    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)
    
    clientes = carregar_clientes()
    user = pedido.get('cliente')
    if user in clientes:
        pontos_ganhos = int(pedido.get('total', 0) // 10)
        clientes[user]['pontos'] = clientes[user].get('pontos', 0) + pontos_ganhos
        salvar_clientes(clientes)

def atualizar_status_pedido(id_pedido, novo_status, mensagem_chat=None):
    pedidos = ler_todos_pedidos()
    foi_atualizado = False
    for p in pedidos:
        if p.get('id') == id_pedido:
            p['status'] = novo_status
            p['notificado'] = False 
            if mensagem_chat:
                p.setdefault('historico_chat', []).append(mensagem_chat)
            foi_atualizado = True
            break
    if foi_atualizado:
        with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=4, ensure_ascii=False)
    return foi_atualizado