from interfaces.tela_dashboard import TelaInicial

if __name__ == "__main__":
    app = TelaInicial()
    app.mainloop()
    

'''def pegar_agora():
    agora = datetime.now()
    entry_data.delete(0, "end")
    entry_hora.delete(0, "end")

    entry_data.insert(0, agora.strftime("%d/%m/%Y"))
    entry_hora.insert(0, agora.strftime("%H:%M"))

def mostrar_valor():
    print("Data:", entry_data.get())
    print("Hora:", entry_hora.get())

app = ctk.CTk()
app.geometry("300x250")

# DATA
ctk.CTkLabel(app, text="Data:").pack()
entry_data = ctk.CTkEntry(app)
entry_data.pack(pady=5)

# HORA
ctk.CTkLabel(app, text="Hora:").pack()
entry_hora = ctk.CTkEntry(app)
entry_hora.pack(pady=5)

# BOTÕES
ctk.CTkButton(app, text="Usar agora", command=pegar_agora).pack(pady=10)
ctk.CTkButton(app, text="Confirmar", command=mostrar_valor).pack()

# inicia com data/hora atual
pegar_agora()

app.mainloop()
import customtkinter as ctk

class ComboBoxAutocomplete(ctk.CTkFrame):
    def __init__(self, master, values, **kwargs):
        super().__init__(master, **kwargs)

        self.values = values
        self.filtered = values

        # Campo de entrada
        self.entry = ctk.CTkEntry(self, width=200)
        self.entry.pack(pady=(0, 5))
        self.entry.bind("<KeyRelease>", self.update_list)

        # Lista de sugestões
        self.listbox = ctk.CTkTextbox(self, width=200, height=100)
        self.listbox.pack()
        self.listbox.bind("<Button-1>", self.select_item)

        self.update_list()

    def update_list(self, event=None):
        texto = self.entry.get().lower()

        self.listbox.delete("0.0", "end")

        self.filtered = [item for item in self.values if texto in item.lower()]

        for item in self.filtered:
            self.listbox.insert("end", item + "\n")

    def select_item(self, event):
        # pega linha clicada
        index = self.listbox.index("@%s,%s" % (event.x, event.y))
        linha = self.listbox.get(index + " linestart", index + " lineend").strip()

        self.entry.delete(0, "end")
        self.entry.insert(0, linha)


# APP
app = ctk.CTk()
app.geometry("300x300")

opcoes = [
    "Python", "Java", "JavaScript", "C#", "C++",
    "Go", "Rust", "Kotlin", "Swift"
]

combo = ComboBoxAutocomplete(app, opcoes)
combo.pack(pady=40)

app.mainloop()'''