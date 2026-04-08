class PacienteErro(Exception):
    def __init__(self, mensagem):
        super().__init__(mensagem)

class CampoObrigatorioErro(PacienteErro):
    def __init__(self, campo):
        super().__init__(f"O campo '{campo}' é obrigatório")


class EmailInvalidoErro(PacienteErro):
    def __init__(self):
        super().__init__("Email inválido")


class DataNascimentoInvalidaErro(PacienteErro):
    def __init__(self):
        super().__init__("Data de nascimento inválida ou no formato incorreto (DD/MM/YYYY)")


class DataFuturaErro(PacienteErro):
    def __init__(self):
        super().__init__("Data de nascimento não pode ser no futuro")
        

class TelefoneInvalidoErro(PacienteErro):
    def __init__(self):
        super().__init__("Telefone inválido")
        

class DocumentoInvalidoError(PacienteErro):
    def __init__(self, mensagem="Documento inválido"):
        super().__init__(mensagem)