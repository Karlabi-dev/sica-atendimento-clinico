import customtkinter as ctk
from tkinter import messagebox
from services.services_atendimento import criar_atendimento
from exceptions.atendimento_exceptions import AtendimentoErro
from controllers.controller_atendimento import AtendimentoController
from tkinter import messagebox

class CadastroAtendimentoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.titulo = ctk.CTkLabel(self,text="Novo Atendimento",font=("Arial", 20, "bold"))
        self.titulo.pack(pady=10, anchor ='w')
        
        self.frame_card= ctk.CTkFrame(self,height=200, corner_radius=10, fg_color="#E8E8E8")
        self.frame_card.pack(fill='both', expand=True, padx=20)
        
        self.frame_card.grid_columnconfigure(0, weight=1)
        self.frame_card.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.frame_card, text="Paciente *",font=("Arial", 13, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.frame_card, placeholder_text="Ex.: Maria dos santos",fg_color="#E8E8E8")
        self.entry_nome.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame_card, text="Data Nascimento *",font=("Arial", 13, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_data = ctk.CTkEntry(self.frame_card, placeholder_text="YYYY-MM-DD",fg_color="#E8E8E8")
        self.entry_data.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame_card, text="Telefone *",font=("Arial", 13, "bold")).grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.entry_telefone = ctk.CTkEntry(self.frame_card, placeholder_text="(00)000000000",fg_color="#E8E8E8")
        self.entry_telefone.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame_card, text="Email *",font=("Arial", 13, "bold")).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.frame_card, placeholder_text="Ex.: Mariaa@gmail.com",fg_color="#E8E8E8")
        self.entry_email.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.frame_card, text="CPF *",font=("Arial", 13, "bold")).grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.entry_cpf = ctk.CTkEntry(self.frame_card, placeholder_text="000.000.000-00",fg_color="#E8E8E8")
        self.entry_cpf.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
    
        self.btn_salvar = ctk.CTkButton(self,text="Salvar",fg_color="#1B9262",command=self.salvar_paciente)
        self.btn_salvar.pack(side='left', pady=10, padx=(20,5))
        self.btn_cancelar = ctk.CTkButton(self,text="Cancelar",fg_color="#C64D4D",command=self.cancelar)
        self.btn_cancelar.pack(side='left', pady=10, padx=(5,20))
        
    def cancelar (self):
        self.entry_nome.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.entry_telefone.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_cpf.delete(0,'end')

    def salvar(self):

        dados = {
            "nome": self.entry_nome.get(),
            "data_nascimento": self.entry_data.get(),
            "telefone": self.entry_telefone.get(),
            "email": self.entry_email.get(),
            "cpf": self.entry_cpf.get()
        }
        try:
            resposta = AtendimentoController.criar(dados)

            if resposta.sucesso:
                messagebox.showinfo("Sucesso", resposta.mensagem)
            else:
                messagebox.showerror("Erro", resposta.erro)

            self.entry_nome.delete(0, "end")
            self.entry_data.delete(0, "end")
            self.entry_telefone.delete(0, "end")
            self.entry_email.delete(0, "end")
            self.entry_cpf.delete(0,'end')
            
        except AtendimentoErro as e:
            messagebox.showerror("Erro", str(e))