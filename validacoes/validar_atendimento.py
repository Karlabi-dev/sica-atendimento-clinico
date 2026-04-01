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
from core.tipo_atendimento import TipoAtendimento
from core.status_consulta import StatusConsulta


class ValidadorAtendimento:

    @staticmethod
    def validar_campos_obrigatorios(dados):
        campos = ["paciente_id", "data", "hora", "tipo", "status"]

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
            data_convertida = datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            raise DataAtendimentoInvalidaErro()

        if data_convertida.date() > datetime.now().date():
            raise DataAtendimentoFuturaErro()

    @staticmethod
    def validar_hora(hora):
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            raise DataAtendimentoInvalidaErro()

    @staticmethod
    def validar_tipo(tipo):
        tipos_validos = [t.value for t in TipoAtendimento]

        if tipo not in tipos_validos:
            raise TipoAtendimentoInvalidoErro()

    @staticmethod
    def validar_status(status):
        status_validos = [s.value for s in StatusConsulta]

        if status not in status_validos:
            raise StatusAtendimentoInvalidoErro()

    @staticmethod
    def validar_atendimento(dados):
        ValidadorAtendimento.validar_campos_obrigatorios(dados)
        ValidadorAtendimento.validar_paciente(dados["paciente_id"])
        ValidadorAtendimento.validar_data(dados["data"])
        ValidadorAtendimento.validar_hora(dados["hora"])
        ValidadorAtendimento.validar_tipo(dados["tipo"])
        ValidadorAtendimento.validar_status(dados["status"])