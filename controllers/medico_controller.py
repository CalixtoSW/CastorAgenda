from sqlalchemy.orm import Session
from models.medicos import Medico
from models.especialidades import Especialidade
import logging

logging.basicConfig(level=logging.DEBUG)
# CastorAgenda/controllers/medico_controller.py
class MedicoController:
    def __init__(self, db_fetch_all):
        self.db_fetch_all = db_fetch_all

    def listar_medicos(self):
        query = "SELECT * FROM public.medicos"
        medicos = self.db_fetch_all.execute_query_zip(query)
        return medicos

    def inserir_medico(self, nome, crm):
        query = "INSERT INTO public.medicos (nome, crm) VALUES (:nome, :crm)"
        self.db_fetch_all.execute_query_ddl(query, {'nome': nome, 'crm': crm})

    def editar_medico(self, id_medico, nome, crm, especialidades):
        query = """
        UPDATE public.medicos
        SET nome = :nome, crm = :crm
        WHERE id = :id_medico
        """
        self.db_fetch_all.execute_query_ddl(query, {'id_medico': id_medico, 'nome': nome, 'crm': crm})

    def delete_medico(self, id_medico):
        query = "DELETE FROM public.medicos WHERE id = :id_medico"
        self.db_fetch_all.execute_query_ddl(query, {'id_medico': id_medico})

    def buscar_medico_por_id(self, id_medico):
        query = "SELECT * FROM public.medicos WHERE id = :id_medico"
        medico = self.db_fetch_all.execute_query_fetchone(query, {'id_medico': id_medico})
        if medico:
            # Aqui você pode garantir que o campo 'especialidades' esteja presente.
            medico['especialidades'] = medico.get('especialidades', [])
        return medico
