import customtkinter as ctk
from ui_login_frame import LoginFrame
from ui_dashboard_frame import DashboardFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard de Cotações")
        self.geometry("975x575")
        
        # Configuração do tema
        ctk.set_appearance_mode("System") # "Dark", "Light" ou "System"
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container para os frames
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_login_frame()

    def show_login_frame(self):
        """Mostra o frame de login."""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.login_frame = LoginFrame(self.container, on_login_success=self.show_dashboard_frame)
        self.login_frame.grid(row=0, column=0, padx=150, pady=50, sticky="nsew")

    def show_dashboard_frame(self):
        """Mostra o frame do dashboard após o login bem-sucedido."""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()
            
        self.dashboard_frame = DashboardFrame(self.container)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()