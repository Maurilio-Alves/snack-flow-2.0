import database
from login import TelaLogin
from dashboard import SnackFlowDash # <--- Mudamos aqui!

def iniciar_app():
    app = SnackFlowDash()
    app.mainloop()

if __name__ == "__main__":
    database.carregar_dados_iniciais()
    login = TelaLogin(on_success=iniciar_app)
    login.mainloop()