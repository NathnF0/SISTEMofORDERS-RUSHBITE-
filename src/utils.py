import os

# Cores para o Terminal (ANSI Escape Codes)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"  # <--- A COR QUE ESTAVA FALTANDO!
BOLD = "\033[1m"
RESET = "\033[0m"

def limpar_console():
    """Limpa a tela do terminal dependendo do Sistema Operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo):
    """Cria um cabeçalho padronizado e limpo."""
    limpar_console()
    print(f"{CYAN}=" * 45 + f"{RESET}")
    print(f"{BOLD}{titulo.upper().center(45)}{RESET}")
    print(f"{CYAN}=" * 45 + f"{RESET}\n")

def pausar():
    """Faz o sistema esperar o usuário ler a informação."""
    input(f"\n{YELLOW}Pressione Enter para continuar...{RESET}")

def ler_float(mensagem):
    """Lê um número decimal com segurança, aceitando vírgula ou ponto."""
    while True:
        entrada = input(mensagem).replace(',', '.')
        try:
            return float(entrada)
        except ValueError:
            print(f"{RED}Erro! Digite um valor numérico válido.{RESET}")