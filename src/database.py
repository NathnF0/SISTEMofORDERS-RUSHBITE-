import json
import os
import random
import string

ARQUIVO_EMPRESAS = "empresas.json"
ARQUIVO_PEDIDOS = "pedidos.json"
ARQUIVO_CLIENTES = "clientes.json"

# --- UTILITÁRIOS ---
def gerar_id_pedido():
    """Gera um ID único estilo #A1B2"""
    return "#" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

# --- GESTÃO DE EMPRESAS ---
def carregar_dados():
    if not os.path.exists(ARQUIVO_EMPRESAS): 
        return {}
    with open(ARQUIVO_EMPRESAS, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except: 
            return {}

def salvar_dados(dados):
    with open(ARQUIVO_EMPRESAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- GESTÃO DE CLIENTES ---
def carregar_clientes():
    if not os.path.exists(ARQUIVO_CLIENTES): 
        return {}
    with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except: 
            return {}

def salvar_clientes(clientes):
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

# --- GESTÃO DE PEDIDOS (O CORAÇÃO DA v0.2.6) ---
def ler_todos_pedidos():
    if not os.path.exists(ARQUIVO_PEDIDOS): 
        return []
    with open(ARQUIVO_PEDIDOS, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except: 
            return []

def salvar_pedido(pedido):
    pedidos = ler_todos_pedidos()
    pedidos.append(pedido)
    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)

def atualizar_status_pedido(id_pedido, novo_status, mensagem_chat=None):
    """
    Atualiza o status e adiciona mensagens ao histórico de chat.
    Essencial para a v0.2.6 (Avaliações e Diálogo Loja-Cliente).
    """
    pedidos = ler_todos_pedidos()
    foi_atualizado = False
    
    for p in pedidos:
        if p.get('id') == id_pedido:
            p['status'] = novo_status
            
            # Se houver mensagem (do lojista ou cliente), adiciona ao histórico
            if mensagem_chat:
                if 'historico_chat' not in p:
                    p['historico_chat'] = []
                p['historico_chat'].append(mensagem_chat)
            
            foi_atualizado = True
            break
            
    if foi_atualizado:
        with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=4, ensure_ascii=False)
        return True
    return False