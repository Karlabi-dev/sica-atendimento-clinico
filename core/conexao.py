import psycopg2
#conexao com banco
conexao_bd = psycopg2.connect(
    host="localhost",
    database = "SICA-BD",
    user = "postgres",
    port = 5432,
    password = "TECTARDE12"
)
cursor = conexao_bd.cursor()
print("DEBUG: Conexão com o banco de dados estabelecida com sucesso!")
