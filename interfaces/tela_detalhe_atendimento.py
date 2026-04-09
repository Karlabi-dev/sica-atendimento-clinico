import customtkinter as ctk
from controllers.controller_atendimento import AtendimentoController
from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame


class DetalheAtendimentoFrame(ctk.CTkFrame):

    def __init__(self, master, app, atendimento, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.app = app
        self.atendimento = atendimento

        container = ctk.CTkScrollableFrame(self, fg_color="#CBCBCB")
        container.pack(padx=10, pady=10, fill='both', expand=True)

        def criar_card(titulo):
            card = ctk.CTkFrame(container, fg_color="#E8E8E8", corner_radius=10)
            card.pack(fill="both", pady=10, padx=10, expand=True)

            ctk.CTkLabel(
                card,
                text=titulo,
                font=("Arial", 18, "bold")
            ).pack(anchor="w", padx=10, pady=(10, 5))

            return card

        def linha(parent, label, valor):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", pady=3, padx=10)

            ctk.CTkLabel(
                frame,
                text=label,
                width=140,
                anchor="w",
                font=("Arial", 13, "bold")
            ).pack(side="left")

            ctk.CTkLabel(
                frame,
                text=valor,
                anchor="w",
                font=("Arial", 13)
            ).pack(side="left")

        card_atendimento = criar_card("Informações do Atendimento")

        linha(card_atendimento, "ID:", atendimento["id"])
        linha(card_atendimento, "Paciente ID:", atendimento["paciente_id"])
        linha(card_atendimento, "Data:", atendimento["data"])
        linha(card_atendimento, "Hora:", atendimento["hora"])
        linha(card_atendimento, "Tipo:", atendimento["tipo"])
        linha(card_atendimento, "Status:", atendimento["status"])
        linha(card_atendimento, "Observações:", atendimento.get("observacoes", ""))

        from controllers.controller_paciente import PacienteController

        paciente_id = atendimento['paciente_id']
        resposta = PacienteController.buscar(paciente_id)

        card_paciente = criar_card("Informações do Paciente")

        if resposta.sucesso and resposta.dados:
            p = resposta.dados

            linha(card_paciente, "ID:", p['id'])
            linha(card_paciente, "Nome:", p['nome'])
            linha(card_paciente, "Nascimento:", p['data_nascimento'])
            linha(card_paciente, "Telefone:", p['telefone'])
            linha(card_paciente, "Email:", p['email'])
            linha(card_paciente, "Documento:", p['doc'])
            linha(card_paciente, "Tipo:", p['tipo_documento'])

        else:
            ctk.CTkLabel(
                card_paciente,
                text="Paciente não encontrado",
                text_color="red",
                font=("Arial", 14, "bold")
            ).pack(pady=10)

 
        botoes = ctk.CTkFrame(container, fg_color="#CBCBCB")
        botoes.pack(fill="x", pady=10, padx=10)

        ctk.CTkButton(
            botoes,
            text="⬅ Voltar",
            command=self.voltar
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes,
            text="✏️ Atualizar Atendimento",
            command=self.atualizar_atendimento
        ).pack(side="left", padx=5)
        
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
        
