import customtkinter as ctk
from tkinter import messagebox as mg
from controllers.controller_paciente import PacienteController
from interfaces.tela_pacientes import PacienteFrame
from tkcalendar import DateEntry


class CadastroPacienteFrame(ctk.CTkFrame):
    def __init__(self, master, app, paciente=None, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.app = app
        self.paciente = paciente

        self.titulo = ctk.CTkLabel(self, text="Novo Paciente", font=("Arial", 20, "bold"))
        self.titulo.pack(pady=10, anchor='w')

        self.frame_card = ctk.CTkFrame(self, height=200, corner_radius=10, fg_color="#E8E8E8")
        self.frame_card.pack(fill='both', expand=True, padx=20)

        self.frame_card.grid_columnconfigure(0, weight=1)
        self.frame_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_card, text="Nome Completo *").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.frame_card, placeholder_text="Ex.: Maria dos Santos")
        self.entry_nome.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.entry_nome.bind("<KeyRelease>", self.validar_nome_input)

        ctk.CTkLabel(self.frame_card, text="Data Nascimento *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_data = DateEntry(
            self.frame_card,
            date_pattern="dd/mm/yyyy",
            font=("Arial",16)
        )
        self.entry_data.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame_card, text="Telefone *").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_telefone = ctk.CTkEntry(self.frame_card, placeholder_text="(00)000000000")
        self.entry_telefone.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.entry_telefone.bind("<KeyRelease>", self.limitar_telefone)

        ctk.CTkLabel(self.frame_card, text="Email *").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.frame_card, placeholder_text="Ex.: email@gmail.com")
        self.entry_email.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.entry_email.bind("<KeyRelease>", self.validar_email_input)

        ctk.CTkLabel(self.frame_card, text="Tipo Documento *").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.tipo_documento = ctk.CTkOptionMenu(
            self.frame_card,
            values=["CPF", "RG"],
            command=self.trocar_tipo_doc
        )
        self.tipo_documento.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

        self.entry_doc = ctk.CTkEntry(self.frame_card, placeholder_text="Digite o documento")
        self.entry_doc.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
        self.entry_doc.bind("<KeyRelease>", self.aplicar_mascara_doc)

        texto_botao = "Atualizar" if self.paciente else "Cadastrar"

        self.btn_salvar = ctk.CTkButton(
            self,
            text=texto_botao,
            fg_color="#1B9262",
            command=self.salvar_paciente
        )
        self.btn_salvar.pack(side='left', pady=10, padx=(20, 5))

        self.btn_cancelar = ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#C64D4D",
            command=self.cancelar
        )
        self.btn_cancelar.pack(side='left', pady=10, padx=(5, 20))

        if self.paciente:
            self.preencher_dados()


    def limitar_telefone(self, event):
        texto = ''.join(filter(str.isdigit, self.entry_telefone.get()))
        self.entry_telefone.delete(0, "end")
        self.entry_telefone.insert(0, texto[:11])


    def trocar_tipo_doc(self, escolha):
        self.entry_doc.delete(0, "end")

        if escolha == "CPF":
            self.entry_doc.configure(placeholder_text="000.000.000-00")
        else:
            self.entry_doc.configure(placeholder_text="Digite o RG")

    def aplicar_mascara_doc(self, event):
        texto = self.entry_doc.get().replace(".", "").replace("-", "")
        tipo = self.tipo_documento.get()

        if tipo == "CPF":
            texto = "".join(filter(str.isdigit, texto))[:11]

            novo = ""
            for i in range(len(texto)):
                if i in [3, 6]:
                    novo += "."
                elif i == 9:
                    novo += "-"
                novo += texto[i]

            self.entry_doc.delete(0, "end")
            self.entry_doc.insert(0, novo)
        else:
            texto = self.entry_doc.get()[:12]

            self.entry_doc.delete(0, "end")
            self.entry_doc.insert(0, texto)
            
    def validar_email_input(self, event):
        texto = self.entry_email.get()
        
        if len(texto) > 254:
            self.entry_email.delete(254, "end")
                
    def validar_nome_input(self, event):
        texto = self.entry_nome.get()

        texto = ''.join(filter(lambda x: x.isalpha() or x.isspace(), texto))

        texto = texto[:100]

        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, texto)

    def preencher_dados(self):
        self.entry_nome.insert(0, self.paciente["nome"])
        self.entry_data.set_date(self.paciente["data_nascimento"])
        self.entry_telefone.insert(0, self.paciente["telefone"])
        self.entry_email.insert(0, self.paciente["email"])
        self.entry_doc.insert(0, self.paciente["doc"])
        self.tipo_documento.set(self.paciente["tipo_documento"])

    def cancelar(self):
        self.entry_nome.delete(0, "end")
        self.entry_telefone.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_doc.delete(0, "end")

    def salvar_paciente(self):
        doc = self.entry_doc.get()
        tipo = self.tipo_documento.get()

        if tipo == "CPF":
            doc = doc.replace(".", "").replace("-", "")

        dados = {
            "nome": self.entry_nome.get(),
            "data_nascimento": self.entry_data.get(),
            "telefone": self.entry_telefone.get(),
            "email": self.entry_email.get(),
            "doc": doc,
            "tipo_documento": tipo
        }

        try:
            if self.paciente:
                response = PacienteController.atualizar(self.paciente["id"], dados)
            else:
                response = PacienteController.criar(dados)

            if response.sucesso:
                mg.showinfo("Sucesso", response.mensagem)
                self.app.trocar_tela(PacienteFrame)
            else:
                mg.showerror("Erro", response.erro)

        except Exception as e:
            mg.showerror("Erro inesperado", str(e))