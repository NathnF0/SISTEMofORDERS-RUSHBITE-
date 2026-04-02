# 🍔 RushBite - Delivery System (CLI)

O **RushBite** é um sistema de gerenciamento de delivery via terminal desenvolvido em Python. O projeto simula a experiência completa de um ecossistema de entregas, com interfaces distintas para lojistas e clientes.

> **Status do Projeto:** v0.1.1 (Arquitetura Modular) 🚀

## ✨ Novidades da v0.1.1
- **Arquitetura Modular:** Divisão de responsabilidades em pacotes (`src/telas`, `src/database`, `src/utils`).
- **Persistência de Dados:** Histórico de pedidos salvo automaticamente em JSON.
- **UX Refinada:** Interface limpa com transição de telas via console clearing.
- **Segurança:** Implementação de `.gitignore` para proteção de dados sensíveis e credenciais de teste.

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **JSON** (Armazenamento de dados)
- **OS & Subprocess** (Manipulação de terminal)

## 📂 Estrutura do Projeto
```text
6º Projeto/
├── src/
│   ├── telas/       # Lógica das interfaces de Cliente e Empresa
│   ├── database.py  # Gerenciamento de carga e salvamento de dados
│   └── utils.py     # Funções utilitárias (Cores, Formatação, Limpeza)
├── main.py          # Ponto de entrada do sistema
└── .gitignore       # Proteção de arquivos de dados locais
