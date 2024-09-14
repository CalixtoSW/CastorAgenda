from config_db import DatabaseConfig
from conn import DatabaseConnection

# Configuração do banco de dados
db_config = DatabaseConfig()

# Criar conexão
db_connection = DatabaseConnection(config=db_config)

# Conectar e executar query
db_connection.connect()

try:
    result = db_connection.execute_query("SELECT 1")
    print(result)
finally:
    db_connection.close()
