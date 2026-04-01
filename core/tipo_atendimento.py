from enum import Enum
class TipoAtendimento(Enum):
    CONSULTA= "Consulta médica"
    TELECONSULTA= "Teleconsulta"
    URGENCIA="Urgência"
    EMERGENCIA ="Emergência"
    EXAME_LAB="Exame laboratorial"
    EXAME_IMG = "Exame de imagem"
    PSICOLOGICO="Psicologico"
    ONDOTOLOGICO="Ondontologico"
    DOMICILIAR="Domiciliar"
    PREVENTIVO="Preventivo"