from engine.database_fetchall import DatabaseFetchAll
from engine.config_db import DatabaseConfig
from controllers.medico_controller import MedicoController

class AppContext:
    def __init__(self):
        # Inicializa o DatabaseFetchAll com as configurações do banco de dados
        self.db_config = DatabaseConfig()
        self.db_fetch_all = DatabaseFetchAll(self.db_config.get_uri())

        # Inicializa o controlador de médicos com a conexão
        self.medico_controller = MedicoController(self.db_fetch_all)

    def get_medico_controller(self):
        # Retorna a instância do MedicoController
        return self.medico_controller

# Cria uma instância única de AppContext que pode ser usada em todo o programa
app_context = AppContext()
