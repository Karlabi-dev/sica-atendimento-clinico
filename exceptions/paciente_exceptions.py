class PacienteErro(Exception):
    """Erro base para paciente"""
    pass


class CampoObrigatorioErro(PacienteErro):
    def __init__(self, campo):
        super().__init__(f"O campo '{campo}' é obrigatório")


class NomeInvalidoErro(PacienteErro):
    def __init__(self):
        super().__init__("Nome inválido. Deve ser um texto com pelo menos 3 caracteres")


class EmailInvalidoErro(PacienteErro):
    def __init__(self):
        super().__init__("Email inválido")


class DataNascimentoInvalidaErro(PacienteErro):
    def __init__(self):
        super().__init__("Data de nascimento inválida ou no formato incorreto (YYYY-MM-DD)")


class DataFuturaErro(PacienteErro):
    def __init__(self):
        super().__init__("Data de nascimento não pode ser no futuro")