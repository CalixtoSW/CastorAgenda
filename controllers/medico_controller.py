from engine.database_fetchall import DatabaseFetchAll

class MedicoController:
    def __init__(self, db_fetch_all: DatabaseFetchAll):
        self.db_fetch_all = db_fetch_all

    def listar_medicos(self):
        query = """
        SELECT med.id, med.nome, med.crm
        FROM public.medicos med
        WHERE med.dt_exclusao IS NULL
        """
        return self.db_fetch_all.execute_query(query)

    def inserir_medico(self, nome, crm, especialidades_ids=None):
        pass
