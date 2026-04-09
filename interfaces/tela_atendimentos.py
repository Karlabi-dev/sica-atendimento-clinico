import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as mg

from interfaces.tela_detalhe_atendimento import DetalheAtendimentoFrame
from controllers.controller_atendimento import AtendimentoController

from core.status_consulta import StatusConsulta

class AtendimentoFrame(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color="#0B1F2E", corner_radius=10, **kwargs)
        self.app = app  

        self.titulo = ctk.CTkLabel(self, text="Atendimentos", text_color="White", font=("Arial", 26, "bold"))
        self.titulo.pack(pady=10, padx=10, anchor='w')

        self.label_loading = ctk.CTkLabel(
            self,
            text="🔄 Carregando atendimentos...",
            font=("Arial", 18),
            text_color="white"
        )
        self.label_loading.pack(pady=50)

        self.after(1000, self.iniciar_carregamento)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_lista = ctk.CTkFrame(self.notebook, fg_color="#E8E8E8")
        self.notebook.add(self.aba_lista, text="Lista de Atendimentos")

        self.aba_detalhes = ctk.CTkFrame(self.notebook, fg_color="#E8E8E8")
        self.notebook.add(self.aba_detalhes, text="Detalhes do Atendimento selecionado")

        self.label_info = ctk.CTkLabel(
            self.aba_detalhes,
            text='Selecione um atendimento da lista dando um "Duplo clique na tabela"',
            font=("Arial", 20)
        )
        self.label_info.pack(pady=50)

        busca_frame = tk.Frame(self.aba_lista, bg="#E8E8E8")
        busca_frame.pack(pady=10)

        tk.Label(busca_frame, text="Buscar Tipo:", bg="#E8E8E8").grid(row=0, column=0, padx=5)

        self.busca_entry = tk.Entry(busca_frame, width=20)
        self.busca_entry.grid(row=0, column=1, padx=5)

        tk.Label(busca_frame, text="Status:", bg="#E8E8E8").grid(row=0, column=2, padx=5)

        self.combo_status = ttk.Combobox(
            busca_frame,
            values=[""] + [status.value for status in StatusConsulta],
            state="readonly",
            width=15
        )
        self.combo_status.grid(row=0, column=3, padx=5)

        ttk.Button(
            busca_frame,
            text="🔍 Buscar",
            command=self.filtrar
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            busca_frame,
            text="❌ Limpar",
            command=self.limpar_busca
        ).grid(row=0, column=5, padx=5)

        colunas = ("id", "paciente_id", "data", "hora", "tipo", "status", "observacoes")

        self.tree_atendimentos = ttk.Treeview(
            self.aba_lista,
            columns=colunas,
            show="headings",
            height=15
        )

        for col in colunas:
            self.tree_atendimentos.heading(col, text=col.title())
            self.tree_atendimentos.column(col, width=120)

        self.tree_atendimentos.pack(fill="both", expand=True)

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

        self.tree_atendimentos.pack(fill="both", expand=True)

        self.tree_atendimentos.bind("<Double-1>", self.abrir_detalhes)

        scroll = ttk.Scrollbar(self.aba_lista, orient="vertical", command=self.tree_atendimentos.yview)
        scroll.pack(side="right", fill="y")
        self.tree_atendimentos.configure(yscrollcommand=scroll.set)

        botoes = ctk.CTkFrame(self.aba_lista)
        botoes.pack(side='bottom', fill='x', pady=5)

        ctk.CTkButton(botoes, text="🗑 Remover", fg_color="#CF2828", command=self.remover_selecionado).pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="+ Novo atendimento", fg_color="#1FC64E", command=self.ir_para_cadastro_atendimentos).pack(side="left", padx=5)

    def iniciar_carregamento(self):
        self.label_loading.destroy()

        AtendimentoController.atualizar_tela(
            self.mostrar_sem_atendimentos,
            self.mostrar_atendimentos
        )

    def carregar_lista(self):
        for item in self.tree_atendimentos.get_children():
            self.tree_atendimentos.delete(item)

        resposta = AtendimentoController.listar()

        if resposta.sucesso and resposta.dados:
            for a in resposta.dados:
                self.tree_atendimentos.insert(
                    "",
                    tk.END,
                    values=(
                        a["id"],
                        a["paciente_id"],
                        a["data"],
                        a["hora"],
                        a["tipo"],
                        a["status"],
                        a["observacoes"]
                    )
                )
            for i, item in enumerate(self.tree_atendimentos.get_children()):
                if i % 2 == 0:
                    self.tree_atendimentos.item(item, tags=("even",))
                else:
                    self.tree_atendimentos.item(item, tags=("odd",))

            self.tree_atendimentos.tag_configure("even", background="#FFFFFF")
            self.tree_atendimentos.tag_configure("odd", background="#EFEFEF")

    def mostrar_atendimentos(self):
        self.carregar_lista()

    def mostrar_sem_atendimentos(self):
        self.frame_card.destroy()

        ctk.CTkLabel(
            self,
            text="Nenhum atendimento cadastrado",
            font=("Arial", 20),
            text_color="white"
        ).pack(pady=30)

        ctk.CTkButton(
            self,
            text="Cadastrar Atendimento",
            command=self.ir_para_cadastro_atendimentos
        ).pack()
        
    def abrir_detalhes(self, event=None):
        selected_item = self.tree_atendimentos.selection()
        if not selected_item:
            return

        item = selected_item[0]
        atendimento_id = self.tree_atendimentos.item(item)["values"][0]

        resposta = AtendimentoController.buscar(atendimento_id)

        if resposta.sucesso and resposta.dados:
            for widget in self.aba_detalhes.winfo_children():
                widget.destroy()

            detalhe = DetalheAtendimentoFrame(self.aba_detalhes, self.app, atendimento=resposta.dados)
            detalhe.pack(fill="both", expand=True)
            
            self.notebook.select(self.aba_detalhes)
        else:
            mg.showerror("Erro", resposta.erro)
            
    def ir_para_cadastro_atendimentos(self):
        from interfaces.tela_cadastro_atendimento import CadastroAtendimentoFrame
        self.app.trocar_tela(CadastroAtendimentoFrame)

    def remover_selecionado(self):
        selected_item = self.tree_atendimentos.selection()

        if not selected_item:
            mg.showwarning("Atenção", "Selecione um atendimento!")
            return

        item = selected_item[0]
        atendimento_id = self.tree_atendimentos.item(item)["values"][0]

        resposta = AtendimentoController.deletar(atendimento_id)

        if resposta.sucesso:
            self.carregar_lista()

    def vizualizar_atendimentos(self):
        selected_item = self.tree_atendimentos.selection()

        if not selected_item:
            mg.showwarning("Atenção", "Selecione um atendimento!")
            return

        item = selected_item[0]
        atendimento_id = self.tree_atendimentos.item(item)["values"][0]

        resposta = AtendimentoController.buscar(atendimento_id)

        if resposta.sucesso:
            self.app.trocar_tela(
                DetalheAtendimentoFrame,
                atendimento=resposta.dados
            )
        else:
            mg.showerror("Erro", resposta.erro)


    def filtrar(self):
        texto = self.busca_entry.get().lower()
        status = self.combo_status.get().lower()

        for item in self.tree_atendimentos.get_children():
            self.tree_atendimentos.delete(item)

        resposta = AtendimentoController.listar()

        if not resposta.sucesso:
            return

        for a in resposta.dados:
            tipo = a["tipo"].lower()
            status_a = a["status"].lower()

            if texto and texto not in tipo:
                continue

            if status and status not in status_a:
                continue

            self.tree_atendimentos.insert(
                "",
                tk.END,
                values=(
                    a["id"],
                    a["paciente_id"],
                    a["data"],
                    a["hora"],
                    a["tipo"],
                    a["status"],
                    a["observacoes"]
                )
            )

    def limpar_busca(self):
        self.busca_entry.delete(0, "end")
        self.combo_status.set("")
        self.carregar_lista()