import re
from datetime import datetime

from exceptions.paciente_exceptions import (
    CampoObrigatorioErro,
    EmailInvalidoErro,
    DataNascimentoInvalidaErro,
    DataFuturaErro,
    PacienteErro,
    DocumentoInvalidoError
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
    
    def validar_doc(documento, tipo):
        doc = documento.strip()

        if not doc:
            raise DocumentoInvalidoError("Documento é obrigatório")

        if tipo == "CPF":
            doc_limpo = doc.replace(".", "").replace("-", "")

            if not doc_limpo.isdigit() or len(doc_limpo) != 11:
                raise DocumentoInvalidoError("CPF deve conter 11 números")

        elif tipo == "RG":
            if len(doc) < 5 or len(doc) > 12:
                raise DocumentoInvalidoError("RG inválido")

        else:
            raise DocumentoInvalidoError("Tipo de documento inválido")

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
        ValidadorPaciente.validar_doc(dados["doc"], dados["tipo_documento"])
        ValidadorPaciente.validar_telefone(dados["telefone"])