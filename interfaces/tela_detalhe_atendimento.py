import customtkinter as ctk
from controllers.controller_atendimento import AtendimentoController
from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame


class DetalheAtendimentoFrame(ctk.CTkFrame):

    def __init__(self, master, app, atendimento, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.app = app
        self.atendimento = atendimento

        ctk.CTkLabel(
            self,
            text="Detalhes do Atendimento",
            font=("Arial", 26, "bold")
        ).pack(pady=10,padx=10)

        container = ctk.CTkFrame(self, fg_color="#E8E8E8")
        container.pack(padx=10, pady=10, fill='both', expand=True)

        # Função para criar linhas de informação
        def linha(label, valor):
            frame = ctk.CTkFrame(container, fg_color="transparent")
            frame.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(frame, text=label, width=150, anchor="w", font=("Arial", 14, "bold")).pack(side="left")
            ctk.CTkLabel(frame, text=valor, anchor="w", font=("Arial", 14)).pack(side="left")

        # Informações do atendimento
        linha("ID:", atendimento["id"])
        linha("Paciente ID:", atendimento["paciente_id"])
        linha("Data:", atendimento["data"])
        linha("Hora:", atendimento["hora"])
        linha("Tipo:", atendimento["tipo"])
        linha("Status:", atendimento["status"])
        linha("Observações:", atendimento.get("observacoes", ""))

        # Botões
        frame_botoes = ctk.CTkFrame(self, fg_color="#CBCBCB")
        frame_botoes.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkButton(frame_botoes, text="⬅ Voltar", command=self.voltar).pack(pady=10, side='left', padx=10)
        ctk.CTkButton(frame_botoes, text="✏️ Atualizar Atendimento", command=self.atualizar_atendimento).pack(side='left', pady=10, padx=10)
        
        self.mostrar_paciente()
        
    def mostrar_paciente(self):
        from controllers.controller_paciente import PacienteController
        paciente_id = self.atendimento['paciente_id']
        resposta = PacienteController.buscar(paciente_id)
        
        ctk.CTkLabel(self, text="_"*100).pack(pady=10)
        frame_paciente = ctk.CTkFrame(self, fg_color="#E8E8E8")
        frame_paciente.pack(fill="both", expand=True, padx=20, pady=10)
        
        if resposta.sucesso and resposta.dados:
            p = resposta.dados
            ctk.CTkLabel(frame_paciente, text="Informações do Paciente", font=("Arial", 20, "bold")).pack(pady=(0,10))
            ctk.CTkLabel(frame_paciente, text=f"ID: {p['id']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_paciente, text=f"Nome: {p['nome']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_paciente, text=f"Nascimento {p['data_nascimento']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_paciente, text=f"Telefone: {p['telefone']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_paciente, text=f"Email: {p['email']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_paciente, text=f"Documento: {p['doc']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_paciente, text=f"Tipo de documento: {p['tipo_documento']}",font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
        else:
            ctk.CTkLabel(frame_paciente, text="Paciente não encontrado", text_color="red",font=("Arial", 16, "bold")).pack( pady=10)

    def voltar(self):
        from interfaces.tela_atendimentos import AtendimentoFrame
        self.app.trocar_tela(AtendimentoFrame)

    def atualizar_atendimento(self):
        self.app.trocar_tela(CadastroAtendimentoFrame, atendimento=self.atendimento)
        
