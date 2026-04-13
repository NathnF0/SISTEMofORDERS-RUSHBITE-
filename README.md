# 🍔 RushBite Delivery System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/version-0.2.8--beta-orange?style=for-the-badge)

O **RushBite** é uma solução completa de PDV (Ponto de Venda) e Delivery operando inteiramente via terminal. Projetado para oferecer uma experiência fluida tanto para o cliente faminto quanto para o empreendedor que busca gerir seu negócio com precisão técnica.

---

## 📸 Demonstração

> [!TIP]
<img width="245" height="216" alt="MenuPrincpal-Github-RB" src="https://github.com/user-attachments/assets/8091e387-6985-4b0e-8a08-e460a27bee49" />

---

## 🔥 Funcionalidades de Elite

### 👤 Módulo do Cliente
- **🛒 Shopping Inteligente:** Cardápio dinâmico que esconde automaticamente itens sem estoque.
- **🔁 Reorder (One-Click):** Histórico inteligente para repetir o último pedido em segundos.
- **⭐ Fidelidade Rush:** Sistema de pontos acumulativos com barra de progresso visual.
- **📍 Logística Estruturada:** Cadastro de endereço detalhado (Rua, Nº, Bairro, CEP e Referência).
- **🎟️ Central de Promoções:** Vitrine exclusiva para cupons de lojas e parcerias globais.

### 🏢 Módulo da Empresa (BI & Management)
- **📈 Dashboard de Performance:** Ranking de produtos mais vendidos e histórico de melhores clientes.
- **💰 Gestão Financeira:** Controle de faturamento bruto e estimativa de lucro líquido.
- **🤝 Contrato RushPartner:** Adesão digital a campanhas de marketing da plataforma.
- **📦 Inventário em Tempo Real:** Ajuste de estoque simples com suporte a itens ilimitados (∞).
- **🔔 Gestão de Pedidos:** Fila de produção com alteração de status e chat integrado.

---

## 🛠️ Arquitetura do Projeto

O sistema utiliza uma arquitetura modular para facilitar a manutenção e escalabilidade:

```text
rushbite/
├── main.py              # Ponto de entrada e sistema de Login/Cadastro
├── src/
│   ├── database.py      # Motor de persistência (JSON NoSQL)
│   ├── utils.py         # UI/UX, cores ANSI e helpers
│   └── telas/
│       ├── cliente.py   # Lógica da jornada do comprador
│       └── empresa.py   # Lógica do painel administrativo
└── data/                # Armazenamento dos arquivos .json
🚀 Instalação e Uso
Clone o repositório:

Bash
git clone [https://github.com/NathnF0/RUSHBITE.git]
Entre no diretório:

Bash
cd rushbite
Inicie o sistema:

Bash
python main.py
📝 Roadmap de Desenvolvimento
[x] v0.2.5: Sistema de Chat e Notificações.

[x] v0.2.8: BI, Fidelidade e Endereço Estruturado.

[ ] v0.3.0: Integração com Gateway de Pagamento (Simulado).

[ ] v0.3.5: Suporte a múltiplos entregadores e rastreio.

🤝 Contribuição
Contribuições são o que fazem a comunidade open source um lugar incrível para aprender, inspirar e criar.

Faça um Fork do projeto.

Crie uma Branch para sua feature (git checkout -b feature/AmazingFeature).

Dê um Commit nas suas alterações (git commit -m 'Add some AmazingFeature').

Faça um Push para a Branch (git push origin feature/AmazingFeature).

Abra um Pull Request.

📜 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

Desenvolvido com ☕ e 🐍 por Nathn
