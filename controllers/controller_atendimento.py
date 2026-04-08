from services.services_atendimento import (
    criar_atendimento,
    listar_atendimento,
    deletar_atendimento,
    contar_atendimentos,
    atualizar_atendimento,
    listar_atendimentos_por_data
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
    def atualizar(id_paciente, dados):
            try:
                atualizar_atendimento(id_paciente, dados)
                return Response(True, "Paciente atualizado com sucesso")
            except AtendimentoErro as e:
                return Response(False, erro=str(e))
        
    @staticmethod
    def listar_por_data(data):
        """
        Retorna atendimentos de uma data específica.
        `data` deve estar no formato 'dd/mm/yyyy'.
        """
        dados = listar_atendimentos_por_data(data)  # função que você cria no service
        return {"sucesso": True, "dados": dados}


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
        
    @staticmethod
    def listar_por_paciente(paciente_id):
        try:
            atendimentos = listar_atendimento() 

            filtrados = [
                a for a in atendimentos if str(a["paciente_id"]) == str(paciente_id)
            ]

            return Response(True, dados=filtrados)

        except Exception as e:
            return Response(False, erro=str(e))
        
    @staticmethod
    def atualizar_tela(tela_sem_paciente, tela_com_paciente):
        total = contar_atendimentos()
        if total == 0:
            tela_sem_paciente()
        else:
            tela_com_paciente()
        
    @staticmethod
    def buscar(id_atendimento):
        try:
            atendimentos = listar_atendimento()
            for a in atendimentos:
                if a["id"] == id_atendimento:
                    return Response(True, dados=a)
            return Response(False, erro="Atendimento não encontrado")
        except Exception as e:
            return Response(False, erro=str(e))