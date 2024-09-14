# Castor_Agenda/controllers/especialidades_controller.py
from engine.database_fetchall import DatabaseFetchAll

class EspecialidadeController:
    def __init__(self, db_fetch_all: DatabaseFetchAll):
        self.db = db_fetch_all

    def create_especialidade(self, nome):
        query = f"INSERT INTO especialistas (nome) VALUES ('{nome}')"
        self.db.execute_query_ddl(query)

    def read_especialidades(self):
        query = "SELECT * FROM especialistas WHERE dt_exclusao IS NULL"
        return self.db.execute_query_df(query)

    def update_especialidade(self, id, new_nome):
        query = f"UPDATE especialistas SET nome = '{new_nome}' WHERE id = {id} AND dt_exclusao IS NULL"
        self.db.execute_query_ddl(query)

    def delete_especialidade(self, id):
        query = f"UPDATE especialistas SET dt_exclusao = NOW() WHERE id = {id}"
        self.db.execute_query_ddl(query)
