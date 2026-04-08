import customtkinter as ctk
from controllers.controller_atendimento import AtendimentoController
from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame

class DetalhePacienteFrame(ctk.CTkFrame):

    def __init__(self, master, app, paciente, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.app = app
        self.paciente = paciente

        ctk.CTkLabel(self,text="Detalhes do Paciente",font=("Arial", 26, "bold")).pack(pady=10, padx=10)
        
        container = ctk.CTkFrame(self, fg_color="#E8E8E8")
        container.pack(padx=10, pady=10, fill='both', expand=True)

        def linha(label, valor):
            frame = ctk.CTkFrame(container, fg_color="transparent")
            frame.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(frame, text=label, width=150, anchor="w", font=("Arial",14)).pack(side="left")
            ctk.CTkLabel(frame, text=valor, anchor="w",font=("Arial",14)).pack(side="left")
            
        linha("ID:", paciente["id"])
        linha("Nome:", paciente["nome"])
        linha("Nascimento:", paciente["data_nascimento"])
        linha("Telefone:", paciente["telefone"])
        linha("Email:", paciente["email"])
        linha("Documento:", paciente["doc"])
        linha("Tipo de documento:", paciente["tipo_documento"])
        
        frame_botoes = ctk.CTkFrame(self,fg_color="#CBCBCB")
        frame_botoes.pack(fill="both", expand=True, padx=20)

        ctk.CTkButton(frame_botoes,text="⬅ Voltar",command=self.voltar).pack(pady=10, side='left',padx=10)
        ctk.CTkButton(frame_botoes,text="✏️ Editar",command=self.editar_paciente).pack(side='left',pady=10, padx=10)
        
        ctk.CTkLabel(self,text="Histórico de Atendimentos",font=("Arial", 16, "bold")).pack(pady=(20, 5))
        resposta = AtendimentoController.listar_por_paciente(paciente["id"])
        frame_lista = ctk.CTkFrame(self,fg_color="#CBCBCB")
        frame_lista.pack(fill="both", expand=True, padx=20)
        
        for atendimento in resposta.dados:
            item = ctk.CTkFrame(frame_lista, fg_color="#FFFFFF")
            item.pack(fill="x", padx=10, pady=5)
            label = ctk.CTkLabel(
                item,
                text=f"ID: {atendimento['id']} - 📅 {atendimento['data']} - {atendimento['tipo']}",
                anchor="w"
            )
            label.pack(padx=10, pady=5)
            
            # Tornar clicável para abrir o detalhe do atendimento
            label.bind("<Button-1>", lambda e, a=atendimento: self.ver_atendimento(a))
            
        ctk.CTkButton(self,text="➕ Novo Atendimento",command=lambda: self.app.trocar_tela(CadastroAtendimentoFrame,paciente=self.paciente)).pack(pady=10)
 
    def voltar(self):
        from interfaces.tela_pacientes import PacienteFrame
        self.app.trocar_tela(PacienteFrame)
    
    def ver_atendimento(self, atendimento):
        from interfaces.tela_detalhe_atendimento import DetalheAtendimentoFrame
        self.app.trocar_tela(DetalheAtendimentoFrame, atendimento=atendimento)
            
    def editar_paciente(self):
        from interfaces.tela_cadastro_pacientes import CadastroPacienteFrame

        self.app.trocar_tela(
            CadastroPacienteFrame,
            paciente=self.paciente
    )
        