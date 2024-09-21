class SalaController:
    def __init__(self, db_fetch_all):
        self.db_fetch_all = db_fetch_all

    def listar_salas(self):
        query = "SELECT * FROM public.salas sl WHERE sl.dt_exclusao is null "
        salas = self.db_fetch_all.execute_query_zip(query)
        return salas

    def cadastrar_sala(self, nome, numero, capacidade):
        query = "INSERT INTO public.salas (nome, numero ,capacidade) VALUES (:nome, :numero, :capacidade)"
        self.db_fetch_all.execute_query_ddl(query, {'nome': nome, 'numero': numero, 'capacidade': capacidade})

    def editar_sala(self, id_sala, nome, numero, capacidade):
        query = "UPDATE public.salas SET nome = :nome, numero = :numero, capacidade = :capacidade WHERE id = :id_sala"
        self.db_fetch_all.execute_query_ddl(query, {'nome': nome, 'numero': numero, 'capacidade': capacidade, 'id_sala': id_sala})

    def excluir_sala(self, id_sala):
        query = "UPDATE public.salas SET dt_exclusao = NOW() WHERE id = :id_sala"
        self.db_fetch_all.execute_query_ddl(query, {'id_sala': id_sala})

    def buscar_sala_por_id(self, id_sala):
        query = "SELECT * FROM public.salas sl WHERE id = :id_sala AND sl.dt_exclusao is null"
        sala = self.db_fetch_all.execute_query_zip(query, {'id_sala': id_sala})
        return sala[0] if sala else None