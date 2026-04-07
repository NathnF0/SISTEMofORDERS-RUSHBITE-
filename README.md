# 🍔 RushBite - Delivery System (v0.2.0)

O **RushBite** é um ecossistema de delivery via terminal, focado em simular a interação real entre Clientes e Lojistas. Nesta versão, implementamos um fluxo completo de checkout, gestão de pedidos e persistência de dados em JSON.

## 🚀 Novidades da v0.2.0 (Ultimate Checkout)

- **Painel Administrativo:** Lojistas podem gerenciar produtos, definir taxas de entrega e cadastrar chaves PIX.
- **Checkout Inteligente:** Escolha entre Entrega ou Retirada, com cálculo automático de taxas.
- **Gestão de Pedidos:** Sistema de status (Pendente -> Preparando -> Saiu para Entrega -> Entregue).
- **Módulo Financeiro:** Relatório de faturamento baseado em pedidos concluídos.
- **UX Aprimorada:** Menus verticais, suporte a cores ANSI e validação de entradas (evitando crashes).

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Lógica central e processamento de dados.
- **JSON**: Armazenamento persistente de empresas e pedidos.
- **Modularização**: Código dividido em `src/telas`, `src/database` e `src/utils`.

## 📂 Estrutura do Projeto

```text
├── main.py              # Ponto de entrada e rotas principais
└── src/
    ├── database.py      # Persistência e manipulação de arquivos JSON
    ├── utils.py         # Auxiliares (Cores, Limpeza de Tela, Validações)
    └── telas/
        ├── cliente.py   # Fluxo de compra, cupons e checkout
        └── empresa.py   # Gestão de estoque, pedidos e financeiro
🔑 Funcionalidades de Destaque
Cupons de Desconto: Use o código RUSH10 para obter 10% de desconto no checkout.

Sistema de Troco: Cálculo automático para pagamentos em dinheiro.

Identidade Visual: Empresas podem configurar Logo (emoji), Descrição e Horário.

Desenvolvido com ☕ e Python por [Seu Nome/Github]


---

### 💡 Por que atualizar agora?

1. **Documentação de Evolução:** Quando você mudar para a **v0.3.0 (Banco de Dados)**, você só precisará adicionar uma linha no README.
2. **Profissionalismo:** Mostra que você não apenas "codifica", mas também sabe documentar o que fez.
3. **Facilidade:** Ajuda você mesmo a lembrar como o sistema funciona daqui a um mês.

**Dica de Git:**
Depois de salvar o README, não esqueça de subir:
```bash
git add README.md
git commit -m "docs: atualiza readme para a v0.2.0"
git push origin main
