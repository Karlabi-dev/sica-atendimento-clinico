import customtkinter as ctk
from datetime import datetime

from controllers.controller_atendimento import AtendimentoController
from services.services_parciente import carregar_dados

from core.status_consulta import StatusConsulta
from core.tipo_atendimento import TipoAtendimento


class CadastroAtendimentoFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.titulo = ctk.CTkLabel(self,text="Novo Atendimento",font=("Arial", 20, "bold"))
        self.titulo.pack(pady=10, anchor ='w')
        
        self.frame_card= ctk.CTkFrame(self,height=200, corner_radius=10, fg_color="#E8E8E8")
        self.frame_card.pack(fill='both', expand=True, padx=20)
        
        self.frame_card.grid_columnconfigure(0, weight=1)
        self.frame_card.grid_columnconfigure(1, weight=1)

        self.pacientes = carregar_dados()
        self.opcoes_pacientes = [
            f'{p["id"]} - {p["nome"]} -{p["cpf"]}' for p in self.pacientes
        ]
        
        ctk.CTkLabel(self.frame_card, text="Selecione um paciente *").grid(row=0, column=0, padx=10, sticky='w')

        self.combo_paciente = ctk.CTkOptionMenu(
            self.frame_card,
            values=self.opcoes_pacientes if self.opcoes_pacientes else ["Nenhum paciente"]
        )
        self.combo_paciente.grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        
        ctk.CTkLabel(self.frame_card, text="Data (dd/mm/yyyy): *").grid(row=2, column=0, padx=10, sticky='w')

        self.entry_data = ctk.CTkEntry(self.frame_card)
        self.entry_data.grid(row=3, column=0,pady=10, padx=10, sticky='ew')

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

        paciente_id = paciente_str.split(" - ")[0].strip()
        dados = {
            "paciente_id": paciente_id,
            "data": self.entry_data.get(),
            "hora": self.entry_hora.get(),
            "tipo": self.combo_tipo.get(),
            "status": self.combo_status.get(),
            "observacoes": self.text_obs.get("0.0", "end").strip()
        }

        response = AtendimentoController.criar(dados)

        if response.sucesso:
            self.mostrar_msg(response.mensagem)
            self.limpar()
        else:
            self.mostrar_msg(response.erro, erro=True)

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

