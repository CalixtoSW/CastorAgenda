from engine.database_fetchall import DatabaseFetchAll
from engine.config_db import DatabaseConfig
from controllers.medico_controller import MedicoController

class AppContext:
    def __init__(self):
        # Inicializa a configuração e conexão com o banco de dados
        self.db_config = DatabaseConfig()
        self.db_fetch_all = DatabaseFetchAll(self.db_config.get_uri())

        # Inicializa o controlador de médicos com a instância de db_fetch_all
        self.medico_controller = MedicoController(self.db_fetch_all)

    def get_medico_controller(self):
        # Retorna a instância do MedicoController
        return self.medico_controller

# Cria uma instância única de AppContext que pode ser usada globalmente
app_context = AppContext()
