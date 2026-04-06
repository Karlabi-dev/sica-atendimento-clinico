import re
from datetime import datetime

from exceptions.paciente_exceptions import (
    CampoObrigatorioErro,
    EmailInvalidoErro,
    DataNascimentoInvalidaErro,
    DataFuturaErro,
    PacienteErro
)

class ValidadorPaciente:

    @staticmethod
    def validar_campos_obrigatorios(dados):
        campos = ["nome", "data_nascimento", "telefone", "email"]

        for campo in campos:
            if campo not in dados or not dados[campo]:
                raise CampoObrigatorioErro(campo)

    @staticmethod
    def validar_nome(nome):
        if not nome or len(nome.strip()) < 3:
            raise PacienteErro("Nome deve ter pelo menos 3 caracteres")

    @staticmethod
    def validar_cpf(cpf):
        if not cpf:
            raise PacienteErro("CPF é obrigatório")

        cpf = cpf.replace(".", "").replace("-", "")

        if not cpf.isdigit() or len(cpf) != 11:
            raise PacienteErro("CPF inválido")

        # evita tipo 11111111111
        if cpf == cpf[0] * 11:
            raise PacienteErro("CPF inválido")

        # validação real do CPF
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
            digito = ((soma * 10) % 11) % 10

            if int(cpf[i]) != digito:
                raise PacienteErro("CPF inválido")

    @staticmethod
    def validar_telefone(telefone):
        if not telefone:
            raise PacienteErro("Telefone é obrigatório")

        telefone = re.sub(r"\D", "", telefone)

        if len(telefone) < 10:
            raise PacienteErro("Telefone inválido")

    @staticmethod
    def validar_email(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            raise EmailInvalidoErro()

    @staticmethod
    def validar_data_nascimento(data):
        try:
            data_convertida = datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            raise DataNascimentoInvalidaErro()

        if data_convertida > datetime.now():
            raise DataFuturaErro()

    @staticmethod
    def validar_paciente(dados):
        ValidadorPaciente.validar_campos_obrigatorios(dados)
        ValidadorPaciente.validar_nome(dados["nome"])
        ValidadorPaciente.validar_email(dados["email"])
        ValidadorPaciente.validar_data_nascimento(dados["data_nascimento"])
        ValidadorPaciente.validar_cpf(dados["cpf"])
        ValidadorPaciente.validar_telefone(dados["telefone"])