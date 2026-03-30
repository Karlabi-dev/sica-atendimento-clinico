from datetime import date
import json
from models.atendimento import Atendimento
from validacoes.validar_atendimento import ValidadorAtendimento

caminho_arquivo = "data/atendimento.json"

def contar_atendimentos_hoje():
    dados = carregar_dados_atendimentos("data/atendimento.json")
    
    hoje = date.today().isoformat()

    return len([a for a in dados if a["data"] == hoje])

def carregar_dados_atendimentos(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def contar_atendimentos():
    dados = carregar_dados_atendimentos("data/atendimento.json")
    return len(dados)

def gerar_id(caminho_arquivo):
    dados = carregar_dados_atendimentos(caminho_arquivo)

    if not dados:
        return 1

    return max(p["id"] for p in dados) + 1

def salvar_atendimento(atendimento, caminho_arquivo):
    dados = carregar_dados_atendimentos(caminho_arquivo)

    dados.append(atendimento.to_dict())

    with open(caminho_arquivo, "w") as f:
        json.dump(dados, f, indent=4)

def criar_atendimento(dados):
    ValidadorAtendimento.validar_atendimento(dados)
    
    novo_id = gerar_id(caminho_arquivo)

    atendimento = Atendimento(
        id=novo_id,
        paciente_id=dados["paciente_id"],
        data=dados["data"],
        tipo=dados["tipo"],
        observacoes=dados["observacoes"],
        status=dados["status"]
    )

    salvar_atendimento(atendimento, caminho_arquivo)

def listar_atendimento():
    return carregar_dados_atendimentos(caminho_arquivo)
    
def deletar_atendimento(id_paciente):
    dados = carregar_dados_atendimentos(caminho_arquivo)

    novos_dados = [p for p in dados if p["id"] != id_paciente]

    if len(dados) == len(novos_dados):
        raise Exception("Atendimento não encontrado")

    salvar_atendimento(novos_dados,caminho_arquivo)