import json
from validacoes.validar_paciente import ValidadorPaciente
from models.paciente import Paciente

caminho_arquivo = "data/pacientes.json"

def gerar_id(caminho_arquivo=caminho_arquivo):
    dados = carregar_dados(caminho_arquivo)

    if not dados:
        return 1
    return max(p["id"] for p in dados) + 1

def contar_pacientes():
    dados = carregar_dados("data/pacientes.json")
    return len(dados)

def salvar_paciente(paciente,caminho_arquivo=caminho_arquivo):
    dados = carregar_dados(caminho_arquivo)
    dados.append(paciente.to_dict())

    with open(caminho_arquivo, "w") as f:
        json.dump(dados, f, indent=4)
        
def criar_paciente(dados, caminho_arquivo=caminho_arquivo):
    ValidadorPaciente.validar_paciente(dados)

    novo_id = gerar_id(caminho_arquivo)

    paciente = Paciente(
        id=novo_id,
        nome=dados["nome"],
        data_nascimento=dados["data_nascimento"],
        telefone=dados["telefone"],
        email=dados["email"],
        doc=dados["doc"],
        tipo_documento= dados["tipo_documento"]
    )

    salvar_paciente(paciente, caminho_arquivo)

def carregar_dados(caminho_arquivo=caminho_arquivo):
    try:
        with open(caminho_arquivo, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def listar_pacientes():
    return carregar_dados(caminho_arquivo)
    
def deletar_paciente(id_paciente):
    dados = carregar_dados(caminho_arquivo)

    novos_dados = [p for p in dados if p["id"] != id_paciente]

    if len(dados) == len(novos_dados):
        raise Exception("Paciente não encontrado")

    with open(caminho_arquivo, "w") as f:
        json.dump(novos_dados, f, indent=4)

def atualizar_paciente(id_paciente, novos_dados):
    dados = carregar_dados()
    for paciente in dados:
        if paciente["id"] == id_paciente:
            ValidadorPaciente.validar_paciente(novos_dados)

            paciente["nome"] = novos_dados["nome"]
            paciente["data_nascimento"] = novos_dados["data_nascimento"]
            paciente["telefone"] = novos_dados["telefone"]
            paciente["email"] = novos_dados["email"]
            paciente["doc"] = novos_dados["doc"]
            paciente["tipo_documento"] = novos_dados["tipo_documento"]

            with open(caminho_arquivo, "w") as f:
                json.dump(dados, f, indent=4)
            return

    raise Exception("Paciente não encontrado") 

def buscar_paciente_por_id(paciente_id):
    pacientes = carregar_dados()
    for p in pacientes:
        if str(p["id"]) == str(paciente_id):
            return p
    return None




