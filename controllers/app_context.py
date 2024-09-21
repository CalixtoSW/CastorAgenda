# CastorAgenda/controllers/app_context.py
from engine.database_fetchall import DatabaseFetchAll
from engine.config_db import DatabaseConfig
from controllers.medico_controller import MedicoController
from controllers.sala_controller import SalaController

class AppContext:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.db_fetch_all = DatabaseFetchAll(self.db_config.get_uri())

        self.medico_controller = MedicoController(self.db_fetch_all)
        self.sala_controller = SalaController(self.db_fetch_all)

    def get_medico_controller(self):
        return self.medico_controller

    def get_sala_controller(self):
        return self.sala_controller

app_context = AppContext()
