# 🍔 RushBite – Terminal Food Ordering System 🍕🍣

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-v0.1.0--alpha-orange?style=for-the-badge" alt="Status Alpha">
  <img src="https://img.shields.io/badge/Interface-Terminal-lightgrey?style=for-the-badge" alt="Terminal Interface">
</p>

**RushBite** is a terminal-based delivery ecosystem designed to simulate real-world interactions between customers and food establishments. This project highlights **modular architecture**, JSON data persistence, and a user-friendly interface with color-coded feedback and robust validations.

---

## 🚀 What's New? (v0.1.0-alpha)
In the latest update, the project underwent a **complete refactoring**:
* **Modularization:** Codebase split into dedicated modules (`src/telas`, `src/utils`) for better scalability and maintenance.
* **Data Validation:** Protection against invalid user inputs (e.g., handling strings in price/quantity fields).
* **JSON Persistence:** Intelligent system for loading and saving data, ensuring business info remains between sessions.
* **UX Enhancements:** ANSI colors used to highlight store status (Open/Closed) and pricing.

---

## 🌟 Key Features

### 🛒 Customer Mode
| Feature | Description |
| :--- | :--- |
| **Smart Navigation** | Auto-filter: only published stores with products are visible. |
| **Real-time Status** | Shows "Open" or "Closed" based on the store's business hours and system time. |
| **Dynamic Cart** | Add multiple items with automatic subtotal and total calculations. |

### 🏪 Business Mode
| Feature | Description |
| :--- | :--- |
| **Inventory Management** | Add and view products with sanitized price inputs. |
| **Customization** | Edit Logo (emojis), Category, Description, and Operating Hours. |
| **Publishing System** | Full control over when the store becomes visible to the public. |

---

## 📂 Project Structure

```text
SISTEMofORDERS-RUSHBITE-/
│
├── main.py                # Entry point (Main executable)
├── empresas.json          # Persistent JSON database
├── .gitignore             # Git ignore filter
└── src/                   # Source code
    ├── database.py        # JSON Load/Save logic
    ├── utils.py           # Helper functions (Colors, Validators)
    └── telas/             # Interface modules
        ├── cliente.py     # Customer menu logic
        └── empresa.py     # Business dashboard logic
🛠️ Technologies
Language: Python 3.11+

Storage: JSON (JavaScript Object Notation)

Native Modules: os, json, datetime

🏁 Getting Started
Clone the repository:

Bash
git clone [https://github.com/NathnF0/SISTEMofORDERS-RUSHBITE-.git](https://github.com/NathnF0/SISTEMofORDERS-RUSHBITE-.git)
Navigate to the folder:

Bash
cd SISTEMofORDERS-RUSHBITE-
Run the App:

Bash
python main.py
💡 Roadmap
[ ] Security: Implement Hashing (BCrypt/Hashlib) for business password protection.

[ ] Order History: Create a pedidos.json module to track completed transactions.

[ ] UI/UX: Add terminal clearing logic (cls/clear) between menu transitions.

[ ] Search: Implement filters to find stores by specific categories.

👨‍💻 Author
NathnF
Information Systems student, Backend & UX enthusiast.

This project demonstrates my ability to build complex logical systems, organize professional file structures, and manage local data persistence.
