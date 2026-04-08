import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as mg

from interfaces.tela_detalhes_paciente import DetalhePacienteFrame
from controllers.controller_paciente import PacienteController

class PacienteFrame(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master,fg_color="#CBCBCB", corner_radius=10, **kwargs)
        self.app = app  

        self.titulo = ctk.CTkLabel(self, text="Pacientes", font=("Arial", 26, "bold"))
        self.titulo.pack(pady=10,padx=10, anchor='w')
        
        self.label_loading = ctk.CTkLabel(
            self,
            text="🔄 Carregando pacientes...",
            font=("Arial", 18)
        )
        self.label_loading.pack(pady=50)
        
        self.after(1000, self.iniciar_carregamento)
        
        self.frame_card = ctk.CTkFrame(self, height=200, corner_radius=10, fg_color="#E8E8E8")
        self.frame_card.pack(padx=10, pady=10, fill='both', expand=True)
        
        busca_frame = tk.Frame(self.frame_card, bg="#E8E8E8")
        busca_frame.pack(pady=10)

        tk.Label(
            busca_frame,
            text="Buscar:",
            bg="#E8E8E8"
        ).grid(row=0, column=0, padx=5)

        self.busca_entry = tk.Entry(busca_frame, width=25)
        self.busca_entry.grid(row=0, column=1, padx=5)

        ttk.Button(
            busca_frame,
            text="🔍 Buscar",
            command=self.filtrar
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            busca_frame,
            text="❌ Limpar",
            command=self.limpar_busca
        ).grid(row=0, column=3, padx=5)

        self.tree_pacientes = ttk.Treeview(self.frame_card, columns=("Id", "Nome", "Data Nascimento", "Telefone", "Email", "Documento", "Tipo documento"), show="headings", height=15)
        for col in self.tree_pacientes['columns']:
            self.tree_pacientes.heading(col, text=col)
        self.tree_pacientes.column("Id", width=50,stretch=False)
        self.tree_pacientes.column("Nome", width=300,stretch=False)
        self.tree_pacientes.column("Data Nascimento", width=100,stretch=False)   
        self.tree_pacientes.column("Telefone", width=100,stretch=False)
        self.tree_pacientes.column("Email", width=300,stretch=False)
        self.tree_pacientes.column("Documento", width=100,stretch=False)
        self.tree_pacientes.column("Tipo documento", width=100,stretch=False)

        self.tree_pacientes.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(self.frame_card, orient="vertical", command=self.tree_pacientes.yview)
        scroll.pack(side="right", fill="y")
        self.tree_pacientes.configure(yscrollcommand=scroll.set)

        botoes = ctk.CTkFrame(self.frame_card)
        botoes.pack(side='bottom', fill='x', pady=5)
        ctk.CTkButton(botoes, text=" Vizualizar Selecionado", command=self.vizualizar_paciente).pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="🗑 Remover Selecionado",fg_color="#CF2828", command=self.remover_selecionado).pack(side="left", padx=5)
        ctk.CTkButton(botoes,text="+Novo Paciente",fg_color="#1FC64E", command=self.ir_para_cadastro_paciente).pack(side="left", padx=5)

      
    def iniciar_carregamento(self):
        self.label_loading.destroy()
        PacienteController.atualizar_tela(
            self.mostrar_sem_pacientes,
            self.mostrar_pacientes
        )


    def carregar_lista(self):
        for item in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(item)

        resposta = PacienteController.listar()
        if resposta.sucesso and resposta.dados:
            for dado in resposta.dados:
                self.tree_pacientes.insert(
                    "",
                    tk.END,
                    values=(
                        dado["id"],
                        dado["nome"],
                        dado["data_nascimento"],
                        dado["telefone"],
                        dado["email"],
                        dado["doc"],
                        dado["tipo_documento"]
                    )
                )
                
    def mostrar_pacientes(self):
        self.carregar_lista()
        self.tree_pacientes.pack(fill="both", expand=True)
    
    def mostrar_sem_pacientes(self):
        self.frame_card.destroy()
        ctk.CTkLabel(self, text="Nenhum paciente cadastrado", font=("Arial", 20,)).pack(pady=(30,5), anchor='center')
        ctk.CTkButton(self,text="Cadastrar Paciente", font=("Arial",13), command=self.ir_para_cadastro_paciente).pack(anchor='center')
    
    def ir_para_cadastro_paciente(self):
        from interfaces.tela_cadastro_pacientes import CadastroPacienteFrame
        self.app.trocar_tela(CadastroPacienteFrame)
    
    def remover_selecionado(self):
        selected_item = self.tree_pacientes.selection()
        if not selected_item:
            mg.showwarning(
            "Atenção",
            "Selecione um paciente para remover!"
        )
            return
        item = selected_item[0]
        paciente_id = self.tree_pacientes.item(item)["values"][0]
        resposta = PacienteController.deletar(paciente_id)
        if resposta.sucesso:
            self.carregar_lista()
            
    def vizualizar_paciente(self):
        selected_item = self.tree_pacientes.selection()
        if not selected_item:
            mg.showwarning(
            "Atenção",
            "Selecione um paciente para Vizualizar!"
        )
            return
        item = selected_item[0]
        paciente_id = self.tree_pacientes.item(item)["values"][0]

        resposta = PacienteController.buscar(paciente_id)

        if resposta.sucesso and resposta.dados:
            self.app.trocar_tela(DetalhePacienteFrame, paciente=resposta.dados)
        else:
            mg.showerror("Erro", resposta.erro)
            
    def limpar_busca(self):
        self.busca_entry.delete(0, "end")
        self.carregar_lista()
            
    def filtrar(self):
        from validacoes.validar_paciente import ValidadorPaciente
        from exceptions.paciente_exceptions import PacienteErro
        nome_busca = self.busca_entry.get().lower()
        for item in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(item)

        resposta = PacienteController.listar()

        if not resposta.sucesso:
            return

        for p in resposta.dados:
            nome = p["nome"].lower()

            if nome_busca and nome_busca not in nome:
                continue

            self.tree_pacientes.insert(
                "",
                tk.END,
                values=(
                    p["id"],
                    p["nome"],
                    p["data_nascimento"],
                    p["telefone"],
                    p["email"],
                    p["doc"],
                    p["tipo_documento"]
                )
            )
 