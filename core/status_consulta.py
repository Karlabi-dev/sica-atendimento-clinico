from enum import Enum
class StatusConsulta(Enum):
    AGENDADA= "Agendada"
    CONFIRMADA="Confrimada"
    EM_ANDAMENTO="Em andamento"
    CONCLUIDA="Concluida"
    CANCELADA="Cancelada"
    FALTOU="Faltou"
    REMARCADA="Remarcada"
    AGUARDANDO="Aguardando"