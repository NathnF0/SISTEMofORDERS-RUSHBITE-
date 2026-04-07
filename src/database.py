import json
import os
import random
import string

ARQUIVO_EMPRESAS = "empresas.json"
ARQUIVO_PEDIDOS = "pedidos.json"

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

def atualizar_status_pedido(id_pedido, novo_status):
    pedidos = ler_todos_pedidos()
    for p in pedidos:
        if p['id'] == id_pedido:
            p['status'] = novo_status
            break
    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)