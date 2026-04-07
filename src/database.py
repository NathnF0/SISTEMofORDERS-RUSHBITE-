import json, os, random, string

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

def atualizar_status_pedido(id_pedido, novo_status, mensagem_chat=None):
    pedidos = ler_todos_pedidos()
    for p in pedidos:
        if p['id'] == id_pedido:
            p['status'] = novo_status
            if mensagem_chat:
                if 'historico_chat' not in p: p['historico_chat'] = []
                p['historico_chat'].append(mensagem_chat)
            break
    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)