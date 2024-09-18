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
        # Atualiza as informações básicas do médico
        query_atualizar = """
        UPDATE public.medicos
        SET nome = :nome, crm = :crm
        WHERE id = :id_medico
        """
        self.db_fetch_all.execute_query_ddl(query_atualizar, {
            'id_medico': id_medico,
            'nome': nome,
            'crm': crm
        })

        # Se nenhuma especialidade for selecionada, define a especialidade padrão
        if not especialidades:
            especialidades = [1]  # ID da especialidade padrão


        query_remover = """
        DELETE FROM public.especialidade_medico
        WHERE medico_id = :id_medico AND especialidade_id NOT IN :especialidades
        """
        self.db_fetch_all.execute_query_ddl(query_remover, {
            'id_medico': id_medico,
            'especialidades': tuple(especialidades)  # Certifique-se de usar tupla para a cláusula IN
        })

        # Adiciona as novas especialidades
        query_adicionar = """
        INSERT INTO public.especialidade_medico (medico_id, especialidade_id)
        VALUES (:id_medico, :especialidade_id)
        ON CONFLICT (medico_id, especialidade_id) DO NOTHING
        """
        for especialidade_id in especialidades:
            self.db_fetch_all.execute_query_ddl(query_adicionar, {
                'id_medico': id_medico,
                'especialidade_id': especialidade_id
            })

    def delete_medico(self, id_medico):
        query = "DELETE FROM public.medicos WHERE id = :id_medico"
        self.db_fetch_all.execute_query_ddl(query, {'id_medico': id_medico})

    def buscar_medico_por_id(self, id_medico):
        # Supondo que você tenha uma conexão com o banco de dados e um modelo para médico
        query = """
        SELECT m.id, m.nome, m.crm, e.id AS especialidade_id, e.nome AS especialidade_nome
        FROM public.medicos m
        LEFT JOIN public.especialidade_medico em ON m.id = em.medico_id
        LEFT JOIN public.especialidades e ON em.especialidade_id = e.id
        WHERE m.id = :id_medico
        """
        params = {'id_medico': id_medico}
        results = self.db_fetch_all.execute_query_dict(query, params)
        if results:
            medico = {
                'id': results[0]['id'],
                'nome': results[0]['nome'],
                'crm': results[0]['crm'],
                'especialidades': [{'id': row['especialidade_id'], 'nome': row['especialidade_nome']} for row in
                                   results]
            }
            return medico
        return {}


