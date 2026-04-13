import os

# CORES ANSI
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

def exibir_cabecalho(texto):
    os.system('cls' if os.name == 'nt' else 'clear')
    linha = "═" * (len(texto) + 4)
    print(f"{CYAN}╔{linha}╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}{texto.upper()}{RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╚{linha}╝{RESET}\n")

def pausar():
    input(f"\n{YELLOW}Pressione Enter para continuar...{RESET}")

def ler_float(label):
    while True:
        try:
            return float(input(label))
        except ValueError:
            print(f"{RED}Erro! Digite um valor numérico (ex: 15.50){RESET}")