import customtkinter as ctk
from interfaces.tela_cadastro_pacientes import CadastroPacienteFrame
from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame
from services.services_parciente import contar_pacientes
from services.services_atendimento import contar_atendimentos, contar_atendimentos_hoje

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FrameCard(ctk.CTkFrame):
    def __init__(self, master, titulo, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 16, "bold")
        )
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

class TelaInicial(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('900x600')
        self.title("SICA - Sistema Inteligente de Clínica e Atendimento")

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0,
            fg_color='#1B263B'
        )
        self.menu_lateral.pack(side="left", fill='y')
        
        def botao_menu(master, texto, comando=None):
            return ctk.CTkButton(
                master,
                text=texto,
                command=comando,
                fg_color="#1B263B",
                hover_color="#324A6D",
                text_color="white",
                corner_radius=10,
                font=("Arial", 14),
                height=40,
                anchor="w"
            )
        ctk.CTkLabel(
            self.menu_lateral,
            text="SICA",
            font=("Arial", 20, 'bold'),
            text_color='white'
        ).pack(pady=20)

        linha = ctk.CTkFrame(self.menu_lateral, height=2, fg_color="#666666")
        linha.pack(fill="x", padx=5, pady=(0, 10))

        botao_menu(self.menu_lateral, "Dashboard", self.abrir_dashboard).pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Pacientes").pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Atendimentos").pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Novo Paciente", self.abrir_tela_cadastro_paciente).pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Novo Atendimento", self.abrir_tela_cadastro_atendimento).pack(padx=5, fill='x')

        self.frame_scrollbar = ctk.CTkScrollableFrame(self, fg_color="#CBCBCB")
        self.frame_scrollbar.pack(fill='both', expand=True)

        self.abrir_dashboard()

    def limpar_tela(self):
        for widget in self.frame_scrollbar.winfo_children():
            widget.destroy()

    def abrir_dashboard(self):
        self.limpar_tela()

        self.card = FrameCard(self.frame_scrollbar, "Dashboard")
        self.card.pack(padx=10, pady=10, fill='both', expand=True)

        self.card.grid_columnconfigure((0, 1, 2), weight=1)
        self.card.grid_rowconfigure(1, weight=1)

        frame_paciente = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_paciente.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        total_pacientes = contar_pacientes()
        ctk.CTkLabel(frame_paciente, text="Total de Pacientes").pack(pady=(10, 0))
        ctk.CTkLabel(frame_paciente,text=str(total_pacientes),font=("Arial", 20)).pack(pady=10)

        frame_atendimento = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_atendimento.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        total_atendimento=contar_atendimentos()
        ctk.CTkLabel(frame_atendimento, text="Total de Atendimentos").pack(pady=(10, 0))
        ctk.CTkLabel(frame_atendimento, text=str(total_atendimento), font=("Arial", 20)).pack(pady=10)

        frame_hoje = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_hoje.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        total_atendimento_hoje = contar_atendimentos_hoje()
        ctk.CTkLabel(frame_hoje, text="Atendimentos Hoje").pack(pady=(10, 0))
        ctk.CTkLabel(frame_hoje, text=str(total_atendimento_hoje), font=("Arial", 20)).pack(pady=10)
        
    def abrir_tela_cadastro_paciente(self):
        self.limpar_tela()

        self.cadastro_frame = CadastroPacienteFrame(self.frame_scrollbar)
        self.cadastro_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
    def abrir_tela_cadastro_atendimento(self):
        self.limpar_tela()

        self.cadastro_frame = CadastroAtendimentoFrame(self.frame_scrollbar)
        self.cadastro_frame.pack(padx=10, pady=10, fill='both', expand=True)