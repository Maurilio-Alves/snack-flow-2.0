import customtkinter as ctk
from tkinter import messagebox

class TelaLogin(ctk.CTk):
    # Mudamos 'callback_sucesso' para 'on_success' para bater com o main.py
    def __init__(self, on_success):
        super().__init__()
        self.callback_sucesso = on_success # Aqui mantemos o uso interno igual
        self.title("ACESSO - BILU BURGER")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Container Central
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        ctk.CTkLabel(self.frame, text="🍔 BILU BURGER\nSISTEMA 2.0", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)

        # CAMPO USUÁRIO (TRAVADO)
        # 1. Colocamos o valor inicial "admin"
        # 2. Desabilitamos a edição com state="disabled"
        self.user_entry = ctk.CTkEntry(self.frame, height=45)
        self.user_entry.insert(0, "admin") 
        self.user_entry.configure(state="disabled") 
        self.user_entry.pack(pady=10, padx=30, fill="x")

        # CAMPO SENHA (FOCO AQUI)
        self.pass_entry = ctk.CTkEntry(self.frame, placeholder_text="Digite sua senha", show="*", height=45)
        self.pass_entry.pack(pady=10, padx=30, fill="x")
        self.pass_entry.focus() # Já deixa o cursor piscando na senha

        self.btn_entrar = ctk.CTkButton(self.frame, text="ENTRAR", height=50, 
                                        fg_color="#27ae60", font=ctk.CTkFont(weight="bold"),
                                        command=self.verificar_login)
        self.btn_entrar.pack(pady=30, padx=30, fill="x")

        self.bind('<Return>', lambda event: self.verificar_login())

    def verificar_login(self):
        # A verificação continua a mesma, mas agora o usuário é sempre admin
        if self.pass_entry.get() == "1234":
            self.destroy()
            self.callback_sucesso()
        else:
            messagebox.showerror("Erro de Acesso", "Senha incorreta!")