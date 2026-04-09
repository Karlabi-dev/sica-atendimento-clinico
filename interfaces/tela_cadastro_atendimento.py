import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox as mg
from tkcalendar import DateEntry

from controllers.controller_atendimento import AtendimentoController
from services.services_parciente import carregar_dados

from core.status_consulta import StatusConsulta
from core.tipo_atendimento import TipoAtendimento

class CadastroAtendimentoFrame(ctk.CTkFrame):

    def __init__(self, master, app, atendimento=None, paciente=None, **kwargs):
        super().__init__(master, fg_color="#0B1F2E", corner_radius=10, **kwargs)

        self.app = app
        self.atendimento = atendimento
        self.paciente = paciente

        self.titulo = ctk.CTkLabel(self,text="Novo Atendimento",font=("Arial", 26, "bold"), text_color="white")
        self.titulo.pack(pady=10,padx=10, anchor ='w')
        ctk.CTkLabel(self,text='Os campos com " * " condiz a campos obrigatorios!',font=("Arial", 11, "bold"), text_color="white").pack(padx=20,  anchor ='w')
        
        self.frame_card= ctk.CTkFrame(self,height=200, corner_radius=10, fg_color="#E8E8E8")
        self.frame_card.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.frame_card.grid_columnconfigure(0, weight=1)
        self.frame_card.grid_columnconfigure(1, weight=1)

        self.pacientes = carregar_dados()
        self.pacientes_filtrados = self.pacientes.copy()
    
        self.opcoes_pacientes = [
            f'ID: {p["id"]} - Nome: {p["nome"]} - Documento: {p["doc"]} ' for p in self.pacientes
        ]
        ctk.CTkLabel(self.frame_card, text="Buscar paciente").grid(row=0, column=1, padx=10, sticky='w')

        self.entry_busca = ctk.CTkEntry(self.frame_card, placeholder_text="Digite o nome...")
        self.entry_busca.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        self.entry_busca.bind("<KeyRelease>", self.filtrar_pacientes)
        
        ctk.CTkLabel(self.frame_card, text="Selecione um paciente *").grid(row=0, column=0, padx=10, sticky='w')

        self.combo_paciente = ctk.CTkOptionMenu(
            self.frame_card,
            values=self.opcoes_pacientes if self.opcoes_pacientes else ["Nenhum paciente"]
        )
        self.combo_paciente.grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        
        ctk.CTkLabel(self.frame_card, text="Data do Atendimento *").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_data = DateEntry(
            self.frame_card,
            date_pattern="dd/mm/yyyy",
            font=("Arial",16)
        )
        self.entry_data.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame_card, text="Hora (HH:MM): *").grid(row=2, column=1, padx=10, sticky='w')

        self.entry_hora = ctk.CTkEntry(self.frame_card)
        self.entry_hora.grid(row=3, column=1,pady=10, padx=10, sticky='ew')

        ctk.CTkLabel(self.frame_card, text="Tipo de Atendimento: *").grid(row=4, column=0, padx=10, sticky='w')

        self.combo_tipo = ctk.CTkOptionMenu(
            self.frame_card,
            values=[tipo.value for tipo in TipoAtendimento]
        )
        self.combo_tipo.grid(row=5, column=0,pady=10, padx=10, sticky='ew')

        ctk.CTkLabel(self.frame_card, text="Status: *").grid(row=4, column=1, padx=10, sticky='w')

        self.combo_status = ctk.CTkOptionMenu(
            self.frame_card,
            values=[status.value for status in StatusConsulta]
        )
        self.combo_status.grid(row=5, column=1,pady=10, padx=10, sticky='ew')

        ctk.CTkLabel(self.frame_card, text="Observações:").grid(row=6, column=0, padx=10, sticky='w')

        self.text_obs = ctk.CTkTextbox(self.frame_card, height=120)
        self.text_obs.grid(row=7, column=0,pady=10, padx=10, sticky='ew')

        self.label_msg = ctk.CTkLabel(self.frame_card, text="")
        self.label_msg.grid(row=8, column=0, padx=10, sticky='ew')

        ctk.CTkButton(self, text="Registrar", command=self.registrar, fg_color="#1B9262").pack(side='left', pady=10, padx=(20,5))
        ctk.CTkButton(self, text="Cancelar", command=self.limpar, fg_color = "#C64D4D").pack(side='left', pady=10, padx=(20,5))
        ctk.CTkButton(self, text="Usar Data/Hora Atual", command=self.preencher_agora).pack(side='left', pady=10, padx=(20,5))
        
        if self.atendimento:
            self.titulo.configure(text="Atualizar Atendimento")  
            self.preencher_campos()


    def filtrar_pacientes(self, event):
        busca = self.entry_busca.get().lower()

        if not busca:
            self.pacientes_filtrados = self.pacientes
        else:
            self.pacientes_filtrados = [
                p for p in self.pacientes
                if busca in p["nome"].lower()
            ]

        novas_opcoes = [
            f'ID: {p["id"]} - Nome: {p["nome"]} - doc: {p["doc"]}'
            for p in self.pacientes_filtrados
        ]

        if not novas_opcoes:
            novas_opcoes = ["Nenhum paciente encontrado"]

        self.combo_paciente.configure(values=novas_opcoes)
        self.combo_paciente.set(novas_opcoes[0])
    
    def preencher_campos(self):
        a = self.atendimento

        paciente_id = a.get("paciente_id")
        paciente = next((p for p in self.pacientes if p["id"] == paciente_id), None)
        if paciente:
            opcao = f'ID: {paciente["id"]} - Nome: {paciente["nome"]} - Documento: {paciente["doc"]}'
            self.combo_paciente.set(opcao)

        self.entry_data.set_date(a.get("data", ""))
        self.entry_hora.delete(0, "end")
        self.entry_hora.insert(0, a.get("hora", ""))

        self.combo_tipo.set(a.get("tipo", self.combo_tipo.cget("values")[0]))
        self.combo_status.set(a.get("status", self.combo_status.cget("values")[0]))

        self.text_obs.delete("0.0", "end")
        self.text_obs.insert("0.0", a.get("observacoes", ""))
    
    def preencher_agora(self):
        agora = datetime.now()

        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, agora.strftime("%d/%m/%Y"))

        self.entry_hora.delete(0, "end")
        self.entry_hora.insert(0, agora.strftime("%H:%M"))

    def registrar(self):
        paciente_str = self.combo_paciente.get()

        if " - " not in paciente_str:
            self.mostrar_msg("Selecione um paciente válido", erro=True)
            return

        paciente_id = int(paciente_str.split(" - ")[0].replace("ID:", "").strip())
        dados = {
            "paciente_id": paciente_id,
            "data": self.entry_data.get(),
            "hora": self.entry_hora.get(),
            "tipo": self.combo_tipo.get(),
            "status": self.combo_status.get(),
            "observacoes": self.text_obs.get("0.0", "end").strip()
        }

        if self.atendimento:
            response = AtendimentoController.atualizar(self.atendimento["id"], dados)
            mg.showinfo(
                "Sucesso",
                "Atendimento Atualizado com sucesso!"
            )
            self.limpar()
        else:
            mg.showinfo(
                "Sucesso",
                "Atendimento cadastrado com sucesso!"
            )
            self.limpar()
            response = AtendimentoController.criar(dados)

    def limpar(self):
        if self.opcoes_pacientes:
            self.combo_paciente.set(self.opcoes_pacientes[0])

        self.combo_tipo.set(self.combo_tipo.cget("values")[0])
        self.combo_status.set(self.combo_status.cget("values")[0])

        self.text_obs.delete("0.0", "end")
        self.entry_data.delete(0, 'end')
        self.entry_hora.delete(0, 'end')

        self.label_msg.configure(text="")

    def mostrar_msg(self, msg, erro=False):
        cor = "red" if erro else "green"
        self.label_msg.configure(text=msg, text_color=cor)

