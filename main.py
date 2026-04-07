from src.utils import exibir_cabecalho, GREEN, RED, RESET, pausar
from src.database import carregar_dados, salvar_dados
from src.telas.empresa import menu_empresa
from src.telas.cliente import menu_cliente

def main():
    while True:
        exibir_cabecalho("RushBite - Sistema de Delivery")
        print("1 - Entrar como Cliente")
        print("2 - Painel da Empresa (Login)")
        print("3 - Cadastrar Nova Empresa")
        print("0 - Sair")
        
        opcao = input("\nEscolha: ")

        if opcao == "1":
            menu_cliente()
        
        elif opcao == "2":
            nome = input("Nome da Empresa: ")
            senha = input("Senha: ")
            dados = carregar_dados()
            
            if nome in dados and dados[nome].get('senha') == senha:
                menu_empresa(nome)
            else:
                print(f"{RED}Login inválido! Verifique nome e senha.{RESET}")
                pausar()

        elif opcao == "3":
            exibir_cabecalho("Cadastro de Parceiro")
            nome = input("Nome da Loja: ")
            dados = carregar_dados()
            
            if nome in dados:
                print(f"{RED}Empresa já cadastrada!{RESET}")
            else:
                categoria = input("Categoria (ex: Lanches): ")
                senha_nova = input("Crie uma senha: ")
                dados[nome] = {
                    "categoria": categoria,
                    "senha": senha_nova,
                    "produtos": {},
                    "taxa_entrega": 0.0,
                    "chave_pix": "Não cadastrada"
                }
                salvar_dados(dados)
                print(f"{GREEN}✅ Empresa cadastrada com sucesso!{RESET}")
            pausar()

        elif opcao == "0":
            break

if __name__ == "__main__":
    main()