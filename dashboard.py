import customtkinter as ctk
import sqlite3
from datetime import datetime
import os
from tkinter import messagebox
import winsound 
import win32print 
import win32ui

import clientes
import produtos
import fretes
import financeiro
import database 

# ==========================================
# CLASSE DA TELA DE LOGIN
# ==========================================
class TelaLogin(ctk.CTk):
    def __init__(self, callback_sucesso):
        super().__init__()
        self.callback_sucesso = callback_sucesso
        self.title("ACESSO - BILU BURGER")
        self.geometry("400x500")
        self.resizable(False, False)

        # Container Central
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        ctk.CTkLabel(self.frame, text="🍔 BILU BURGER\nSISTEMA 2.0", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)

        # CAMPO USUÁRIO (TRAVADO COM ESTILO)
        ctk.CTkLabel(self.frame, text="Usuário:", font=("Arial", 12)).pack(padx=30, anchor="w")
        self.user_entry = ctk.CTkEntry(self.frame, height=45)
        self.user_entry.insert(0, "admin") 
        self.user_entry.configure(state="readonly") # Fica travado, mas visível
        self.user_entry.pack(pady=(5, 15), padx=30, fill="x")

        # CAMPO SENHA (FOCO DIRETO)
        ctk.CTkLabel(self.frame, text="Senha:", font=("Arial", 12)).pack(padx=30, anchor="w")
        self.pass_entry = ctk.CTkEntry(self.frame, placeholder_text="****", show="*", height=45)
        self.pass_entry.pack(pady=(5, 10), padx=30, fill="x")
        
        # Garante que o cursor comece na senha
        self.pass_entry.focus_set() 

        self.btn_entrar = ctk.CTkButton(self.frame, text="ENTRAR", height=50, 
                                        fg_color="#27ae60", font=ctk.CTkFont(weight="bold"),
                                        command=self.verificar_login)
        self.btn_entrar.pack(pady=30, padx=30, fill="x")

        self.bind('<Return>', lambda event: self.verificar_login())

    def verificar_login(self):
        # Agora só checa a senha, já que o usuário está travado em admin
        if self.pass_entry.get() == "1234":
            self.destroy()
            self.callback_sucesso()
        else:
            messagebox.showerror("Erro de Acesso", "Senha incorreta!")
            self.pass_entry.delete(0, 'end') # Limpa a senha se errar

