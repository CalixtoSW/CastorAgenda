# Castor_Agenda/controllers/Medicoss_controller.py
from engine.database_fetchall import DatabaseFetchAll

class MedicosController:
    def __init__(self, db_fetch_all: DatabaseFetchAll):
        self.db = db_fetch_all

    def create_Medicos(self, nome):
        query = f"INSERT INTO medicos (nome) VALUES ('{nome}')"
        self.db.execute_query_ddl(query)

    def read_Medicoss(self):
        query = "SELECT * FROM medicos WHERE dt_exclusao IS NULL"
        return self.db.execute_query_df(query)

    def update_Medicos(self, id, new_nome):
        query = f"UPDATE medicos SET nome = '{new_nome}' WHERE id = {id} AND dt_exclusao IS NULL"
        self.db.execute_query_ddl(query)

    def delete_Medicos(self, id):
        query = f"UPDATE medicos SET dt_exclusao = NOW() WHERE id = {id}"
        self.db.execute_query_ddl(query)
