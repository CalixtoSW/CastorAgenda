# CastorAgenda\controllers\especialidade_medico_controller.py
from sqlalchemy.orm import Session

import logging

logging.basicConfig(level=logging.DEBUG)

class EspecialidadeMedicoController:
    def __init__(self, db_fetch_all):
        self.db_fetch_all = db_fetch_all

    def listar_especialidades_medico(self, medico_id):
        query = """
        SELECT em.id, e.nome AS especialidade, em.dt_criacao
        FROM especialidade_medico em
        JOIN especialidades e ON em.especialidade_id = e.id
        WHERE em.medico_id = :medico_id
        """
        especialidades_medico = self.db_fetch_all.execute_query_zip(query, {'medico_id': medico_id})
        return especialidades_medico

    def adicionar_especialidade_medico(self, medico_id, especialidade_id):
        query = """
        INSERT INTO especialidade_medico (medico_id, especialidade_id)
        VALUES (:medico_id, :especialidade_id)
        """
        self.db_fetch_all.execute_query_ddl(query, {
            'medico_id': medico_id,
            'especialidade_id': especialidade_id
        })

    def remover_especialidade_medico(self, id_especialidade_medico):
        query = """
        DELETE FROM especialidade_medico
        WHERE id = :id_especialidade_medico
        """
        self.db_fetch_all.execute_query_ddl(query, {
            'id_especialidade_medico': id_especialidade_medico
        })
