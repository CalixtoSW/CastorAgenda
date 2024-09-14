# CastorAgenda\CastorAgenda\controllers\medicos_controller.py
from engine.database_fetchall import DatabaseFetchAll


class MedicosController:
    def __init__(self, db_fetch_all: DatabaseFetchAll):
        self.db = db_fetch_all

    def create_medico(self, nome, crm, especialidades_ids=None):
        query = f"""
        INSERT INTO public.medicos (nome, crm) 
        VALUES ('{nome}', '{crm}') 
        RETURNING id
        """
        medico_id = self.db.execute_query_fetchone(query)['id']

        # Adiciona a especialidade padrão "CLINICA GERAL"
        self.add_especialidade_medico(medico_id,
                                      "SELECT id FROM public.especialidades WHERE nome = 'CLINICA GERAL'")

        # Adiciona outras especialidades, se fornecidas
        if especialidades_ids:
            self.add_especialidades(medico_id, especialidades_ids)

        return medico_id

    def add_especialidade_medico(self, medico_id, especialidade_id):
        query = f"""
        INSERT INTO public.especialidade_medico (medico_id, especialidade_id)
        VALUES ({medico_id}, ({especialidade_id}))
        """
        self.db.execute_query_ddl(query)

    def add_especialidades(self, medico_id, especialidades_ids):
        for especialidade_id in especialidades_ids:
            self.add_especialidade_medico(medico_id, especialidade_id)

    def read_medicos(self):
        query = """
        SELECT medicos.id, medicos.nome, medicos.crm, 
               ARRAY_AGG(especialidades.nome) AS especialidades, 
               medicos.dt_criacao 
        FROM public.medicos 
        JOIN public.especialidade_medico ON medicos.id = especialidade_medico.medico_id
        JOIN public.especialidades ON especialidade_medico.especialidade_id = especialidades.id
        WHERE medicos.dt_exclusao IS NULL
        GROUP BY medicos.id
        """
        df = self.db.execute_query_df(query)

        # Convertendo o DataFrame para uma lista de dicionários
        medicos = df.to_dict(orient='records')
        return medicos

    def read_medico_by_id(self, medico_id):
        query = f"""
        SELECT medicos.id, medicos.nome, medicos.crm, 
               ARRAY_AGG(especialidades.nome) AS especialidades, 
               medicos.dt_criacao 
        FROM public.medicos 
        JOIN public.especialidade_medico ON medicos.id = especialidade_medico.medico_id
        JOIN public.especialidades ON especialidade_medico.especialidade_id = especialidades.id
        WHERE medicos.id = {medico_id} AND medicos.dt_exclusao IS NULL
        GROUP BY medicos.id
        """
        result = self.db.execute_query_fetchone(query)
        return result

    def read_especialidades(self):
        query = "SELECT id, nome FROM public.especialidades"
        return self.db.execute_query_fetchall(query)

    def get_id_by_name(self, nome):
        query = f"SELECT id FROM public.especialidades WHERE nome = '{nome}'"
        result = self.db.execute_query_fetchone(query)
        return result['id'] if result else None

    def update_medico(self, id, nome, crm, especialidades):
        # Atualiza as informações do médico
        query = f"UPDATE public.medicos SET nome = '{nome}', crm = '{crm}' WHERE id = {id}"
        self.db.execute_query_ddl(query)

        # Atualiza as especialidades
        self.update_especialidades(id, especialidades)

    def update_especialidades(self, medico_id, especialidades):
        # Remove todas as especialidades atuais do médico
        delete_query = f"DELETE FROM public.especialidade_medico WHERE medico_id = {medico_id}"
        self.db.execute_query_ddl(delete_query)

        # Adiciona as novas especialidades
        for especialidade in especialidades:
            especialidade_id = self.get_id_by_name(especialidade)
            if especialidade_id:
                self.add_especialidade_medico(medico_id, especialidade_id)

    def remove_especialidade_medico(self, medico_id, especialidade_id):
        # Implementação para remover a especialidade do médico
        query = "DELETE FROM especialidades_medicos WHERE medico_id = %s AND especialidade_id = %s"
        self.db.execute(query, (medico_id, especialidade_id))
        self.db.commit()
