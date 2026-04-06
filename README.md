🏥 SICA - Sistema Inteligente de Clinica e Atendimento.

Sistema desktop desenvolvido em Python utilizando Tkinter/CustomTkinter, com o objetivo de gerenciar pacientes e seus atendimentos de forma simples e organizada.

---

📌 Funcionalidades

👤 Pacientes

- ✅ Cadastrar paciente
- 📋 Listar pacientes
- 🔍 Buscar por nome
- ✏️ Editar paciente
- ❌ Remover paciente
- 📄 Visualizar detalhes do paciente
- 📊 Histórico de atendimentos por paciente

🩺 Atendimentos

- ✅ Cadastrar atendimento
- 📋 Listar atendimentos
- 🔍 Filtrar por tipo ou status
- ❌ Remover atendimento
- 📄 Visualizar detalhes do atendimento
- 🔗 Vinculação com paciente

---

🧱 Estrutura do Projeto

SICA/
│
├── controllers/
│   ├── controller_paciente.py
│   └── controller_atendimento.py
│
├── core/
│   ├── response.py
│   ├── status_consulta.py
│   └── tipo_atendimento.py
│
├── data/
│   ├── pacientes.json
│   └── atendimentos.json
│
├── exceptions/
│   ├── paciente_exceptions.py
│   └── atendimento_exceptions.py
│
├── interfaces/
│   ├── tela_dashboard.py
│   ├── tela_pacientes.py
│   ├── tela_cadastro_pacientes.py
│   ├── tela_detalhes_paciente.py
│   ├── tela_atendimentos.py
│   ├── tela_cadastro_atendimento.py
│   └── tela_detalhe_atendimento.py
│
├── models/
│   ├── paciente.py
│   └── atendimento.py
│
├── services/
│   ├── services_parciente.py
│   └── services_atendimento.py
│
├── validacoes/
│   ├── validar_paciente.py
│   └── validar_atendimento.py
│
├── main.py
└── README.md

---

⚙️ Tecnologias Utilizadas

- 🐍 Python 3.11+
- 🖼️ Tkinter
- 🎨 CustomTkinter
- 📁 JSON (armazenamento de dados)

---

▶️ Como Executar

1. Clone o projeto:

git clone https://github.com/Karlabi-dev/sica-atendimento-clinico.git

- Abra a Pasta do projeto:

cd SICA

2. Execute o sistema:

python main.py

---

💾 Armazenamento de Dados

Os dados são armazenados em arquivos JSON:

- "data/pacientes.json"
- "data/atendimentos.json"

---

🧠 Arquitetura

O sistema segue uma separação em camadas:

- Interfaces (UI) → Telas com Tkinter e Customtkinter
- Controllers → Intermediação entre UI e lógica
- Services → Regras de negócio e manipulação de dados
- Models → Estrutura dos dados
- Validações → Regras de validação
- Exceptions → Tratamento de erros
- Core → Classes auxiliares (Response, enums)

---

📌 Observações

- O sistema não utiliza banco de dados, apenas JSON
- Ideal para estudos de arquitetura MVC adaptada
- Fácil de expandir para SQLite ou API futuramente

---

🚀 Melhorias Futuras

- 🔐 Sistema de login
- 🗄️ Migração para banco de dados (SQLite/PostgreSQL)
- 📊 Dashboard com gráficos
- 🔎 Filtros avançados
- 📅 Agenda de atendimentos

---

👨‍💻 Autora

Karla Bianca Gonzaga

---