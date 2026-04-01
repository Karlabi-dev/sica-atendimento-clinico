class AtendimentoErro(Exception):
    pass


class CampoObrigatorioAtendimentoErro(AtendimentoErro):
    def __init__(self, campo):
        super().__init__(f"O campo '{campo}' é obrigatório")


class DataAtendimentoInvalidaErro(AtendimentoErro):
    def __init__(self):
        super().__init__("Data ou hora inválida")

class DataAtendimentoFuturaErro(AtendimentoErro):
    def __init__(self):
        super().__init__("A data do atendimento não pode ser no futuro")


class TipoAtendimentoInvalidoErro(AtendimentoErro):
    def __init__(self):
        super().__init__("Tipo de atendimento inválido")


class StatusAtendimentoInvalidoErro(AtendimentoErro):
    def __init__(self):
        super().__init__("Status do atendimento inválido")


class PacienteNaoEncontradoErro(AtendimentoErro):
    def __init__(self):
        super().__init__("Paciente não encontrado")