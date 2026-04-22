import json
import os
import random
import string

ARQUIVO_EMPRESAS = "empresas.json"
ARQUIVO_PEDIDOS = "pedidos.json"
ARQUIVO_CLIENTES = "clientes.json"

import json
import os

CAMINHO_CONFIG = "database/config.json" # Caminho dentro da sua pasta de dados

def carregar_config_loja():
    # Se o arquivo não existir, cria o padrão
    if not os.path.exists(CAMINHO_CONFIG):
        config_padrao = {
            "nome": "RushBite Burger",
            "logo": "🚀🥊🍔",
            "descricao": "O nocaute de sabor no seu paladar!",
            "taxa_entrega": 7.00,
            "horario_abertura": "18:00",
            "horario_fechamento": "23:30",
            "loja_aberta": True,
            "estoque_ativo": True
        }
        salvar_config_loja(config_padrao)
        return config_padrao
    
    with open(CAMINHO_CONFIG, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_config_loja(config):
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


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

def obter_status_nivel(xp):
    """Retorna o nome do nível e o multiplicador de desconto com base no XP."""
    if xp >= 500:
        return "🏆 RUSH MASTER", 0.15  # 15% de desconto
    elif xp >= 200:
        return "🥇 OURO", 0.10         # 10% de desconto
    elif xp >= 50:
        return "🥈 PRATA", 0.05        # 5% de desconto
    else:
        return "🥉 BRONZE", 0.00       # Sem desconto extra