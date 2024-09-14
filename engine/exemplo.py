from config_db import DatabaseConfig
from conn import DatabaseConnection
from database_fetchall import DatabaseFetchAll

# Configuração do banco de dados
db_config = DatabaseConfig()

# Verificar se a URI está correta
print("Database URI:", db_config.get_uri())

# Criar conexão
db_connection = DatabaseConnection(config=db_config)
db_connection.connect()

# Criar executor de operações SQL
db_fetch_all = DatabaseFetchAll(connection=db_connection)

try:
    # Executar um SELECT e imprimir o resultado
    result = db_fetch_all.execute_query("SELECT 1")
    print(result)

    # Executar uma operação DDL e confirmar que a tabela foi criada
    db_fetch_all.execute_query_ddl("CREATE TABLE IF NOT EXISTS public.test(id SERIAL PRIMARY KEY, nome VARCHAR(50));")

    # Inserir um registro na tabela
    db_fetch_all.execute_query_ddl("INSERT INTO public.test (nome) VALUES ('Teste');")

    # Ler os dados como DataFrame e exibir
    df = db_fetch_all.execute_query_df("SELECT * FROM public.test;")
    print(df)
finally:
    db_connection.close()
