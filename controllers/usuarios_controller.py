# Castor_Agenda/controllers/usuarios_controller.py
import hashlib
from engine.database_fetchall import DatabaseFetchAll

class UsuarioController:
    def __init__(self, db_fetch_all: DatabaseFetchAll):
        self.db = db_fetch_all

    def create_usuario(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = f"INSERT INTO public.usuarios (username, password) VALUES ('{username}', '{hashed_password}')"
        self.db.execute_query_ddl(query)

    def get_usuario(self, username):
        query = f"SELECT * FROM public.usuarios WHERE username = '{username}' AND dt_exclusao IS NULL"
        result = self.db.execute_query(query)
        return result[0] if result else None

    def authenticate(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = self.get_usuario(username)
        if user and user[2] == hashed_password:
            return True
        return False
