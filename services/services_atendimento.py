import json
from datetime import datetime

ARQUIVO = "data/atendimentos.json"

def contar_atendimentos():
    atendimentos = carregar_atendimento()
    return len(atendimentos)

def contar_atendimentos_hoje():
    atendimentos = carregar_atendimento()
    
    hoje = datetime.now().strftime("%d/%m/%Y")

    return sum(1 for a in atendimentos if a["data"] == hoje)

def carregar_atendimento():
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_todos(atendimentos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(atendimentos, f, indent=4, ensure_ascii=False)

def gerar_id(atendimentos):
    if not atendimentos:
        return 1
    
    return max(a["id"] for a in atendimentos) + 1

def criar_atendimento(dados):
    atendimentos = carregar_atendimento()
    
    novo = {
        "id": gerar_id(atendimentos),
        "paciente_id": dados["paciente_id"],
        "data": dados["data"],
        "hora": dados["hora"],
        "tipo": dados["tipo"],
        "status": dados["status"],
        "observacoes": dados.get("observacoes", "")
    }

    atendimentos.append(novo)
    salvar_todos(atendimentos)

def listar_atendimento():
    return carregar_atendimento()

def deletar_atendimento(id_atendimento):
    atendimentos = carregar_atendimento()
    novos = [a for a in atendimentos if a["id"] != id_atendimento]

    salvar_todos(novos)

def atualizar_atendimento(id_atendimento, dados):
    atendimentos = carregar_atendimento()
    atualizado = False

    for a in atendimentos:
        if a["id"] == id_atendimento:
            # Atualiza apenas os campos presentes em dados
            for chave in ["paciente_id", "data", "hora", "tipo", "status", "observacoes"]:
                if chave in dados:
                    a[chave] = dados[chave]
            atualizado = True
            break

    if atualizado:
        salvar_todos(atendimentos)
    else:
        raise ValueError(f"Atendimento com id {id_atendimento} não encontrado.")