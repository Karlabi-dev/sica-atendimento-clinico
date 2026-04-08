import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox as mg
import datetime as dt
import locale

from interfaces.tela_cadastro_pacientes import CadastroPacienteFrame
from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame
from interfaces.tela_detalhes_paciente import DetalhePacienteFrame
from interfaces.tela_atendimentos import AtendimentoFrame
from interfaces.tela_pacientes import PacienteFrame

from services.services_parciente import contar_pacientes,carregar_dados
from services.services_atendimento import contar_atendimentos, contar_atendimentos_hoje
from controllers.controller_atendimento import AtendimentoController
from controllers.controller_paciente import PacienteController


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FrameCard(ctk.CTkFrame):
    def __init__(self, master, titulo, **kwargs):
        super().__init__(master, fg_color="#CBCBCB", corner_radius=10, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 20, "bold")
        )
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

class TelaInicial(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('900x600')
        self.title("SICA - Sistema Inteligente de Clínica e Atendimento")
        self.attributes("-fullscreen", True)

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
        botao_menu(self.menu_lateral, "Pacientes", self.abrir_tela_pacientes).pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Atendimentos",self.abrir_tela_atendimentos).pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Novo Paciente", self.abrir_tela_cadastro_paciente).pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Novo Atendimento", self.abrir_tela_cadastro_atendimento).pack(padx=5, fill='x')
        botao_menu(self.menu_lateral, "Sair", self.sair).pack(padx=5, fill='x')

        self.frame_scrollbar = ctk.CTkScrollableFrame(self, fg_color="#CBCBCB")
        self.frame_scrollbar.pack(fill='both', expand=True)

        self.abrir_dashboard()
        
    def limpar_tela(self):
        for widget in self.frame_scrollbar.winfo_children():
            widget.destroy()
    
    def sair(self):
        confirmar = mg.askyesno(
            "Sair", "Tem certeza que deseja Sair?"
        )
        if confirmar:
            self.destroy()
            
    def abrir_dashboard(self):
        self.limpar_tela()
        
        self.card = FrameCard(self.frame_scrollbar, "Dashboard")
        self.card.pack(padx=10, pady=10, fill='both', expand=True)

        # Frame do título com data e hora
        frame_titulo = ctk.CTkFrame(self.card, fg_color="#CBCBCB")
        frame_titulo.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        label_data = ctk.CTkLabel(frame_titulo, text=self.data(), font=("Arial", 16))
        label_data.grid(row=1, column=0, sticky="w")
        
        self.label_hora = ctk.CTkLabel(frame_titulo, font=("Arial",16))
        self.label_hora.grid(row=2, column=0, sticky="w")
        self.atualizar_hora()
        
        self.card.grid_columnconfigure((0, 1, 2), weight=1)
        self.card.grid_rowconfigure(1, weight=1)

        frame_paciente = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_paciente.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        total_pacientes = contar_pacientes()
        ctk.CTkLabel(frame_paciente, text="Total de Pacientes").pack(pady=(10, 0))
        ctk.CTkLabel(frame_paciente, text=str(total_pacientes), font=("Arial", 20)).pack(pady=10)

        frame_atendimento = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_atendimento.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        total_atendimento = contar_atendimentos()
        ctk.CTkLabel(frame_atendimento, text="Total de Atendimentos").pack(pady=(10, 0))
        ctk.CTkLabel(frame_atendimento, text=str(total_atendimento), font=("Arial", 20)).pack(pady=10)

        frame_hoje = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_hoje.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        total_atendimento_hoje = contar_atendimentos_hoje()
        ctk.CTkLabel(frame_hoje, text="Atendimentos Hoje").pack(pady=(10, 0))
        ctk.CTkLabel(frame_hoje, text=str(total_atendimento_hoje), font=("Arial", 20)).pack(pady=10)

        atendimentos_hoje = AtendimentoController.listar()
        pacientes = carregar_dados()

        hoje_str = dt.datetime.now().strftime("%d/%m/%Y")
        atendimentos_hoje = [
            a for a in atendimentos_hoje.dados if a["data"] == hoje_str
        ]

        frame_tree = ctk.CTkFrame(self.card, fg_color="#FFFFFF", corner_radius=10)
        frame_tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame_tree, text="Atendimentos recentes de hoje").pack(pady=(10, 0))

        if atendimentos_hoje:
            colunas = ("id", "paciente", "hora", "tipo", "status")
            tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=10)
            for col in colunas:
                tree.heading(col, text=col.title())
                tree.column(col, width=120)
            tree.pack(fill="both", expand=True, padx=10, pady=10)
            for a in atendimentos_hoje:
                paciente_nome = next(
                    (p["nome"] for p in pacientes if p["id"] == a["paciente_id"]),
                    "Desconhecido"
                )
                tree.insert(
                    "", 
                    "end", 
                    iid=a["paciente_id"],
                    values=(
                        a["id"],
                        paciente_nome,
                        a["hora"],
                        a["tipo"],
                        a["status"]
                    )
                )
                
                def abrir_paciente(event):
                    item_selecionado = tree.focus() 
                    if item_selecionado:
                        paciente_id = item_selecionado 
                        resposta = PacienteController.buscar(paciente_id)

                        if resposta.sucesso and resposta.dados:
                            self.trocar_tela(DetalhePacienteFrame, paciente=resposta.dados)
                        else:
                            mg.showerror("Erro", resposta.erro)
   

                tree.bind("<Double-1>", abrir_paciente)
        else:
            ctk.CTkLabel(frame_tree, text="Nenhum atendimento realizado hoje", text_color="gray").pack(pady=20)

        ctk.CTkButton(frame_tree, text="➕ Novo Atendimento", fg_color="#1B9262",
                    command=lambda: self.trocar_tela(CadastroAtendimentoFrame)).pack(pady=10)


    def data(self):
        dias = [
            "segunda-feira", "terça-feira", "quarta-feira",
            "quinta-feira", "sexta-feira", "sábado", "domingo"
        ]

        meses = [
            "janeiro", "fevereiro", "março", "abril",
            "maio", "junho", "julho", "agosto",
            "setembro", "outubro", "novembro", "dezembro"
        ]

        agora = dt.datetime.now()

        dia_semana = dias[agora.weekday()]
        mes = meses[agora.month - 1]

        data_formatada = f"{dia_semana}, {agora.day:02d} de {mes} de {agora.year}"

        return data_formatada.capitalize()
    
    def atualizar_hora(self):
        agora = dt.datetime.now()
        hora_fromatada= agora.strftime("%H:%M:%S")
        self.label_hora.configure(text=f"Horario Atual: {hora_fromatada}")
        self.label_hora.after(1000,self.atualizar_hora)
        

    def trocar_tela(self, TelaClasse, **kwargs):
        for widget in self.frame_scrollbar.winfo_children():
            widget.destroy()
        self.tela_atual = TelaClasse(self.frame_scrollbar, self, **kwargs)
        self.tela_atual.pack(fill='both', expand=True)
    
        
    def abrir_tela_cadastro_paciente(self):
        self.trocar_tela(CadastroPacienteFrame)
        
    def abrir_tela_cadastro_atendimento(self):
        self.trocar_tela(CadastroAtendimentoFrame)
        
    def abrir_tela_atendimentos(self):
        self.trocar_tela(AtendimentoFrame)
        
    def abrir_tela_pacientes(self):
        self.trocar_tela(PacienteFrame)