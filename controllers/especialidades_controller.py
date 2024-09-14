# Importe a classe Especialidade se estiver em outro arquivo
from models.especialidades import Especialidade
from engine.database_fetchall import DatabaseFetchAll

class Especialidade:
    def __init__(self, id, nome, dt_criacao):
        self.id = id
        self.nome = nome
        self.dt_criacao = dt_criacao

class EspecialidadeController:
    def __init__(self, db_fetch_all: DatabaseFetchAll):
        self.db = db_fetch_all

    def create_especialidade(self, nome):
        query = f"INSERT INTO public.especialidades (nome) VALUES ('{nome.upper()}')"
        self.db.execute_query_ddl(query)

    def read_especialidades(self):
        query = "SELECT id, nome, dt_criacao FROM public.especialidades WHERE dt_exclusao IS NULL"
        rows = self.db.execute_query_df(query)
        especialidades = [Especialidade(row['id'], row['nome'], row['dt_criacao']) for index, row in rows.iterrows()]
        return especialidades

    def update_especialidade(self, id, new_nome):
        query = f"UPDATE public.especialidades SET nome = '{new_nome}' WHERE id = {id} AND dt_exclusao IS NULL"
        self.db.execute_query_ddl(query)

    def delete_especialidade(self, id):
        query = f"UPDATE public.especialidades SET dt_exclusao = NOW() WHERE id = {id}"
        self.db.execute_query_ddl(query)

    def get_id_by_name(self, nome):
        query = f"SELECT id FROM public.especialidades WHERE nome = '{nome}' AND dt_exclusao IS NULL"
        result = self.db.execute_query_fetchone(query)
        return result['id'] if result else None
