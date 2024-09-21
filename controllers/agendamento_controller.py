class AgendamentoController:
    def __init__(self, db_fetch_all):
        self.db_fetch_all = db_fetch_all

    def listar_agendamentos(self):
        query = """
        SELECT a.id, a.data, a.hora, s.nome AS sala, m.nome AS medico, p.nome AS paciente
        FROM public.agendamentos a
        JOIN public.salas s ON a.sala_id = s.id
        JOIN public.medicos m ON a.medico_id = m.id
        JOIN public.paciente p ON a.paciente_id = p.id_paciente
        WHERE a.dt_exclusao IS NULL
        """
        agendamentos = self.db_fetch_all.execute_query_zip(query)
        return agendamentos

    def cadastrar_agendamento(self, data, hora, sala_id, medico_id, paciente_id):
        query = """
        INSERT INTO public.agendamentos (data, hora, sala_id, medico_id, paciente_id)
        VALUES (:data, :hora, :sala_id, :medico_id, :paciente_id)
        """
        self.db_fetch_all.execute_query_ddl(query, {
            'data': data, 'hora': hora, 'sala_id': sala_id, 'medico_id': medico_id, 'paciente_id': paciente_id
        })

    def editar_agendamento(self, id_agendamento, data, hora, sala_id, medico_id, paciente_id):
        query = """
        UPDATE public.agendamentos
        SET data = :data, hora = :hora, sala_id = :sala_id, medico_id = :medico_id, paciente_id = :paciente_id
        WHERE id = :id_agendamento
        """
        self.db_fetch_all.execute_query_ddl(
            query, {
                'data': data, 'hora': hora, 'sala_id': sala_id, 'medico_id': medico_id, 'paciente_id': paciente_id, 'id_agendamento': id_agendamento
            }
        )

    def excluir_agendamento(self, id_agendamento):
        query = "UPDATE public.agendamentos SET dt_exclusao = NOW() WHERE id = :id_agendamento"
        self.db_fetch_all.execute_query_ddl(query, {'id_agendamento': id_agendamento})

    def buscar_agendamento_por_id(self, id_agendamento):
        query = "SELECT * FROM public.agendamentos WHERE id = :id_agendamento AND dt_exclusao IS NULL"
        agendamento = self.db_fetch_all.execute_query_zip(query, {'id_agendamento': id_agendamento})
        return agendamento[0] if agendamento else None

    def buscar_agendamentos_por_dia(self, data):
        query = """
        SELECT a.id, a.data, a.hora, s.nome AS sala, m.nome AS medico, p.nome AS paciente
        FROM public.agendamentos a
        JOIN public.salas s ON a.sala_id = s.id
        JOIN public.medicos m ON a.medico_id = m.id
        JOIN public.paciente p ON a.paciente_id = p.id_paciente
        WHERE a.data = :data AND a.dt_exclusao IS NULL
        """
        agendamentos = self.db_fetch_all.execute_query_zip(query, {'data': data})
        return agendamentos
