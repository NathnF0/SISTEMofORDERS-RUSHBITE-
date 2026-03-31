# src/utils.py

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"

# VERIFIQUE SE ESTA FUNÇÃO ESTÁ AQUI EMBAIXO:
def ler_float(mensagem):
    """Garante que o preço seja um número válido"""
    while True:
        try:
            return float(input(mensagem).replace(',', '.'))
        except ValueError:
            print("\033[91mErro: Digite um valor numérico válido.\033[0m")