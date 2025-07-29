import customtkinter as ctk
import api_client
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from functools import partial # Importamos 'partial' para ajudar a passar argumentos para os botões

plt.set_loglevel('critical')

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        
        self.currency_file = "currencies.txt"
        self._load_currencies()

        self.scroll_direction = 1
        self.scroll_step = 0.001

        # --- Títulos e Frames (como antes) ---
        self.title_label = ctk.CTkLabel(self, text="Dashboard de Cotações", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        self.last_updated_label = ctk.CTkLabel(self, text="Atualizando...", font=ctk.CTkFont(size=12))
        self.last_updated_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        
        self.add_frame = ctk.CTkFrame(self)
        self.add_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.add_frame.grid_columnconfigure(0, weight=1)
        
        self.new_currency_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Adicionar Moeda (ex: CAD, JPY)")
        self.new_currency_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        
        self.add_currency_button = ctk.CTkButton(self.add_frame, text="Adicionar", width=100, command=self._add_new_currency)
        self.add_currency_button.grid(row=0, column=1, padx=(5, 5), pady=10)

        self.refresh_button = ctk.CTkButton(self.add_frame, text="Atualizar Cotações", width=160, command=self.update_quotes)
        self.refresh_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Usando a altura que você definiu
        self.scrollable_cards_frame = ctk.CTkScrollableFrame(self, orientation='horizontal', height=500)
        self.scrollable_cards_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.scrollable_cards_frame._scrollbar.grid_forget()

        self.inner_cards_frame = ctk.CTkFrame(self.scrollable_cards_frame, fg_color="transparent")
        self.inner_cards_frame.pack(fill="both", expand=True)

        self.update_quotes()
        self._auto_scroll()

    def _auto_scroll(self):
        start, end = self.scrollable_cards_frame._parent_canvas.xview()
        if end >= 1.0: self.scroll_direction = -1
        elif start <= 0.0: self.scroll_direction = 1
        self.scrollable_cards_frame._parent_canvas.xview_scroll(self.scroll_direction, "units")
        self.after(15, self._auto_scroll)

    # --- FUNÇÃO DE DELETAR (NOVA) ---
    def _delete_currency(self, currency_code_to_delete):
        """Remove uma moeda da lista ativa, salva a alteração e atualiza o dashboard."""
        print(f"Tentando deletar a moeda: {currency_code_to_delete}")
        if currency_code_to_delete in self.active_currencies:
            self.active_currencies.remove(currency_code_to_delete)
            self._save_currencies()
            self.update_quotes() # Redesenha o dashboard sem a moeda deletada
        else:
            print(f"Erro: A moeda {currency_code_to_delete} não foi encontrada na lista ativa.")

    def update_quotes(self):
        self.last_updated_label.configure(text="Buscando cotações...")
        quotes = api_client.get_currency_quotes(self.active_currencies)
        
        for widget in self.inner_cards_frame.winfo_children():
            widget.destroy()

        if quotes:
            for i, (code, data) in enumerate(quotes.items()):
                # Passamos o frame interno como pai do card
                card = self.create_currency_card(self.inner_cards_frame, data)
                card.grid(row=0, column=i, padx=10, pady=10, sticky="ns")
            
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.last_updated_label.configure(text=f"Última atualização: {now}")
        elif not self.active_currencies:
             self.last_updated_label.configure(text="Nenhuma moeda para exibir. Adicione uma moeda acima.")
        else:
            self.last_updated_label.configure(text="Falha ao carregar dados.")
        
        self.after(300000, self.update_quotes)

    # --- FUNÇÃO create_currency_card ATUALIZADA ---
    def create_currency_card(self, parent, data):
        """Cria o card da moeda, incluindo o botão de deletar."""
        card = ctk.CTkFrame(parent, border_width=2, corner_radius=10)
        
        # --- DADOS DA MOEDA ---
        name = data.get('name', 'N/A').split('/')[0]
        code = data.get('code', '') # Pegamos o código (ex: 'USD')
        bid = float(data.get('bid', 0))
        ask = float(data.get('ask', 0))
        high = float(data.get('high', 0))
        pct_change = float(data.get('pctChange', 0))
        color = "green" if pct_change >= 0 else "red"
        symbol = "▲" if pct_change >= 0 else "▼"

        # --- BOTÃO DE DELETAR (NOVO) ---
        # Usamos 'partial' para criar uma função que já contém o 'code' da moeda específica deste card.
        # Isso garante que cada botão "X" saiba exatamente qual moeda deletar.
        delete_command = partial(self._delete_currency, code)
        delete_button = ctk.CTkButton(card, text="X", width=20, height=20, command=delete_command, fg_color="red", hover_color="#C00000")
        delete_button.place(relx=0.98, rely=0.02, anchor="ne") # Posiciona no canto superior direito

        # --- WIDGETS DE INFORMAÇÃO (como antes) ---
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5), padx=10)
        price_text = f"R$ {bid:.2f}".replace('.', ',')
        ctk.CTkLabel(card, text=price_text, font=ctk.CTkFont(size=22)).pack(pady=5, padx=10)
        change_text = f"{symbol} {pct_change:.2f}%".replace('.', ',')
        ctk.CTkLabel(card, text=change_text, font=ctk.CTkFont(size=14), text_color=color).pack(pady=5, padx=10)
        
        # --- GRÁFICO (como antes) ---
        historical_data = api_client.get_historical_data(code, days=30)
        if historical_data:
            df = pd.DataFrame(historical_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df['bid'] = pd.to_numeric(df['bid'])
            fig = Figure(figsize=(4, 1.5), dpi=80, facecolor="#2b2b2b")
            ax = fig.add_subplot(111)
            ax.plot(df['timestamp'], df['bid'], color=color, linewidth=2)
            ax.axis('off')
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            fig.tight_layout(pad=0)
            canvas = FigureCanvasTkAgg(fig, master=card)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10, padx=10, fill="x", expand=True)

        # --- INFORMAÇÕES ADICIONAIS (como antes) ---
        ctk.CTkLabel(card, text=f"Máxima: R$ {high:.2f}".replace('.', ','), font=ctk.CTkFont(size=12)).pack(pady=(2, 2), padx=10)
        ctk.CTkLabel(card, text=f"Venda: R$ {ask:.2f}".replace('.', ','), font=ctk.CTkFont(size=12)).pack(pady=(2, 10), padx=10)

        return card

    # --- O resto das funções (_load_currencies, _save_currencies, _add_new_currency) continua o mesmo ---
    def _load_currencies(self):
        if os.path.exists(self.currency_file):
            with open(self.currency_file, "r") as f:
                self.active_currencies = [line.strip().upper() for line in f if line.strip()]
        else:
            self.active_currencies = ['USD', 'EUR', 'BTC']
            self._save_currencies()

    def _save_currencies(self):
        with open(self.currency_file, "w") as f:
            for currency in self.active_currencies:
                f.write(f"{currency}\n")

    def _add_new_currency(self):
        new_code = self.new_currency_entry.get().strip().upper()
        if not new_code: return
        if new_code in self.active_currencies:
            self.new_currency_entry.delete(0, 'end')
            return
        self.last_updated_label.configure(text=f"Validando moeda {new_code}...")
        test_data = api_client.get_historical_data(new_code, days=1)
        if test_data:
            self.active_currencies.append(new_code)
            self._save_currencies()
            self.new_currency_entry.delete(0, 'end')
            self.update_quotes()
        else:
            self.last_updated_label.configure(text=f"Código de moeda inválido: {new_code}")