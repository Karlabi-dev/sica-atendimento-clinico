from datetime import datetime

from exceptions.atendimento_exceptions import (
    CampoObrigatorioAtendimentoErro,
    DataAtendimentoInvalidaErro,
    DataAtendimentoFuturaErro,
    TipoAtendimentoInvalidoErro,
    StatusAtendimentoInvalidoErro,
    PacienteNaoEncontradoErro
)

from services.services_parciente import buscar_paciente_por_id


class ValidadorAtendimento:

    @staticmethod
    def validar_campos_obrigatorios(dados):
        campos = ["paciente_id", "data", "tipo", "status"]

        for campo in campos:
            if campo not in dados or not dados[campo]:
                raise CampoObrigatorioAtendimentoErro(campo)


    @staticmethod
    def validar_paciente(paciente_id):
        paciente = buscar_paciente_por_id(paciente_id)

        if not paciente:
            raise PacienteNaoEncontradoErro()


    @staticmethod
    def validar_data(data):
        try:
            data_convertida = datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            raise DataAtendimentoInvalidaErro()

        if data_convertida > datetime.now():
            raise DataAtendimentoFuturaErro()


    @staticmethod
    def validar_tipo(tipo):
        tipos_validos = ["Consulta", "Retorno", "Exame"]

        if tipo not in tipos_validos:
            raise TipoAtendimentoInvalidoErro()


    @staticmethod
    def validar_status(status):
        status_validos = ["Agendado", "Concluido", "Cancelado"]

        if status not in status_validos:
            raise StatusAtendimentoInvalidoErro()


    @staticmethod
    def validar_atendimento(dados):
        ValidadorAtendimento.validar_campos_obrigatorios(dados)
        ValidadorAtendimento.validar_paciente(dados["paciente_id"])
        ValidadorAtendimento.validar_data(dados["data"])
        ValidadorAtendimento.validar_tipo(dados["tipo"])
        ValidadorAtendimento.validar_status(dados["status"])