import random
import time
from src.utils import GREEN, RED, RESET, CYAN, BOLD, YELLOW

def processar_pagamento_gateway(valor, metodo):
    print(f"\n{CYAN}💳 Conectando ao Gateway de Pagamento...{RESET}")
    time.sleep(1.5)
    
    if metodo == "Pix":
        codigo_pix = f"RUSH{random.randint(1000, 9999)}BITE{random.randint(100, 999)}PAY"
        print(f"\n{BOLD}CÓDIGO PIX COPIA E COLA:{RESET}")
        print(f"{YELLOW}{codigo_pix}{RESET}")
        print(f"\n{CYAN}Aguardando confirmação do banco...{RESET}")
        time.sleep(3) # Simula o tempo do webhook do banco
        
    elif metodo == "Cartão":
        print(f"{CYAN}Validando transação com a operadora...{RESET}")
        time.sleep(2)
        
    # Simulação de sucesso (95% de chance)
    if random.random() > 0.05:
        print(f"{GREEN}✅ PAGAMENTO APROVADO!{RESET}")
        return True
    else:
        print(f"{RED}❌ PAGAMENTO REJEITADO PELA OPERADORA.{RESET}")
        return False