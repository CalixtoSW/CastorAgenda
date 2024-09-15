from engine.database_fetchall import DatabaseFetchAll

class MedicoController:
    def __init__(self, db_fetch_all):
        self.db_fetch_all = db_fetch_all

    def listar_medicos(self):
        query = """
        SELECT med.id, med.nome, med.crm
        FROM public.medicos med
        WHERE med.dt_exclusao IS NULL
        ORDER BY id DESC
        """
        return self.db_fetch_all.execute_query_zip(query)

    def inserir_medico(self, nome, crm):
        insert_medico_query = """
        INSERT INTO public.medicos (nome, crm, dt_criacao)
        VALUES (:nome, :crm, NOW())
        """
        params = {'nome': nome, 'crm': crm}
        return self.db_fetch_all.execute_query_ddl(insert_medico_query, params)


