import customtkinter as ctk
from controllers.controller_atendimento import AtendimentoController
from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame


class DetalhePacienteFrame(ctk.CTkFrame):

    def __init__(self, master, app, paciente, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.app = app
        self.paciente = paciente

        container = ctk.CTkScrollableFrame(self, fg_color="#CBCBCB")
        container.pack(padx=10, pady=10, fill='both', expand=True)

        def criar_card(titulo):
            card = ctk.CTkFrame(container, fg_color="#E8E8E8", corner_radius=10)
            card.pack(fill="x", pady=10, padx=10, expand=True)

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

        card_paciente = criar_card("Informações do Paciente")

        linha(card_paciente, "ID:", paciente["id"])
        linha(card_paciente, "Nome:", paciente["nome"])
        linha(card_paciente, "Nascimento:", paciente["data_nascimento"])
        linha(card_paciente, "Telefone:", paciente["telefone"])
        linha(card_paciente, "Email:", paciente["email"])
        linha(card_paciente, "Documento:", paciente["doc"])
        linha(card_paciente, "Tipo:", paciente["tipo_documento"])

        card_historico = criar_card("Histórico de Atendimentos")

        resposta = AtendimentoController.listar_por_paciente(paciente["id"])

        if resposta.sucesso and resposta.dados:
            for atendimento in resposta.dados:
                item = ctk.CTkFrame(card_historico, fg_color="#FFFFFF", corner_radius=8)
                item.pack(fill="x", padx=10, pady=5)

                label = ctk.CTkLabel(
                    item,
                    text=f"ID do Atendimento: {atendimento['id']}  |  📅 Data:  {atendimento['data']}  | Tipo: {atendimento['tipo']} | Status: {atendimento['status']}",
                    anchor="w",
                    font=("Arial", 13)
                )
                label.pack(padx=10, pady=8)
                label.bind("<Button-1>", lambda e, a=atendimento: self.ver_atendimento(a))

        else:
            ctk.CTkLabel(
                card_historico,
                text="Nenhum atendimento encontrado",
                font=("Arial", 13)
            ).pack(pady=10)

        card_botoes = ctk.CTkFrame(container, fg_color="#CBCBCB")
        card_botoes.pack(fill="x", pady=10, padx=10)

        ctk.CTkButton(
            card_botoes,
            text="⬅ Voltar",
            command=self.voltar
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            card_botoes,
            text="✏️ Editar",
            command=self.editar_paciente
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            card_botoes,
            text="➕ Novo Atendimento",
            fg_color="#1FC64E",
            command=lambda: self.app.trocar_tela(
                CadastroAtendimentoFrame,
                paciente=self.paciente
            )
        ).pack(side='left', padx=5)
        
    def voltar(self):
        from interfaces.tela_pacientes import PacienteFrame
        self.app.trocar_tela(PacienteFrame)

    def ver_atendimento(self, atendimento):
        from interfaces.tela_detalhe_atendimento import DetalheAtendimentoFrame
        self.app.trocar_tela(DetalheAtendimentoFrame, atendimento=atendimento)

    def editar_paciente(self):
        from interfaces.tela_cadastro_pacientes import CadastroPacienteFrame
        self.app.trocar_tela(CadastroPacienteFrame, paciente=self.paciente)