# ==========================================
# CLASSE PRINCIPAL DO SISTEMA
# ==========================================
class SnackFlowDash(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SNACK FLOW 2.0 - Bilu Burger (Oficial Online)")
        self.geometry("1280x800")
        
        self.carrinho_atual = []
        self.valor_lanches = 0.0
        self.valor_taxa_atual = 0.0 
        self.aba_ativa = "monitor" 
        self.monitor_job = None 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.montar_interface()
        self.mostrar_monitor()

    def montar_interface(self):
        # --- MENU LATERAL ---
        self.menu_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.menu_frame, text="BILU MENU", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        for cat in ["Artesanal", "Tradicional", "Variados", "Bebidas", "Adicionais"]:
            ctk.CTkButton(self.menu_frame, text=cat, command=lambda c=cat: self.abrir_vendas(c)).pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(self.menu_frame, text="GESTÃO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(30,5))
        
        ctk.CTkButton(self.menu_frame, text="👥 CLIENTES", fg_color="#8e44ad", command=lambda: self.mudar_aba(clientes.abrir_aba_clientes)).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.menu_frame, text="🍔 CARDÁPIO", fg_color="#e67e22", command=lambda: self.mudar_aba(produtos.abrir_aba_produtos)).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.menu_frame, text="🚚 FRETES", fg_color="#27ae60", command=self.abrir_aba_fretes_com_refresh).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.menu_frame, text="📊 FINANCEIRO", fg_color="#d35400", command=self.verificar_senha_financeiro).pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(self.menu_frame, text="💰 FECHAR CAIXA", fg_color="#c0392b", command=self.gerar_fechamento_caixa).pack(pady=5, padx=20, fill="x")
        
        self.btn_monitor = ctk.CTkButton(self.menu_frame, text="📺 MONITOR", fg_color="#34495e", command=self.mostrar_monitor)
        self.btn_monitor.pack(side="bottom", pady=20, padx=20, fill="x")

        # --- ÁREA CENTRAL ---
        self.centro_frame = ctk.CTkFrame(self, corner_radius=10)
        self.centro_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.label_centro = ctk.CTkLabel(self.centro_frame, text="BILU BURGER", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_centro.pack(pady=15)
        self.scroll_area = ctk.CTkScrollableFrame(self.centro_frame, height=550)
        self.scroll_area.pack(expand=True, fill="both", padx=20, pady=10)

        # --- CARRINHO ---
        self.carrinho_frame = ctk.CTkFrame(self, width=300)
        self.carrinho_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.carrinho_frame, text="🛒 CARRINHO", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        self.entry_cliente = ctk.CTkEntry(self.carrinho_frame, placeholder_text="Nome do Cliente...")
        self.entry_cliente.pack(pady=5, padx=20, fill="x")
        self.taxa_var = ctk.StringVar(value="Balcão / Retirada")
        self.menu_frete = ctk.CTkOptionMenu(self.carrinho_frame, values=self.buscar_bairros_no_db(), variable=self.taxa_var, command=self.atualizar_taxa_automatica)
        self.menu_frete.pack(pady=5, padx=20, fill="x")
        self.txt_carrinho = ctk.CTkTextbox(self.carrinho_frame, width=250, height=300, font=("Consolas", 12))
        self.txt_carrinho.pack(padx=10, pady=10)
        self.label_total = ctk.CTkLabel(self.carrinho_frame, text="TOTAL: R$ 0.00", font=("Arial", 22, "bold"), text_color="#2ecc71")
        self.label_total.pack(pady=5)
        ctk.CTkButton(self.carrinho_frame, text="LIMPAR", fg_color="#c0392b", command=self.limpar_carrinho).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.carrinho_frame, text="FECHAR PEDIDO 🚀", height=50, fg_color="#27ae60", command=self.finalizar_venda).pack(side="bottom", pady=20, padx=20, fill="x")

    def gerar_fechamento_caixa(self):
        dialogo = ctk.CTkInputDialog(text="Digite a senha de Gerência:", title="Fechar Dia")
        dialogo.after(100, lambda: dialogo._entry.configure(show="*"))
        senha = dialogo.get_input()
        
        if senha != "1234":
            if senha is not None: messagebox.showerror("Erro", "Senha incorreta!")
            return

        hoje = datetime.now().strftime("%Y-%m-%d")
        try:
            conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            cursor.execute("SELECT cliente, lanche, total FROM pedidos WHERE status = 'FINALIZADO' AND hora_entrada LIKE ?", (f'{hoje}%',))
            pedidos_hoje = cursor.fetchall(); conn.close()

            resumo_pag = {"PIX": 0.0, "DINHEIRO": 0.0, "CARTÃO": 0.0, "OUTRO": 0.0}
            produtos_qtd = {}; total_dia = 0.0

            for cli, lanch, valor in pedidos_hoje:
                total_dia += valor
                pago = False
                for met in ["PIX", "DINHEIRO", "CARTÃO"]:
                    if met in cli.upper():
                        resumo_pag[met] += valor
                        pago = True; break
                if not pago: resumo_pag["OUTRO"] += valor
                
                itens = lanch.split('|')[0].split(',')
                for i in itens:
                    n = i.strip().upper()
                    if n: produtos_qtd[n] = produtos_qtd.get(n, 0) + 1

            data_f = datetime.now().strftime('%d/%m/%Y %H:%M')
            msg = f"\n{'='*30}\n      BILU BURGER - SITE\n     FECHAMENTO DETALHADO\n{'='*30}\nDATA: {data_f}\n{'-'*30}\n"
            msg += f"DINHEIRO:      R$ {resumo_pag['DINHEIRO']:>8.2f}\nPIX:           R$ {resumo_pag['PIX']:>8.2f}\n"
            msg += f"CARTAO:        R$ {resumo_pag['CARTÃO']:>8.2f}\n{'-'*30}\n  --- ITENS VENDIDOS ---\n"
            for prod, qtd in sorted(produtos_qtd.items()):
                msg += f"{qtd:02}x {prod[:20]:<20}\n"
            msg += f"{'-'*30}\nTOTAL GERAL:   R$ {total_dia:>8.2f}\nPEDIDOS:       {len(pedidos_hoje):>8}\n{'='*30}\n\n\n\n\n"

            messagebox.showinfo("Sucesso", f"Fechamento Gerado!\nTotal: R$ {total_dia:.2f}")

            try:
                nome_imp = win32print.GetDefaultPrinter()
                hprinter = win32print.OpenPrinter(nome_imp)
                win32print.StartDocPrinter(hprinter, 1, ("Fechamento", None, "RAW"))
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, msg.encode('utf-8'))
                win32print.EndPagePrinter(hprinter); win32print.EndDocPrinter(hprinter); win32print.ClosePrinter(hprinter)
            except: pass
        except Exception as e: messagebox.showerror("Erro", f"Erro: {e}")

    def verificar_senha_financeiro(self):
        dialogo = ctk.CTkInputDialog(text="Digite a senha:", title="Acesso")
        dialogo.after(100, lambda: dialogo._entry.configure(show="*"))
        senha = dialogo.get_input()
        if senha == "1234": self.mudar_aba(financeiro.abrir_aba_financeiro)
        elif senha is not None: messagebox.showerror("Erro", "Senha incorreta!")

    def imprimir_cupom(self, cliente, lanche, total, endereco="Balcão", bairro="-", taxa=0.0, vias=2):
        try:
            nome_imp = win32print.GetDefaultPrinter(); hprinter = win32print.OpenPrinter(nome_imp)
            data_h = datetime.now().strftime("%d/%m/%Y %H:%M")
            titulos = ["*** VIA COZINHA ***", "*** VIA ENTREGA ***"]
            for i in range(vias):
                corpo = f"\n      {titulos[i]}\n      BILU BURGER - SITE\n{'-'*30}\nDATA: {data_h}\nCLIENTE: {cliente}\nEND: {endereco}\n{'-'*30}\nITENS:\n{lanche}\n{'-'*30}\nTOTAL: R$ {total:.2f}\n{'-'*30}\n\n\n\n\n"
                win32print.StartDocPrinter(hprinter, 1, ("Pedido", None, "RAW"))
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, corpo.encode('utf-8'))
                win32print.EndPagePrinter(hprinter); win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)
        except: pass

    def integrar_pedidos_nuvem(self):
        pedidos_nuvem = database.buscar_pedidos_da_nuvem()
        if pedidos_nuvem:
            try: winsound.PlaySound("alerta.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except: pass 
            conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            for id_nuvem, dados in pedidos_nuvem.items():
                cli = dados.get('cliente', 'Site'); lanch = dados.get('lanche', ''); total = dados.get('total', 0)
                end = dados.get('endereco', '').strip(); bai = dados.get('bairro', '').strip(); tax = dados.get('taxaEntrega', 0)
                info = lanch if not end or "nao informado" in end.lower() else f"{lanch} | END: {end}"
                cursor.execute("INSERT INTO pedidos (cliente, lanche, total, status, hora_entrada) VALUES (?, ?, ?, ?, ?)",
                               (f"🌐 {cli}", info, total, 'PREPARANDO', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                try: self.imprimir_cupom(cli, lanch, total, end, bai, tax)
                except: pass
                database.limpar_pedido_da_nuvem(id_nuvem)
            conn.commit(); conn.close()

    def mostrar_monitor(self):
        self.aba_ativa = "monitor"; self.limpar_tela_central()
        self.label_centro.configure(text="📺 MONITOR DE PRODUÇÃO")
        def refresh_pedidos():
            if self.aba_ativa != "monitor": return
            self.integrar_pedidos_nuvem()
            for widget in self.scroll_area.winfo_children(): widget.destroy()
            try:
                conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
                cursor.execute("UPDATE pedidos SET lanche = REPLACE(lanche, ' | END: Nao informado', '') WHERE lanche LIKE '%Nao informado%'")
                conn.commit()
                cursor.execute("SELECT id, cliente, lanche, total FROM pedidos WHERE status != 'FINALIZADO' ORDER BY id DESC")
                pedidos = cursor.fetchall(); conn.close()
                for p_id, cli, lanch, tot in pedidos:
                    cor = "#3498db" if "🌐" in cli else "#555"
                    card = ctk.CTkFrame(self.scroll_area, border_width=2, border_color=cor)
                    card.pack(pady=3, padx=10, fill="x")
                    txt_frame = ctk.CTkFrame(card, fg_color="transparent")
                    txt_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
                    ctk.CTkLabel(txt_frame, text=f"# {p_id:03} - {cli.upper()}", font=("Arial", 14, "bold"), text_color="#3498db" if "🌐" not in cli else "#2ecc71", anchor="w").pack(fill="x")
                    ctk.CTkLabel(txt_frame, text=f"DET: {lanch}", font=("Arial", 11), text_color="#e67e22", wraplength=400, justify="left", anchor="w").pack(fill="x")
                    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                    btn_frame.pack(side="right", padx=5)
                    ctk.CTkButton(btn_frame, text="🖨️", width=40, height=40, fg_color="#34495e", font=("Arial", 18), command=lambda c=cli, l=lanch, t=tot: self.imprimir_cupom(c, l, t)).pack(side="left", padx=2)
                    ctk.CTkButton(btn_frame, text="OK", width=50, height=40, fg_color="#27ae60", font=("Arial", 11, "bold"), command=lambda i=p_id: self.concluir_pedido(i)).pack(side="left", padx=2)
            except: pass
            self.monitor_job = self.after(5000, refresh_pedidos)
        refresh_pedidos()

    def concluir_pedido(self, p_id):
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("UPDATE pedidos SET status = 'FINALIZADO' WHERE id = ?", (p_id,))
        conn.commit(); conn.close(); self.mostrar_monitor()

    def mudar_aba(self, mod):
        self.aba_ativa = "gestao"; self.limpar_tela_central(); mod(self.scroll_area, self.label_centro)

    def limpar_tela_central(self):
        if self.monitor_job: self.after_cancel(self.monitor_job); self.monitor_job = None
        for widget in self.scroll_area.winfo_children(): widget.destroy()

    def abrir_vendas(self, cat):
        self.aba_ativa = "vendas"; self.limpar_tela_central(); self.label_centro.configure(text=f"CATEGORIA: {cat.upper()}")
        self.after(50, lambda: produtos.gerar_botoes_venda(cat, self.scroll_area, self.adicionar_ao_carrinho))

    def abrir_aba_fretes_com_refresh(self):
        self.mudar_aba(fretes.abrir_aba_fretes); self.menu_frete.configure(values=self.buscar_bairros_no_db())

    def buscar_bairros_no_db(self):
        try:
            conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            cursor.execute("SELECT bairro FROM fretes ORDER BY bairro ASC")
            b = [row[0] for row in cursor.fetchall()]; conn.close(); return ["Balcão / Retirada"] + b
        except: return ["Balcão / Retirada"]

    def atualizar_taxa_automatica(self, esc):
        if esc == "Balcão / Retirada": self.valor_taxa_atual = 0.0
        else:
            conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
            cursor.execute("SELECT valor FROM fretes WHERE bairro = ?", (esc,))
            res = cursor.fetchone(); self.valor_taxa_atual = res[0] if res else 0.0; conn.close()
        self.atualizar_total()

    def adicionar_ao_carrinho(self, n, p):
        self.carrinho_atual.append(n); self.valor_lanches += p; self.txt_carrinho.insert("end", f"• {n} - R${p:.2f}\n"); self.atualizar_total()

    def atualizar_total(self):
        self.label_total.configure(text=f"TOTAL: R$ {self.valor_lanches + self.valor_taxa_atual:.2f}")

    def limpar_carrinho(self):
        self.carrinho_atual = []; self.valor_lanches = 0.0; self.valor_taxa_atual = 0.0
        self.txt_carrinho.delete("1.0", "end"); self.entry_cliente.delete(0, 'end'); self.taxa_var.set("Balcão / Retirada"); self.atualizar_total()

    def finalizar_venda(self):
        if not self.carrinho_atual: return
        dialogo = ctk.CTkInputDialog(text="1-PIX | 2-DINHEIRO | 3-CARTÃO", title="Pagamento")
        dialogo.after(100, lambda: dialogo._entry.configure(show="*")) 
        op = dialogo.get_input()
        if not op: return 
        pag = {"1": "PIX", "2": "DINHEIRO", "3": "CARTÃO"}.get(op, "OUTRO")
        nome = self.entry_cliente.get() or "Balcão"
        conn = sqlite3.connect('snackflow.db'); cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente, lanche, total, status, hora_entrada) VALUES (?, ?, ?, ?, ?)",
                       (f"{nome} ({pag})", ", ".join(self.carrinho_atual), self.valor_lanches + self.valor_taxa_atual, 'PREPARANDO', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit(); conn.close(); self.limpar_carrinho(); self.mostrar_monitor()

# ==========================================
# INICIALIZAÇÃO DO SISTEMA
# ==========================================
def iniciar_sistema():
    app = SnackFlowDash()
    app.mainloop()

if __name__ == "__main__":
    # Inicia pela tela de login. Se sucesso, chama 'iniciar_sistema'
    tela_acesso = TelaLogin(callback_sucesso=iniciar_sistema)
    tela_acesso.mainloop()