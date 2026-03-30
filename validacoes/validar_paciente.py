import re
from datetime import datetime

from exceptions.paciente_exceptions import (
    CampoObrigatorioErro,
    NomeInvalidoErro,
    EmailInvalidoErro,
    DataNascimentoInvalidaErro,
    DataFuturaErro
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
        if not isinstance(nome, str) or len(nome.strip()) < 3:
            raise NomeInvalidoErro()


    @staticmethod
    def validar_email(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            raise EmailInvalidoErro()


    @staticmethod
    def validar_data_nascimento(data):
        try:
            data_convertida = datetime.strptime(data, "%Y-%m-%d")
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