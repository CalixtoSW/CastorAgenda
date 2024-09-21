class PacienteController:
    def __init__(self, db_fetch_all):
        self.db_fetch_all = db_fetch_all

    def listar_pacientes(self):
        query = """SELECT
                    id_paciente, nome, dt_nascimento, sexo, telefone, email, endereco, dt_criacao  
                    FROM public.paciente pc where pc.dt_exclusao is null"""
        pacientes = self.db_fetch_all.execute_query_zip(query)
        return pacientes

    def cadastrar_paciente(self, nome, dt_nascimento, sexo, telefone=None, email=None, endereco=None):
        query = """
        INSERT INTO public.paciente 
        (nome, dt_nascimento, sexo, telefone, email, endereco) 
        VALUES (:nome, :dt_nascimento, :sexo, :telefone, :email, :endereco)
        """
        params = {
            'nome': nome,
            'dt_nascimento': dt_nascimento,
            'sexo': sexo,
            'telefone': telefone,
            'email': email,
            'endereco': endereco
        }
        self.db_fetch_all.execute_query_ddl(query, params)

    def editar_paciente(self, id_paciente, nome=None, dt_nascimento=None, sexo=None, telefone=None, email=None,
                        endereco=None):
        query = """
        UPDATE public.paciente 
        SET 
            nome = COALESCE(:nome, nome),
            dt_nascimento = COALESCE(:dt_nascimento, dt_nascimento),
            sexo = COALESCE(:sexo, sexo),
            telefone = COALESCE(:telefone, telefone),
            email = COALESCE(:email, email),
            endereco = COALESCE(:endereco, endereco)
        WHERE id_paciente = :id_paciente
        """
        params = {
            'id_paciente': id_paciente,
            'nome': nome,
            'dt_nascimento': dt_nascimento,
            'sexo': sexo,
            'telefone': telefone,
            'email': email,
            'endereco': endereco
        }
        self.db_fetch_all.execute_query_ddl(query, params)

    def excluir_paciente(self, id_paciente):
        query = "UPDATE public.paciente SET dt_exclusao = NOW() WHERE id_paciente = :id_paciente"
        self.db_fetch_all.execute_query_ddl(query, {'id_paciente': id_paciente})

    def buscar_paciente_por_id(self, id_paciente):
        query = """SELECT
                        id_paciente, nome, dt_nascimento, sexo, telefone, email, endereco, dt_criacao  
                    FROM public.paciente WHERE id_paciente = :id_paciente AND dt_exclusao IS NULL"""
        paciente = self.db_fetch_all.execute_query_zip(query, {'id_paciente': id_paciente})
        return paciente[0] if paciente else None


