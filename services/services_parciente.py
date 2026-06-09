from validacoes.validar_paciente import ValidadorPaciente
from Banco.conexao import conexao_bd, cursor


def criar_paciente(nome, data_nascimento, telefone, email, doc, tipo_documento):
    try:
    
        dados = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "telefone": telefone,
            "email": email,
            "doc": doc,
            "tipo_documento": tipo_documento,
        }
        ValidadorPaciente.validar_paciente(dados)

        sql = """
            INSERT INTO pacientes(nome, data_nascimento, telefone, email, doc, tipo_documento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, data_nascimento, telefone, email, doc, tipo_documento))
        conexao_bd.commit()
        return cursor.lastrowid

    except Exception as erro:
        conexao_bd.rollback()
        print("DEBUG: Erro ao cadastrar:", erro)
        raise  

def consultar_pacientes():
    try:
        sql = "SELECT * FROM pacientes ORDER BY id"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as erro:
        print("DEBUG: Erro ao consultar:", erro)
        return []


def contar_pacientes():
    try:
        sql = "SELECT COUNT(*) FROM pacientes"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as erro:
        print("Erro ao contar pacientes:", erro)
        return 0


def listar_pacientes():
    try:
        sql = "SELECT * FROM pacientes"
        cursor.execute( sql)
        return cursor.fetchall()
    except Exception as erro:
        print("Erro ao listar pacientes:", erro)
        return []


def deletar_paciente(id):
    try:
        sql_check = "SELECT id FROM pacientes WHERE id = %s" 
        cursor.execute(sql_check, (id,))

        if cursor.fetchone() is None:
            raise Exception("Paciente não encontrado")

        sql_delete = "DELETE FROM pacientes WHERE id = %s"
        cursor.execute(sql_delete, (id,))
        conexao_bd.commit()
        return True
    except Exception as erro:
        conexao_bd.rollback()
        print("Erro ao deletar paciente:", erro)
        raise


def atualizar_paciente(id, novos_dados):
    try:
        sql_check = "SELECT id FROM pacientes WHERE id = %s"
        cursor.execute(sql_check, (id,))

        if cursor.fetchone() is None:
            raise Exception("Paciente não encontrado")

        ValidadorPaciente.validar_paciente(novos_dados)

        sql_update = """
            UPDATE pacientes
            SET nome = %s,
                data_nascimento = %s,
                telefone = %s,
                email = %s,
                doc = %s,
                tipo_documento = %s
            WHERE id = %s
        """
        cursor.execute(sql_update, (
            novos_dados["nome"],
            novos_dados["data_nascimento"],
            novos_dados["telefone"],
            novos_dados["email"],
            novos_dados["doc"],
            novos_dados["tipo_documento"],
            id,
        ))
        conexao_bd.commit()
        return True
    except Exception as erro:
        conexao_bd.rollback()
        print("Erro ao atualizar paciente:", erro)
        raise


def buscar_paciente_por_id(paciente_id):
    try:
        sql = "SELECT * FROM pacientes WHERE id = %s"
        cursor.execute(sql, (paciente_id,))
        return cursor.fetchone()
    except Exception as erro:
        print("Erro ao buscar paciente:", erro)
        return None