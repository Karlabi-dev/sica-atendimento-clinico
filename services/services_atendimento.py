from Banco.conexao import conexao_bd, cursor
from datetime import datetime

def contar_atendimentos():
    try:
        sql = "SELECT COUNT(*) FROM atendimentos"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as erro:
        print("Erro ao contar atendimentos:", erro)
        return 0  

def contar_atendimentos_hoje():
    try:
        hoje = datetime.now().strftime("%d/%m/%Y")
        sql = "SELECT COUNT(*) FROM atendimentos WHERE data_atendimento = %s"
        cursor.execute(sql, (hoje,))
        return cursor.fetchone()[0]
    except Exception as erro:
        print("Erro ao contar atendimentos de hoje:", erro)
        return 0

def listar_atendimento():
    try:
        sql = "SELECT * FROM atendimentos"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as erro:
        print("Erro ao listar atendimentos:", erro)
        return []


def listar_atendimentos_por_data(data_str):
    """
    data_str: 'dd/mm/yyyy'
    Retorna a lista de
     atendimentos dessa data.
    """
    atendimentos = listar_atendimento()
    return [a for a in atendimentos if a["data_atendimento"] == data_str]

def criar_atendimento(paciente_id, data_atendimento, hora, tipo, status, observarcoes=""):
    try:
        dados ={
            "paciente_id": paciente_id,
            "data_atendimento": data_atendimento,
            "hora": hora,
            "tipo": tipo,
            "status": status,
            "observarcoes": observarcoes
        }
        sql = """
                INSERT INTO atendimentos (paciente_id, data_atendimento, hora, tipo, status, observarcoes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
    
        cursor.execute(sql, (paciente_id, data_atendimento, hora, tipo, status, observarcoes))
        conexao_bd.commit()
        return cursor.lastrowid
    except Exception as erro:
        conexao_bd.rollback()
        print("Erro ao criar atendimento:", erro)
        raise

def deletar_atendimento(id_atendimento):
    try:
        sql = "DELETE FROM atendimentos WHERE id = %s"
        cursor.execute(sql, (id_atendimento,))
        conexao_bd.commit()
    except Exception as erro:
        conexao_bd.rollback()
        print("Erro ao deletar atendimento:", erro)
        raise
    
def atualizar_atendimento(id_atendimento, dados):
    try:
        sql = """
            UPDATE atendimentos
            SET paciente_id = %s, data_atendimento = %s, hora = %s, tipo = %s, status = %s, observarcoes = %s
            WHERE id = %s
        """
        cursor.execute(sql, (
            dados.get("paciente_id"),
            dados.get("data_atendimento"),
            dados.get("hora"),
            dados.get("tipo"),
            dados.get("status"),
            dados.get("observarcoes"),
            id_atendimento
        ))
        conexao_bd.commit()
    except Exception as erro:
        conexao_bd.rollback()
        print("Erro ao atualizar atendimento:", erro)
        raise