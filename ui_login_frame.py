import customtkinter as ctk
from database import Database

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.db = Database()
        self.on_login_success = on_login_success

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.label = ctk.CTkLabel(self, text="Acesso ao Sistema", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.login_button = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.login_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.register_button = ctk.CTkButton(self, text="Registrar", command=self.register, fg_color="transparent", border_width=1)
        self.register_button.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="", text_color="red")
        self.message_label.grid(row=5, column=0, padx=20, pady=(0, 10))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.check_user(username, password):
            self.message_label.configure(text="", text_color="green")
            self.on_login_success() # Chama a função de callback
        else:
            self.message_label.configure(text="Usuário ou senha inválidos.", text_color="red")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        success, message = self.db.add_user(username, password)
        if success:
            self.message_label.configure(text=message, text_color="green")
        else:
            self.message_label.configure(text=message, text_color="red")