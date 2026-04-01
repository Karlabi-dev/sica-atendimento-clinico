from services.services_atendimento import (
    criar_atendimento,
    listar_atendimento,
    deletar_atendimento
)

from validacoes.validar_atendimento import ValidadorAtendimento
from exceptions.atendimento_exceptions import AtendimentoErro
from core.response import Response


class AtendimentoController:

    @staticmethod
    def criar(dados):
        try:
            ValidadorAtendimento.validar_atendimento(dados)

            criar_atendimento(dados)

            return Response(True, "Atendimento criado com sucesso")

        except AtendimentoErro as e:
            return Response(False, erro=str(e))

        except Exception as e:
            return Response(False, erro="Erro interno: " + str(e))


    @staticmethod
    def listar():
        try:
            atendimentos = listar_atendimento()
            return Response(True, dados=atendimentos)

        except Exception as e:
            return Response(False, erro=str(e))


    @staticmethod
    def deletar(id_atendimento):
        try:
            if not id_atendimento:
                raise AtendimentoErro("ID do atendimento é obrigatório")

            deletar_atendimento(id_atendimento)

            return Response(True, "Atendimento deletado com sucesso")

        except AtendimentoErro as e:
            return Response(False, erro=str(e))

        except Exception as e:
            return Response(False, erro=str(e))