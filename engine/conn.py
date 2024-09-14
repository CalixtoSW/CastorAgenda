import psycopg2
from psycopg2.extensions import connection
from config_db import DatabaseConfig


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection: connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                dbname=self.config.database,
                user=self.config.user,
                password=self.config.password
            )

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str):
        if not self.connection:
            raise Exception("Database not connected")

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
