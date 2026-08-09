<div align="center">

<img src="imagens/logo_sica.png" alt="Logo do SICA" width="150">

# SICA — Sistema Inteligente de Clínica e Atendimento

Aplicação desktop para gerenciamento de pacientes e atendimentos, desenvolvida em Python com uma arquitetura organizada em camadas.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-interface-1F6AA5?style=for-the-badge)](https://customtkinter.tomschimansky.com/)
[![JSON](https://img.shields.io/badge/JSON-persistência-000000?style=for-the-badge&logo=json&logoColor=white)](https://www.json.org/)

[Funcionalidades](#-funcionalidades) • [Arquitetura](#-arquitetura) • [Como executar](#-como-executar) • [Roadmap](#-roadmap)

</div>

## 💡 Sobre o projeto

O SICA foi criado para simplificar o cadastro e o acompanhamento de pacientes e atendimentos clínicos. O projeto prioriza separação de responsabilidades, validação de dados e uma interface desktop acessível.

Ele representa minha evolução em Python: além da interface gráfica, trabalhei com regras de negócio, controllers, models, tratamento de exceções e persistência local.

## ✨ Funcionalidades

### Pacientes

- Cadastrar, listar, buscar e editar pacientes
- Remover registros
- Visualizar detalhes e histórico de atendimentos
- Validar dados antes do armazenamento

### Atendimentos

- Cadastrar e listar atendimentos
- Filtrar por tipo ou status
- Vincular um atendimento a um paciente
- Visualizar detalhes e remover registros
- Exibir indicadores no dashboard

## 🛠 Tecnologias

| Tecnologia | Uso no projeto |
|---|---|
| Python | Regras de negócio e organização da aplicação |
| Tkinter / CustomTkinter | Interface gráfica desktop |
| TkCalendar | Seleção de datas nos formulários |
| JSON | Persistência local dos dados |
| Orientação a Objetos | Models, controllers, validações e exceções |

## 🧱 Arquitetura

~~~mermaid
flowchart LR
    UI[Interfaces] --> C[Controllers]
    C --> V[Validações]
    C --> S[Services]
    S --> M[Models]
    S --> D[(Arquivos JSON)]
    C --> E[Exceptions]
~~~

~~~text
.
├── interfaces/    # Telas e componentes visuais
├── controllers/   # Orquestração dos casos de uso
├── services/      # Regras e persistência
├── models/        # Entidades do domínio
├── validacoes/    # Validação dos dados
├── exceptions/    # Erros específicos do domínio
├── core/          # Enums e objetos auxiliares
├── data/          # Dados persistidos em JSON
└── main.py        # Ponto de entrada
~~~

## ▶ Como executar

### Pré-requisitos

- Python 3.11 ou superior
- Tkinter disponível na instalação do Python

~~~bash
git clone https://github.com/Karlabi-dev/sica-atendimento-clinico.git
cd sica-atendimento-clinico
python -m venv .venv
~~~

Ative o ambiente virtual e instale as dependências:

~~~bash
pip install customtkinter tkcalendar
python main.py
~~~

## 🧠 Aprendizados

- construção de interfaces desktop com múltiplas telas;
- aplicação de arquitetura em camadas;
- encapsulamento de regras em controllers e services;
- validação e tratamento de exceções;
- persistência e relacionamento de dados em JSON.

## 🚀 Roadmap

- [ ] Migrar a persistência para PostgreSQL
- [ ] Criar autenticação e perfis de acesso
- [ ] Adicionar testes automatizados
- [ ] Implementar filtros e relatórios avançados
- [ ] Evoluir o back-end para uma API REST

## 👩‍💻 Autora

**Karla Bianca Gonzaga** — desenvolvedora Full Stack em formação, com Python como principal tecnologia e em busca da primeira oportunidade como estagiária ou desenvolvedora júnior.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Karla%20Bianca-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/karla-bianca-563734355)
