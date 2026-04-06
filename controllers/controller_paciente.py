from services.services_parciente import (
    criar_paciente,
    listar_pacientes,
    buscar_paciente_por_id,
    atualizar_paciente,
    deletar_paciente,
    contar_pacientes
)
from exceptions.paciente_exceptions import PacienteErro
from core.response import Response


class PacienteController:

    @staticmethod
    def criar(dados):
        try:
            criar_paciente(dados)
            return Response(True, "Paciente criado com sucesso")
        except PacienteErro as e:
            return Response(False, erro=str(e))

    @staticmethod
    def listar():
        try:
            pacientes = listar_pacientes()
            return Response(True, dados=pacientes)
        except Exception as e:
            return Response(False, erro=str(e))

    @staticmethod
    def buscar(id_paciente):
        try:
            paciente = buscar_paciente_por_id(id_paciente)

            if not paciente:
                return Response(False, erro="Paciente não encontrado")

            return Response(True, dados=paciente)
        except Exception as e:
            return Response(False, erro=str(e))

    @staticmethod
    def atualizar(id_paciente, dados):
        try:
            atualizar_paciente(id_paciente, dados)
            return Response(True, "Paciente atualizado com sucesso")
        except PacienteErro as e:
            return Response(False, erro=str(e))

    @staticmethod
    def deletar(id_paciente):
        try:
            deletar_paciente(id_paciente)
            return Response(True, "Paciente deletado com sucesso")
        except Exception as e:
            return Response(False, erro=str(e))

    @staticmethod
    def atualizar_tela(tela_sem_paciente, tela_com_paciente):
        total = contar_pacientes()
        if total == 0:
            tela_sem_paciente()
        else:
            tela_com_paciente()