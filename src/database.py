# src/database.py
import json
import os

def carregar_empresas():
    if os.path.exists("empresas.json"):
        with open("empresas.json", "r") as f:
            try:
                empresas = json.load(f)
            except:
                empresas = {}
    else:
        empresas = {}

    # Criar empresas fake se vazio
    if not empresas:
        empresas = {
            "Pizza do Tony": {
                "senha": "123", "categoria": "Pizza", "descricao": "Melhor pizza da cidade",
                "produtos": {"Mussarela": 18, "Calabresa": 20}, "publicada": True,
                "horario": {"abertura": "10:00", "fechamento": "23:00"}, "logo": "🍕"
            }
        }
    
    # Validação de formato (suas linhas de correção)
    for nome, dados in list(empresas.items()):
        if isinstance(dados, str):
            empresas[nome] = {
                "senha": dados, "categoria": "", "descricao": "", "produtos": {},
                "publicada": False, "horario": {"abertura": "00:00", "fechamento": "23:59"}, "logo": ""
            }
    return empresas

def salvar_empresas(empresas):
    with open("empresas.json", "w") as f:
        json.dump(empresas, f, indent=4)