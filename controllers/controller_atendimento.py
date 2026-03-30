from services.services_atendimento import (
    criar_atendimento,
    listar_atendimentos,
    deletar_atendimento
)

from exceptions.atendimento_exceptions import AtendimentoErro
from core.response import Response

class AtendimentoController:

    @staticmethod
    def criar(dados):
        try:
            criar_atendimento(dados)
            return Response(True, "Atendimento criado com sucesso")

        except AtendimentoErro as e:
            return Response(False, erro=str(e))


    @staticmethod
    def listar():
        try:
            atendimentos = listar_atendimentos()
            return Response(True, dados=atendimentos)

        except Exception as e:
            return Response(False, erro=str(e))


    @staticmethod
    def deletar(id_atendimento):
        try:
            deletar_atendimento(id_atendimento)
            return Response(True, "Atendimento deletado com sucesso")

        except Exception as e:
            return Response(False, erro=str(e))