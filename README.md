# 🍔 Bilu Burger - Snack Flow 2.0 🚀

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Firebase](https://img.shields.io/badge/Firebase-Realtime--DB-orange.svg)](https://firebase.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Uma solução Full-Stack de Delivery para lanchonetes, integrando cardápio web e gestão desktop em tempo real.**

O **Snack Flow 2.0** é um sistema completo desenvolvido para o **Bilu Burger**. Ele resolve o problema de recebimento de pedidos via WhatsApp, centralizando tudo em um Dashboard automatizado com alertas sonoros e impressão de comandas.

---

## 🏗️ Arquitetura do Sistema

O projeto é dividido em três camadas principais:

1.  **Web Menu (Frontend):** Site responsivo onde o cliente escolhe os lanches e finaliza o pedido.
2.  **Firebase Cloud (Bridge):** Atua como o cérebro em nuvem, recebendo pedidos do site e enviando notificações em tempo real para o balcão.
3.  **Desktop Dashboard (Control):** Aplicação Python robusta que monitora a produção, gerencia fretes e automatiza a impressão.

---

## ✨ Funcionalidades Principais

### 🌐 Cardápio Online
* Interface intuitiva e otimizada para mobile.
* Cálculo automático de taxa de entrega por bairro.
* Envio direto para o banco de dados sem necessidade de recarregar a página.

### 💻 Painel de Gestão (Desktop)
* **Monitor de Produção:** Visualização instantânea de novos pedidos.
* **Alertas Sonoros:** Aviso sonoro customizado (`alerta.wav`) para cada nova venda.
* **Gestão de Banco de Dados:** Histórico de clientes e pedidos via SQLite.
* **Impressão Automática:** Geração de cupom para cozinha via impressora térmica.
* **Controle de Fretes:** Cadastro dinâmico de bairros e taxas.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Interface Gráfica:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern UI)
- **Banco de Dados:** SQLite (Local) e Firebase Realtime Database (Cloud)
- **Hospedagem:** Firebase Hosting
- **Empacotamento:** PyInstaller

---

## 🔧 Instalação e Configuração

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/snack-flow-2.0.git](https://github.com/seu-usuario/snack-flow-2.0.git)

   Instalar Dependências:

Bash
pip install customtkinter firebase-admin
Configurar Firebase:

Adicione seu arquivo serviceAccountKey.json na raiz do projeto.

Gerar o Executável (.exe):

Bash
pyinstaller --noconsole --onefile --add-data "snackflow.db;." --add-data "alerta.wav;." main.py
📈 Próximas Atualizações (Roadmap)
[ ] Relatórios financeiros mensais com gráficos.

[ ] Integração com API de pagamentos (Pix Automático).

[ ] Sistema de fidelidade para clientes frequentes.

👨‍💻 Desenvolvedor
Maurilio Alves – Full Stack Developer & Burger Enthusiast 🍔

## 🔑 Configuração do Firebase

Para que o sistema funcione, você precisa configurar o seu próprio projeto no Firebase:

1. Vá até o [Console do Firebase](https://console.firebase.google.com/).
2. Crie um novo projeto e ative o **Realtime Database** e o **Hosting**.
3. Gere uma nova chave privada em: `Configurações do Projeto` > `Contas de Serviço` > `Gerar nova chave privada`.
4. Salve o arquivo JSON baixado na raiz do projeto com o nome de `firebase_config.json`.

5. **Atenção:** Nunca compartilhe ou suba este arquivo JSON para repositórios públicos, pois ele contém suas credenciais de acesso.
6. ![WhatsApp Image 2026-02-09 at 11 06 19 PM](https://github.com/user-attachments/assets/7ec7db5d-f531-4fd1-b2ea-4597caf593a0)
