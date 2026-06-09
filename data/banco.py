from Banco.conexao import conexao_bd, cursor

def cadastrar(nome,data_nascimento, telefone, email, doc, tipo_documento):

    try:
        sql = """
            Insert into cliente_bd(nome,data_nascimento, telefone, email, doc, tipo_documento)
            VALUES(%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql,(nome,data_nascimento, telefone, email, doc, tipo_documento))
        conexao_bd.commit()
    except Exception as erro:
        print("Erro ao cadastrar:", erro)

def consultar_clientes():
    try:
        sql = "SELECT * FROM cliente_bd ORDER BY id_cliente"

        cursor.execute(sql)

        clientes = cursor.fetchall()

        return clientes
    #Menssagem de erro
    except Exception as erro:
        print("Erro ao consultar:", erro)
        return []