import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as mg

from interfaces.tela_detalhes_paciente import DetalhePacienteFrame
from controllers.controller_paciente import PacienteController



class PacienteFrame(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color="#0B1F2E", corner_radius=10, **kwargs)
        self.app = app

        self.titulo = ctk.CTkLabel(self, text="Pacientes",text_color="white", font=("Arial", 26, "bold"))
        self.titulo.pack(pady=10, padx=10, anchor='w')
        
        self.label_loading = ctk.CTkLabel(
            self,
            text="🔄 Carregando pacientes...",
            font=("Arial", 18),
            text_color="white"
        )
        self.label_loading.pack(pady=50)

        self.after(2000, self.iniciar_carregamento)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_lista = ctk.CTkFrame(self.notebook, fg_color="#E8E8E8")
        self.notebook.add(self.aba_lista, text="Lista de Pacientes")

        self.aba_detalhes = ctk.CTkFrame(self.notebook, fg_color="#E8E8E8")
        self.notebook.add(self.aba_detalhes, text="Detalhes do Paciente selecionado")

        self.label_info = ctk.CTkLabel(
            self.aba_detalhes,
            text='Selecione um paciente da lista dando um "Duplo clique na tabela"',
            font=("Arial", 20)
        )
        self.label_info.pack(pady=50)

        busca_frame = tk.Frame(self.aba_lista, bg="#E8E8E8")
        busca_frame.pack(pady=10)

        tk.Label(busca_frame, text="Buscar por nome:", bg="#E8E8E8").grid(row=0, column=0, padx=5)

        self.busca_entry = tk.Entry(busca_frame, width=25)
        self.busca_entry.grid(row=0, column=1, padx=5)

        ttk.Button(busca_frame, text="🔍 Buscar", command=self.filtrar).grid(row=0, column=2, padx=5)
        ttk.Button(busca_frame, text="❌ Limpar", command=self.limpar_busca).grid(row=0, column=3, padx=5)

        self.tree_pacientes = ttk.Treeview(
            self.aba_lista,
            columns=("ID", "Nome", "Data Nascimento", "Telefone", "Email", "Documento", "Tipo documento"),
            show="headings",
            height=15
        )

        for col in self.tree_pacientes['columns']:
            self.tree_pacientes.heading(col, text=col, anchor="center")
            self.tree_pacientes.column(col, anchor="center")
        
        self.tree_pacientes.column("ID",width=30)
            
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#F7F7F7",
            foreground="#333333",
            rowheight=28,
            fieldbackground="#F7F7F7",
            borderwidth=0
        )

        style.map(
            "Treeview",
            background=[("selected", "#4A90E2")],
            foreground=[("selected", "white")]
        )

        style.configure(
            "Treeview.Heading",
            background="#E0E0E0",
            foreground="#222222",
            font=("Arial", 12, "bold"),
            relief="flat"
        )
        
        style.map(
            "Treeview.Heading",
            background=[("active", "#D6D6D6")]
        )

        self.tree_pacientes.pack(fill="both", expand=True)

        self.tree_pacientes.bind("<Double-1>", self.abrir_detalhes)

        scroll = ttk.Scrollbar(self.aba_lista, orient="vertical", command=self.tree_pacientes.yview)
        scroll.pack(side="right", fill="y")
        self.tree_pacientes.configure(yscrollcommand=scroll.set)

        botoes = ctk.CTkFrame(self.aba_lista)
        botoes.pack(side='bottom', fill='x', pady=5)

        ctk.CTkButton(
            botoes,
            text="🗑 Remover Selecionado",
            fg_color="#CF2828",
            command=self.remover_selecionado
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes,
            text="+ Novo Paciente",
            fg_color="#1FC64E",
            command=self.ir_para_cadastro_paciente
        ).pack(side="left", padx=5)

        self.carregar_lista()


    def iniciar_carregamento(self):
        self.label_loading.destroy()

        PacienteController.atualizar_tela(
            self.mostrar_sem_pacientes,
            self.mostrar_pacientes
        )
        
    def mostrar_pacientes(self):
        self.carregar_lista()

    def mostrar_sem_pacientes(self):
        self.notebook.destroy()

        ctk.CTkLabel(
            self,
            text="Nenhum paciente cadastrado",
            font=("Arial", 20),
            text_color="white"
        ).pack(pady=30)

        ctk.CTkButton(
            self,
            text="Cadastrar Paciente",
            command=self.ir_para_cadastro_paciente
        ).pack()
    
    def abrir_detalhes(self, event=None):
        selected_item = self.tree_pacientes.selection()
        if not selected_item:
            return

        item = selected_item[0]
        paciente_id = self.tree_pacientes.item(item)["values"][0]

        resposta = PacienteController.buscar(paciente_id)

        if resposta.sucesso and resposta.dados:
            for widget in self.aba_detalhes.winfo_children():
                widget.destroy()

            detalhe = DetalhePacienteFrame(self.aba_detalhes, self.app, paciente=resposta.dados)
            detalhe.pack(fill="both", expand=True)

            self.notebook.select(self.aba_detalhes)
        else:
            mg.showerror("Erro", resposta.erro)


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
            for i, item in enumerate(self.tree_pacientes.get_children()):
                if i % 2 == 0:
                    self.tree_pacientes.item(item, tags=("even",))
                else:
                    self.tree_pacientes.item(item, tags=("odd",))

            self.tree_pacientes.tag_configure("even", background="#FFFFFF")
            self.tree_pacientes.tag_configure("odd", background="#EFEFEF")

    def ir_para_cadastro_paciente(self):
        from interfaces.tela_cadastro_pacientes import CadastroPacienteFrame
        self.app.trocar_tela(CadastroPacienteFrame)

    def remover_selecionado(self):
        selected_item = self.tree_pacientes.selection()
        if not selected_item:
            mg.showwarning("Atenção", "Selecione um paciente para remover!")
            return

        item = selected_item[0]
        paciente_id = self.tree_pacientes.item(item)["values"][0]

        resposta = PacienteController.deletar(paciente_id)
        if resposta.sucesso:
            self.carregar_lista()

    def limpar_busca(self):
        self.busca_entry.delete(0, "end")
        self.carregar_lista()

    def filtrar(self):
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